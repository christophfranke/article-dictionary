import re
from translate_shell.translate import translate

def chunk_list(input_list, chunk_size):
    """Chunks a list into smaller lists of a specified size."""
    return [input_list[i:i + chunk_size] for i in range(0, len(input_list), chunk_size)]

def translate_single_word(word, src_language='el', dest_language='en'):
    translation_result = translate(word, source_lang='el', target_lang='en').results[0]
    primary = translation_result['paraphrase']
    alternatives = translation_result['alternatives']

    return [primary] + alternatives

def translate_words(words, src_language='el', dest_language='en', chunk_size=200):
    translations = {}
    
    if words:
        # Chunk the list of words to be translated into smaller lists
        word_chunks = chunk_list(words, chunk_size)

        # Translate each chunk of words
        for chunk in word_chunks:
            # Join the words in the chunk into a single string
            chunk_text = '.\n##\n'.join(chunk)

            # Translate the chunk
            translation_result = translate(chunk_text, source_lang='el', target_lang='en').results[0]

            # Use regex to split the translations back into a list
            primary_chunk = re.split(r'.?\s*\#\#\s*', translation_result['paraphrase'])

            # Populate the translations dictionary with primary translations
            for original, translation in zip(chunk, primary_chunk):
                translations[original] = [translation.strip()]

    return translations
