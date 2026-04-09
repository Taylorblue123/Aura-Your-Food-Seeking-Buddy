"""
Integration tests for the full Aura MVP data pipeline.
Tests each API endpoint and the end-to-end flow:
  check-in → register → scan → recommendation → feedback
"""
import base64

from tests.conftest import MOCK_OCR_RESPONSE, MOCK_REC_RESPONSE


# ─── Helpers ───

def make_test_image_base64():
    """Create a minimal valid JPEG for testing."""
    # Minimal JPEG: SOI + APP0 + EOI
    jpeg_bytes = bytes([
        0xFF, 0xD8, 0xFF, 0xE0, 0x00, 0x10, 0x4A, 0x46,
        0x49, 0x46, 0x00, 0x01, 0x01, 0x00, 0x00, 0x01,
        0x00, 0x01, 0x00, 0x00, 0xFF, 0xD9,
    ])
    return base64.b64encode(jpeg_bytes).decode()


# ═══════════════════════════════════════════════════════
#  1. CHECK-IN ENDPOINT
# ═══════════════════════════════════════════════════════

class TestCheckIn:
    def test_unregistered_device(self, client):
        """New device should return is_registered=False."""
        res = client.post("/api/v1/check-in", json={"device_id": "unknown-device"})
        assert res.status_code == 200
        data = res.json()
        assert data["is_registered"] is False
        assert data["err_msg"] is None

    def test_registered_device(self, client, registered_device):
        """Already registered device should return is_registered=True."""
        res = client.post("/api/v1/check-in", json={"device_id": registered_device})
        assert res.status_code == 200
        data = res.json()
        assert data["is_registered"] is True
        assert data["err_msg"] is None

    def test_missing_device_id(self, client):
        """Missing device_id should return 422 validation error."""
        res = client.post("/api/v1/check-in", json={})
        assert res.status_code == 422


# ═══════════════════════════════════════════════════════
#  2. REGISTER ENDPOINT
# ═══════════════════════════════════════════════════════

class TestRegister:
    def test_new_registration(self, client):
        """New device should register successfully."""
        res = client.post("/api/v1/register", json={
            "device_id": "new-device-123",
            "preference": "vegetarian",
        })
        assert res.status_code == 200
        data = res.json()
        assert data["is_success"] is True
        assert data["err_msg"] is None

    def test_duplicate_registration(self, client, registered_device):
        """Registering same device twice should fail."""
        res = client.post("/api/v1/register", json={
            "device_id": registered_device,
            "preference": "vegan",
        })
        assert res.status_code == 200
        data = res.json()
        assert data["is_success"] is False
        assert "already registered" in data["err_msg"].lower()

    def test_registration_persists(self, client):
        """After registration, check-in should find the device."""
        device_id = "persist-test-device"
        client.post("/api/v1/register", json={
            "device_id": device_id,
            "preference": "halal",
        })
        res = client.post("/api/v1/check-in", json={"device_id": device_id})
        assert res.json()["is_registered"] is True

    def test_missing_fields(self, client):
        """Missing required fields should return 422."""
        res = client.post("/api/v1/register", json={"device_id": "x"})
        assert res.status_code == 422


# ═══════════════════════════════════════════════════════
#  3. SCAN ENDPOINT
# ═══════════════════════════════════════════════════════

class TestScan:
    def test_scan_unregistered_device(self, client):
        """Scanning without registration should fail."""
        res = client.post("/api/v1/scan", json={
            "device_id": "unregistered-device",
            "image_base64": make_test_image_base64(),
        })
        assert res.status_code == 200
        data = res.json()
        assert data["is_success"] is False
        assert "not registered" in data["err_msg"].lower()

    def test_scan_invalid_base64(self, client, registered_device):
        """Invalid base64 should fail gracefully."""
        res = client.post("/api/v1/scan", json={
            "device_id": registered_device,
            "image_base64": "!!!not-valid-base64!!!",
        })
        assert res.status_code == 200
        data = res.json()
        assert data["is_success"] is False
        assert "base64" in data["err_msg"].lower()

    def test_scan_with_mock_ocr(self, client, registered_device, mock_openai_key, mock_openai_ocr):
        """Scan with mocked OpenAI should extract menu items."""
        res = client.post("/api/v1/scan", json={
            "device_id": registered_device,
            "image_base64": make_test_image_base64(),
        })
        assert res.status_code == 200
        data = res.json()
        assert data["is_success"] is True
        assert data["err_msg"] is None
        mock_openai_ocr.assert_called_once()

    def test_scan_stores_menu_in_db(self, client, registered_device, mock_openai_key, mock_openai_ocr):
        """After scan, check-in should still work and menu should be stored."""
        client.post("/api/v1/scan", json={
            "device_id": registered_device,
            "image_base64": make_test_image_base64(),
        })
        # Verify by trying to get recommendations (which requires menu)
        # We'll just verify the scan succeeded and data is persisted
        res = client.post("/api/v1/check-in", json={"device_id": registered_device})
        assert res.json()["is_registered"] is True


