from pathlib import Path
import pandas as pd
from rapidfuzz import process


class NutritionLookup:
    """
    Handles nutrition lookup for detected food items.
    """

    def __init__(self):
        # Project root
        base_dir = Path(__file__).resolve().parent.parent

        csv_path = base_dir / "datasets" / "nutrition_dataset.csv"

        self.df = pd.read_csv(csv_path)

        self.df["food_normalized"] = (
            self.df["food_normalized"]
            .astype(str)
            .str.lower()
            .str.strip()
        )

        self.food_list = self.df["food_normalized"].tolist()

    def normalize_food_name(self, food_name: str) -> str:
        """
        Normalize YOLO class names.
        """

        return (
            food_name.lower()
            .replace("-", " ")
            .replace("_", " ")
            .strip()
        )

    def get_nutrition(self, food_name: str, score_threshold: int = 80):

        food_name = self.normalize_food_name(food_name)

        match = process.extractOne(food_name, self.food_list)

        if not match:
            return None

        matched_food, score, _ = match

        if score < score_threshold:
            return None

        row = self.df[
            self.df["food_normalized"] == matched_food
        ].iloc[0]

        return {
            "Detected Food": food_name,
            "Matched Food": matched_food.title(),
            "Match Score": round(float(score), 2),
            "Serving Basis": "Per 100 g",
            "Calories (kcal/100g)": float(row["Calories (kcal per 100g)"]),
            "Protein (g/100g)": float(row["Protein (g per 100g)"]),
            "Carbohydrates (g/100g)": float(row["Carbohydrates (g per 100g)"]),
            "Fat (g/100g)": float(row["Fat (g per 100g)"])
        }