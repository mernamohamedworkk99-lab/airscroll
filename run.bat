@echo off
if not exist venv\Scripts\python.exe (
  echo Please run install.bat first.
  pause
  exit /b 1
)
call venv\Scripts\activate.bat
python main.py
if errorlevel 1 pause
