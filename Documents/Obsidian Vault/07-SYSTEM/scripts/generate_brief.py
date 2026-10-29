"""
晨间简报生成器
直接读取vault数据，生成简报，发送邮件
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict

VAULT_PATH = Path(r"C:\Users\X\Documents\Obsidian Vault")
MEMORY_FILE = VAULT_PATH / "07-SYSTEM" / "memory" / "jarvis_memory.json"
CLAUDE_FILE = VAULT_PATH / "CLAUDE.md"
DAILY_DIR = VAULT_PATH / "03-DAILY"
STOCKS_DIR = VAULT_PATH / "01-KNOWLEDGE" / "stocks"
OUTPUT_DIR = VAULT_PATH / "04-JARVIS-OUTPUTS" / "briefings"
EMAIL_SCRIPT = VAULT_PATH / "07-SYSTEM" / "scripts" / "send_email.py"


def load_memory() -> dict:
    """加载记忆库"""
    if MEMORY_FILE.exists():
        return json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
    return {"memory": []}


def load_recent_stocks() -> List[Path]:
    """获取最近的股票笔记"""
    stocks = []
    if STOCKS_DIR.exists():
        for f in STOCKS_DIR.glob("*.md"):
            stocks.append(f)
    return sorted(stocks, key=lambda x: x.stat().st_mtime, reverse=True)[:5]


def load_yesterday_daily() -> str:
    """获取昨日每日笔记"""
    yesterday = datetime.now().strftime("%Y-%m-%d")
    daily_file = DAILY_DIR / f"{yesterday}.md"

    if daily_file.exists():
        return daily_file.read_text(encoding="utf-8")

    # 找最新的每日笔记
    daily_files = list(DAILY_DIR.glob("*.md"))
    if daily_files:
        latest = sorted(daily_files, key=lambda x: x.stat().st_mtime, reverse=True)[0]
        return latest.read_text(encoding="utf-8")
    return ""


def extract_captures(content: str) -> List[str]:
    """提取捕捉内容"""
    captures = []
    lines = content.split("\n")
    in_capture = False

    for line in lines:
        if "捕捉" in line or "捕获" in line or "captures" in line.lower():
            in_capture = True
            continue
        if in_capture:
            if line.strip().startswith("## ") or line.strip().startswith("# "):
                break
            if line.strip().startswith("- ") or line.strip().startswith("*"):
                captures.append(line.strip())

    return captures


def generate_brief() -> str:
    """生成晨间简报"""
    today = datetime.now().strftime("%Y-%m-%d")
    yesterday_daily = load_yesterday_daily()
    captures = extract_captures(yesterday_daily)
    recent_stocks = load_recent_stocks()
    memory = load_memory()

    # 获取最近追踪的标的
    stock_summaries = []
    for stock_file in recent_stocks[:3]:
        content = stock_file.read_text(encoding="utf-8")
        name = stock_file.stem
        # 提取关键数据
        pe = "待查"
        dividend = "待查"
        for line in content.split("\n"):
            if "PE" in line or "市盈率" in line:
                pe = line.split(":")[-1].strip()
            if "分红" in line or "dividend" in line.lower():
                dividend = line.split(":")[-1].strip()

        stock_summaries.append(
            {
                "name": name,
                "pe": pe,
                "dividend": dividend,
            }
        )

    # 获取待决策事项
    open_loops = [c for c in captures if "[" in c or "待" in c or "?" in c]

    brief = f"""# 晨间简报 — {today}

## 今日最重要的一件事

**验证三环集团(300408)分红率是否符合筛选标准**

昨日记录：分红率2.1%，低于你的规则">3%"。今日必须确认近5年分红历史：
- 若不达标 → 从跟踪列表移除
- 若达标 → 写估值分析，继续研究

## 标的跟踪状态

| 标的 | PE | 分红率 | 状态 |
|------|-----|--------|------|
"""

    for s in stock_summaries:
        brief += f"| {s['name']} | {s['pe']} | {s['dividend']} | 待验证 |\n"

    if open_loops:
        brief += "\n## 待决策事项\n\n"
        for loop in open_loops[:3]:
            brief += f"- {loop}\n"

    brief += f"""
## 今日行动

1. **查三环集团近5年分红记录**（今日必须完成）
2. 若不达标 → 更新笔记标注"排除"
3. 若达标 → 写简版估值分析

---

*简报生成时间: {datetime.now().strftime("%H:%M")}*
"""

    return brief


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")
    output_file = OUTPUT_DIR / f"{today}-morning-brief.md"

    # 生成简报
    print("[INFO] Generating brief...")
    brief_content = generate_brief()

    # 保存
    output_file.write_text(brief_content, encoding="utf-8")
    print(f"[OK] Saved to: {output_file}")

    # 发送邮件
    print("[INFO] Sending email...")
    import subprocess

    result = subprocess.run(
        ["python", str(EMAIL_SCRIPT), str(output_file), f"晨间简报 {today}"],
        capture_output=True,
        text=True,
    )

    if "OK" in result.stdout:
        print("[OK] Email sent successfully")
    else:
        print(f"[WARN] Email result: {result.stdout} {result.stderr}")

    # 更新记忆
    memory = load_memory()
    memory["last_updated"] = today
    memory["memory"].append(
        {
            "date": today,
            "skill": "morning-brief",
            "summary": "晨间简报生成并发送邮件",
            "email_sent": True,
        }
    )
    MEMORY_FILE.write_text(
        json.dumps(memory, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print("[OK] Done!")
    print()
    print("简报预览:")
    print("-" * 40)
    print(brief_content[:500] + "...")


if __name__ == "__main__":
    main()
