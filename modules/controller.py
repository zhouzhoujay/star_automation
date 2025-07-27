# modules/controller.py

import time
import pydirectinput
from modules.utils import jitter, jitter_point, update_watchdog
from config import CLICK_JITTER, SLEEP_JITTER

def click(x, y):
    xj, yj = jitter_point(x, y, CLICK_JITTER)
    pydirectinput.moveTo(xj, yj)
    time.sleep(jitter(0.05, SLEEP_JITTER))
    pydirectinput.click()
    update_watchdog()

def press_key(key, duration=0.1):
    pydirectinput.keyDown(key)
    time.sleep(jitter(duration, SLEEP_JITTER))
    pydirectinput.keyUp(key)
    update_watchdog()

def move_forward(duration=1.5):
    press_key('w', duration)

def sweep_camera(steps, move_px, delay):
    """Rotate camera 360° by sweeping mouse horizontally."""
    for _ in range(steps):
        pydirectinput.moveRel(move_px, 0)
        time.sleep(jitter(delay, SLEEP_JITTER))
    update_watchdog()
