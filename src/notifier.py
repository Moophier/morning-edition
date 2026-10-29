import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

load_dotenv()


def send_report(report_content, filename="weekly_github_trending.md"):
    msg = MIMEMultipart()
    msg["From"] = os.getenv("SMTP_USER")
    msg["To"] = os.getenv("RECIPIENT_EMAIL")
    msg["Subject"] = "Weekly GitHub Trending Report"

    body = "本周 GitHub Trending 报告见附件。"
    msg.attach(MIMEText(body, "plain", "utf-8"))

    attachment = MIMEApplication(report_content.encode("utf-8"), Name=filename)
    attachment.add_header("Content-Disposition", "attachment", filename=filename)
    msg.attach(attachment)

    with smtplib.SMTP(
        os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT", "587"))
    ) as server:
        server.starttls()
        server.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASSWORD"))
        server.send_message(msg)
