from googletrans import Translator

def chunk_list(input_list, chunk_size):
    """Chunks a list into smaller lists of a specified size."""
    return [input_list[i:i + chunk_size] for i in range(0, len(input_list), chunk_size)]

def translate_words(words, src_language='el', dest_language='en', chunk_size=500):
    translator = Translator()
    translations = []
    
    if words:
        # Chunk the list of words to be translated into smaller lists
        word_chunks = chunk_list(words, chunk_size)

        # Translate each chunk of words
        for chunk in word_chunks:
            # Join the words in the chunk into a single string
            chunk_text = '.\n'.join(chunk)

            # Translate the chunk and split the translations back into a list
            chunk_translations = translator.translate(chunk_text, src=src_language, dest=dest_language).text.split('.\n')

            # Append the translations to the overall list
            translations.extend(chunk_translations)

    return translations
