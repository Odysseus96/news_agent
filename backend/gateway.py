# gateway.py
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from apscheduler.schedulers.background import BackgroundScheduler
from main import run_analysis

app = FastAPI()

# === ⏰ 定时任务调度部分 ===
scheduler = BackgroundScheduler()

def scheduled_job():
    print("📅 正在自动分析新闻并生成邮件报告")
    result = run_analysis("请分析今天的科技新闻")
    print("✅ 自动报告生成完成：", result["report"][:100], "...")

# 每天早上 9 点执行一次任务
scheduler.add_job(scheduled_job, trigger="cron", hour=9, minute=0)
scheduler.start()

# === 📡 接口供 Dify 调用 ===
class DifyRequest(BaseModel):
    inputs: dict
    query: str

@app.post("/chat")
async def chat_endpoint(request: DifyRequest):
    query = request.query
    try:
        final_state = run_analysis(query)
        return JSONResponse({
            "reply": final_state["report"]
        })
    except Exception as e:
        return JSONResponse({
            "reply": f"❌ 出错了：{str(e)}"
        })

# 用于测试手动运行
@app.get("/run-news-agent")
async def manual_run():
    result = run_analysis("请分析今天的科技新闻")
    return {"message": "✅ 手动运行完成", "report": result["report"]}
