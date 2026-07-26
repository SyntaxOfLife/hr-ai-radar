# HR × AI 资讯台 — 实施计划

> 2026-07-20 确认 · 待执行

## 最终信息源配置（9 个源）

### 保留（3 个）

| ID | 名称 | RSS/方式 | 默认栏目 | 地区 | 等级 |
|----|------|----------|----------|------|------|
| hr_dive | HR Dive | RSS: `https://www.hrdive.com/feeds/news/` | 组织与人才管理 | 全球 | 行业媒体 |
| josh_bersin | Josh Bersin | RSS: `https://joshbersin.com/category/hr-technology/feed/` | 案例、报告与趋势 | 全球 | 权威媒体 |
| aihot | AIHOT | RSS: `https://aihot.virxact.com/feed/daily.xml` | 案例、报告与趋势 | 全球 | AI 垂直源 |

### 新增（6 个）

| ID | 名称 | RSS/方式 | 默认栏目 | 地区 | 等级 |
|----|------|----------|----------|------|------|
| gov_cn | 中国政府网 | RSS: `http://www.gov.cn/rss/` | 政策与劳动合规 | 全国 | 官方政策 |
| mohrss_law | 人社部-政策法规 | RSS: `http://www.mohrss.gov.cn/gkml/xxgk/rss.xml` | 政策与劳动合规 | 全国 | 官方政策 |
| mohrss_jd | 人社部-政策解读 | RSS: `http://www.mohrss.gov.cn/gkml/zcjd/rss.xml` | 政策与劳动合规 | 全国 | 官方解读 |
| 36kr | 36氪 | RSS: `https://36kr.com/feed`（全站，需关键词过滤） | 跨栏目 | 全国 | 行业媒体 |
| moka | Moka 博客 | 页面解析 `blog.mokahr.com` | AI 招聘与招聘工具 | 中国 | HR 产品 |
| bipo | BIPO 博客 | 页面解析 `blog.bipoinfo.com` | 组织与人才管理 | 全球 | HR 产品 |

### 不接入

| 源 | 原因 |
|----|------|
| 上海人社局 | 无 RSS，页面解析不稳定，先暂停 |
| HRTechChina | 仅邮件订阅，无 RSS 无稳定列表页 |
| 飞书更新日志 | SPA 动态页面，requests 不可达 |
| 北森、钉钉 | 明确不要 |
| 猎聘、智联 | 内容偏营销，信号密度低 |

---

## 阶段一：信息源 + 去噪音 + 前端细节（预计 4-5 天）

### 1.1 前端细节修复

**文件**: `hr/index.html`

- 加载失败时显示“加载失败，请稍后重试” + 刷新按钮
- 空数据时区分“暂无资讯”与“加载失败”
- 添加 favicon（复用 assets/logo.svg 或新建简单 HR 图标）
- 移动端底部留白优化

### 1.2 AIHOT 噪音过滤

**文件**: `scripts/update_hr_radar.py`

- 对 AIHOT 来源额外做 HR 关键词二次过滤
- HR 不相关的内容直接丢弃，不强行分类
- 调整分类优先级：政策关键词避免误匹配英文泛 HR 文章

### 1.3 接入 RSS 源（中国政府网、人社部×2、36氪）

**文件**: `config/hr_sources.json`、`scripts/update_hr_radar.py`

- 三个政府源直接用 `feedparser` 接入，和现有 RSS 源同一套逻辑
- 36氪全站 RSS 接入后，用关键词白名单过滤：
  ```
  劳动、用工、招聘、裁员、社保、公积金、仲裁、合规、
  HR、人才、培训、薪酬、灵活用工、劳务派遣、竞业限制、
  个人信息保护、AI 面试、AI 招聘、人力资源、员工
  ```
- 36氪过滤后按关键词分到各栏目

### 1.4 页面解析源（Moka、BIPO）

**文件**: `scripts/update_hr_radar.py`（新增 `fetch_moka()`、`fetch_bipo()` 函数）

