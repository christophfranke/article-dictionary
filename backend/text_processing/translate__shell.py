from translate_shell.translate import translate

def chunk_list(input_list, chunk_size):
    """Chunks a list into smaller lists of a specified size."""
    return [input_list[i:i + chunk_size] for i in range(0, len(input_list), chunk_size)]

def translate_words(words, src_language='el', dest_language='en', chunk_size=500):
    translations = {}
    
    if words:
        # Chunk the list of words to be translated into smaller lists
        word_chunks = chunk_list(words, chunk_size)

        # Translate each chunk of words
        for chunk in word_chunks:
            # Join the words in the chunk into a single string
            chunk_text = '.\n'.join(chunk)

            # Translate the chunk and split the translations back into a list
            chunk_translations = translate(chunk_text, source_lang='el', target_lang='en').results[0].paraphrase.split('.\n')

            # Populate the translations dictionary
            for original, translation in zip(chunk, chunk_translations):
                translations[original] = translation

    return translations

words_to_translate = ['συμμετοχή', 'ένα']
try:
    translations = translate_words(words_to_translate)
    for word, translation in translations.items():
        print(f"Translated Word: {word} -> {translation}")
except ValueError as ve:
    print(f"Error: {ve}")
