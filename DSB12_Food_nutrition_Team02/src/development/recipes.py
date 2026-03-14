import requests
import random
import numpy as np
import pandas as pd
from typing import List, Dict, Tuple
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

# -----------------------------
# CONSTANTS
# -----------------------------

USDA_API_KEY = "FJJzYwBSmxgFXXvtcYUQBiQgSjcDAKEXdCdVotOg"
USDA_BASE_URL = "https://api.nal.usda.gov/fdc/v1"


DAILY_VALUES = {
    "Total Fat": 78,
    "Saturated Fat": 20,
    "Cholesterol": 300,
    "Total Carbohydrate": 275,
    "Dietary Fiber": 28,
    "Total Sugars": 50,
    "Sodium": 2300,
    "Protein": 50,

    "Vitamin A": 900, 
    "Vitamin C": 90,
    "Calcium": 1300,
    "Iron": 18,
    "Vitamin D": 20, 
    "Vitamin E": 15,
    "Vitamin K": 120, 
    "Thiamin": 1.2,
    "Riboflavin": 1.3,
    "Niacin": 16,
    "Vitamin B6": 1.7,
    "Folate": 400,
    "Vitamin B12": 2.4,
    "Biotin": 30,
    "Pantothenic acid": 5,
    "Phosphorus": 1250,
    "Iodine": 150,
    "Magnesium": 420,
    "Zinc": 11,
    "Selenium": 55,
    "Copper": 0.9,
    "Manganese": 2.3,
    "Chromium": 35,
    "Molybdenum": 45,
    "Chloride": 2300,
    "Potassium": 4700,
    "Choline": 550
}

VALUES = {'sodium' : 0.0, 'protein' : 0.0, 'fat' : 0.0, 'calories' : 0.0}

# -----------------------------
# USDA NUTRITION FACTS
# -----------------------------

class NutritionFacts:

    def __init__(self, api_key: str = USDA_API_KEY):
        self.api_key = api_key

    def _search_food(self, ingredient: str) -> int | None:
        """Search ingredient and return best fdcId."""
        url = f"{USDA_BASE_URL}/foods/search"
        payload = {"query": ingredient, "pageSize": 1}

        response = requests.post(
            url,
            params={"api_key": self.api_key},
            json=payload,
            timeout=10
        )

        foods = response.json().get("foods", [])
        if not foods:
            return None
        return foods[0]["fdcId"]

    def _fetch_nutrients(self, fdc_id: int) -> Dict[str, float]:
        url = f"{USDA_BASE_URL}/food/{fdc_id}"
        response = requests.get(
            url,
            params={"api_key": self.api_key},
            timeout=10
        )

        nutrients = {}
        for item in response.json().get("foodNutrients", []):
            name = item["nutrient"]["name"]
            amount = item.get("amount")
            if name in DAILY_VALUES and amount is not None:
                nutrients[name] = amount

        return nutrients

    def daily_value_percentages(self, ingredient: str) -> Dict[str, int]:
    
        fdc_id = self._search_food(ingredient)
        if not fdc_id:
            return {}

        nutrients = self._fetch_nutrients(fdc_id)
        percentages = {}

        for nutrient, value in nutrients.items():
            dv = DAILY_VALUES[nutrient]
            percentages[nutrient] = int(round((value / dv) * 100))

        return percentages
    
    def train_values(self, ingredient: str) -> Dict[str, float]:
        fdc_id = self._search_food(ingredient)
        if not fdc_id:
            return {}
        
        nutrients = self._fetch_nutrients(fdc_id)
        nutrient_values={}

        for nutrient, value in nutrients.items():
            for key, _ in VALUES.items():
                if key in nutrient.lower():
                    nutrient_values[key] = value
                if key not in nutrient_values:
                    nutrient_values[key] = 0.0        
        return nutrient_values

# -----------------------------
# RECIPE SIMILARITY
# -----------------------------