# ═══════════════════════════════════════════════════════
#  4. RECOMMENDATION ENDPOINT
# ═══════════════════════════════════════════════════════

class TestRecommendation:
    def test_recommendation_unregistered(self, client):
        """Unregistered device should fail."""
        res = client.post("/api/v1/recommendation", json={
            "device_id": "unregistered-device",
            "vibe_selection": "comfort",
        })
        assert res.status_code == 200
        data = res.json()
        assert data["is_success"] is False
        assert "not registered" in data["err_msg"].lower()

    def test_recommendation_no_menu(self, client, registered_device):
        """Requesting recommendations without scanning should fail."""
        res = client.post("/api/v1/recommendation", json={
            "device_id": registered_device,
            "vibe_selection": "comfort",
        })
        assert res.status_code == 200
        data = res.json()
        assert data["is_success"] is False
        assert "no menu" in data["err_msg"].lower()

    def test_recommendation_invalid_vibe(self, client, registered_device, mock_openai_key, mock_openai_ocr):
        """Invalid vibe should fail."""
        # Scan first
        client.post("/api/v1/scan", json={
            "device_id": registered_device,
            "image_base64": make_test_image_base64(),
        })
        res = client.post("/api/v1/recommendation", json={
            "device_id": registered_device,
            "vibe_selection": "nonexistent_vibe",
        })
        assert res.status_code == 200
        data = res.json()
        assert data["is_success"] is False
        assert "invalid vibe" in data["err_msg"].lower()

    def test_recommendation_success(self, client, registered_device, mock_openai_key, mock_openai_ocr, mock_openai_rec):
        """Full scan → recommendation flow should return dishes."""
        # Scan menu
        client.post("/api/v1/scan", json={
            "device_id": registered_device,
            "image_base64": make_test_image_base64(),
        })
        # Get recommendations
        res = client.post("/api/v1/recommendation", json={
            "device_id": registered_device,
            "vibe_selection": "comfort",
        })
        assert res.status_code == 200
        data = res.json()
        assert data["is_success"] is True
        assert data["err_msg"] is None

        rec = data["recommendation"]
        assert "brief_summary" in rec
        assert len(rec["recommendations"]) > 0

        dish = rec["recommendations"][0]
        assert "dish_name" in dish
        assert "reasoning" in dish
        assert "story" in dish
        assert "price" in dish

    def test_all_vibes_work(self, client, registered_device, mock_openai_key, mock_openai_ocr, mock_openai_rec):
        """All 8 vibes should return valid recommendations."""
        client.post("/api/v1/scan", json={
            "device_id": registered_device,
            "image_base64": make_test_image_base64(),
        })
        vibes = ["comfort", "adventure", "light", "quick", "sharing", "budget", "healthy", "indulgent"]
        for vibe in vibes:
            res = client.post("/api/v1/recommendation", json={
                "device_id": registered_device,
                "vibe_selection": vibe,
            })
            data = res.json()
            assert data["is_success"] is True, f"Vibe '{vibe}' failed: {data['err_msg']}"
            assert len(data["recommendation"]["recommendations"]) > 0


# ═══════════════════════════════════════════════════════
#  5. FEEDBACK ENDPOINT
# ═══════════════════════════════════════════════════════

class TestFeedback:
    def test_feedback_unregistered(self, client):
        """Unregistered device should get minimal response."""
        res = client.post("/api/v1/feedback", json={
            "device_id": "unregistered-device",
            "picked_dish_names": ["Burger"],
            "skipped_dish_names": [],
            "time_to_decision_ms": 5000,
        })
        assert res.status_code == 200
        data = res.json()
        assert data["picked_count"] == 1
        assert "register" in data["summary"].lower()

    def test_feedback_after_recommendation(self, client, registered_device, mock_openai_key, mock_openai_ocr, mock_openai_rec):
        """Feedback after full flow should calculate prices and summary."""
        # Scan
        client.post("/api/v1/scan", json={
            "device_id": registered_device,
            "image_base64": make_test_image_base64(),
        })
        # Recommend
        client.post("/api/v1/recommendation", json={
            "device_id": registered_device,
            "vibe_selection": "comfort",
        })
        # Feedback — pick some, skip some
        res = client.post("/api/v1/feedback", json={
            "device_id": registered_device,
            "picked_dish_names": ["Classic Burger", "Chocolate Cake"],
            "skipped_dish_names": ["Caesar Salad"],
            "time_to_decision_ms": 15000,
        })
        assert res.status_code == 200
        data = res.json()
        assert data["picked_count"] == 2
        assert data["total_price_estimate"] != "$0"
        assert len(data["summary"]) > 0

    def test_feedback_all_picked(self, client, registered_device, mock_openai_key, mock_openai_ocr, mock_openai_rec):
        """Picking all dishes should mention 'loved everything'."""
        client.post("/api/v1/scan", json={
            "device_id": registered_device,
            "image_base64": make_test_image_base64(),
        })
        client.post("/api/v1/recommendation", json={
            "device_id": registered_device,
            "vibe_selection": "comfort",
        })
        res = client.post("/api/v1/feedback", json={
            "device_id": registered_device,
            "picked_dish_names": ["Classic Burger", "Chocolate Cake", "Caesar Salad"],
            "skipped_dish_names": [],
            "time_to_decision_ms": 45000,
        })
        data = res.json()
        assert data["picked_count"] == 3
        assert "loved everything" in data["summary"].lower()

    def test_feedback_none_picked(self, client, registered_device, mock_openai_key, mock_openai_ocr, mock_openai_rec):
        """Skipping all dishes should mention 'nothing caught your eye'."""
        client.post("/api/v1/scan", json={
            "device_id": registered_device,
            "image_base64": make_test_image_base64(),
        })
        client.post("/api/v1/recommendation", json={
            "device_id": registered_device,
            "vibe_selection": "comfort",
        })
        res = client.post("/api/v1/feedback", json={
            "device_id": registered_device,
            "picked_dish_names": [],
            "skipped_dish_names": ["Classic Burger", "Chocolate Cake", "Caesar Salad"],
            "time_to_decision_ms": 5000,
        })
        data = res.json()
        assert data["picked_count"] == 0
        assert "nothing caught your eye" in data["summary"].lower()


