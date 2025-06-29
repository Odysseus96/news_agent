import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime
import os

def generate_source_bar_chart(news_list: list[dict], output_dir: str = "./logs"):
    today = datetime.today().strftime("%Y-%m-%d")
    path = os.path.join(output_dir, f"{today}_bar.png")

    sources = [n["source"] for n in news_list]
    count = Counter(sources)
    labels, values = zip(*count.items())

    plt.figure(figsize=(8, 4))
    plt.barh(labels, values, color="skyblue")
    plt.title("新闻来源分布")
    plt.xlabel("文章数")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
