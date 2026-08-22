<div align="center">

# HR × AI Radar

## Human Resources meets Artificial Intelligence

**Every weekday at 8:00 AM (Beijing time), it aggregates global HR news and Chinese labor policy, translates them into Chinese, and ranks them by HR×AI relevance.**

[![Live](https://img.shields.io/badge/Live-SyntaxOfLife.github.io%2Fhr--ai--radar-blue?style=flat-square)](https://SyntaxOfLife.github.io/hr-ai-radar/hr/)
[![License](https://img.shields.io/badge/license-MIT-green.svg?style=flat-square)](LICENSE)

**Live site** → [SyntaxOfLife.github.io/hr-ai-radar/hr/](https://SyntaxOfLife.github.io/hr-ai-radar/hr/)

</div>

---

## What is this

An information radar for HR teams. It automatically aggregates global HR news and Chinese labor policy every day, translates them into Chinese, and scores them by HR×AI relevance, helping HR professionals quickly understand:

- Changes in labor, social insurance, and compliance policies
- How AI is reshaping recruiting, organizational management, and training
- HR products and enterprise practices worth evaluating

## Features

- **9 automated sources** + manually curated WeChat articles
- **AI Chinese translation** (SiliconFlow GLM-4)
- **Relevance scoring** with "High relevance" and "All" views
- **6 categories**: Policy & Compliance / AI Recruiting / Org & Talent / L&D / HR Products / Cases & Trends
- **Daily auto-update via GitHub Actions** (8:00 AM Beijing time)

## Sources

| Source | Type | Coverage |
|--------|------|----------|
| HR Dive | RSS | Org & talent, US policy |
| AIHR | RSS | AI recruiting, L&D |
| HRExecutive | RSS | Cases, HR products |
| HRZone | RSS | Org & talent |
| Chief Learning Officer | RSS | L&D |
| WorkLife | RSS | Org & talent |
| Littler | RSS | Employment law, worker classification |
| ELA | RSS | EU posted workers, cross-border employment |
| AIHOT | RSS | AI industry (all view) |
| Curated WeChat | Manual | Chinese labor policy |

## Tech stack

- Python 3.11 + feedparser + BeautifulSoup
- GitHub Actions scheduled scraping
- GitHub Pages static hosting
- SiliconFlow GLM-4 Chinese translation

## Directory structure

```
config/hr_sources.json        # Source configuration
scripts/update_hr_radar.py    # Scrape + classify + score + translate
data/manual_items.json        # Manually curated WeChat articles
hr/index.html                 # Frontend
.github/workflows/update-hr-radar.yml  # Auto update
```

## How to add a WeChat article

Edit `data/manual_items.json` and add an entry:

```json
{
  "title": "Article title",
  "url": "https://mp.weixin.qq.com/s/xxxxxx",
  "category": "政策与劳动合规",
  "source_name": "劳动法库",
  "region": "中国"
}
```

Articles auto-expire after 3 days.

## Disclaimer

This site only aggregates public information and does not constitute legal advice. Policy content should be verified against official sources and legal counsel.

## Acknowledgements

This project is forked from [LearnPrompt/ai-news-radar](https://github.com/LearnPrompt/ai-news-radar), a beautifully engineered AI news aggregator. We kept its technical skeleton (RSS fetching + keyword scoring + static hosting + GitHub Actions automation) and adapted the domain from "general AI news" to "HR × AI".

The original authors built an engineering system far beyond what we could have accomplished — multi-source deduplication, story-line merging, three-persona reviews, source health monitoring, and much more. The value of this project lies only in the domain adaptation and content curation; the vast majority of the technical credit belongs to the original project.

If this project is useful to you, please also thank the authors of [ai-news-radar](https://github.com/LearnPrompt/ai-news-radar).

## License

MIT
