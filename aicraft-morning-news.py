#!/usr/bin/env python3
"""
AICraft 每日早报 Agent
每天 8:00 自动抓三大板块全球最新新闻
部署: GZ /opt/aicraft/monitor/ · Cron: 0 8 * * *
"""

import re
import subprocess
from datetime import datetime
from pathlib import Path

LOG_DIR = Path("/opt/aicraft/monitor/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
REPORT_FILE = LOG_DIR / f"morning_brief_{datetime.now().strftime('%Y%m%d')}.md"

# 关键搜索词
SEARCHES = {
    "AI聚合平台": [
        "AI API aggregation platform OpenRouter 2026",
        "大模型API中转站 API聚合平台 2026",
    ],
    "AI短剧/视频": [
        "AI short drama AI video generation 2026",
        "AI短剧 AI漫剧 出海 2026",
    ],
    "AI智能体/Skills": [
        "AI agent marketplace GPT Store Coze 2026",
        "AI智能体市场 2026",
    ],
    "日本/南美市场": [
        "Japan AI API market 2026",
        "Brazil AI developer API 2026",
    ],
    "数据跨境/合规": [
        "China data cross-border AI regulation 2026",
        "数据出境 负面清单 AI 2026",
    ],
    "竞品动态": [
        "OpenRouter SiliconFlow 竞争 2026",
        "DeepSeek Qwen MiniMax API 定价 2026",
    ],
}


def search_news(query):
    """用 curl 搜 Google News"""
    try:
        import urllib.parse
        url = f"https://news.google.com/rss/search?q={urllib.parse.quote(query)}&hl=en-US&sort=date"
        result = subprocess.run(
            ["curl", "-sk", "-m", "10", url],
            capture_output=True, text=True, timeout=15
        )
        items = re.findall(r'<title>([^<]+)</title>', result.stdout)
        # Filter out Google boilerplate
        news = [t for t in items if 'Google' not in t and t.strip()][:5]
        return news
    except:
        return []


def main():
    print(f"[早报] {datetime.now().strftime('%Y-%m-%d %H:%M')} 开始采集")
    report = f"# AICraft 每日早报 · {datetime.now().strftime('%Y年%m月%d日')}\n\n"

    total_news = 0
    for category, queries in SEARCHES.items():
        report += f"## {category}\n\n"
        for q in queries:
            news = search_news(q)
            for n in news:
                if len(n) > 10:
                    report += f"- {n}\n"
                    total_news += 1
        report += "\n"

    report += f"\n---\n*自动生成 · {total_news} 条新闻 · AICraft Morning Brief Agent*"

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report)

    # Also save as latest
    latest = LOG_DIR / "LATEST_BRIEF.md"
    latest.write_text(report, encoding="utf-8")

    print(f"[早报] 完成 · {total_news} 条新闻 → {REPORT_FILE}")
    print(report[:500])


if __name__ == "__main__":
    main()
