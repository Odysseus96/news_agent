# 资讯日报agent(开发中)

### 代码架构

```
backend/
├── main.py                           # 主分析入口
├── gateway.py                        # FastAPI 网关 + Dify 对接 + 定时触发
├── config.py                         # 配置文件（邮箱、模型等）
├── requirements.txt                  # 依赖库清单
│
├── data/                             # 原始新闻源（json/md）
├── logs/                             # 每日报告日志（markdown）
├── vector_index/                     # LlamaIndex 存储目录（向量库）
│
├── agent/                            # LangGraph Agent 路由系统
│   ├── state.py                      # AgentState 类型
│   ├── graph.py                      # LangGraph 状态机构建
│   ├── analysis_agent.py             # 分析 Agent
│   └── retriever_agent.py            # 检索 Agent（可调用工具）
│
├── tools/                            # LangChain Tools
│   ├── retriever_tool.py             # LlamaIndex 检索工具封装
│   ├── mailer_tool.py                # 邮件工具封装
│   └── summarizer_tool.py            # 可选摘要工具
│
├── scheduler/                        # 定时调度器
│   └── scheduler.py                  # 启动每天定时抓取+分析
│
└── fetcher/                          # 🆕 抓取模块
    ├── crawler.py                    # RSS + 网页正文抓取
    ├── parser.py                     # 内容提取与清洗
    ├── ingest.py                     # 保存Markdown & 入库LlamaIndex
    └── fetch_news.py                 # 一键拉取新闻脚本（入口）

```
### 运行
```bash
#!/bin/bash
echo "🔧 启动新闻分析 Agent 服务..."
uvicorn gateway:app --host 0.0.0.0 --port 8000

```

### 整体架构(临时)

``` mermaid
graph TD
    A[Dify前端界面] -->|用户输入新闻主题| B(LangChain主Agent)
    B --> C{决策路由}
    C -->|需要深度检索| D[LlamaIndex检索引擎]
    C -->|需要总结/邮件| E[Summary Agent]
    D -->|返回相关新闻| F[Analysis Agent]
    F -->|生成报告| G[邮件发送]
    G --> H[用户邮箱]
    A -->|调用API| I[FastAPI网关]
    I --> B
```