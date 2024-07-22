import spacy
from langdetect import detect

import en_core_web_sm
import de_core_news_sm
import el_core_news_md

from .translate import translate_token, translate_entity, translate_text


def highlight_first_difference(str1, str2, context_range=5):
    min_len = min(len(str1), len(str2))
    index = None

    for i in range(min_len):
        if str1[i] != str2[i]:
            index = i
            break

    if index is None:
        if len(str1) != len(str2):
            index = min_len
            str1_diff = '' if len(str1) <= min_len else str1[min_len:]
            str2_diff = '' if len(str2) <= min_len else str2[min_len:]
            print(f"Strings differ in length at index {index}.")
            print(f"String 1 extra part: {str1_diff}")
            print(f"String 2 extra part: {str2_diff}")
        else:
            print("Strings are identical.")
        return

    start = max(index - context_range, 0)
    end = min(index + context_range + 1, max(len(str1), len(str2)))

    context_str1 = str1[start:end]
    context_str2 = str2[start:end]

    print(f"First difference at index {index}:")
    print(f"String 1: {context_str1}")
    print(f"String 2: {context_str2}")
    print(f"Character difference: '{str1[index]}' != '{str2[index]}'")


def should_ignore_token(token, language):
    if (token.is_space or
        token.is_currency or
        token.is_punct or
        token.is_bracket or
        token.is_quote or
        token.like_email or
        token.like_url
    ):
        return True
    try:
        return language != detect(token.text)
    except Exception:
        return True


def should_ignore_entity(entity, language):
    return all([should_ignore_token(token, language) for token in entity])


def get_entity(token, src_language):
    if token.ent_iob_ == 'B':
        doc = token.doc
        entity = next((ent for ent in doc.ents if token in ent), None)
        if entity is not None:
            return {
                'display': entity.text,
                'word': entity.text,
                'space': entity.text_with_ws[len(entity.text):],
                'lemma': ''.join([f'{token.lemma_}{token.whitespace_}' for token in entity]).strip(),
                'pos': entity.label_,
                'ignore': should_ignore_entity(entity, src_language)
            }
    return None


def get_word(token, src_language):
    if token.ent_iob_ != 'O':
        return None
    if should_ignore_token(token, src_language):
        return {
            'display': token.text,
            'word': token.text,
            'space': token.whitespace_,
            'lemma': token.lemma_,
            'pos': token.pos_,
            'ignore': True
        }
    if token.pos_ == 'AUX' and token.dep_ == 'aux':
        return {
            'display': token.text,
            'word': f'{token.text} {token.head.text}',
            'space': token.whitespace_,
            'lemma': token.head.lemma_,
            'pos': token.head.pos_,
            'ignore': False
        }
    else:
        if token.pos_ == 'VERB':
            subtoken = next((sub for sub in token.subtree if sub.pos_ == 'AUX' and sub.dep_ == 'aux' and sub.head == token), None)
            if subtoken:
                return {
                    'display': token.text,
                    'word': f'{subtoken.text} {token.text}',
                    'space': token.whitespace_,
                    'lemma': token.lemma_,
                    'pos': token.pos_,
                    'ignore': False
                }
        return {
            'display': token.text,
            'word': token.text,
            'space': token.whitespace_,
            'lemma': token.lemma_,
            'pos': token.pos_,
            'ignore': False
        }


def get_token(token, lang):
    entity = get_entity(token, lang)
    if entity is not None:
        return entity
    return get_word(token, lang)


def process(text, src_language, tgt_language):
    doc = create_doc(text, src_language)
    print(f'Analyzed document {dir(doc)}')

    # for token in doc:
    #     entity = next((ent for ent in doc.ents if token in ent), None)
    #     if entity is not None:
    #         if not should_ignore_entity(entity, src_language) and token.ent_iob_== 'B':
    #             # translation = translate_entity(entity, src_language, tgt_language)
    #             # print(f'{token.text} -> {[sub.text for sub in token.subtree]}')
    #             print(f'{entity.text} - {spacy.explain(entity.label_)}')
    #     else:
    #         if not should_ignore_token(token, src_language):
    #             # print(f'{token.text} -> {[sub.text for sub in token.subtree]}')
    #             if token.pos_ == 'AUX' and token.dep_ == 'aux':
    #                 text = f'{token.text} {token.head.text}'
    #                 # translation = translate_text(text, src_language, tgt_language)
    #                 lemma = token.head.lemma_
    #                 pos = token.head.pos_
    #                 print(f'{text} - {spacy.explain(pos)} - {lemma} - {token.ent_iob_}')
    #             else:
    #                 subtoken = next((sub for sub in token.subtree if sub.pos_ == 'AUX' and sub.dep_ == 'aux' and sub.head == token), None)
    #                 if subtoken:
    #                     text = f'{subtoken.text} {token.text}'
    #                     # translation = translate_text(text, src_language, tgt_language)
    #                     print(f'{text} - {spacy.explain(token.pos_)} ({token.pos_}) - {token.lemma_} - {token.ent_iob_}')
    #                 else:
    #                     # translation = translate_token(token, src_language, tgt_language)
    #                     print(f'{token.text} - {spacy.explain(token.pos_)} - {token.lemma_} - {token.ent_iob_}')

    # ignored_tokens = [token.text for token in tokens if should_ignore_token(token, src_language)]
    # print(f'Ignored: {ignored_tokens}')

    # found_entities = [(ent.text, ent.label_) for ent in doc.ents]
    # print(f'Found entities: {found_entities}')

    tokens = [token for token in (get_token(t, src_language) for t in doc) if token is not None]
    content = ''.join([f'{token['display']}{token['space']}' for token in tokens])
    # print('content:\n', content)
    print('IS CORRECT:', content == text)
    if content != text:
        highlight_first_difference(text, content, context_range=50)
    for token in tokens:
        print(token)


def get_nlp(lang):
    if lang == 'en':
        return en_core_web_sm.load()
    if lang == 'de':
        return de_core_news_sm.load()
    if lang == 'el':
        return el_core_news_md.load()
    raise AssertionError(f"Language not supported: {lang}")


def create_doc(text, lang):
    nlp = get_nlp(lang)
    return nlp(text)
