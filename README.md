<div align="center">

# HR × AI 资讯台

## 聚焦人力资源与人工智能交叉领域

**每天早上 8 点，自动汇总海外 HR 资讯 + 中国劳动政策，翻译成中文，按相关度精选。**

[![Live](https://img.shields.io/badge/Live-SyntaxOfLife.github.io%2Fhr--ai--radar-blue?style=flat-square)](https://SyntaxOfLife.github.io/hr-ai-radar/hr/)
[![License](https://img.shields.io/badge/license-MIT-green.svg?style=flat-square)](LICENSE)

**在线站** → [SyntaxOfLife.github.io/hr-ai-radar/hr/](https://SyntaxOfLife.github.io/hr-ai-radar/hr/)

</div>

---

## 这是什么

一个面向 HR 团队的信息资讯台，每天自动抓取全球 HR 资讯和中国劳动政策，翻译成中文，按 HR×AI 相关度打分排序，帮助 HR 从业者快速了解：

- 劳动用工、社保、合规政策变化
- AI 如何影响招聘、组织管理、培训
- 值得评估的 HR 产品和企业实践

## 功能

- **9 个自动信息源** + 微信公众号人工精选
- **AI 中文翻译**（硅基流动 GLM-4）
- **相关度打分**，区分"高相关度"和"全部"两档，最高分置顶为"要闻"
- **6 个栏目分类**，政策合规 / AI招聘 / 组织人才 / 学习发展 / HR产品 / 案例趋势
- **两栏布局**，桌面端侧栏分类导航 + 来源分布
- **搜索**，实时过滤标题、摘要、来源
- **已读标记**，本地保存阅读进度
- **PWA 支持**，可添加到手机主屏，像 App 一样打开
- **GitHub Actions 每天自动更新**（北京时间 8:00）

## 信息源

| 来源 | 类型 | 覆盖 |
|------|------|------|
| HR Dive | RSS | 组织人才、美国政策 |
| AIHR | RSS | AI 招聘、学习发展 |
| HRExecutive | RSS | 案例报告、HR 产品 |
| HRZone | RSS | 组织人才 |
| Chief Learning Officer | RSS | 学习发展 |
| WorkLife | RSS | 组织人才 |
| Littler | RSS | 雇佣法、用工分类 |
| ELA | RSS | 欧盟派遣工、跨境用工 |
| AIHOT | RSS | AI 行业（全量档） |
| 公众号人工精选 | 手动 | 中国劳动政策 |

## 技术栈

- Python 3.11 + feedparser + BeautifulSoup
- GitHub Actions 定时抓取
- GitHub Pages 静态托管
- 硅基流动 GLM-4 中文翻译

## 目录结构

```
config/hr_sources.json   # 信息源配置
scripts/update_hr_radar.py  # 抓取 + 分类 + 打分 + 翻译
data/manual_items.json   # 公众号人工精选
hr/index.html            # 前端页面
hr/manifest.json         # PWA 配置
hr/sw.js                 # Service Worker（离线缓存）
hr/icon.svg              # 应用图标
.github/workflows/update-hr-radar.yml  # 自动更新
```

## 如何添加公众号文章

编辑 `data/manual_items.json`，添加条目：

```json
{
  "title": "文章标题",
  "url": "https://mp.weixin.qq.com/s/xxxxxx",
  "category": "政策与劳动合规",
  "source_name": "劳动法库",
  "region": "中国"
}
```

文章默认 3 天后自动下线。

## 免责声明

本页面仅汇总公开资讯，不构成劳动法律意见。政策类内容请以官方原文及法务意见为准。

## 致谢

本项目 fork 自 [LearnPrompt/ai-news-radar](https://github.com/LearnPrompt/ai-news-radar)，一个设计精良的 AI 新闻聚合器。我们保留了它的技术骨架（RSS 抓取 + 关键词打分 + 静态托管 + GitHub Actions 自动化），把场景从"泛 AI 新闻"改造成"HR × AI 资讯"。

原项目的作者们完成了我远不能及的工程量——多源去重、故事线合并、三口味锐评、源健康监控等一整套体系。本项目的价值仅仅在于做了场景替换和内容筛选，技术上的绝大部分都归功于原项目。

如果这个项目对你有用，请一并感谢 [ai-news-radar](https://github.com/LearnPrompt/ai-news-radar) 的原作者。

## License

MIT
