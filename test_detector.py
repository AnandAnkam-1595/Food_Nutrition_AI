from inference.detector import FoodDetector


detector = FoodDetector()

results = detector.detect_food(
    "sample_images/apple.png"
)

print(results)