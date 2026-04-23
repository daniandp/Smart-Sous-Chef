import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SPOONACULAR_API_KEY")

def get_recipes(ingredients):
    try: 
        findByIngUrl = "https://api.spoonacular.com/recipes/findByIngredients"

        params ={
            "ingredients": ingredients,
            "number": 10,
            "apiKey": API_KEY

        }

        response = requests.get(findByIngUrl, params=params)

        if response.status_code != 200:
            
            return None
        
        return response.json()
    except Exception as err:
        print("API Error")
        return None