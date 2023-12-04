from deepl import DeepL

def translate_words(words, src_language='el', dest_language='en', deepl_api_key=None):
    if not deepl_api_key:
        raise ValueError("DeepL API key is required for translation. Get one from https://www.deepl.com/pro#developer.")

    # Initialize DeepL client with the provided API key
    deepl = DeepL(deepl_api_key)

    translations = {}

    if isinstance(words, str):
        # If a single word is provided, convert it to a list
        words = [words]

    try:
        # Translate each word using DeepL API
        for word in words:
            translation_result = deepl.translate(word, target_lang=dest_language, source_lang=src_language)
            translated_word = translation_result['translations'][0]['text']
            translations[word] = translated_word

    except Exception as e:
        raise ValueError(f"Translation failed: {str(e)}")

    return translations

# Example usage:
deepl_api_key = 'YOUR_DEEPL_API_KEY'
words_to_translate = ["Bonjour", "Hola", "Guten Tag"]

try:
    translations = translate_words(words_to_translate, src_language='fr', dest_language='en', deepl_api_key=deepl_api_key)
    for word, translation in translations.items():
        print(f"Translated Word: {word} -> {translation}")
except ValueError as ve:
    print(f"Error: {ve}")
