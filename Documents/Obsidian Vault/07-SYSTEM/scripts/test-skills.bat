@echo off
REM Jarvis 快速测试脚本
REM 用于手动测试各个技能

set VAULT_PATH=C:\Users\X\Documents\Obsidian Vault

echo ========================================
echo Jarvis 技能测试
echo ========================================
echo.
echo 可用技能:
echo   1. morning-brief      - 晨间简报
echo   2. capture-processor  - 捕获处理器
echo   3. connection-finder  - 连接查找器
echo   4. weekly-synthesis   - 每周综合
echo   5. belief-tracker     - 信念追踪器
echo   6. decision-intelligence - 决策智能
echo   7. pattern-detector   - 模式检测器
echo   8. 全部运行
echo   0. 退出
echo.

set /p choice=选择要测试的技能 (0-8): 

if "%choice%"=="1" goto morning-brief
if "%choice%"=="2" goto capture-processor
if "%choice%"=="3" goto connection-finder
if "%choice%"=="4" goto weekly-synthesis
if "%choice%"=="5" goto belief-tracker
if "%choice%"=="6" goto decision-intelligence
if "%choice%"=="7" goto pattern-detector
if "%choice%"=="8" goto all
if "%choice%"=="0" goto end

:morning-brief
call "%VAULT_PATH%\07-SYSTEM\scripts\run-skill.bat" morning-brief
goto end

:capture-processor
call "%VAULT_PATH%\07-SYSTEM\scripts\run-skill.bat" capture-processor
goto end

:connection-finder
call "%VAULT_PATH%\07-SYSTEM\scripts\run-skill.bat" connection-finder
goto end

:weekly-synthesis
call "%VAULT_PATH%\07-SYSTEM\scripts\run-skill.bat" weekly-synthesis
goto end

:belief-tracker
call "%VAULT_PATH%\07-SYSTEM\scripts\run-skill.bat" belief-tracker
goto end

:decision-intelligence
call "%VAULT_PATH%\07-SYSTEM\scripts\run-skill.bat" decision-intelligence
goto end

:pattern-detector
call "%VAULT_PATH%\07-SYSTEM\scripts\run-skill.bat" pattern-detector
goto end

:all
echo 即将运行全部技能...
call "%VAULT_PATH%\07-SYSTEM\scripts\run-skill.bat" morning-brief
call "%VAULT_PATH%\07-SYSTEM\scripts\run-skill.bat" capture-processor
call "%VAULT_PATH%\07-SYSTEM\scripts\run-skill.bat" connection-finder
call "%VAULT_PATH%\07-SYSTEM\scripts\run-skill.bat" weekly-synthesis
call "%VAULT_PATH%\07-SYSTEM\scripts\run-skill.bat" belief-tracker
call "%VAULT_PATH%\07-SYSTEM\scripts\run-skill.bat" decision-intelligence
call "%VAULT_PATH%\07-SYSTEM\scripts\run-skill.bat" pattern-detector
echo 全部技能执行完成!
goto end

:end
pause