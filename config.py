# config.py

# YOLOv8 Class IDs (must match your training)
CLASS_HAMMER = 0
CLASS_OK = 1
CLASS_CONNECT = 2
CLASS_ENTER_GAME = 3

# Sweep configuration
SWEEP_STEPS = 20
SWEEP_MOVE = 50
SWEEP_DELAY = 0.1

# Idle and retry timings
IDLE_DELAY = 60
RETRY_MAX = 3

# Randomization factors
CLICK_JITTER = 5         # px jitter around click point
SLEEP_JITTER = 0.2       # random ± seconds added to sleeps

# Watchdog config
WATCHDOG_TIMEOUT = 300   # seconds: restart if no actions
