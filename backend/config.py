import os
from dotenv import load_dotenv

load_dotenv()

AI_KEYWORDS = [
    "科技", "物流", "人工智能", "具身智能", "AI", "AGI", "数字化",
    "大模型", "深度学习", "机器学习", "transformer", "chatgpt", "llm", "多模态",
    "智能体", "agent", "智能机器人", "智能制造", "智慧物流",
    "企业数字化", "自动驾驶", "机器人流程自动化", "RPA"
]

rss_sources = [
    # 🚀 科研 / 技术前沿
    {"url": "https://www.sciencedaily.com/rss/top/technology.xml", "source": "ScienceDaily"},
    {"url": "https://www.technologyreview.com/feed/", "source": "MIT Tech Review"},

    # 🧠 AI & 大模型中文专栏
    {"url": "https://www.jiqizhixin.com/rss", "source": "机器之心"},

    # 📦 中文科技媒体 / 企业动态
    {"url": "https://36kr.com/feed", "source": "36Kr"},
    {"url": "https://www.leiphone.com/feed", "source": "雷锋网"},
    {"url": "https://www.infoq.cn/public/v1/article/rss", "source": "InfoQ 中文"},  # 替代 Gartner

    # 🚛 物流 & 制造
    {"url": "https://iot.ofweek.com/RSSFeed.ashx", "source": "OFweek 物联网"},
    {"url": "https://www.sohu.com/rss/633/", "source": "搜狐 - 智慧物流"},
    {"url": "https://www.sohu.com/rss/147/", "source": "搜狐 - 自动驾驶"},
]



EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

EMAIL_FROM = os.getenv('EMAIL_FROM')

VECTOR_STORE_DIR = os.getenv("VECTOR_STORE_DIR", "./vector_index")

# 验证必需的环境变量
if not EMAIL_PASSWORD:
    raise ValueError("EMAIL_PASSWORD 环境变量未设置")
if not EMAIL_FROM:
    raise ValueError("EMAIL_SENDER 环境变量未设置")
if not EMAIL_RECEIVER:
    raise ValueError("EMAIL_RECEIVER 环境变量未设置")

# 嵌入模型配置
EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "local")

# Local 模式
LOCAL_EMBEDDING_MODEL = os.getenv("LOCAL_EMBEDDING_MODEL", "quentinz/bge-large-zh-v1.5:latest")

# OpenAI 模式
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "")

# Ollama 模式
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY", "ollama-placeholder-key")
OLLAMA_API_BASE = os.getenv("OLLAMA_API_BASE", "http://localhost:11434/v1")
