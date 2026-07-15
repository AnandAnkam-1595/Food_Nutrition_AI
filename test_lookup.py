from nutrition.nutrition_lookup import NutritionLookup

lookup = NutritionLookup()

foods = [
    "pizza",
    "hamburger",
    "fried-rice",
    "apple",
    "ramen-noodle",
    "croissant"
]

for food in foods:
    print("\n")
    print(lookup.get_nutrition(food))