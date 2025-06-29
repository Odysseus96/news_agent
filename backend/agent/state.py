from typing import List, Optional, TypedDict


class AgentState(TypedDict):
    user_query: str
    news_data: Optional[List[dict]]
    report: Optional[str]