"""Run this file to verify that AirScroll dependencies are installed."""
import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import customtkinter
from PIL import Image

print("OpenCV:", cv2.__version__)
print("MediaPipe:", mp.__version__)
print("NumPy:", np.__version__)
print("PyAutoGUI: imported")
print("CustomTkinter: imported")
print("Pillow: imported")
print("\nAirScroll setup check passed.")
