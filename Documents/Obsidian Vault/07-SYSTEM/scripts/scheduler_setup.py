"""
Jarvis 调度器 - Windows 任务计划程序配置
自动在 Windows 中创建所有 7 个技能的调度任务
"""

# -*- coding: utf-8 -*-
import os
import subprocess
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

VAULT_PATH = r"C:\Users\X\Documents\Obsidian Vault"
SCRIPTS_PATH = os.path.join(VAULT_PATH, "07-SYSTEM", "scripts")
SKILL_RUNNER = os.path.join(SCRIPTS_PATH, "run-skill.bat")

SCHEDULES = [
    ("morning-brief", "6", "0", "D", "晨间简报 - 每天早上6点"),
    ("capture-processor", "20", "0", "D", "捕获处理器 - 每天晚上8点"),
    ("connection-finder", "23", "0", "D", "连接查找器 - 每天晚上11点"),
    ("weekly-synthesis", "19", "0", "0", "每周综合 - 每周日晚上7点"),
    ("belief-tracker", "8", "0", "1", "信念追踪器 - 每周一早上8点"),
    ("decision-intelligence", "9", "0", "1", "决策智能 - 每周一早上9点"),
    ("pattern-detector", "8", "1", "M", "模式检测器 - 每月1号早上8点"),
]


def create_task(
    task_name, hour, minute, day_of_week=None, day_of_month=None, description=""
):
    """创建 Windows 计划任务"""

    hour_str = hour.zfill(2)
    minute_str = minute.zfill(2)

    if day_of_month:
        trigger_type = "MONTHLY"
        trigger_args = f"/SC MONTHLY /D 1 /ST {hour_str}:{minute_str}"
    elif day_of_week:
        days = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
        trigger_type = "WEEKLY"
        trigger_args = (
            f"/SC WEEKLY /D {days[int(day_of_week)]} /ST {hour_str}:{minute_str}"
        )
    else:
        trigger_type = "DAILY"
        trigger_args = f"/SC DAILY /ST {hour_str}:{minute_str}"

    task_full_name = f"Jarvis-{task_name}"

    delete_cmd = f'schtasks /Delete /TN "{task_full_name}" /F 2>nul'
    subprocess.run(delete_cmd, shell=True, capture_output=True)

    create_cmd = f'schtasks /Create /TN "{task_full_name}" {trigger_args} /TR "\\"{SKILL_RUNNER}\\" {task_name}" /F'

    print(f"创建任务: {task_full_name}")
    print(f"  命令: {create_cmd}")

    result = subprocess.run(create_cmd, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"  [OK] Success")
        return True
    else:
        print(f"  [FAIL] {result.stderr}")
        return False


def main():
    print("=" * 50)
    print("Jarvis 调度器 - Windows 任务计划程序配置")
    print("=" * 50)
    print()

    print(f"Vault 路径: {VAULT_PATH}")
    print(f"技能运行器: {SKILL_RUNNER}")
    print()

    print("将创建以下调度任务:\n")
    for skill, hour, minute, day_type, desc in SCHEDULES:
        print(f"  {desc}")
    print()

    confirm = input("继续创建这些任务? (y/n): ")
    if confirm.lower() != "y":
        print("已取消")
        return

    print()

    success_count = 0
    for skill, hour, minute, day_type, desc in SCHEDULES:
        day_of_week = day_type if day_type in ["0", "1"] else None
        day_of_month = "1" if day_type == "M" else None

        if create_task(skill, hour, minute, day_of_week, day_of_month, desc):
            success_count += 1
        print()

    print("=" * 50)
    print(f"完成! 成功创建 {success_count}/{len(SCHEDULES)} 个任务")
    print("=" * 50)


if __name__ == "__main__":
    main()
