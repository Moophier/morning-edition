@echo off
REM Jarvis 一键执行并发送邮件
REM 用法: run-skill-email.bat <技能名> [邮件主题]
REM 例如: run-skill-email.bat morning-brief

set VAULT_PATH=C:\Users\X\Documents\Obsidian Vault
set SKILL_NAME=%1
set EMAIL_SUBJECT=%2

if "%SKILL_NAME%"=="" (
    echo 用法: run-skill-email.bat ^<技能名^> [邮件主题]
    echo 例如: run-skill-email.bat morning-brief "晨间简报"
    exit /b 1
)

set SKILL_FILE=%VAULT_PATH%\07-SYSTEM\skills\%SKILL_NAME%.md
set OUTPUT_DIR=%VAULT_PATH%\04-JARVIS-OUTPUTS\%SKILL_NAME%s

if not exist "%SKILL_FILE%" (
    echo 技能文件不存在: %SKILL_FILE%
    exit /b 1
)

REM 创建输出目录
if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

REM 生成日期字符串
for /f "tokens=1-3 delims=/ " %%a in ('date /t') do (
    set DATE_STR=%%a-%%b-%%c
)

REM 设置默认邮件主题
if "%EMAIL_SUBJECT%"=="" (
    set EMAIL_SUBJECT=%SKILL_NAME% %DATE_STR%
)

echo [%date% %time%] 执行技能: %SKILL_NAME%
echo 邮件主题: %EMAIL_SUBJECT%

REM 执行 opencode（通过 run-skill.bat）
call "%VAULT_PATH%\07-SYSTEM\scripts\run-skill.bat" %SKILL_NAME% "GENERATE_OUTPUT"

REM 查找最新生成的文件
for /f "tokens=*" %%f in ('dir /b /o-d "%OUTPUT_DIR%\*.md" 2^>nul') do (
    set LATEST_FILE=%OUTPUT_DIR%\%%f
    goto :found
)

:found
if defined LATEST_FILE (
    echo 发送邮件: %LATEST_FILE%
    python "%VAULT_PATH%\07-SYSTEM\scripts\send_email.py" "%LATEST_FILE%" "%EMAIL_SUBJECT%"
    echo 完成!
) else (
    echo 没有找到生成的文件，跳过邮件发送
)

REM 清理变量
set LATEST_FILE=
set DATE_STR=