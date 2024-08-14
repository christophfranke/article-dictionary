
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


def combine_with_auxiliaries(head):
    subtokens = [sub.text for sub in head.subtree if sub == head or (sub.pos_ == 'AUX' and sub.dep_ == 'aux' and sub.head == head)]
    return ' '.join(subtokens)


def redirect_auxiliaries(tokens, sent):
    for t in tokens:
        token = t['token'] if t['type'] == 'WORD' else None
        if token is not None:
            if token.pos_ == 'AUX' and token.dep_ == 'aux':
                t['word'] = combine_with_auxiliaries(token.head)
                t['lemma'] = token.head.lemma_
                t['pos'] = token.head.pos_
            else:
                t['word'] = combine_with_auxiliaries(token)

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
