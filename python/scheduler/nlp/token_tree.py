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
    subtokens = [sub.text for sub in head.subtree if sub == head or (sub.pos_ == 'AUX' and sub.dep_ == 'aux' and sub.head == head)]
    return ' '.join(subtokens)


def redirect_auxiliaries(tokens):
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


def is_part_of_entity(token):
    return token.head.ent_iob_ == 'B' or token.head.ent_iob_ == 'I'


def redirect_articles(tokens):
    for t in tokens:
        token = t['token'] if t['type'] == 'WORD' else None
        if token is not None:
            # combine det with non-entity
            if token.pos_ == 'DET' and token.dep_ == 'det' and not is_part_of_entity(token.head):
                t['word'] = f'{token.text} {token.head.text}'
                t['lemma'] = token.head.lemma_
                t['pos'] = token.head.pos_
            else:
                # combine adp with non-entity
                if token.pos_ == 'ADP' and token.dep_ == 'case' and not is_part_of_entity(token.head):
                    t['word'] = f'{token.text} {token.head.text}'
                    t['lemma'] = token.head.lemma_
                    t['pos'] = token.head.pos_
            # combine det with entity
            if token.pos_ == 'DET' and token.dep_ == 'det' and is_part_of_entity(token.head):
                for ent in token.sent.ents:
                    if token.head in ent:
                        t['word'] = f'{token.text} {ent.text}'
                        t['lemma'] = ent.lemma_
                        t['pos'] = ent.label_
                        break
            else:
                # combine adp with entity
                if token.pos_ == 'ADP' and token.dep_ == 'case' and is_part_of_entity(token.head):
                    for ent in token.sent.ents:
                        if token.head in ent:
                            t['word'] = f'{token.text} {ent.text}'
                            t['lemma'] = ent.lemma_
                            t['pos'] = ent.label_
                            break
            # combine non-entity with det
            determiner = find_determiner(token)
            if determiner:
                t['word'] = f'{determiner.text} {token.text}'
            else:
                # combine non-entity with adp
                adpunct = find_case(token)
                if adpunct:
                    t['word'] = f'{adpunct.text} {token.text}'

        # combine entity with det
        entity_has_determiner = False
        if t['type'] == 'ENTITY':
            children = [child['token'] for child in t['children'] if child['type'] == 'WORD']
            for token in children:
                determiner = find_determiner(token)
                if determiner:
                    t['word'] = f'{determiner.text} {t['display']}'
                    entity_has_determiner = True
                    break
        # combine entity with adp
        if not entity_has_determiner:
            if t['type'] == 'ENTITY':
                children = [child['token'] for child in t['children'] if child['type'] == 'WORD']
                for token in children:
                    adpunct = find_case(token)
                    if adpunct:
                        t['word'] = f'{adpunct.text} {t['display']}'
                        break

    return tokens


def redirect(tokens, sent):
    return redirect_articles(
        redirect_auxiliaries(tokens)
    )


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
            children = redirect(collapse(stripped, sent), sent)
            ignore_if_wrong_language(children, language)
            _, stripped_children = strip_ignore(children)
            tree.append({
                'display': display,
                'children': stripped_children,
                'type': 'SENTENCE',
            })

    return finalize(tree)
