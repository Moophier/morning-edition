@echo off
schtasks /query /fo csv /v | findstr /i "jarvis"
pause