- Moka: 解析 `blog.mokahr.com` 文章列表页，提取标题、链接、日期
- BIPO: 解析 `blog.bipoinfo.com` 文章列表页
- 每个函数独立 try/except，单个源挂了不影响其他源
- 控制台输出抓取条数，方便手动运行时排查

### 1.5 更新配置文件

**文件**: `config/hr_sources.json`

- 新增 `type: "html"` 类型，用于页面解析源
- 新增 `filter_keywords` 字段（36氪专用）
- 保持兼容现有结构

---

## 阶段二：AI 中文摘要（预计 3-5 天）

### 2.1 标题中译 + 一句话摘要

**文件**: `scripts/update_hr_radar.py`（新增 LLM 调用模块）

- 对所有英文标题调用 LLM API 生成中文标题（不超过 25 字）
- 生成一句话摘要（不超过 80 字），说清楚文章讲了什么
- 新增 GitHub Secret：`LLM_API_KEY`
- 建议模型：DeepSeek V3 或通义千问（便宜、中文好）
- 成本控制：每轮最多处理 30 条，超过截断
- LLM 不可用时降级为原始英文标题，不阻断流程
- 输出字段扩展：`title_zh`、`summary_zh`

### 2.2 分类升级

**文件**: `scripts/update_hr_radar.py`

- 现有关键词分类作为 baseline
- LLM 对每条做一次二轮判断：给定 6 个栏目名 + 文章标题/摘要，选最合适的
- LLM 返回低置信度的，fallback 到关键词结果
- LLM 不可用时完全回退关键词分类

### 2.3 精选评分排序

**文件**: `scripts/update_hr_radar.py`

- 每条打一个 0-1 的 HR 相关度分：
  - 关键词命中数
  - 是否 AI×HR 交叉
  - 来源等级加权（官方政策 > 行业媒体 > AI 垂直源）
  - 时效性加权（当天 > 昨天 > 更早）
- 按分排序取 Top 12，替代当前“按时间倒序取前 12”

### 2.4 前端字段适配

**文件**: `hr/index.html`

- 如有 `title_zh`，优先展示中文标题，英文标题作为副标题
- 展示 `summary_zh` 摘要行
- 调整卡片布局容纳新字段

---

## 不做的

- 不做定时触发修复（维持手动运行）
- 不做源健康监控 dashboard
- 不做 Persona 三口味锐评
- 不做故事合并
- 不做 Tab 切换 / 搜索 / 复杂筛选
- 不接 X、抖音、小红书、公众号
- 页面保持单文件 `hr/index.html`，不拆分为 SPA 架构

---

## 文件变更清单

| 阶段 | 文件 | 变更类型 |
|------|------|----------|
| 一 | `hr/index.html` | 修改（前端细节） |
| 一 | `config/hr_sources.json` | 扩展（6 个新源） |
| 一 | `scripts/update_hr_radar.py` | 大幅修改（新 fetcher + 噪音过滤 + 分类修正） |
| 二 | `scripts/update_hr_radar.py` | 追加（LLM 模块 + 评分排序） |
| 二 | `hr/index.html` | 修改（中文标题 + 摘要展示） |
| 二 | `.github/workflows/update-hr-radar.yml` | 修改（增加 LLM_API_KEY secret 引用） |

---

## 验收标准

阶段一完成后：
- 手动运行 `python scripts/update_hr_radar.py` 成功，无报错
- `data/hr-radar.json` 包含来自 9 个源的内容
- 中国政府网、人社部的政策文章出现在“政策与劳动合规”栏目
- 36氪文章经过关键词过滤，HR 相关的内容正确分类
- AIHOT 噪音被过滤，不再出现纯 AI 技术新闻
- `hr/index.html` 正常加载并展示数据

阶段二完成后：
- 英文文章显示中文标题和摘要
- 分类准确率明显高于纯关键词
- LLM 不可用时系统不崩溃
