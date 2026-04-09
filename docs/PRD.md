# Gusto — PRD Skeleton

> **Status:** Draft — 带入 ChatPRD 填充细节
> **Author:** Watson
> **Last updated:** 2026-04-03
> **Phase:** Phase 1 → Phase 2 过渡中

---

## 1. Product Overview

### One-liner
帮你从"不知道吃什么"变成"想去试试看"。

### Problem
任何人到了一个新城市、甚至本地人面对日常决策疲劳时，都面临"不知道吃什么"的问题。68% 的美国人说决定吃什么是最大的用餐挑战（Factor/Wakefield 调查）。

现有工具的问题：
- **Yelp / Google Maps**：信息过载，500 家餐厅每家几百条评论，不帮你做决定
- **Ollie / MealThinker / Eat This Much**：只解决在家做饭，不解决外出吃饭
- **SnapCalorie / Foodvisor**：拍照记录热量，不推荐该吃什么
- **ChatGPT / Claude**：没有持久记忆，不了解用户，没有位置感知

### Solution
一个 AI 食物顾问 APP，主动推荐附近值得探索的餐厅和菜品。用户只需 👍 或换一个。越用越懂你。

### Positioning
介于餐厅发现（Yelp）和在家做饭规划（Ollie）之间的空白地带——AI 驱动的外出饮食决策。

### Product Tone
探索优先。健康目标放后续设置页，不在核心流程中制造约束感。

### Design Philosophy: 陪伴式设计 (Companion Design)

> **Core Insight:** 传统食物 APP（Yelp、Ollie）遵循 UX 2.0 范式——把用户建模为冰冷的特征参数（口味、预算、距离），然后做信息匹配和分发。Gusto 遵循 UX 3.0 范式——对用户的完整人格、情感和当下 context 进行建模，以 companion 的身份陪伴用户走上一段饮食探索旅程。这是 Gusto 和所有现有食物 APP 的根本区别。
>
> 参考框架：ACM IX Magazine（2026.3）UX 3.0 Paradigm Framework — 提出 AI 时代的 UX 需要融入用户意图和情感识别、社会性响应交互模型。

**Gusto 的设计哲学不是围绕"屏幕"构建的，而是围绕三个陪伴时刻构建的：**

**Moment 1 — 接住你 (Catch You)**
用户打开 APP 的瞬间，Gusto 已经准备好了。它感知你的当下状态——时间、地点、也许是疲惫或好奇——然后以一个温暖的姿态迎接你。"Hey，今天累了吧。我找到了一个让你安心的角落。"
- 情感关键词：安全、被接住、零负担
- 对标体验：Flourish 的小圆球在等你，不是 Yelp 的 500 条结果扔给你
- 当前 MVP 映射：Onboarding + Screen 1（推荐卡片）

**Moment 2 — 陪你去 (Go With You)**
用户决定去了。Gusto 不是给完信息就消失——它陪你走过去，告诉你到了以后点什么，给你信心推门进去。"走过去 3 分钟。进去点 chicken boti，相信我。"
- 情感关键词：信心、陪伴、不是一个人
- 对标体验：一个懂吃的朋友带你去他的秘密小店
- 当前 MVP 映射：Screen 2（进门指南）

**Moment 3 — 记住我们 (Remember Us)**
用户吃完了。这不是一次交易的结束——是一段共同经历的沉淀。Gusto 问一句"怎么样？"，用户不是打分，是分享一个感受。Gusto 记住这次经历，下一次推荐更懂你。
- 情感关键词：感恩、共同记忆、成长
- 对标体验：和朋友吃完饭后的那句"下次还来这家"
- 当前 MVP 映射：简单的餐后反馈 → 偏好更新
- 未来可能：饮食探索日记、共同经历时间线

**循环：记住我们 → 下一次接住你时更懂你。这是 learning loop，也是用户永远不想离开的原因。**

> **重要：** 以上三个时刻是 Gusto 的根本设计框架，高于任何具体的屏幕布局。当前 MVP 用"Screen 1 + Screen 2 + 餐后反馈"来承载这三个时刻，但未来的交互形态可能完全不同（语音、push notification、甚至 AR）。屏幕会变，三个陪伴时刻不会变。

**五条设计原则（从用户自身感受中提炼，服务于三个时刻）：**

