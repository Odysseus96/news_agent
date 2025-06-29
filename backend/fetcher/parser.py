from .crawler import fetch_rss_entries, extract_full_article
from datetime import datetime
from typing import List, Dict
from feedparser import FeedParserDict

def parse_news_from_rss(rss_url: str, source: str) -> List[Dict[str, str]]:
    """
    从 RSS 链接中获取结构化新闻内容
    """
    parsed: List[Dict[str, str]] = []
    entries: List[FeedParserDict] = fetch_rss_entries(rss_url)

    for entry in entries:
        try:
            link = str(entry.get("link", ""))
            if not link.startswith("http"):
                continue  # 无效链接

            body = extract_full_article(link)
            parsed.append({
                "title": entry.get("title", "无标题"),
                "link": link,
                "published": str(entry.get("published", datetime.now())),
                "source": source,
                "content": body
            })
        except Exception as e:
            print(f"[parse_news_from_rss] 单条解析失败: {e}")
            continue

    return parsed

