from langdetect import detect


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
    subtokens = (sub.norm_ for sub in head.subtree if sub == head or (sub.pos_ == 'AUX' and sub.dep_ == 'aux' and sub.head == head))
    return ' '.join(subtokens)


def redirect_auxiliaries(tokens):
    for t in tokens:
        token = t['token'] if t['type'] == 'WORD' else None
        if token is not None:
            if token.pos_ == 'AUX' and token.dep_ == 'aux' and 'redirect' not in t:
                t['word'] = combine_with_auxiliaries(token.head)
                t['lemma'] = token.head.lemma_
                t['pos'] = token.head.pos_
                t['redirect'] = 'aux'
            else:
                if 'redirect' not in t:
                    new_word = combine_with_auxiliaries(token)
                    if t['word'] != new_word:
                        t['word'] = new_word
                        t['redirect'] = 'aux'


def find_determiner(token):
    try:
        return next(
            t for t in token.children if t.pos_ == 'DET' and t.dep_ == 'det' and t.head == token
        )
    except StopIteration:
        return None


def find_case(token):
    try:
        return next(
            t for t in token.children if t.pos_ == 'ADP' and t.dep_ == 'case' and t.head == token
        )
    except StopIteration:
        return None


def is_determiner(t, head):
    return t.pos_ == 'DET' and t.dep_ == 'det' and t.head == head


def is_determiner_in(t, entity):
    return t.pos_ == 'DET' and t.dep_ == 'det' and t.head in entity


def is_adpunct(t, head):
    return t.pos_ == 'ADP' and t.dep_ == 'case' and t.head == head


def is_adpunct_in(t, entity):
    return t.pos_ == 'ADP' and t.dep_ == 'case' and t.head in entity


def combine_det_case_tok(token):
    return ' '.join(t.norm_ for t in token.subtree if is_determiner(t, token) or is_adpunct(t, token) or t == token)


def combine_det_case_ent(ent):
    return ' '.join(t.text for t in ent.sent if is_determiner_in(t, ent) or is_adpunct_in(t, ent) or t in ent)


def is_part_of_entity(token):
    return token.ent_iob_ == 'B' or token.ent_iob_ == 'I'


def redirect_articles(tokens):
    for t in tokens:
        token = t['token'] if t['type'] == 'WORD' else None
        if token is not None:
            if is_adpunct(token, token.head) or is_determiner(token, token.head) and 'redirect' not in t:
                # combine det/case with non-entity
                if not is_part_of_entity(token.head):
                    t['word'] = combine_det_case_tok(token.head)
                    t['lemma'] = token.head.lemma_
                    t['pos'] = token.head.pos_
                    t['redirect'] = 'det'
                # combine det/case with entity
                else:
                    for ent in token.sent.ents:
                        if token.head in ent:
                            t['word'] = combine_det_case_ent(ent)
                            t['lemma'] = ent.lemma_
                            t['pos'] = ent.label_
                            t['redirect'] = 'det'
                            break
            else:
                if 'redirect' not in t:
                    # combine non-entity with det/case
                    new_word = combine_det_case_tok(token)
                    if new_word != t['word']:
                        t['word'] = new_word
                        t['redirect'] = 'det'

        # combine entity with det/case
        if t['type'] == 'ENTITY':
            # every entity has at least one child which is a word
            token = t['children'][0]['token']
            for ent in token.sent.ents:
                if token in ent:
                    t['word'] = combine_det_case_ent(ent)
                    t['lemma'] = ent.lemma_
                    t['pos'] = ent.label_
                    t['redirect'] = 'det'
                    break


def redirect(tokens, sent):
    redirect_articles(tokens)
    redirect_auxiliaries(tokens)


def finalize(tree):
    for elem in tree:
        if 'children' in elem:
            elem['children'] = finalize(elem['children'])
        if 'token' in elem:
            del elem['token']

    return tree


def ignore_if_wrong_language(tokens, language):
    for token in tokens:
        try:
            token['ignore'] = language != detect(token['word'])
        except Exception:
            token['ignore'] = True


def create_token_tree(tokens, docs, language):
    tree = []
    for doc in docs:
        for sent in doc.sents:
            prespace, stripped = strip_ignore([tokens[tok.i] for tok in sent])
            display = prespace + ''.join([f'{token['display']}{token['space']}' for token in stripped])
            children = collapse(stripped, sent)
            redirect(children, sent)
            ignore_if_wrong_language(children, language)
            _, stripped_children = strip_ignore(children)
            tree.append({
                'display': display,
                'children': stripped_children,
                'type': 'SENTENCE',
            })

    return finalize(tree)
