from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from tools.mailer_tool import GmailSendMessage
from tools.retriever_tool import retrieve_news

tools = [retrieve_news, GmailSendMessage]

prompt = ChatPromptTemplate.from_template("""
你是一名科技趋势分析师。基于以下新闻生成 Markdown 格式的分析报告，要求：
- 总结主要内容
- 提供数据对比（使用表格）
- 给出图表建议
内容如下：
{input}
""")

agent = create_tool_calling_agent(
    llm=ChatOpenAI(model="deepseek-r1:8b"),
    tools=tools,
    prompt=prompt
)

def analysis_agent(state) -> dict:
    input_news = state.get("news_data", [])
    report = agent.invoke({
        "input": "\n\n".join(input_news)
    })
    return {
        "user_query": state["user_query"],
        "news_data": input_news,
        "report": report
    }
