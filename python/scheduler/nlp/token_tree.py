
def strip_ignore(tokens):
    prespace = ''
    result_tokens = []
    ignore_space = ''
    previous_token = None

    for token in tokens:
        if token.get('ignore'):
            # If the token is ignored, concatenate its display and space to ignore_space
            ignore_space += token.get('display', '') + token.get('space', '')
        else:
            # If there is a previous non-ignored token, update its space
            if previous_token is not None:
                previous_token['space'] += ignore_space
                ignore_space = ''
            else:
                prespace = ignore_space
                ignore_space = ''

            result_tokens.append(token)
            previous_token = token  # Set the current token as the previous token

    # If all tokens are ignored, add ignore_space to prespace
    if not result_tokens:
        prespace = ignore_space

    return prespace, result_tokens


def collapse_entities(tokens, sent):
    result = []
    entity = None
    for t in tokens:
        token = t['token'] if t['type'] == 'WORD' else None
        if token is None:
            result.append(t)
        elif token.ent_iob_ == 'B':
            if entity is not None:
                result.append(entity)
            entity = {
                'children': [t],
                'type': 'ENTITY',
                'pos': token.ent_type_
            }
        elif token.ent_iob_ == 'I' and entity is not None:
            entity['children'].append(t)
        else:
            if entity is not None:
                result.append(entity)
            entity = None
            result.append(t)

    if entity is not None:
        result.append(entity)

    for t in result:
        if t['type'] == 'ENTITY':
            children = t['children']
            t['display'] = ''.join([f"{token['display']}{token['space']}" for token in children[:-1]])
            t['display'] += children[-1]['display']
            t['lemma'] = ''.join([f"{token['lemma']}{token['space']}" for token in children[:-1]])
            t['lemma'] += children[-1]['lemma']
            t['space'] = children[-1]['space']
            t['word'] = t['display']

    return result


def collapse(tokens, sent):
    return collapse_entities(tokens, sent)


def redirect_auxiliaries(tokens, sent):
    for t in tokens:
        token = t['token'] if t['type'] == 'WORD' else None
        if token is not None:
            if token.pos_ == 'AUX' and token.dep_ == 'aux':
                t['word'] = f'{token.text} {token.head.text}'
                t['lemma'] = token.head.lemma_
                t['pos'] = token.head.pos_
            if token.pos_ == 'VERB':
                subtoken = next(
                    (sub for sub in token.subtree if sub.pos_ == 'AUX' and sub.dep_ == 'aux' and sub.head == token),
                    None
                )
                if subtoken:
                    t['word'] = f'{subtoken.text} {token.text}'

    return tokens


def redirect(tokens, sent):
    return redirect_auxiliaries(tokens, sent)


def finalize(tree):
    for elem in tree:
        if 'children' in elem:
            elem['children'] = finalize(elem['children'])
        if 'token' in elem:
            del elem['token']

    return tree


def create_token_tree(tokens, docs):
    tree = []
    for doc in docs:
        for sent in doc.sents:
            prespace, stripped = strip_ignore([tokens[tok.i] for tok in sent])
            display = prespace + ''.join([f'{token['display']}{token['space']}' for token in stripped])
            children = redirect(collapse(stripped, sent), sent)
            tree.append({
                'display': display,
                'children': children,
                'type': 'SENTENCE',
            })

    return finalize(tree)


def get_word(token, src_language):
    if token.ent_iob_ != 'O':
        return None
    if should_ignore_token(token, src_language):
        return {
            'display': token.text,
            'word': token.text.strip(),
            'space': token.whitespace_,
            'lemma': token.lemma_,
            'pos': token.pos_,
            'ignore': True
        }
    if token.pos_ == 'AUX' and token.dep_ == 'aux':
        return {
            'display': token.text,
            'word': f'{token.text} {token.head.text}'.strip(),
            'space': token.whitespace_,
            'lemma': token.head.lemma_,
            'pos': token.head.pos_,
            'ignore': False
        }
    else:
        if token.pos_ == 'VERB':
            subtoken = next(
                (sub for sub in token.subtree if sub.pos_ == 'AUX' and sub.dep_ == 'aux' and sub.head == token),
                None
            )
            if subtoken:
                return {
                    'display': token.text,
                    'word': f'{subtoken.text} {token.text}'.strip(),
                    'space': token.whitespace_,
                    'lemma': token.lemma_,
                    'pos': token.pos_,
                    'ignore': False
                }
        return {
            'display': token.text,
            'word': token.text.strip(),
            'space': token.whitespace_,
            'lemma': token.lemma_,
            'pos': token.pos_,
            'ignore': False
        }

