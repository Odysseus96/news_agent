# fetcher/web_parser.py

import requests
from bs4 import BeautifulSoup
from typing import Optional

try:
    from readability import Document as ReadableDoc
    USE_READABILITY = True
except ImportError:
    USE_READABILITY = False

def extract_text_from_url(url: str) -> Optional[str]:
    """
    抓取网页并提取正文内容。优先使用 readability，否则 fallback 基本提取。
    """
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        html = resp.text

        if USE_READABILITY:
            doc = ReadableDoc(html)
            summary_html = doc.summary()
            soup = BeautifulSoup(summary_html, "html.parser")
            return soup.get_text(separator="\n").strip()

        soup = BeautifulSoup(html, "html.parser")
        paras = soup.find_all("p")
        text = "\n".join(p.get_text().strip() for p in paras if len(p.get_text()) > 50)
        return text.strip() or None

    except Exception as e:
        print(f"[web_parser] 抓取 / 解析失败: {url} - {e}")
        return None