1. **Safe Corner（安全的角落）：** APP 的感觉是一个温暖的庇护所，不是一个信息工具。用户打开 APP 时应该感到被接住，而不是被扔进信息海洋。
2. **One Thing, Not a List（一个东西，不是一个列表）：** 永远只展示一个推荐，不给用户选择负担。
3. **Companion, Not Algorithm（伙伴，不是算法）：** 推荐应该感觉像"一个认识你的朋友已经帮你想好了"，不是"一个系统吐出了一条结果"。语气是对话式的、温暖的。
4. **Catch Me（接住我）：** 用户不需要做任何工作。打开 APP 的瞬间，推荐已经准备好了。零认知负担启动。
5. **Adaptive Soul（自然生长的人格）：** Gusto 的人格不是用户在设置里选择的，而是在陪伴过程中自然适应用户的——如果你是安静内向的人，Gusto 变得温柔轻声；如果你是活泼外向的人，Gusto 变得俏皮活力。不只是口味越用越准，连说话方式都越来越像"你的那个朋友"。人格是 learning loop 的一部分，不是预设参数。

### UX 3.0 对 AI-Native 产品的启发

> 以下洞察超出 Gusto 本身，但记录在 PRD 中作为设计决策的理论支撑。

2026 年 AI-native 产品的 UX 正在经历一个范式转移：

| 维度 | UX 2.0（移动互联网时代） | UX 3.0（AI Companion 时代） |
|------|------------------------|---------------------------|
| 用户建模 | 特征参数（年龄、偏好、位置） | 完整人格 + 情感 + 当下 context |
| 系统角色 | 信息匹配与分发引擎 | 有记忆、有人格的 companion |
| 交互模式 | 用户搜索 → 系统返回列表 | 系统主动准备 → 用户只需回应 |
| 情感设计 | 效率优先（快速找到信息） | 关系优先（感到被理解和陪伴） |
| 记忆层 | Session-based（每次重新开始） | Persistent memory（越用越懂你） |
| 成功指标 | 点击率、转化率 | 信任感、回访意愿、情感连接 |
| 反馈机制 | 评分/评论（交易结束） | 共同记忆（关系延续） |
| 人格层 | 固定品牌调性（同一个声音对所有人） | 自然适应每个用户（它长成了"你的那个朋友"） |

Gusto 的定位：**第一个用 UX 3.0 范式设计的食物发现 APP。**

### Competitive Reference
> 目的不是商业竞争分析，而是参考类似问题的已有解决方案。

| 产品 | 解决什么 | 可借鉴 | 我们的不同 |
|------|---------|--------|-----------|
| Yelp / Google Maps | 搜索和浏览餐厅 | 餐厅数据丰富 | 我们帮做决定，不给 500 条结果 |
| Ollie / MealThinker | 在家做饭吃什么 | Learning loop、个性化 | 我们解决外出吃饭 |
| SnapCalorie / Foodvisor | 拍照记录热量 | 食物图像识别 | 我们推荐该吃什么，不是记录吃了什么 |
| ChatGPT / Claude | 通用问答 | LLM 推荐能力 | 我们有持久记忆 + 位置感知 + 零输入交互 |
| Eat By Prompt | FEAST 框架指南 | Prompt 设计思路 | 我们是产品不是指南 |

---

## 2. Target User

### Phase 1 测试用户
Watson 自己——在 Oakland 的华人，CS 背景，想探索本地食物但经常不知道吃什么。

### 延展用户画像
- 在新城市的非本地人（留学生、新移民、出差/旅行者）
- 日常有"吃什么"决策疲劳的本地人
- 有饮食限制（过敏/素食/宗教）但不想因此放弃探索的人

---

## 3. Success Criteria (Phase 1)

**不是赚钱，不是市场验证。**

- Watson 自己愿意每天打开
- 一周内帮他走进 3 家从没去过的餐厅
- 坐下来知道吃什么，享受探索过程
- 核心验证：产品是否让外出饮食从"生存导向"变成"探索发现导向"

---

## 4. Core User Flow

### MVP 核心场景
路过陌生餐厅不敢进 → APP 降低探索门槛

