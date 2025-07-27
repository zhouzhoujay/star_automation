# star_automation
to automate material collection
1. FULL REQUIREMENTS SPECIFICATION
1.1 Functional Requirements
UI State Handling

Detect and click on:

“连接开始” (Connect)

“进入游戏” (Enter Game)

Message box with “确定” (OK)

Handle disconnections by re-logging automatically.

Item Collection Cycle

Continuously detect hammer icons (resource markers).

Navigate character toward detected hammer icon using W/A/S/D.

When collection prompt appears, press F.

After collecting, perform a 360° camera sweep to find new icons.

If none found, idle for 60 seconds, then repeat.

Error Handling

If icons are not detected after multiple sweeps, retry login or idle longer.

Log events for debugging.

1.2 Non-Functional Requirements
Performance:

Image detection must run at least 5–10 FPS for smooth operation.

Reliability:

State transitions must never get stuck.

Modularity:

State machine must be extendable (e.g., adding combat detection).

Safety:

No DLL injection, only screen capture + simulated input to avoid anti-cheat triggers.

1.3 System Architecture
Architecture Layers

Capture Layer

Uses mss to capture game window frames.

Detection Layer

YOLOv8 for:

Hammer icon detection

“确定”, “连接开始”, “进入游戏” button detection

Fallback: Template matching for static buttons.

Control Layer

Uses pydirectinput to send mouse & keyboard inputs.

State Machine Layer

Controls:

Login → Message box → World exploration

Error handling (idle, reconnect)

1.4 Architecture Diagram
pgsql
Copy
Edit
 ┌──────────────┐     ┌───────────────┐
 │  Screen Grab  │───►│  YOLOv8 Model  │───┐
 └──────────────┘     └───────────────┘   │
       ▲                                  ▼
       │                           ┌─────────────┐
       │                           │ State Machine│
       │                           ├─────────────┤
       │                           │ Login        │
       │                           │ MessageBox   │
       │                           │ World Loop   │
       │                           └─────┬───────┘
       │                                 │
       ▼                                 ▼
   ┌──────────────┐               ┌───────────────┐
   │ pydirectinput │◄─────────────│ Input Commands │
   └──────────────┘               └───────────────┘
1.5 State Machine Diagram
rust
Copy
Edit
[LOGIN]
   |  detect "连接开始"/"进入游戏"
   v
[MESSAGEBOX]
   | detect "确定" button
   v
[WORLD LOOP]
   |
   | detect hammer icons?
   |----Yes----> navigate & collect
   |
   |----No----> 360° camera sweep -> idle -> retry
1.6 Modules Breakdown
capture.py – Screen capture via mss

detector.py – YOLOv8 detection

controller.py – Keyboard & mouse control using pydirectinput

statemachine.py – Game state manager

main.py – Orchestrates the loop

2. MINIMAL WORKING PROTOTYPE (YOLOv8)
This is a barebones version:

Detect hammer icon & buttons using YOLOv8

Click buttons / move forward if hammer detected

No full modularity yet (for clarity)

2.1 Installation
Open terminal in VS Code and run:

bash
Copy
Edit
pip install ultralytics mss pydirectinput opencv-python
2.2 YOLOv8 Model Setup
Collect ~100 screenshots of hammer icon, buttons, etc.

Annotate using LabelImg or Roboflow.

Train YOLOv8 model:

bash
Copy
Edit
yolo detect train data=data.yaml model=yolov8n.pt epochs=50 imgsz=640
Place trained model as model.pt in project folder.

2.3 Code (main.py)
python
Copy
Edit
import time
import cv2
import mss
import numpy as np
import pydirectinput
from ultralytics import YOLO

# Load YOLOv8 model
model = YOLO("model.pt")

def capture_screen():
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Primary screen
        img = np.array(sct.grab(monitor))
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

def click(x, y):
    pydirectinput.moveTo(x, y)
    time.sleep(0.05)
    pydirectinput.click()

def move_forward(duration=1.5):
    pydirectinput.keyDown('w')
    time.sleep(duration)
    pydirectinput.keyUp('w')

while True:
    frame = capture_screen()
    results = model(frame, verbose=False)

    if len(results[0].boxes) == 0:
        print("No objects detected. Sweeping...")
        # TODO: Add 360° sweep logic here
        time.sleep(1)
        continue

    for box in results[0].boxes:
        cls_id = int(box.cls[0])
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        # Example: hammer icon is class 0, OK button class 1
        if cls_id == 0:  # hammer icon
            print("Hammer icon found")
            # Move forward (just a placeholder)
            move_forward(2)

        elif cls_id == 1:  # OK button
            click((x1+x2)//2, (y1+y2)//2)

    time.sleep(0.5)
2.4 What This Does
Captures screen

Runs YOLOv8 detection

If hammer icon is found → move forward

If button is found → click it

Loops forever

