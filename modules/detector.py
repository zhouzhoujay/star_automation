# modules/detector.py

from ultralytics import YOLO
import cv2

class Detector:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def detect(self, frame):
        """Run YOLO detection and return list of detections."""
        results = self.model(frame, verbose=False)
        detections = []
        if results and results[0].boxes is not None:
            for box in results[0].boxes:
                cls_id = int(box.cls[0])
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                detections.append({
                    "class_id": cls_id,
                    "box": (x1, y1, x2, y2),
                    "confidence": float(box.conf[0])
                })
        return detections