### 核心交互
APP 主动推荐一个最适合你的选择——不是给你一堆让你挑，而是"我帮你想好了"。用户通过对话式按钮回应（"想去！"/"今天不太想"/"换个口味"），而不是左滑右滑。交互成本和滑动一样低，但感觉像在回应一个朋友的建议，不是在翻一副牌。

> **为什么不用左滑右滑？** 左滑右滑的本质是"我不确定你要什么，给你一堆让你筛选"——这是 UX 2.0 的信息筛选逻辑，只不过穿了 Tinder 的衣服。UX 3.0 的 companion 会说"今天就这家，走吧"。用户的回应不是"这张牌不要"，而是"嗯，今天不太想吃这个"——Gusto 会回"好，我再想想"然后给出下一个推荐。

### 连续陪伴旅程

> **核心转变：** 不再用"Screen 1 → Screen 2"的屏幕跳转思维，而是一段连续的陪伴对话。三个 Moment 之间没有硬边界——它是一段从"下班了吧"到"第一口怎么样"的完整陪伴，Gusto 一直在。
>
> **交互形态：** 不是聊天框（冰冷），不是传统屏幕跳转（割裂），而是介于两者之间——每一步都是一个温暖的卡片或画面，配上对话式按钮。用户只需点按钮回应，永远不需要打字。
>
> **自适应节奏（Adaptive Rhythm）：** 同样的三个 Moment，根据用户当下状态调整速度和密度。很饿时三个 Moment 在 30 秒内完成，心情低落时慢慢陪伴。不是两个不同的 APP，是一个 APP 能感知你的状态并调整自己的步调。

---

**Moment 1 — 接住你 (Catch You)**

三个节拍（Beats）：

Beat 1：Gusto 感知并共情
- Context-aware 智能问候（LLM 根据当下 context 实时生成）
- Context 信号：时间、地点、使用频率、天气
- 示例："下班了吧？今天辛苦了。" / "周末想出去探索？" / "夜宵时间？"

Beat 2：用户回应当下状态
- 2-3 个对话式按钮（Gusto 基于 context 智能生成，不是每次一样）
- 涵盖：心情 + 用餐场景 + 口味倾向
- 示例按钮："是的，想吃点暖的" / "今天心情不错，想探索" / "随便，你帮我决定"
- 如果 GPS 显示你一个人、时间是工作日晚上，跳过"一个人还是朋友"这个问题——已经知道了
- **约束：最多 2-3 个按钮，不能更多。Catch Me 原则——零认知负担。**

Beat 3：Gusto 基于 context + 用户回应 推荐
- 一个推荐（不是列表），包含：
  - 食物大图
  - 店名 + 距离
  - **氛围标签**（"安静，适合一个人" / "热闹，适合朋友"）
  - 一句话推荐理由（对话式语气）
- 对话式回应按钮："想去！" / "今天不太想" / "换个口味"
- 当用户说"今天不太想"，Gusto 回应"好，我再想想"

> **关键洞察：氛围 ≥ 口味。** 一个口味完美匹配但氛围不对的推荐（如一个人去聚会餐厅），结果是糟糕的体验。推荐时必须告知氛围信息。（来源：创始人亲身验证——Menlo Park 缅甸餐厅经历）

---

**Moment 2 — 陪你去 (Go With You)**

不是一个静态信息页，而是从"决定去"到"坐下来点菜"的持续陪伴：

Beat 1：为什么值得去
- 餐厅故事和背景（"这是一家妈妈和儿子开的巴基斯坦餐厅"）
- 简单介绍 Neighbourhood（"这条街很安静，适合散步过去"）
- 氛围描述（"店里比较温馨，吧台和散座都有"）

Beat 2：陪你走过去
- 导航 + 距离 + 预计时间
- 路上的轻松语气（"走过去 5 分钟，不远"）

Beat 3：进门和点菜
- 推荐 2-3 道适合你的菜品 + 推荐理由
- **菜品推荐诚实标注**（"这些信息来自网上菜单和评价，到了可以再确认一下实际菜单"）
- **需求变更时的快速调整**——对话式按钮："菜单上没这个" / "想换个口味" / "帮我选个招牌"
- **绝不要求用户打字重来。** 一个按钮解决调整，不是重新输入需求。

---

**Moment 3 — 记住我们 (Remember Us)**

不是事后弹窗评分，而是从上菜那一刻就开始的共同经历：

