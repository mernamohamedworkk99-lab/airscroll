@echo off
setlocal
echo ========================================
echo AirScroll - Windows setup
echo ========================================
where py >nul 2>nul
if errorlevel 1 (
  echo Python Launcher not found. Install Python 3.12 from python.org first.
  pause
  exit /b 1
)
py -3.12 --version
if errorlevel 1 (
  echo Python 3.12 was not found. Install Python 3.12 (64-bit), then retry.
  pause
  exit /b 1
)
if not exist venv (
  py -3.12 -m venv venv
)
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
  echo.
  echo Installation failed. Check the error above and the README troubleshooting section.
  pause
  exit /b 1
)
echo.
echo Setup complete. Run run_airscroll.bat to launch AirScroll.
pause
