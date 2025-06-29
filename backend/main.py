from agent.graph import graph_executor
from agent.state import AgentState

def run_analysis(query: str) -> dict:
    state: AgentState = {
        "user_query": query,
        "news_data": None,
        "report": None
    }
    final_state = graph_executor.invoke(state)
    return final_state