class RecipeSimilarity:

    def __init__(self, recipes_df: pd.DataFrame):
        self.df = recipes_df.copy()
        self.ingredient_index = self._build_vocab()

    def _build_vocab(self) -> Dict[str, int]:
        vocab = set()
        for ing_list in self.df["ingredients"]:
            vocab.update(ing_list)
        return {ing: idx for idx, ing in enumerate(sorted(vocab))}

    def _vectorize(self, ingredients: List[str]) -> np.ndarray:
        vec = np.zeros(len(self.ingredient_index))
        for ing in ingredients:
            if ing in self.ingredient_index:
                vec[self.ingredient_index[ing]] = 1
        return vec

    def top_similar(
        self,
        ingredients: List[str],
        top_n: int = 3
    ) -> List[Tuple[str, float, str]]:

        query_vec = self._vectorize(ingredients).reshape(1, -1)
        recipe_vectors = np.vstack(
            self.df["ingredients"].apply(self._vectorize).values
        )

        sims = cosine_similarity(query_vec, recipe_vectors)[0]
        top_idx = sims.argsort()[::-1][:top_n]

        results = []
        for i in top_idx:
            row = self.df.iloc[i]
            results.append((row["title"], row["rating"], row["url"]))

        return results

#
#   DAILY MENU GENERATOR
#

class DailyMenuGenerator:
    def __init__(self):
        self.ingredients_df = pd.read_csv('../data/ingredients_df.csv')
        self.nutrition_df = pd.read_csv('../data/nutrition_facts_pct.csv').set_index("ingredient").drop(columns=['title'])
        self.links_df = pd.read_csv('../data/recipes_urls.csv')[['title', 'url', 'rating']]
        self.ratings_df = pd.read_csv('../data/recipes_urls.csv')[["title", "rating"]]
        self.data = self._prepare_recipe_data()

    def _prepare_recipe_data(self):
        recipe_data = []

        for _, row in self.ingredients_df.iterrows():
            title = row['title']
            used_ingredients = row.drop('title')[row.drop('title') == 1].index.tolist()


            nutrition = self.nutrition_df.loc[self.nutrition_df.index.intersection(used_ingredients)]
            nutrition_percent = nutrition.sum(skipna=True)


            rating_row = self.ratings_df[self.ratings_df['title'] == title]
            rating = float(rating_row['rating'].iloc[0]) if not rating_row.empty else 0.0



            link_row = self.links_df[self.links_df['title'] == title]
            url = link_row['url'].values[0] if not link_row.empty else "URL not found"

            recipe_data.append({
                "title": title,
                "ingredients": used_ingredients,
                "nutrition": nutrition_percent.to_dict(),
                "rating": rating,
                "url": url
            })

        return recipe_data

    def _select_top_recipes(self, count=3):

        valid = []

        for recipe in self.data:
            over_nutrient = any(float(v) > 1.0 for v in recipe['nutrition'].values())
            if not over_nutrient:
                valid.append(recipe)

        sorted_recipes = sorted(valid, key=lambda x: x['rating'], reverse=True)
        return sorted_recipes[:count]

    def generate_daily_menu(self):
        categories = ["BREAKFAST", "LUNCH", "DINNER"]
        menu = dict()

        top_recipes = self._select_top_recipes(count=9)
        random.shuffle(top_recipes)

        for i, meal in enumerate(categories):
            menu[meal] = top_recipes[i*3:(i+1)*3]

        for meal, recipes in menu.items():
            print(f"\n{meal}\n" + "-"*30)
            for r in recipes:
                print(f"{r['title']} (rating: {r['rating']})")
                print("Ingredients:")
                for ing in r['ingredients']:
                    print(f"- {ing}")
                print("Nutrients:")
                for n, v in r['nutrition'].items():
                    print(v)
                    print(f"- {n.lower()}: {round(v*100, 1)}%")
                print(f"URL: {r['url']}\n")