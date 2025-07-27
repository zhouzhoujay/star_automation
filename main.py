# main.py

from modules.capture import capture_screen
from modules.detector import Detector
from modules.statemachine import StateMachine
from modules.utils import log

MODEL_PATH = "models/model.pt"

if __name__ == "__main__":
    log("[START] Bot initialized.")
    detector = Detector(MODEL_PATH)
    sm = StateMachine(detector, capture_screen)
    sm.run()
