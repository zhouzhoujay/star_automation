# modules/capture.py

import mss
import cv2
import numpy as np

def capture_screen():
    """Capture full screen and return as BGR numpy array."""
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        img = np.array(sct.grab(monitor))
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
