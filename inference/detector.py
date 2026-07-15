from ultralytics import YOLO
from config import MODEL_PATH, CONFIDENCE_THRESHOLD


class FoodDetector:
    """
    Food Detector using YOLOv8.
    Loads the model once and performs food detection.
    """

    def __init__(self, model_path=None):

        # Use custom model if available, otherwise use pretrained YOLO
        if model_path is None:
            try:
                self.model = YOLO(MODEL_PATH)
                print("✅ Custom FoodAI model loaded successfully.")
            except Exception:
                print("⚠️ Custom model not found. Using yolov8s.pt")
                self.model = YOLO("yolov8s.pt")
        else:
            self.model = YOLO(model_path)

    def detect_food(self, image_path):

        results = self.model.predict(
            source=image_path,
            conf=CONFIDENCE_THRESHOLD,
            verbose=False
        )

        detections = []

        for result in results:

            names = result.names

            for box in result.boxes:

                class_id = int(box.cls[0])
                confidence = float(box.conf[0])

                x1, y1, x2, y2 = box.xyxy[0].tolist()

                detections.append({

                    "class_id": class_id,

                    "food": names[class_id],

                    "confidence": round(confidence, 3),

                    "bbox": [
                        round(x1),
                        round(y1),
                        round(x2),
                        round(y2)
                    ]

                })

        return detections