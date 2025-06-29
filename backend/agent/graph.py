from typing import TypedDict, Optional, List
from langgraph.graph import StateGraph, END
from tools.retriever_tool import retrieve_news
from agent.analysis_agent import analysis_agent
from agent.state import AgentState


def route_input(state: AgentState):
    if "政策" in state["user_query"] or "分析" in state["user_query"]:
        return "call_retriever"
    return "direct_summary"

# 构建 LangGraph 工作流
workflow = StateGraph(AgentState)
workflow.add_node("retriever", retrieve_news)
workflow.add_node("analyst", analysis_agent)
workflow.add_conditional_edges("start", route_input, {
    "call_retriever": "retriever",
    "direct_summary": "analyst"
})
workflow.add_edge("retriever", "analyst")
workflow.add_edge("analyst", END)

graph_executor = workflow.compile()