Beat 1：记录
- 用户本能地想拍照——Gusto 接住这个冲动
- 拍照后 Gusto 回应："这个看起来太棒了！"

Beat 2：庆祝
- Gusto 和你一起庆祝（"我就知道你会喜欢这种地方"）
- 不是"请对本次服务评分"，而是"我们一起经历了一件好事"

Beat 3：分享
- 用户可以分享给朋友
- Gusto 记住这次经历，更新你的偏好画像
- "下次再带你发现新的。"

> **循环：** Moment 3 的记忆 → 下一次 Moment 1 时 Gusto 更懂你。这是 learning loop 的情感版本。

### Screen 2 数据策略：LLM + Web Search 作为主数据引擎

> **Key Insight:** 结构化菜单 API（Google Places Menu、Yelp）覆盖率极低（验证结果 0%），且无免费可靠的第三方菜单数据源。但 LLM + Web Search 可以实时从餐厅官网、DoorDash、Yelp、米其林等多个来源聚合菜品信息，覆盖率和信息丰富度远超任何单一 API。

**主引擎：LLM + Web Search（实时聚合）**
- 输入：餐厅名 + 位置 + 用户偏好画像
- LLM 自动搜索餐厅官网、外卖平台、点评网站
- 输出：餐厅介绍 + 推荐 2-3 道适合用户的菜品 + 推荐理由 + 人均价格
- 优势：覆盖率接近 100%，信息来源多样，能结合用户偏好做个性化推荐

**辅助数据：Google Places API（结构化基础信息）**
- 提供：餐厅名、位置、距离、照片、评分、营业时间、editorial summary
- 用途：Screen 1 推荐卡片的基础数据 + Screen 2 的辅助上下文

**Fallback（v1.1）：用户拍摄实体菜单**
- 当用户已在餐厅内，可拍菜单获取更精确的菜品推荐

**Trade-offs：**
- 延迟：每次 Screen 2 加载需要 3-5 秒（LLM + Web Search 耗时）→ 可接受，用户在做决定不是在刷短视频
- 成本：每次推荐 = 一次带 Web Search 的 LLM 调用 → Phase 1 单用户，成本可忽略

### 入口优先级
- **Entry A（主动推荐）：** MVP v1 — 打开 APP 即看到推荐卡片
- **Entry B（路过识别）：** v1.1 — GPS 定位附近餐厅，直接进入 Screen 2

---

## 5. Onboarding Flow

### 漏斗设计（3 步）

**Step 1 — 硬性排除（安全边界）**
- "有什么绝对不吃的？"
- 多选：过敏源 / 宗教饮食禁忌 / 素食-纯素 / 无
- 目的：排除不安全选项

**Step 2 — 视觉口味测试（核心偏好）**
- 从预设的 15 张食物图片中随机展示 10 张
- 用户对每张图 👍 想吃 / 👎 不想
- 图片覆盖 8 种菜系、3 级口味轻重、3 级辣度、3 级熟悉度
- AI 从结果同时推断：菜系偏好 + 口味倾向 + 探索倾向
- 交互方式：轻引导（"滑动你想吃的食物，帮我快速了解你的口味"），不显式分阶段

**Step 3 — AI 总结确认（建立信任）**
- "看起来你偏爱亚洲菜系，喜欢清爽口味，对新食物有一定好奇心。对吗？"
- 用户可确认或微调
- 目的：让用户觉得"它懂我了"→ 产生持续使用的信任基础

### 不在 Onboarding 中问的
- 饮食目标（减脂/增肌）→ 与探索优先调性矛盾，放后续设置页
- 用餐社交场景（一个人/朋友）→ 属于每次使用的动态 context
- 菜系偏好勾选 → 从视觉测试中推断，不显式询问

### 视觉口味测试图片集设计

15 张预标注食物图片，每张标注 4 个维度：

