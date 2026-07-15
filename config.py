from pathlib import Path


# Food Nutrition AI - Configuration

# Project Information
PROJECT_NAME = "Food Nutrition AI"
VERSION = "2.0"
MODEL_NAME = "YOLOv8s"

# Project Root

BASE_DIR = Path(__file__).resolve().parent

# Model

MODEL_PATH = BASE_DIR / "models" / "best.pt"

NUM_CLASSES = 80

IMAGE_SIZE = 640

CONFIDENCE_THRESHOLD = 0.50      # Change after testing if required

# Nutrition Dataset

NUTRITION_DATASET = BASE_DIR / "datasets" / "nutrition_dataset.csv"

SERVING_BASIS = "Per 100 g"


# Output Directory

OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)