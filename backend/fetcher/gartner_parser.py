# fetcher/gartner_parser.py

import requests
from bs4 import BeautifulSoup
from fetcher.web_parser import extract_text_from_url
from typing import List, Dict

def fetch_gartner_article_list(list_url: str) -> List[Dict]:
    """
    抓取 Gartner Markdown 中文部分或分析文章列表页的标题+链接
    """
    try:
        res = requests.get(list_url, timeout=10)
        res.raise_for_status()
    except Exception as e:
        print(f"[fetch_gartner_parser] 列表页抓取失败: {e}")
        return []

    soup = BeautifulSoup(res.text, "html.parser")
    items = []
    for a in soup.select("a[href]"):
        href = a["href"]
        if "gartner.com.cn" in href and ("AI" in a.text or "智能" in a.text):
            items.append({"title": a.text.strip(), "link": href})

    return items

def parse_and_ingest_gartner(list_url: str, source: str = "Gartner"):
    """
    抓取列表、获取正文、封装为 news dict 列表
    """
    article_infos = fetch_gartner_article_list(list_url)
    results = []
    for info in article_infos:
        content = extract_text_from_url(info["link"])
        if not content:
            continue
        results.append({
            "title": info["title"],
            "link": info["link"],
            "published": "",  # 可省略或手动设置
            "source": source,
            "content": content
        })
    return results