| # | Image | Cuisine | Weight | Spice | Familiarity |
|---|-------|---------|--------|-------|-------------|
| 1 | Fresh poke bowl | Japanese-Hawaiian | Light | Mild | High |
| 2 | Tonkotsu ramen | Japanese | Heavy | Mild | High |
| 3 | Sichuan mapo tofu | Chinese | Medium | Hot | Medium |
| 4 | Pho | Vietnamese | Light | Mild | High |
| 5 | Pad Thai | Thai | Medium | Medium | High |
| 6 | Chicken tikka masala | Indian | Heavy | Medium | Medium |
| 7 | Margherita pizza | Italian | Medium | Mild | High |
| 8 | Grilled steak + fries | American | Heavy | Mild | High |
| 9 | Fish tacos | Mexican | Light | Medium | High |
| 10 | Mediterranean mezze | Middle Eastern | Light | Mild | Medium |
| 11 | Korean bibimbap | Korean | Medium | Medium | Medium |
| 12 | Ethiopian injera platter | Ethiopian | Medium | Medium | Low |
| 13 | Fried chicken + biscuit | American South | Heavy | Mild | High |
| 14 | Acai bowl | Brazilian | Light | Mild | High |
| 15 | Lamb shawarma wrap | Middle Eastern | Medium | Medium | Medium |

**设计原则：**
- 内置对比对：同菜系不同轻重（#1 poke vs #2 tonkotsu）检测口味偏好
- 探索度探测器：#12 Ethiopian（对大多数人陌生）检测猎奇倾向
- 图片来源：Unsplash / Pexels 免费图库

**偏好映射：** 用户滑完后，将所有 👍/👎 图片的标签汇总，传给 LLM 生成偏好画像摘要。

---

## 6. MVP Feature Scope

### v1 — IN
- Onboarding 三步流程（第一次见面，不属于日常循环）
- 连续陪伴旅程：Moment 1 → Moment 2 → Moment 3 基础版
  - Moment 1：Context-aware 智能问候 + 用户状态回应（按钮）+ 推荐（含氛围标签）
  - Moment 2：餐厅故事 + 菜品推荐 + 需求变更按钮（"菜单上没这个"/"换口味"）
  - Moment 3 基础版：简单的餐后回应（"怎么样？"→ 按钮回应 → Gusto 记住）
- 自适应节奏（急切模式 vs 陪伴模式的基础版）
- Context 信号采集（时间、地点、使用频率）
- Google Places API 集成（餐厅数据 + 照片 + AI summary + 氛围信息）
- LLM + Web Search 实时菜品聚合引擎
- LLM 推荐引擎（Claude API，用于问候语 + 推荐理由 + 对话回应 + 氛围判断）
- 用户偏好画像存储（Supabase）
- 行为历史记录（feeding learning loop）
- PWA 部署（Vercel）

### v1.1 — NEXT
- Entry B：路过识别餐厅（GPS 定位）
- 菜单拍照扫描（解决推荐菜品和实际菜单不符的问题）
- 健康/饮食目标设置页
- Moment 3 完整版：拍照 → 庆祝 → 分享给朋友
- 饮食探索日记（共同经历时间线）

### v2 — FUTURE
- **主动式推送（Proactive AI）：** Gusto 学习用户的时间、地点、行为规律，在合适的时刻主动推送邀请，不等用户打开 APP
- 用户账号/登录系统（替代 device ID）
- 社交功能/社区
- 每周饮食规划
- 餐厅预订集成
- Native app（iOS/Android）
- Agent API endpoint（为个人 AI agent 提供服务）

---

## 7. Data Sources

### 数据架构（双引擎）

**引擎 1：Google Places API (New) — 结构化餐厅基础数据**
- 提供：餐厅名、位置、距离、照片、评分、价位、营业时间、editorial summary、reviews
- 用途：Moment 1 推荐卡片的基础数据 + **氛围判断**（reviews 中提取）
- 免费额度 $200/月，足够个人 MVP

**引擎 2：LLM + Web Search — 实时菜品信息 + 餐厅故事聚合**
- 提供：具体菜品推荐、菜品描述、价格、推荐理由、**餐厅文化背景和故事**、**氛围描述**
- 数据来源：LLM 实时搜索餐厅官网、DoorDash、Yelp、米其林、美食博客等
- 用途：Moment 2 陪伴旅程的核心数据引擎
- 优势：覆盖率接近 100%
- **已知局限：推荐菜品可能与实际菜单不符（已验证）。需在推荐时诚实标注，并提供快速调整按钮。**

