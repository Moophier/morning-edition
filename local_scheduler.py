"""
本地定时任务调度器
Local Task Scheduler for Windows
自动运行 Autoresearch + Morning Brief
"""

import schedule
import time
import subprocess
import sys
from datetime import datetime
import os


def run_autoresearch():
    """运行策略优化"""
    print(f"\n{'='*60}")
    print(f"[{datetime.now()}] Running Autoresearch...")
    print('='*60)
    try:
        subprocess.run([sys.executable, 'autoresearch_stock.py', '60'], 
                     cwd=os.path.dirname(os.path.abspath(__file__)))
        print(f"Autoresearch completed at {datetime.now()}")
    except Exception as e:
        print(f"Autoresearch error: {e}")


def run_morning_brief():
    """运行晨间报告"""
    print(f"\n{'='*60}")
    print(f"[{datetime.now()}] Running Morning Brief...")
    print('='*60)
    try:
        subprocess.run([sys.executable, 'morning_brief.py'],
                     cwd=os.path.dirname(os.path.abspath(__file__)))
        print(f"Morning Brief completed at {datetime.now()}")
    except Exception as e:
        print(f"Morning Brief error: {e}")


def run_morning_edition():
    """生成 Morning Edition Hacker News 杂志"""
    print(f"\n{'='*60}")
    print(f"[{datetime.now()}] Generating Morning Edition Magazine...")
    print('='*60)
    try:
        subprocess.run([sys.executable, 'morning_edition.py'],
                     cwd=os.path.dirname(os.path.abspath(__file__)))
        print(f"Morning Edition completed at {datetime.now()}")
    except Exception as e:
        print(f"Morning Edition error: {e}")


def run_full_daily():
    """运行完整流程: Autoresearch + Morning Brief"""
    print(f"\n{'='*60}")
    print(f"[{datetime.now()}] Running Full Daily Automation...")
    print('='*60)
    try:
        # Step 1: Autoresearch
        print("\n[Step 1/2] Running Autoresearch...")
        subprocess.run([sys.executable, 'autoresearch_stock.py', '30'],
                     cwd=os.path.dirname(os.path.abspath(__file__)))
        
        # Step 2: Morning Brief
        print("\n[Step 2/2] Running Morning Brief...")
        subprocess.run([sys.executable, 'morning_brief.py'],
                     cwd=os.path.dirname(os.path.abspath(__file__)))
        
        print(f"\nFull daily automation completed at {datetime.now()}")
    except Exception as e:
        print(f"Error: {e}")


def main():
    print("""
========================================
  Local Task Scheduler
  本地定时任务调度器
========================================
  
   选项:
   1. 每天凌晨运行 (03:00 Autoresearch + 07:00 Morning Edition + 07:30 Brief)
   2. 每天早上运行 (07:00 Morning Edition only)
   3. 立即运行完整流程 (测试用)
   4. 退出
  
========================================
""")
    
    choice = input("请选择 (1-4): ").strip()
    
    if choice == '1':
        schedule.every().day.at("03:00").do(run_autoresearch)
        schedule.every().day.at("07:00").do(run_morning_edition)
        schedule.every().day.at("07:30").do(run_morning_brief)
        
        print("\n已设置定时任务:")
        print("  - 每天 03:00: 运行 Autoresearch (策略优化)")
        print("  - 每天 07:00: 生成 Morning Edition (Hacker News杂志)")
        print("  - 每天 07:30: 运行 Morning Brief (报告)")
        print("\n按 Ctrl+C 停止调度...")
        
        while True:
            schedule.run_pending()
            time.sleep(60)
    
    elif choice == '2':
        schedule.every().day.at("07:00").do(run_morning_edition)
        
        print("\n已设置定时任务:")
        print("  - 每天 07:00: 生成 Morning Edition (Hacker News杂志)")
        print("\n按 Ctrl+C 停止调度...")
        
        while True:
            schedule.run_pending()
            time.sleep(60)
    
    elif choice == '3':
        # Immediate test
        run_full_daily()
    
    elif choice == '4':
        print("退出")
        return
    
    else:
        print("无效选择")


if __name__ == "__main__":
    main()