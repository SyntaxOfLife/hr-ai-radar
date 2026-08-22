# HR × AI 资讯台 Agent Notes

## Scope

This repo powers the HR × AI 资讯台 static site — a daily aggregation of global HR news and Chinese labor policy, translated to Chinese and ranked by HR×AI relevance. Forked from [LearnPrompt/ai-news-radar](https://github.com/LearnPrompt/ai-news-radar).

## Working Rules

- Keep changes small and reviewable.
- Do not commit private feeds, secrets, tokens, cookies, or `.env` values.
- Prefer stable public RSS/Atom sources before adding custom scrapers.
- HR-specific sources go through `config/hr_sources.json`.
- Manually curated Chinese articles go in `data/manual_items.json`.

## Source Strategy

Default source priority:

1. Official RSS/Atom feeds.
2. HR-specific media and legal publications.
3. Manually curated WeChat articles (China labor policy).

Avoid account-bound feeds, login-gated pages, and fragile scrapers.

## Common Commands

```bash
python scripts/update_hr_radar.py
python -m http.server 8080
```

Frontend: `hr/index.html` — reads `data/hr-radar.json`.