### 为什么不用菜单 API
- Google Places Menu URI 覆盖率 0%（已验证）
- Yelp 菜单数据覆盖参差不齐
- OpenMenu 主要覆盖连锁餐厅，独立小店缺失
- Foodspark/Dotlas 为企业级商业服务，MVP 阶段不值得
- **LLM + Web Search 的覆盖率和信息质量超过以上所有方案**

---

## 8. User Profile Data Model

> **Note:** 具体 schema 在 SPEC.md 中定义。PRD 只标注"存什么"。

### 需要持久化的数据
- 硬性排除（过敏源、宗教禁忌、素食）
- Onboarding 偏好画像（LLM 生成的文字摘要 + 原始标签数据）
- **氛围偏好**（从行为中学习：独自 vs 社交、安静 vs 热闹、正式 vs 休闲）
- 每次推荐交互记录（哪家店、用户回应了什么按钮、时间戳、context 信号）
- 去过的餐厅（手动确认或自动检测）
- Moment 3 记录（拍照、感受回应、菜品反馈）
- **自适应节奏偏好**（从行为中学习：用户倾向快速决定还是慢慢陪伴）

### 核心护城河
越用越懂用户（learning loop）。付费意愿排序：个性化积累 > 社交社区 > 内容知识。

---

## 9. Technical Constraints

| 维度 | 决策 | 理由 |
|------|------|------|
| 平台 | PWA（React/Next.js） | 开发最快，不需要上架 App Store |
| 部署 | Vercel | 免费，一条命令部署 |
| 后端/存储 | Supabase（PostgreSQL + Auth） | 免费层足够，云端存储保护用户数据不丢失 |
| 身份识别 | Device ID（v1）→ 账号系统（v2） | MVP 阶段不需要登录 |
| LLM | Claude API + Web Search | 推荐生成 + 偏好总结 + 实时菜品信息聚合 |
| 学习机制 | LLM-based（非传统 ML） | 单用户数据量不够跑协同过滤，LLM 天然能理解行为历史 |
| 餐厅基础数据 | Google Places API (New) | 照片 + 评分 + 位置 + editorial summary |
| 菜品数据 | LLM + Web Search（实时） | 覆盖率远超任何结构化菜单 API |
| 工具链 | ChatPRD → Stitch → Claude Code | Think Here, Execute There |

### 未来架构演进方向（不影响 MVP 决策）
- PWA → Native app（后端不变，只换前端壳）
- 单用户 → 多用户（Supabase 天然支持）
- 人用 → Agent 用（加 API endpoint）

### Privacy & Permissions
- **GPS 权限：** PWA 首次使用时请求位置权限，需明确说明用途（"用于发现你附近的餐厅"）。用户拒绝时降级为手动输入地址。
- **数据存储：** 用户偏好和行为数据存储在 Supabase 云端，与 Device ID 关联。Phase 1 不收集姓名/邮箱等个人身份信息。
- **第三方 API：** 用户位置数据传给 Google Places API 做附近搜索。需在首次使用时告知。
- **数据删除：** 提供清除所有个人数据的选项。

---

## 10. Open Questions & Risks

### Open Questions
- [ ] 连续陪伴旅程的具体视觉形态（Stitch 设计阶段探索——不是聊天框，不是屏幕跳转，是介于两者之间的温暖卡片流）
- [ ] 自适应节奏的切换逻辑（什么 context 信号触发急切模式 vs 陪伴模式）
- [ ] 推荐算法的 prompt 设计（SPEC.md 阶段确定）
- [ ] 15 张 Onboarding 图片的实际采集和标注（执行阶段）
- [ ] Moment 3 的拍照 + 分享交互的具体形态

### Week 0 Validation Plan

**验证 1：Google Places API 数据覆盖率 — ✅ 已完成**
- 结果：Palo Alto 20 家餐厅，照片 100%、reviews 100%、editorial summary 70%、价位 95%
- Menu URI 覆盖率 0% → 导致架构调整为 LLM + Web Search 主引擎
- 结论：Moment 1 推荐数据充分可行，Moment 2 由 LLM + Web Search 驱动

**验证 2：LLM + Web Search 菜品推荐质量 — ✅ 已完成（含已知局限）**
- 测试：对 Zareen's（Palo Alto）发送带用户偏好的推荐请求
- 结果：LLM 成功从多来源聚合菜品信息，质量高
- **已知局限：推荐菜品可能与实际菜单不符（创始人亲身验证）。** 需在推荐时标注信息来源，并提供"菜单上没这个"按钮快速调整。

