#!/usr/bin/env python3
"""HR x AI - update script"""

import json
import hashlib
import os
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.parse import urljoin
import feedparser
import requests
from bs4 import BeautifulSoup

CONFIG_PATH = Path("config/hr_sources.json")
OUTPUT_DIR = Path("data")
OUTPUT_PATH = OUTPUT_DIR / "hr-radar.json"

HR_KEYWORDS = {
    "policy": [
        "劳动合同", "劳动关系", "劳动争议", "社保", "公积金", "最低工资",
        "工时", "加班", "休假", "人才引进", "职业技能",
        "培训补贴", "裁员", "竞业限制", "劳务派遣", "灵活用工", "外包",
        "个人信息保护", "员工数据", "员工监控", "算法治理", "自动化决策",
        "劳动法", "劳动仲裁", "用工合规", "工资支付", "薪酬调整", "福利政策",
        "社会保险", "就业促进",
        "人力资源社会保障", "人社部", "国务院", "人社局",
        "labor law", "social security", "severance", "non-compete",
        "minimum wage", "overtime pay", "employee data privacy",
        "department of labor", "DOL", "EEOC", "OSHA",
        "lawsuit", "harassment", "discrimination", "wrongful",
        "labor department", "proposes rule", "regulation",
        "wage and hour", "FMLA", "FLSA", "health coverage",
        "workers compensation", "unemployment",
        "equal pay", "pay equity", "pay gap", "gender pay",
        "class action", "settlement", "arbitration",
        "paid leave", "sick leave", "family leave",
        "commute", "commuting", "expense reimbursement",
        "worker misclassification", "independent contractor",
        "joint employer", "union", "collective bargaining"
    ],
    "ai_recruiting": [
        "AI招聘", "智能招聘", "AI面试", "简历筛选", "人才画像",
        "招聘自动化", "候选人匹配", "智能人岗匹配",
        "AI recruiting", "AI hiring", "AI-powered hiring",
        "resume screening", "talent acquisition", "smart interview",
        "applicant tracking", "ATS", "AI agent", "AI agents",
        "AI-powered recruitment", "automated hiring",
        "AI sourcing", "AI assessment", "chatbot",
        "recruitment automation", "predictive hiring"
    ],
    "org_talent": [
        "组织设计", "人才盘点", "组织发展", "OD", "HRBP",
        "员工体验", "人才梯队", "绩效管理",
        "organization design", "talent review", "employee experience",
        "people analytics", "succession planning",
        "performance review", "performance management",
        "employee engagement", "company culture", "workplace culture",
        "organizational", "workforce planning",
        "talent strategy", "talent management", "retention",
        "burnout", "well-being", "wellbeing", "wellness",
        "hybrid work", "remote work", "return to office", "RTO",
        "employee survey", "employee satisfaction",
        "DEI", "diversity", "inclusion", "belonging",
        "chief people officer", "CHRO", "VP of people"
    ],
    "learning": [
        "AI培训", "学习发展", "技能转型", "企业培训", "岗位技能",
        "人才培养", "L&D", "技能提升", "职业培训",
        "upskilling", "reskilling", "learning and development",
        "corporate training", "workforce training",
        "skills gap", "skills development", "career development",
        "coaching", "mentoring", "onboarding",
        "professional development", "credential",
        "AI skills", "AI literacy", "digital skills",
        "leadership development", "manager training"
    ],
    "hr_product": [
        "HR SaaS", "飞书 People", "北森", "Moka", "Workday",
        "SAP SuccessFactors", "人力资源系统", "招聘系统", "HRIS",
        "薪酬管理", "考勤系统", "HR数字化", "员工服务",
        "HR tech", "HR platform", "HR management system",
        "payroll software", "HR automation", "HR software",
        "HR system", "HR tool", "people operations platform",
        "HR analytics", "people analytics software",
        "benefits platform", "compensation software",
        "time tracking", "workforce management software"
    ],
    "cases": [
        "案例", "调研报告", "白皮书", "行业报告", "HR趋势",
        "人才趋势", "年度报告", "薪酬报告",
        "HR report", "HR trend", "talent trend", "HR research",
        "workforce report", "HR case study",
        "survey", "study finds", "report finds",
        "workers say", "employees say", "workers report",
        "CEO pay", "executive compensation",
        "best places to work", "top companies",
        "workforce of the future", "future of work",
        "state of", "outlook"
    ]
}

