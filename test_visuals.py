from inference.detector import FoodDetector
from utils.visualisation import Visualizer

detector = FoodDetector()

detections = detector.detect_food("sample_images/pizza.jpg")

visualizer = Visualizer()

output = visualizer.draw_detections(
    "sample_images/pizza.jpg",
    detections
)

print(output)