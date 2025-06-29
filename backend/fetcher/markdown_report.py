import os
from datetime import datetime

def save_news_as_markdown(news_list: list[dict], output_dir: str = "./logs"):
    os.makedirs(output_dir, exist_ok=True)
    today = datetime.today().strftime("%Y-%m-%d")
    md_path = os.path.join(output_dir, f"{today}.md")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# 🗞️ {today} 科技新闻日报\n\n")
        f.write(f"共收录新闻条目：{len(news_list)} 篇\n\n")
        f.write("## 📊 来源统计图\n")
        f.write(f"![](./{today}_bar.png)\n\n")
        f.write("## 📰 新闻列表\n")

        for idx, news in enumerate(news_list, 1):
            f.write(f"### {idx}. {news['title']}\n")
            f.write(f"- 来源: {news['source']}\n")
            f.write(f"- 链接: {news['link']}\n")
            f.write(f"- 发布时间: {news['published']}\n\n")
            f.write(f"{news['content'][:500]}...\n\n---\n")
