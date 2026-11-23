@echo off
setlocal
if not exist venv\Scripts\python.exe (
  echo Virtual environment not found. Run setup_windows.bat first.
  pause
  exit /b 1
)
venv\Scripts\python.exe main.py
if errorlevel 1 (
  echo AirScroll exited with an error. Read the terminal message above.
  pause
)
