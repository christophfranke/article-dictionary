import spacy
import re
from langdetect import detect

from .helper import highlight_first_difference

import en_core_web_lg
import el_core_news_lg
import de_core_news_lg
import es_core_news_lg
import ru_core_news_lg
import pt_core_news_lg
import pl_core_news_lg
import it_core_news_lg
import fr_core_news_lg


def should_ignore_token(token, language):
    if (token.is_space or
        token.is_currency or
        token.is_punct or
        token.is_bracket or
        token.is_quote or
        token.like_email or
        token.like_url or
        '\n' in token.text or
        ']' in token.text or
        '[' in token.text
    ):
        return True
    try:
        return language != detect(token.text)
    except Exception:
        return True


def get_token(token, lang):
    return {
        'display': token.text,
        'word': token.norm_,
        'space': token.whitespace_,
        'lemma': token.lemma_,
        'pos': token.pos_,
        'morph': token.morph.to_dict(),
        'type': 'WORD',
        'token': token,
        'ignore': should_ignore_token(token, lang),
    }


def preprocess(text):
    pattern = r'\.\[(\d+)\]'  # Match a period followed by [ and digits and ]
    replacement = r'. [\1]'   # Replace with a period, a space, and the captured digits within brackets

    result = re.sub(pattern, replacement, text)

    return result


def process(text, src_language, tgt_language):
    processed_text = preprocess(text)
    doc = create_doc(processed_text, src_language)

    tokens = [token for token in (get_token(t, src_language) for t in doc) if token is not None]
    content = ''.join([f'{token['display']}{token['space']}' for token in tokens])
    if content != processed_text:
        highlight_first_difference(processed_text, content, context_range=50)

    return tokens, doc


def get_nlp(lang):
    if lang == 'en':
        return en_core_web_lg.load()
    if lang == 'el':
        return el_core_news_lg.load()
    if lang == 'de':
        return de_core_news_lg.load()
    if lang == 'es':
        return es_core_news_lg.load()
    if lang == 'ru':
        return ru_core_news_lg.load()
    if lang == 'pt':
        return pt_core_news_lg.load()
    if lang == 'pl':
        return pl_core_news_lg.load()
    if lang == 'it':
        return it_core_news_lg.load()
    if lang == 'fr':
        return fr_core_news_lg.load()
    raise AssertionError(f"Language not supported: {lang}")


def create_doc(text, lang):
    nlp = get_nlp(lang)
    return nlp(text)
