from collections import Counter

from inference.detector import FoodDetector
from nutrition.nutrition_lookup import NutritionLookup
from config import CONFIDENCE_THRESHOLD


class FoodInference:


    def __init__(self):
        """Initialize detector and nutrition lookup."""

        self.detector = FoodDetector()
        self.nutrition_lookup = NutritionLookup()

    def analyze_image(self, image_path):
        """
        Analyze a food image.

        Args:
            image_path (str): Path to the input image.

        """

        detections = self.detector.detect_food(image_path)

        foods = []
        food_counter = Counter()

        total_calories = 0
        total_protein = 0
        total_carbohydrates = 0
        total_fat = 0

        for detection in detections:

            # Ignore low-confidence detections
            if detection["confidence"] < CONFIDENCE_THRESHOLD:
                continue

            food_counter[detection["food"]] += 1

            nutrition = self.nutrition_lookup.get_nutrition(
                detection["food"]
            )
            
            if nutrition is None:

                nutrition = {

                    "Detected Food": detection["food"],

                    "Matched Food": "Not Found",

                    "Serving Basis": "N/A",

                    "Calories (kcal/100g)": 0,

                    "Protein (g/100g)": 0,

                    "Carbohydrates (g/100g)": 0,

                    "Fat (g/100g)": 0

                }

            if nutrition:
                total_calories += nutrition["Calories (kcal/100g)"]
                total_protein += nutrition["Protein (g/100g)"]
                total_carbohydrates += nutrition["Carbohydrates (g/100g)"]
                total_fat += nutrition["Fat (g/100g)"]
                
            foods.append({

                "food": detection["food"],

                "confidence": round(detection["confidence"], 3),

                "bbox": detection["bbox"],

                "nutrition": nutrition

            })

        # Handle images with no food detected
        if not foods:
            return {
                "message": "No food items detected."
            }

        return {

            "food_counts": dict(food_counter),

            "foods": foods,

            "nutrition_summary": {
                "Serving Basis": "Per 100 g for each detected food item",

                "Calories": round(total_calories, 2),

                "Protein": round(total_protein, 2),

                "Carbohydrates": round(total_carbohydrates, 2),

                "Fat": round(total_fat, 2)

            }

        }