**验证 3：PWA GPS 权限体验 — ⬜ 待完成**
- 在手机浏览器中测试 Geolocation API 的精度和权限请求流程
- 确认 iOS Safari 和 Android Chrome 都能正常工作

**验证 4：创始人亲身用餐体验 — ✅ 已完成（两次）**

经历 A：使用 Claude 推荐 Menlo Park 缅甸餐厅
- 痛点 1：到门口对餐厅一无所知（背景、菜品、氛围），感到慌张
- 痛点 2：一个人进入聚会氛围的餐厅，坐在吧台很尴尬 → **氛围匹配比口味更重要**
- 痛点 3：Claude 推荐的菜菜单上没有，需要打字重新问，放弃后找服务员
- 痛点 4：价位偏高但事先不知道
- 痛点 5：吃完后旅程直接断裂，没有分享、庆祝、记录的环节

经历 B：使用 Claude 推荐附近餐厅（当天）
- 痛点 1：去的路上感到不安（陌生地方）
- 痛点 2：推荐的菜品很多在菜单上找不到
- 痛点 3：需求变更时要费力打字，体验很差，不想再问了
- 痛点 4：坐下来以后旅程结束，想拍照分享但没有承接

**这两次经历直接验证了 Gusto 三个 Moment 设计的必要性，并催生了以下设计决策：**
1. 推荐必须包含氛围标签（适合一个人 / 聚会 / 约会）
2. Moment 2 必须提供餐厅背景故事和 Neighbourhood 介绍
3. 菜品推荐需诚实标注置信度，提供快速调整按钮（不打字）
4. Moment 3 必须存在——接住用户拍照、庆祝、分享的本能冲动

### Known Risks
| 风险 | 影响 | 缓解方案 |
|------|------|---------|
| ~~Google Places 菜单数据覆盖率低~~ | ~~质量下降~~ | ✅ 已解决：改用 LLM + Web Search 作为主引擎 |
| LLM + Web Search 延迟（3-5 秒） | Moment 2 加载慢 | 加 loading 动画；用户在做决定不是刷短视频，可接受 |
| **菜品推荐与实际菜单不符（已验证）** | **信任崩塌（最高优先级）** | **诚实标注信息来源 + "菜单上没这个"按钮快速调整 + v1.1 菜单拍照扫描** |
| **氛围不匹配（已验证）** | **整体体验变差** | **推荐时标注氛围标签 + Moment 1 Beat 2 采集用餐场景** |
| LLM 推荐不准或幻觉 | 用户失去信任 | Onboarding 偏好画像 + 持续学习 + 可纠正 + Google Reviews 交叉验证 |
| GPS 精度不够 | 推荐距离不准 | 显示距离范围而非精确距离 |
| 用户 Onboarding 流失 | 没有偏好数据 | 允许跳过，用默认推荐 |
| API 成本超出免费额度 | 需要付费 | Phase 1 只有一个用户，不可能超 |
| Web Search 结果不稳定 | 不同时间搜到不同内容 | 缓存已搜索过的餐厅数据到 Supabase |
| **Moment 2-3 连续陪伴的技术实现** | **实时性要求高** | **分阶段实现：v1 基础版 Moment 3，v1.1 完整版** |

---

## Appendix: Execution Plan

### 四周启动计划（Part-time，每周 8-10 小时）

**第 0 周：验证 + 环境配置**
- 发 20 条私信验证需求
- 做落地页收集 20 个邮箱
- 配置 Claude Code + Stitch + ChatPRD 工具链
- ~~验证 Google Places 覆盖率~~ ✅ 已完成
- ~~验证 LLM + Web Search 菜品推荐质量~~ ✅ 已完成
- **待完成：验证 PWA GPS 权限体验**

**第 1 周：最小原型**
- 周一：ChatPRD 完成正式 PRD
- 周三：Stitch 出核心页面设计
- 周五+周末：Claude Code 实现 MVP

**第 2 周：自己用**
- 不写代码，只用自己的 APP 吃饭
- 记录每次使用体验和问题

**第 3 周：迭代**
- 根据使用反馈修改
- 重新部署

此后重复第 2-3 周循环。
