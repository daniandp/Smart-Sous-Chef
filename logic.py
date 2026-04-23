def process_ingredients(entry_data):

    raw_list = entry_data.split(',')
    
    clean_ingredients = []
    
    for item in raw_list:

        stripped_item = item.strip()
        
        lowercase_item = stripped_item.lower()

        if lowercase_item != "":
            clean_ingredients.append(lowercase_item)
            
    formatted_data = ",".join(clean_ingredients)
    
    return formatted_data

def validate_api_response(response_json):
   
    if not response_json:
        return False

    if 'status' in response_json:
        if response_json['status'] == 'failure':
            return False

    return True