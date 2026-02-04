Check-in
PS: 每一次打开app时候client都会检查Check-in状态
- Check-in Request
  - Device ID (前端获取或者生成一个唯一的设备ID标识)
- Check-in Response
  - isRegistered:bool: true / false
  - errMsg

Registration
PS：第一次使用（数据库没device ID记录），把所选preference和ID发给后端生成profile entry
- Register Request
  - Device ID
  - Preference selection (Enum)
- Register Response
  - isSuccess: Bool
  - errMsg

Scan
PS：拍照上传以及识别菜单内容
- ScanRequest
  - Device ID
  - ImageBase64
- ScanResponse
  - isSuccess: Bool (1. 图片上传 2. 图片OCR)
  - errMsg (1. 图片上传 2. 图片OCR)

Recommendation
PS: 选择vibe后，给出recommendation response前端进行显示和渲染
- RecommendationRequest
  - Device ID
  - Vibe Selection: Enum
- RecommendationResponse
  - isSuccess
  - errMsg
  - Optional Recommendation (Json): 
    - BriefSummary: 一句话总结
    - Recommendations List
"recommendations": [
    {
      "dish_name": "Pad Thai",
      "reasoning": "A mild, sweet noodle dish perfect for first-timers",
      "story": "The most popular Thai dish for a reason",
      "warnings"?: ["Contains peanuts - please verify with staff"],
      "price": "14",
      "Emoji":
    },
     {
      "dish_name": "Pad Thai",
      "reasoning": "A mild, sweet noodle dish perfect for first-timers",
      "story": "The most popular Thai dish for a reason",
      "warnings"?: ["Contains peanuts - please verify with staff"],
      "price": "14",
      "Emoji":
    },
  ]
Feedback
PS：用户筛选完推荐菜单列表后，返回一个feedback
- FeedbackRequest/Response
Request:
{
  "picked_dish_names": ["dish_id_1", "dish_id_2"],
  "skipped_dish_names": ["dish_id_3"],
  "time_to_decision_ms": 45230 // Client-side measured
}
Response (200 OK):
{
  "picked_count": 2,
  "total_price_estimate": "$24-28",
  "summary": "You don't like spicy food, and a bit hesitate"
  //"celebration_type": "first_order" | "perfect_match" | "quick_decision" | null
}
DB Schema
- userProfile Table
  - DeviceID
  - Preference selection
  - CurrentMenu: Json
  - CurrentVibe: Json
  - CurrentRecommendations
  - CurrentFeedback

Logic Flow
Scan Logic Function
ScanRequest (DeviceID, Base64) => Save Image + Call OCR service + Update DB (userProfile) + Response (success) + Delete Image

Recommendation Function
RecommendationRequest （Vibe selection）=> Update current vibe in table => call llm service for recommendation list => Update CurrentRecommendations => Recommendation Response

Feedback Function
FeedbackRequest => Call llm service for feedback => Update Feedback => FeedbackResponse


