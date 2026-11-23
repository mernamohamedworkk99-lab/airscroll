# AirScroll — Touchless Screen Control

**AirScroll** is a webcam-based Python desktop prototype for hands-free scrolling. It offers two modes: hand pinch and eye blink.

## Features
- Live webcam preview in a desktop GUI
- MediaPipe tracking for up to two hands at the same time
- Thumb-index pinch recognition on either hand
- If both hands pinch, their vertical positions are combined into one scroll signal
- Vertical hand movement mapped to scrolling
- MediaPipe Face Mesh eye landmark tracking
- Single blink (scroll down) and quick double blink (scroll up)
- Exponential smoothing for hand movement
- Start/stop camera and switch interaction mode
- Centralized sensitivity settings in `config.py`

## Tech stack
Python 3.12 · OpenCV · MediaPipe · PyAutoGUI · NumPy · CustomTkinter · Pillow

## Requirements
- Windows 10 or 11
- Python 3.12 (64-bit recommended)
- Laptop/USB webcam
- Camera permission enabled in Windows

## Quick start (Windows)
1. Extract the ZIP file.
2. Install Python 3.12 from [python.org](https://www.python.org/downloads/). During installation, enable the Python Launcher option.
3. Double-click `setup_windows.bat` and wait for package installation.
4. Double-click `run_airscroll.bat`.

Or run manually in PowerShell from the project directory:

```powershell
py -3.12 -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python test_setup.py
python main.py
```

## Using AirScroll
1. Click **START CAMERA**.
2. Choose **Hand Pinch** or **Blink**.
3. Hand Pinch: pinch thumb and index on either hand; keep the pinch and move vertically. You can also pinch with both hands and move them together.
4. Blink: look toward the camera. A single deliberate blink scrolls down after a short wait; two quick blinks scroll up.
5. Click **STOP CAMERA** to stop.

## Tuning
Edit `config.py`:
- `PINCH_THRESHOLD`: increase to make pinching easier to trigger; decrease to require a tighter pinch.
- `HAND_SCROLL_GAIN`: increase for faster hand scrolling.
- `HAND_DEADZONE`: increase to ignore more small movements.
- `BLINK_EAR_THRESHOLD`: adjust if blinks are not detected reliably. Lower values require more eye closure; higher values are more sensitive.
- `DOUBLE_BLINK_WINDOW`: time allowed between two blinks.

Tune one setting at a time and test under the lighting conditions where the application will be used.

## Troubleshooting
**Camera does not open**
- Close Zoom, Teams, browser camera tabs, and other apps using the webcam.
- Check Windows Settings → Privacy & security → Camera.
- If you have multiple cameras, change `CAMERA_INDEX` in `config.py` (try 1).

**MediaPipe or package installation fails**
- Confirm Python is 3.12: `python --version`.
- Recreate the virtual environment if it was created with another Python version.
- Install dependencies using `pip install -r requirements.txt`.

**Gestures trigger too easily or not at all**
- Improve lighting and keep your face/hand visible.
- Adjust the thresholds in `config.py`.
- Try the hand mode first; blink detection is more sensitive to camera angle and individual eye shape.

**Scroll direction feels reversed**
- Adjust the sign of the scroll amount in `modules/vision_controller.py` for your preferred behavior.

## Project structure

```text
AirScroll/
├── main.py
├── config.py
├── requirements.txt
├── setup_windows.bat
├── run_airscroll.bat
├── run_diagnostics.bat
├── test_setup.py
├── modules/
│   ├── vision_controller.py
│   └── scroll_controller.py
├── utils/
│   └── smoothing.py
├── tests/
│   └── test_smoothing.py
└── docs/
    ├── PROJECT_OVERVIEW.md
    └── LINKEDIN_POST.md
```

## Tests
After installing dependencies:

```powershell
python -m unittest discover -s tests -v
```

The unit tests cover the smoothing helper. `test_setup.py` checks that required packages can be imported. Hardware testing still requires a webcam and a real desktop session.

## Limitations
- This is an educational prototype and has not been validated across all devices.
- Blink recognition may need calibration for different users and lighting.
- The app sends scroll events to the currently focused window.
- Do not rely on this prototype for safety-critical or sensitive workflows.

## License
MIT — see `LICENSE`.
