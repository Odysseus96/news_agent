from config import AI_KEYWORDS

def is_ai_related(news: dict) -> bool:
    content = (news["title"] + news["content"]).lower()
    return any(keyword.lower() in content for keyword in AI_KEYWORDS)
