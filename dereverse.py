#!/usr/bin/env python3

# removes reverse cards
# they don't work well for me and increase the workload twofold
# WARNING: destructive operation

from anki.storage import Collection

deck_name = '<deck>'
reverse_card_type = '<type>'
reverse_trigger_field = '<field>'
collection_path = '<path>'

collection = Collection(collection_path)
try:
    deck = collection.decks.byName(deck_name)
    if not deck:
        raise ValueError('deck \'{}\' not found'.format(deck_name))

    reverse_card_ids = set()
    for noteId in collection.findNotes('deck:\'{}\''.format(deck_name)):
        note = collection.getNote(noteId)
        for card in note.cards():
            if card.template()['name'] == reverse_card_type:
                reverse_card_ids.add(card.id)
        # unset the trigger field to prevent reverse card generation
        if note[reverse_trigger_field]:
            note[reverse_trigger_field] = ''
            note.flush()
    collection.remCards(reverse_card_ids, notes=False)
finally:
    collection.close()
