"""Central configuration for AirScroll."""
CAMERA_INDEX = 0
CAMERA_WIDTH = 960
CAMERA_HEIGHT = 540
CAMERA_FPS = 30

# Hand pinch tuning (supports one or two detected hands)
PINCH_THRESHOLD = 0.045       # Normalized thumb-index distance
HAND_DEADZONE = 0.010         # Ignore tiny vertical movements
HAND_SCROLL_GAIN = 260        # Larger = faster scrolling
MAX_SCROLL_STEP = 5

# Blink tuning (Face Mesh eye-aspect ratio)
BLINK_EAR_THRESHOLD = 0.19
MIN_BLINK_SECONDS = 0.055
MAX_BLINK_SECONDS = 0.60
DOUBLE_BLINK_WINDOW = 0.55
BLINK_SCROLL_AMOUNT = 4

# UI / processing
FRAME_QUEUE_SIZE = 2
STATUS_UPDATE_INTERVAL_MS = 80
