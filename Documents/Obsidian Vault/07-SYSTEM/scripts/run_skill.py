"""
Jarvis 一键执行技能并发送邮件
Usage: python run_skill.py <skill_name>
Example: python run_skill.py morning-brief
"""

import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path

VAULT_PATH = Path(r"C:\Users\X\Documents\Obsidian Vault")
SKILLS_PATH = VAULT_PATH / "07-SYSTEM" / "skills"
SCRIPTS_PATH = VAULT_PATH / "07-SYSTEM" / "scripts"
EMAIL_SCRIPT = SCRIPTS_PATH / "send_email.py"

SKILL_CONFIG = {
    "morning-brief": {
        "output_dir": "04-JARVIS-OUTPUTS/briefings",
        "date_prefix": True,
        "email_subject": "晨间简报",
    },
    "capture-processor": {
        "output_dir": "04-JARVIS-OUTPUTS",
        "date_prefix": True,
        "email_subject": "捕获处理报告",
    },
    "connection-finder": {
        "output_dir": "04-JARVIS-OUTPUTS/connections",
        "date_prefix": True,
        "email_subject": "连接发现报告",
    },
    "weekly-synthesis": {
        "output_dir": "04-JARVIS-OUTPUTS/syntheses",
        "date_prefix": True,
        "email_subject": "每周综合",
    },
    "belief-tracker": {
        "output_dir": "04-JARVIS-OUTPUTS",
        "date_prefix": True,
        "email_subject": "信念追踪报告",
    },
    "decision-intelligence": {
        "output_dir": "04-JARVIS-OUTPUTS/reviews",
        "date_prefix": True,
        "email_subject": "决策回顾",
    },
    "pattern-detector": {
        "output_dir": "04-JARVIS-OUTPUTS/patterns",
        "date_prefix": True,
        "email_subject": "模式检测报告",
    },
}


def get_output_filename(skill_name: str) -> Path:
    """获取技能输出文件名"""
    config = SKILL_CONFIG.get(skill_name, {})
    output_dir = VAULT_PATH / config.get("output_dir", "04-JARVIS-OUTPUTS")

    os.makedirs(output_dir, exist_ok=True)

    today = datetime.now()

    if config.get("date_prefix"):
        date_str = today.strftime("%Y-%m-%d")
        filename = f"{date_str}-{skill_name}.md"
    else:
        filename = f"{skill_name}.md"

    return output_dir / filename


def generate_content(skill_name: str, output_file: Path):
    """使用 opencode 生成技能内容"""
    skill_file = SKILLS_PATH / f"{skill_name}.md"

    if not skill_file.exists():
        print(f"[ERROR] Skill file not found: {skill_file}")
        return False

    config = SKILL_CONFIG.get(skill_name, {})
    email_subject = config.get("email_subject", skill_name)
    if config.get("date_prefix"):
        email_subject = f"{email_subject} {datetime.now().strftime('%Y-%m-%d')}"

    prompt = f"""请执行技能文件: {skill_file.as_posix()}

根据技能文件中的指令，生成内容并保存到: {output_file.as_posix()}

完成后：
1. 确认文件已保存
2. 发送邮件到配置的邮箱，邮件主题: {email_subject}
"""

    print(f"[INFO] Generating content for skill: {skill_name}")

    try:
        result = subprocess.run(
            ["opencode", "run", prompt],
            cwd=VAULT_PATH,
            capture_output=True,
            text=True,
            timeout=180,
        )

        print(f"[DEBUG] stdout: {result.stdout[:500] if result.stdout else 'None'}")
        if result.stderr:
            print(f"[DEBUG] stderr: {result.stderr[:500]}")

        return result.returncode == 0 or output_file.exists()

    except subprocess.TimeoutExpired:
        print("[ERROR] Command timed out")
        return False
    except Exception as e:
        print(f"[ERROR] {e}")
        return False


def send_email(output_file: Path):
    """发送邮件"""
    config = SKILL_CONFIG.get(skill_name, {})
    email_subject = config.get("email_subject", skill_name)
    if config.get("date_prefix"):
        email_subject = f"{email_subject} {datetime.now().strftime('%Y-%m-%d')}"

    print(f"[INFO] Sending email with subject: {email_subject}")

    try:
        result = subprocess.run(
            ["python", str(EMAIL_SCRIPT), str(output_file), email_subject],
            capture_output=True,
            text=True,
            timeout=30,
        )

        if "OK" in result.stdout:
            print("[OK] Email sent successfully")
            return True
        else:
            print(f"[ERROR] Email failed: {result.stdout} {result.stderr}")
            return False

    except Exception as e:
        print(f"[ERROR] {e}")
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python run_skill.py <skill_name>")
        print("Available skills:")
        for name in SKILL_CONFIG.keys():
            print(f"  - {name}")
        sys.exit(1)

    skill_name = sys.argv[1]

    if skill_name not in SKILL_CONFIG:
        print(f"[ERROR] Unknown skill: {skill_name}")
        print(f"Available: {', '.join(SKILL_CONFIG.keys())}")
        sys.exit(1)

    print("=" * 50)
    print(f"Jarvis Skill Runner: {skill_name}")
    print("=" * 50)

    # 获取输出文件路径
    output_file = get_output_filename(skill_name)
    print(f"[INFO] Output file: {output_file}")

    # 生成内容
    success = generate_content(skill_name, output_file)

    if not success:
        print("[WARN] Content generation may have failed, checking output file...")

    # 如果文件不存在但有内容，手动创建
    if not output_file.exists():
        print("[INFO] Creating default content...")
        default_content = f"""# {SKILL_CONFIG[skill_name]["email_subject"]} — {datetime.now().strftime("%Y-%m-%d")}

*由 Jarvis 自动生成*

---
技能: {skill_name}
时间: {datetime.now().strftime("%Y-%m-%d %H:%M")}
"""
        output_file.write_text(default_content, encoding="utf-8")

    # 发送邮件
    send_email(output_file)

    print("=" * 50)
    print("Done!")


if __name__ == "__main__":
    skill_name = sys.argv[1] if len(sys.argv) > 1 else "morning-brief"
    main()