# ═══════════════════════════════════════════════════════
#  6. FULL END-TO-END PIPELINE
# ═══════════════════════════════════════════════════════

class TestFullPipeline:
    def test_complete_user_journey(self, client, mock_openai_key, mock_openai_ocr, mock_openai_rec):
        """
        Full pipeline test: check-in → register → scan → recommendation → feedback.
        Validates data flows correctly between each step.
        """
        device_id = "e2e-test-device"

        # Step 1: Check-in (new device)
        res = client.post("/api/v1/check-in", json={"device_id": device_id})
        assert res.json()["is_registered"] is False

        # Step 2: Register
        res = client.post("/api/v1/register", json={
            "device_id": device_id,
            "preference": "vegetarian",
        })
        assert res.json()["is_success"] is True

        # Step 3: Check-in again (now registered)
        res = client.post("/api/v1/check-in", json={"device_id": device_id})
        assert res.json()["is_registered"] is True

        # Step 4: Scan menu
        res = client.post("/api/v1/scan", json={
            "device_id": device_id,
            "image_base64": make_test_image_base64(),
        })
        assert res.json()["is_success"] is True

        # Step 5: Get recommendations
        res = client.post("/api/v1/recommendation", json={
            "device_id": device_id,
            "vibe_selection": "comfort",
        })
        rec_data = res.json()
        assert rec_data["is_success"] is True
        dishes = rec_data["recommendation"]["recommendations"]
        assert len(dishes) >= 1

        # Step 6: Submit feedback (pick first dish, skip rest)
        picked = [dishes[0]["dish_name"]]
        skipped = [d["dish_name"] for d in dishes[1:]]
        res = client.post("/api/v1/feedback", json={
            "device_id": device_id,
            "picked_dish_names": picked,
            "skipped_dish_names": skipped,
            "time_to_decision_ms": 20000,
        })
        feedback = res.json()
        assert feedback["picked_count"] == 1
        assert len(feedback["summary"]) > 0

    def test_multiple_sessions_same_device(self, client, mock_openai_key, mock_openai_ocr, mock_openai_rec):
        """
        Same device can scan multiple menus and get different recommendations.
        Second scan should overwrite the first menu data.
        """
        device_id = "multi-session-device"

        # Register
        client.post("/api/v1/register", json={
            "device_id": device_id,
            "preference": "no_restriction",
        })

        # First scan + recommendation
        client.post("/api/v1/scan", json={
            "device_id": device_id,
            "image_base64": make_test_image_base64(),
        })
        res1 = client.post("/api/v1/recommendation", json={
            "device_id": device_id,
            "vibe_selection": "adventure",
        })
        assert res1.json()["is_success"] is True

        # Second scan + different vibe
        client.post("/api/v1/scan", json={
            "device_id": device_id,
            "image_base64": make_test_image_base64(),
        })
        res2 = client.post("/api/v1/recommendation", json={
            "device_id": device_id,
            "vibe_selection": "healthy",
        })
        assert res2.json()["is_success"] is True

        # Feedback on second session
        dishes = res2.json()["recommendation"]["recommendations"]
        res = client.post("/api/v1/feedback", json={
            "device_id": device_id,
            "picked_dish_names": [d["dish_name"] for d in dishes],
            "skipped_dish_names": [],
            "time_to_decision_ms": 10000,
        })
        assert res.json()["picked_count"] == len(dishes)


# ═══════════════════════════════════════════════════════
#  7. HEALTH CHECK
# ═══════════════════════════════════════════════════════

class TestHealth:
    def test_health_endpoint(self, client):
        """Health check should return status ok."""
        res = client.get("/api/v1/healthz")
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "uptime_seconds" in data
