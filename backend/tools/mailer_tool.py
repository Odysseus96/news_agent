from langchain.tools import tool
from config import EMAIL_RECEIVER, EMAIL_FROM, EMAIL_PASSWORD
import smtplib
from email.mime.text import MIMEText

def GmailSendMessage(input: dict) -> str:
    """ 发送新闻分析邮件 """
    # 检查必需的配置
    if not EMAIL_PASSWORD:
        return "错误：EMAIL_PASSWORD 未配置"
    if not EMAIL_RECEIVER:
        return "错误：EMAIL_RECEIVER 未配置"
    if not EMAIL_FROM:
        return "错误：EMAIL_FROM 未配置"
    
    try:
        msg = MIMEText(input["body"], "plain", "utf-8")
        msg["Subject"] = input.get("subject", "科技新闻报告")
        msg["From"] = EMAIL_FROM
        msg["To"] = input.get("to", EMAIL_RECEIVER)

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(EMAIL_FROM, EMAIL_PASSWORD)  # 现在 EMAIL_PASSWORD 确保不是 None
        server.sendmail(EMAIL_FROM, [EMAIL_RECEIVER], msg.as_string())
        server.quit()
        return "邮件发送成功"
    except Exception as e:
        return f"邮件发送失败：{str(e)}"
