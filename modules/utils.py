# modules/utils.py

import time, random, logging, os, sys

LOG_PATH = "logs/run.log"
logging.basicConfig(filename=LOG_PATH, level=logging.INFO, format="%(asctime)s - %(message)s")

last_action_time = time.time()

def log(msg):
    print(msg)
    logging.info(msg)

def jitter(value, factor=0.2):
    """Return value ± factor random offset."""
    return value + random.uniform(-factor, factor)

def jitter_point(x, y, jitter_px=5):
    """Randomize click position ± jitter_px."""
    return x + random.randint(-jitter_px, jitter_px), y + random.randint(-jitter_px, jitter_px)

def update_watchdog():
    global last_action_time
    last_action_time = time.time()

def watchdog_check(timeout):
    """Restart if bot inactive too long."""
    if time.time() - last_action_time > timeout:
        log("[WATCHDOG] No actions for too long. Restarting bot.")
        os.execv(sys.executable, ['python'] + sys.argv)
