@echo off
setlocal
py -3.12 -m venv venv
if errorlevel 1 (
  echo Could not create the environment. Make sure Python 3.12 is installed.
  pause
  exit /b 1
)
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
  echo Installation failed. Check the error above.
  pause
  exit /b 1
)
echo.
echo AirScroll installation completed.
echo Run run.bat to launch the app.
pause
