from inference.inference import FoodInference

pipeline = FoodInference()

result = pipeline.analyze_image(
    "sample_images/apple.png"
)

print(result)