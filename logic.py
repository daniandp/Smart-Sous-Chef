def process_ingredients(raw_input):
    """
    Validates and cleans the raw ingredient input from the user.
    Returns a tuple: (cleaned_ingredients_string, error_message)
    """
    if not raw_input or not raw_input.strip():
        return None, 'Please enter at least one ingredient.'

    # Split by comma, strip whitespace, remove empty entries
    parts = [item.strip() for item in raw_input.split(',')]
    ingredients = [item for item in parts if item]

    if len(ingredients) == 0:
        return None, 'No valid ingredients found. Please separate ingredients with commas.'

    if len(ingredients) > 20:
        return None, 'Too many ingredients. Please enter 20 or fewer.'

    # Remove any ingredients that are just numbers or special characters
    cleaned = [i for i in ingredients if any(c.isalpha() for c in i)]

    if not cleaned:
        return None, 'Please enter valid ingredient names.'

    # Spoonacular expects a comma-separated string
    return ','.join(cleaned), None
