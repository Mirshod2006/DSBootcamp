import sys
from joblib import load
import pandas as pd
from recipes import NutritionFacts, RecipeSimilarity, DailyMenuGenerator

# -----------------------------
# CONFIGURATION
# -----------------------------

MODEL_PATH = "../data/model.pkl"
RECIPES_CSV = "../data/recipes_urls.csv"


# -----------------------------
# HELPER FUNCTIONS
# -----------------------------

def parse_ingredients(arg: str) -> list[str]:
    return [x.strip().lower() for x in arg.split(",") if x.strip()]


def forecast_message(predicted_class: str) -> str:
    messages = {
        "bad": (
            "You might find it tasty, but in our opinion, it is a bad idea to have a\n"
            "dish with that list of ingredients."
        ),
        "so-so": (
            "This dish looks acceptable, but it is not particularly healthy nor harmful."
        ),
        "great": (
            "Great choice! This dish looks nutritious and well balanced."
        )
    }
    return messages.get(predicted_class, "No forecast available.")


def print_section(title: str):
    print(title)
    print("-" * len(title))


# -----------------------------
# MAIN LOGIC
# -----------------------------

def main():
    if len(sys.argv) < 2:
        print("Usage: python nutritionist.py ingredient1,ingredient2,...")
        sys.exit(1)

    ingredients = parse_ingredients(",".join(sys.argv[1:]))

    # =============================
    # I. OUR FORECAST
    # =============================

    model = load(MODEL_PATH)
    facts = NutritionFacts()

    data_list = []
    for ingredient in ingredients:
        data_list.append(facts.train_values(ingredient))

    data_list = [pd.DataFrame([x]) for x in data_list]

    train_data = pd.concat(data_list, axis=0).sum().to_frame().T

    predicted_class = model.predict(train_data)[0]

    rating_map = {1: 'bad', 2: 'bad', 3: 'so-so', 4: 'so-so', 5: 'great'}
    if isinstance(predicted_class, (int, float)):
        predicted_class = rating_map.get(int(predicted_class), "bad")

    print("I. OUR FORECAST")
    print(forecast_message(predicted_class))
    print()


    # =============================
    # II. NUTRITION FACTS
    # =============================

    print("II. NUTRITION FACTS")
    for ingredient in ingredients:
        print(ingredient.capitalize())
        nutrient_percentages = facts.daily_value_percentages(ingredient)

        if not nutrient_percentages:
            print("No nutrition data found.")
        else:
            for nutrient, percent in nutrient_percentages.items():
                print(f"{nutrient} - {percent}% of Daily Value")
        print()

    # =============================
    # III. TOP-3 SIMILAR RECIPES
    # =============================

    print("III. TOP-3 SIMILAR RECIPES:")

    recipes_df = pd.read_csv(RECIPES_CSV)

    recipes_df["ingredients"] = recipes_df["ingredients"]

    similarity = RecipeSimilarity(recipes_df)
    top_recipes = similarity.top_similar(ingredients, top_n=3)

    for title, rating, url in top_recipes:
        print(f"- {title}, rating: {rating}, URL:")
        print(url)

    print("\n\nDAILY MENUS (BONUS): ")


    menu = DailyMenuGenerator()

    menu.generate_daily_menu()


if __name__ == "__main__":
    main()
