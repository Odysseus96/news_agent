# fetcher/fetch_news.py

from fetcher.parser import parse_news_from_rss
from fetcher.ingest import ingest_news
from config import rss_sources

def fetch_all_news():
    all_news = []
    for feed in rss_sources:
        news = parse_news_from_rss(feed["url"], feed["source"])
        all_news.extend(news)

    ingest_news(all_news)