NOISE_KEYWORDS = [
    "娱乐", "明星", "八卦", "体育", "彩票", "旅游", "美食",
    "游戏", "影视", "股票", "炒股", "crypto", "bitcoin"
]

AI_KEYWORDS = [
    "AI", "人工智能", "大模型", "LLM", "生成式", "GenAI", "Agent",
    "智能体", "算法", "自动化", "机器学习", "深度学习",
    "artificial intelligence", "machine learning", "automation",
    "generative AI", "large language model"
]

SOURCE_PRIORS = {
    "hr_dive": 0.5, "aihr": 0.5, "hrexecutive": 0.5,
    "hrzone": 0.5, "clo": 0.5, "worklife": 0.5, "aihot": 0.2
}


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def fetch_rss(source):
    url = source.get("url", "")
    if not url:
        return []
    items = []
    try:
        parsed = feedparser.parse(url)
        for entry in parsed.entries:
            title = entry.get("title", "")
            link = entry.get("link", "")
            if not title or not link:
                continue
            parsed_time = None
            published = entry.get("published", "")
            if published:
                try:
                    if hasattr(entry, "published_parsed") and entry.published_parsed:
                        parsed_time = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
                    elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
                        parsed_time = datetime(*entry.updated_parsed[:6], tzinfo=timezone.utc)
                except Exception:
                    pass
            if not parsed_time:
                parsed_time = datetime.now(timezone.utc)
            items.append({
                "title": title,
                "url": link,
                "published_at": parsed_time.isoformat(),
                "source_id": source.get("id", "unknown"),
                "source_name": source.get("name", "Unknown"),
                "source_region": source.get("region", ""),
                "source_level": source.get("level", "")
            })
    except Exception as e:
        print("  抓取失败 {}: {}".format(source.get("name"), e))
    return items


def fetch_html_page(source):
    url = source.get("url", "")
    sid = source.get("id", "")
    name = source.get("name", "Unknown")
    if not url:
        return []
    items = []
    try:
        resp = requests.get(url, timeout=30, headers={
            "User-Agent": "Mozilla/5.0 (compatible; HR-Radar/1.0)"
        })
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        article_selectors = [
            "article", ".post", ".post-item", ".blog-item",
            ".article-item", ".entry", ".post-preview", ".post-list > *"
        ]
        title_selectors = [
            "h2 a", "h3 a", ".title a", ".post-title a",
            ".entry-title a", "a.title"
        ]
        date_selectors = [
            "time", ".date", ".post-date", ".entry-date",
            ".published", ".meta time", ".post-meta time"
        ]
        articles = []
        for sel in article_selectors:
            articles = soup.select(sel)
            if articles:
                break
        if not articles:
            articles = [soup]
        for article in articles[:30]:
            title_el = None
            for tsel in title_selectors:
                title_el = article.select_one(tsel)
                if title_el:
                    break
            if not title_el:
                continue
            title = title_el.get_text(strip=True)
            link = title_el.get("href", "")
            if not title or not link:
                continue
            if link.startswith("/"):
                link = urljoin(url, link)
            published = datetime.now(timezone.utc)
            for dsel in date_selectors:
                date_el = article.select_one(dsel)
                if date_el:
                    date_text = date_el.get("datetime", "") or date_el.get_text(strip=True)
                    parsed = parse_date_from_text(date_text)
                    if parsed:
                        published = parsed
                        break
            items.append({
                "title": title,
                "url": link,
                "published_at": published.isoformat(),
                "source_id": sid,
                "source_name": name,
                "source_region": source.get("region", ""),
                "source_level": source.get("level", "")
            })
    except Exception as e:
        print("  页面解析失败 {} ({}): {}".format(name, url, e))
    return items


