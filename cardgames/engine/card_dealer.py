# card_dealer.py
# VB-style card dealer 

# 1. IMPORT the Card class from your model
from .model import Card

def dealCards(state):
    """
    VB-style dealCards
    - consumes state.LIST_DECK
    - populates col.contents with Card objects
    """
    from .engine import sync_column_contents

    print(f"DEBUG: Dealer starting. Deck size: {len(state.LIST_DECK)}")

    for col in state.kup:
        # Clear any old data (VB-style reset)
        col.contents = []
        col.weight = 0

        # How many cards does this column want? (e.g. 7 for Solitaire tableau)
        num = int(col.num_cards or 0)
        if num <= 0:
            continue

        # VB: shufle_any_cards = "1" means this column pulls from the main deck
        if str(col.shufle_any_cards) == "1":
            for _ in range(num):
                if not state.LIST_DECK:
                    break
                
                # Take the top card from the deck
                item = state.LIST_DECK.pop(0)

                # CHECK: Is it a string or an object?
                if isinstance(item, str):
                    # If it's a string code (VB style), turn it into a Card object
                    new_card = Card(code=item)
                else:
                    # If it's already a Card object, just use it
                    new_card = item
                
                # Link the card to this column
                new_card.column_index = col.index
                col.contents.append(new_card)

        else:
            # VB: predefined contents_at_start (e.g. fixed layout games)
            if hasattr(col, 'contents_at_start') and col.contents_at_start:
                for code in col.contents_at_start.split(","):
                    if code.strip():
                        col.contents.append(Card(code=code.strip()))

        col.weight = len(col.contents)

        # 🔐 Sync the VB-style contents_str ("s13,h12...")
        sync_column_contents(state, col)

    #print(f"DEBUG: Dealing finished. Cards left in deck: {len(state.LIST_DECK)}")