# fetcher/crawler.py

import feedparser
import requests
from bs4 import BeautifulSoup
from typing import List, Any
from feedparser import FeedParserDict

def fetch_rss_entries(rss_url: str) -> List[FeedParserDict]:
    """
    从 RSS 源中获取新闻条目
    """
    try:
        feed = feedparser.parse(rss_url)
        return feed.entries
    except Exception as e:
        print(f"[fetch_rss_entries] RSS 抓取失败: {rss_url} - {e}")
        return []

def extract_full_article(url: str) -> str:
    """
    抓取网页正文内容（简单抓取所有段落）
    """
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        paragraphs = soup.find_all("p")
        text = "\n".join(p.get_text().strip() for p in paragraphs if len(p.get_text()) > 30)
        return text if text else "[无正文内容]"
    except Exception as e:
        print(f"[extract_full_article] 抓取失败: {url} - {e}")
        return "[抓取失败]"