def parse_date_from_text(text):
    from dateutil import parser as dateparser
    try:
        dt = dateparser.parse(text, fuzzy=True)
        if dt is None:
            return None
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        return None


def classify_item(title):
    t = title.lower()
    if any(kw.lower() in t for kw in HR_KEYWORDS["policy"]):
        return "政策与劳动合规"
    if any(kw.lower() in t for kw in HR_KEYWORDS["ai_recruiting"]):
        return "AI 招聘与招聘工具"
    if any(kw.lower() in t for kw in HR_KEYWORDS["org_talent"]):
        return "组织与人才管理"
    if any(kw.lower() in t for kw in HR_KEYWORDS["learning"]):
        return "学习发展与技能转型"
    if any(kw.lower() in t for kw in HR_KEYWORDS["hr_product"]):
        return "HR 产品与数字化"
    if any(kw.lower() in t for kw in HR_KEYWORDS["cases"]):
        return "案例、报告与趋势"
    return None


def is_hr_relevant(title, source_id=""):
    if source_id in ("hr_dive", "aihr", "hrzone", "hrexecutive", "talentculture", "aihot"):
        return True
    t = title.lower()
    for noise in NOISE_KEYWORDS:
        if noise.lower() in t:
            return False
    all_hr = []
    for kw_list in HR_KEYWORDS.values():
        all_hr.extend(kw_list)
    has_hr = any(kw.lower() in t for kw in all_hr)
    has_ai = any(kw.lower() in t for kw in AI_KEYWORDS)
    return has_hr or has_ai


def is_ai_hr_crossover(title):
    t = title.lower()
    all_hr = []
    for kw_list in HR_KEYWORDS.values():
        all_hr.extend(kw_list)
    has_hr = any(kw.lower() in t for kw in all_hr)
    has_ai = any(kw.lower() in t for kw in AI_KEYWORDS)
    return has_hr and has_ai


def score_item(item):
    t = item.get("title", "").lower()
    tz = item.get("title_zh", "").lower()
    combined = t + " " + tz
    sid = item.get("source_id", "")
    prior = SOURCE_PRIORS.get(sid, 0.3)

    all_hr = []
    for kw_list in HR_KEYWORDS.values():
        all_hr.extend(kw_list)
    hr_hits = sum(1 for kw in all_hr if kw.lower() in combined)
    ai_hits = sum(1 for kw in AI_KEYWORDS if kw.lower() in combined)

    low = ["harassment", "lawsuit", "sexist", "discrimination", "slur", "bias claim", "骚扰", "歧视"]

    hr_score = min(hr_hits / 3.0, 1.0) * prior
    ai_score = min(ai_hits / 1.0, 1.0) * prior

    relevance = max(hr_score, ai_score)

    if sid == "aihot" and hr_hits == 0:
        return min(relevance, 0.25)

    if hr_hits > 0 and ai_hits > 0:
        relevance = min(0.55 + hr_score * 0.2 + ai_score * 0.3, 1.0)

    if any(kw.lower() in combined for kw in low):
        relevance *= 0.4

    return round(relevance, 2)

def translate_title(title, api_key):
    if not api_key:
        return title, ""
    try:
        resp = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={"Authorization": "Bearer " + api_key},
            json={
                "model": "deepseek-v4-flash",
                "messages": [{"role": "user", "content": (
                    "直接输出中文标题和摘要。格式：中文标题||摘要\n\n英文标题：" + title
                )}],
                "max_tokens": 500,
                "temperature": 0.3
            },
            timeout=60
        )
        msg = resp.json()["choices"][0]["message"]
        text = msg.get("content", "") or msg.get("reasoning_content", "")
        for line in text.split("\n"):
            line = line.strip()
            if "||" in line:
                parts = line.split("||", 1)
                p0 = parts[0].strip()
                p1 = parts[1].strip() if len(parts) > 1 else ""
                return (p0, p1) if p0 else (title, "")
        last = text.strip().split("\n")[-1].strip()
        return (last[:25], last[26:110]) if len(last) > 25 else (title, "")
    except Exception as e:
        print("  翻译异常: " + str(type(e).__name__))
        return title, ""


