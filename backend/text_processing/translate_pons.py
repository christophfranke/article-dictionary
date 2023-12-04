import requests

def translate_word(word, src_language='el', dest_language='en'):
    try:
        base_url = 'https://api.pons.com/v1/dictionary'
        endpoint = f'{base_url}?q={word}&l={src_language}{dest_language}'

        response = requests.get(endpoint)

        # Check if the response status code indicates success (200 OK)
        if response.status_code != 200:
            response.raise_for_status()

        try:
            # Try to parse the response as JSON
            data = response.json()
        except ValueError:
            raise ValueError(f"Translation failed: Invalid JSON response")

        if 'error' in data:
            raise ValueError(f"Translation error: {data['error']['message']}")

        # Extract the translation from the response
        if 'hits' in data and data['hits']:
            entry = data['hits'][0]
            translation = entry['target']
            return translation
        else:
            raise ValueError(f"No translation found for the word: {word}")

    except requests.exceptions.RequestException as e:
        raise ValueError(f"Translation failed: {str(e)}")

def translate_words(words, src_language='el', dest_language='en'):
    translations = {}

    for word in words:
        try:
            translation = translate_word(word, src_language, dest_language)
            translations[word] = translation
        except ValueError as ve:
            translations[word] = str(ve)

    return translations
