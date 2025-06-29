from fetcher.fetch_news import fetch_all_news
from main import run_analysis

def scheduled_job():
    print("🗞 正在抓取科技新闻...")
    fetch_all_news()
    print("✅ 抓取完成，开始生成摘要")
    run_analysis("请分析今天的科技新闻")
