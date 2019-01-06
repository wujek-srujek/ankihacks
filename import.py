#!/usr/bin/env python3

# imports a text file (question and answer separated by '=') adding notes for each line

from anki.storage import Collection

model_name = '<model>'
deck_name = '<deck>'
collection_path = '<path>'
data_source = '<source>'

collection = Collection(collection_path)
try:
    # gets the desired model and sets the desired deck id on it, then sets it as the current model
    # this strange API is the way it all works: the current model is used when a new Note is created
    # and when cards are generated their target deck is taken from the model (unless overriding is used)
    model = collection.models.byName(model_name)
    if not model:
        raise ValueError('model \'{}\' not found'.format(model_name))
    deck = collection.decks.byName(deck_name)
    if not deck:
        raise ValueError('deck \'{}\' not found'.format(deck_name))
    model['did'] = deck['id']
    collection.models.setCurrent(model)

    with open(data_source, encoding='utf-8') as lines:
        total_cards = 0
        for i, line in enumerate(lines):
            if '=' not in line:
                print('Ignoring line {}: \'{}\''.format(i+1, line.strip()))
                continue
            question, answer = line.split('=', maxsplit=1)
            note = collection.newNote(forDeck=False)
            note['Front'] = question.strip()
            note['Back'] = answer.strip()
            # note['Add Reverse'] = 'y'
            total_cards += collection.addNote(note)
        print('Added {} cards'.format(total_cards))
finally:
    collection.close()
