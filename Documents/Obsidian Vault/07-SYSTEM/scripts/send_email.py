"""
Jarvis 邮件发送模块
用于发送晨间简报等报告到邮箱
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pathlib import Path


def load_email_config():
    """从 .env 加载邮件配置"""
    env_path = Path.home() / ".env"
    config = {}

    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and "=" in line:
                    key, value = line.split("=", 1)
                    config[key.strip()] = value.strip()

    return config


def send_brief_via_email(content: str, subject: str = None) -> bool:
    """发送简报到邮箱"""
    config = load_email_config()

    email_user = config.get("EMAIL_USER")
    email_pass = config.get("EMAIL_PASS")
    email_to = config.get("EMAIL_TO", email_user)

    if not email_user or not email_pass:
        print("[ERROR] Email config not found in .env")
        return False

    if subject is None:
        today = datetime.now().strftime("%Y-%m-%d")
        subject = f"晨间简报 {today}"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = email_user
    msg["To"] = email_to

    # 纯文本版本
    text_content = f"""【Jarvis 晨间简报】
{datetime.now().strftime("%Y-%m-%d %H:%M")}

{content}
"""

    # HTML版本
    html_content = f"""
<html>
<head>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; padding: 20px; }}
h1 {{ color: #1a1a2e; border-bottom: 2px solid #16213e; padding-bottom: 10px; }}
h2 {{ color: #0f3460; margin-top: 20px; }}
.highlight {{ background: #f0f4ff; padding: 15px; border-radius: 8px; margin: 10px 0; }}
.action {{ color: #e94560; font-weight: bold; }}
table {{ border-collapse: collapse; width: 100%; margin: 10px 0; }}
td, th {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
th {{ background: #f5f5f5; }}
</style>
</head>
<body>
{content}
<hr>
<small>由 Jarvis 自动生成 | {datetime.now().strftime("%Y-%m-%d %H:%M")}</small>
</body>
</html>
"""

    msg.attach(MIMEText(text_content, "plain", "utf-8"))
    msg.attach(MIMEText(html_content, "html", "utf-8"))

    try:
        # QQ邮箱使用SSL
        with smtplib.SMTP_SSL("smtp.qq.com", 465) as server:
            server.login(email_user, email_pass)
            server.sendmail(email_user, email_to, msg.as_string())

        print(f"[OK] Email sent to {email_to}")
        return True

    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")
        return False


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python send_email.py <content_file> [subject]")
        sys.exit(1)

    content_file = sys.argv[1]
    subject = sys.argv[2] if len(sys.argv) > 2 else None

    with open(content_file, "r", encoding="utf-8") as f:
        content = f.read()

    success = send_brief_via_email(content, subject)
    sys.exit(0 if success else 1)
