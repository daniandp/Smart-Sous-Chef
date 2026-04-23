from flask import Flask, render_template, request, jsonify
from logic import process_ingredients
from api import get_recipes, get_recipe_info  # ### NEW ###: Added get_recipe_info

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    raw_input = data.get('ingredients', '')
    print(f"Input received: {raw_input}")

    ingredients, error = process_ingredients(raw_input)
    print(f"Processed ingredients: {ingredients}, error: {error}")
    if error:
        return jsonify({'error': error}), 400

    recipes, error = get_recipes(ingredients)
    print(f"Recipes: {recipes}, error: {error}")
    if error:
        return jsonify({'error': error}), 500

    return jsonify({'recipes': recipes})

# ==========================================
# ### NEW ###: Route for the internal recipe page
# ==========================================
@app.route('/recipe/<int:recipe_id>')
def recipe_detail(recipe_id):
    recipe, error = get_recipe_info(recipe_id)
    if error:
        return f"Error loading recipe: {error}", 500
    return render_template('recipe.html', recipe=recipe)

if __name__ == '__main__':
    app.run(debug=True)