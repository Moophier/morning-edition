@echo off
REM Jarvis 一键执行技能
REM 用法: run.bat <技能名>
REM 例如: run.bat morning-brief

set VAULT_PATH=C:\Users\X\Documents\Obsidian Vault
set SKILL_NAME=%1

if "%SKILL_NAME%"=="" (
    echo 用法: run.bat ^<技能名^>
    echo 例如: run.bat morning-brief
    echo.
    echo 可用技能:
    echo   morning-brief      - 晨间简报
    echo   generate-brief     - 生成并发送晨间简报(推荐)
    exit /b 1
)

cd /d "%VAULT_PATH%"

if "%SKILL_NAME%"=="morning-brief" (
    echo 执行晨间简报...
    python "07-SYSTEM\scripts\generate_brief.py"
) else (
    echo 未知技能: %SKILL_NAME%
    echo 可用: morning-brief, generate-brief
    exit /b 1
)

pause