def dedupe_items(items):
    seen_urls = set()
    seen_titles = set()
    result = []
    for item in items:
        url = item.get("url", "")
        title = item.get("title", "")
        if url in seen_urls:
            continue
        seen_urls.add(url)
        title_norm = title.strip().lower()
        if title_norm in seen_titles:
            continue
        seen_titles.add(title_norm)
        result.append(item)
    return result


def main():
    print("=" * 40)
    print("HR x AI 资讯台 - 更新脚本")
    print("=" * 40)
    config = load_config()
    api_key = os.environ.get("DEEPSEEK_API_KEY", "")
    categories = config.get("categories", [])
    sources = config.get("sources", [])
    all_items = []
    for source in sources:
        if not source.get("enabled", True):
            continue
        src_type = source.get("type", "rss")
        print("正在抓取: {} ...".format(source["name"]))
        if src_type == "html":
            items = fetch_html_page(source)
        else:
            items = fetch_rss(source)
        print("  获取 {} 条".format(len(items)))
        all_items.extend(items)
    print("\n总计抓取: {} 条原始资讯".format(len(all_items)))

    lookback = config.get("lookback_days", 7)
    cutoff = datetime.now(timezone.utc) - timedelta(days=lookback)
    recent = []
    for item in all_items:
        try:
            pt = datetime.fromisoformat(item["published_at"])
            if pt >= cutoff:
                recent.append(item)
        except Exception:
            recent.append(item)
    print("时间窗口过滤 ({} 天内): {} 条".format(lookback, len(recent)))

    processed = []
    aihot_total = 0
    aihot_kept = 0
    for item in recent:
        title = item.get("title", "")
        sid = item.get("source_id", "")
        if sid == "aihot":
            aihot_total += 1
        if not is_hr_relevant(title, source_id=sid):
            continue
        if sid == "aihot":
            aihot_kept += 1
        category = classify_item(title)
        if not category:
            category = item.get("default_category", "案例、报告与趋势")
        item["is_ai_hr"] = is_ai_hr_crossover(title)
        item["category"] = category
        uid = hashlib.md5("{}{}".format(item["url"], item["title"]).encode()).hexdigest()[:12]
        item["id"] = uid
        item["title_zh"], item["summary_zh"] = translate_title(title, api_key)
        item["relevance"] = score_item(item)
        processed.append(item)

    print("HR 相关筛选后: {} 条".format(len(processed)))
    if aihot_total > 0:
        print("  AIHOT: {} 条 -> 保留 {} 条 (过滤 {} 条)".format(aihot_total, aihot_kept, aihot_total - aihot_kept))

    processed = dedupe_items(processed)
    print("去重后: {} 条".format(len(processed)))
    processed.sort(key=lambda x: x.get("relevance", 0), reverse=True)

    limit = config.get("daily_pick_limit", 12)
    final_items = processed[:limit]

    categorized = {cat: [] for cat in categories}
    for item in final_items:
        cat = item.get("category", "案例、报告与趋势")
        if cat in categorized:
            categorized[cat].append(item)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output = {
        "generated_at": datetime.now(timezone(timedelta(hours=8))).isoformat(),
        "name": config.get("name", "HR x AI 资讯台"),
        "total_count": len(final_items),
        "categories": categories,
        "items_by_category": categorized,
        "all_items": final_items
    }
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("\n已生成: {}".format(OUTPUT_PATH))
    print("   共 {} 条精选资讯".format(len(final_items)))


if __name__ == "__main__":
    main()
