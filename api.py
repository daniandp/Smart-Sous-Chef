import os
import requests
from dotenv import load_dotenv

load_dotenv()

SPOONACULAR_API_KEY = os.getenv('SPOONACULAR_API_KEY')
BASE_URL = 'https://api.spoonacular.com/recipes/findByIngredients'

def get_recipes(ingredients):
    """
    Calls Spoonacular API with a comma-separated ingredients string.
    Returns a tuple: (list_of_recipes, error_message)
    """
    if not SPOONACULAR_API_KEY:
        return None, 'API key not configured.'

    params = {
        'ingredients': ingredients,
        'number': 6,           # return 6 recipes
        'ranking': 1,          # maximize used ingredients
        'ignorePantry': True,
        'apiKey': SPOONACULAR_API_KEY
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data:
            return [], None

        recipes = []
        for item in data:
            recipes.append({
                'id': item.get('id'),
                'title': item.get('title'),
                'image': item.get('image'),
                'usedIngredientCount': item.get('usedIngredientCount', 0),
                'missedIngredientCount': item.get('missedIngredientCount', 0),
                'usedIngredients': [i['name'] for i in item.get('usedIngredients', [])],
                'missedIngredients': [i['name'] for i in item.get('missedIngredients', [])],
                'link': f"https://spoonacular.com/recipes/{item.get('title', '').replace(' ', '-').lower()}-{item.get('id')}"
            })

        return recipes, None

    except requests.exceptions.ConnectionError:
        return None, 'Could not connect to Spoonacular. Check your internet connection.'
    except requests.exceptions.Timeout:
        return None, 'Request timed out. Please try again.'
    except requests.exceptions.HTTPError as e:
        if response.status_code == 402:
            return None, 'API daily limit reached. Try again tomorrow.'
        return None, f'API error: {str(e)}'
    except Exception as e:
        return None, f'Unexpected error: {str(e)}'

# ==========================================
# ### NEW ###: Function to fetch recipe info
# ==========================================
def get_recipe_info(recipe_id):
    """
    Fetches full information for a specific recipe ID.
    """
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {'apiKey': SPOONACULAR_API_KEY}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json(), None
    except Exception as e:
        return None, str(e)