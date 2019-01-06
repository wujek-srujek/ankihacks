#!/usr/bin/env python3

# prints information about deck and model names and ids

from anki.storage import Collection

collection_path = '<path>'

collection = Collection(collection_path)
try:
    print('Decks')
    for deck in sorted(collection.decks.all(), key=lambda deck: deck['name']):
        print('  {} [{}{}]'.format(deck['name'],
                                   deck['id'], ', filtered' if deck['dyn'] else ''))
    print()
    print('Models')
    for model in sorted(collection.models.all(), key=lambda model: model['name']):
        print('  {} [{}]'.format(model['name'], model['id']))
finally:
    collection.close()
