# modules/statemachine.py

import time
from modules.controller import click, move_forward, sweep_camera
from modules.utils import log, watchdog_check
from config import *

class StateMachine:
    def __init__(self, detector, capture_fn):
        self.detector = detector
        self.capture_fn = capture_fn
        self.retry_count = 0

    def run(self):
        """Main state machine loop."""
        while True:
            watchdog_check(WATCHDOG_TIMEOUT)
            frame = self.capture_fn()
            detections = self.detector.detect(frame)

            if self._handle_ui_states(detections):
                continue

            self._world_loop(detections)

    def _handle_ui_states(self, detections):
        for d in detections:
            x1, y1, x2, y2 = d["box"]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            if d["class_id"] in [CLASS_CONNECT, CLASS_ENTER_GAME, CLASS_OK]:
                log(f"[UI] Clicking button: {d['class_id']}")
                click(cx, cy)
                time.sleep(jitter(2, SLEEP_JITTER))
                return True
        return False

    def _world_loop(self, detections):
        hammer_found = False

        for d in detections:
            if d["class_id"] == CLASS_HAMMER:
                hammer_found = True
                log("[WORLD] Hammer found → moving forward")
                move_forward(2)
                time.sleep(jitter(0.5, SLEEP_JITTER))
                break

        if not hammer_found:
            log("[WORLD] No hammer found → sweeping camera")
            sweep_camera(SWEEP_STEPS, SWEEP_MOVE, SWEEP_DELAY)
            self.retry_count += 1

            if self.retry_count >= RETRY_MAX:
                log("[ERROR] No hammer detected after multiple attempts. Idling.")
                time.sleep(IDLE_DELAY)
                self.retry_count = 0
