@echo off
REM Jarvis Skill Runner - 技能执行器
REM 用法: run-skill.bat ^<技能名^>
REM 例如: run-skill.bat morning-brief

set VAULT_PATH=C:\Users\X\Documents\Obsidian Vault
set SKILL_NAME=%1

if "%SKILL_NAME%"=="" (
    echo 用法: run-skill.bat ^<技能名^>
    echo 例如: run-skill.bat morning-brief
    exit /b 1
)

set SKILL_FILE=%VAULT_PATH%\07-SYSTEM\skills\%SKILL_NAME%.md

if not exist "%SKILL_FILE%" (
    echo 技能文件不存在: %SKILL_FILE%
    exit /b 1
)

REM 创建日志目录
if not exist "%VAULT_PATH%\07-SYSTEM\logs" mkdir "%VAULT_PATH%\07-SYSTEM\logs"

REM 记录执行开始
echo [%date% %time%] 开始执行技能: %SKILL_NAME% >> "%VAULT_PATH%\07-SYSTEM\logs\skill-execution.log"

REM 执行技能
opencode run "请执行技能文件 %SKILL_FILE% 中的所有指令。完成后报告执行结果。"

REM 记录执行结束
echo [%date% %time%] 技能执行完成: %SKILL_NAME% >> "%VAULT_PATH%\07-SYSTEM\logs\skill-execution.log"