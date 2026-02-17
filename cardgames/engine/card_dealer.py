# card_dealer.py
# VB-style card dealer

from .model import Card


def dealCards(state):
    """
    VB-style dealCards.
    Deals cards into each column according to the game script rules.

    Decision tree per column (mirrors VB logic exactly):

      1. shufle_any_cards == "1"
            → Draw num_cards from the top of the shuffled deck.
              This is also triggered by contents_at_start=next (same thing).

      2. shufle_any_cards == "0"  AND  contents_at_start is a card list
            → Place exactly those named cards into the column.
              These cards are NOT in the deck (the [DECK] set= line
              deliberately excludes them, per readme.txt).

      3. shufle_any_cards == "0"  AND  contents_at_start is empty / missing
            → Column starts empty (num_cards=0 usually confirms this).
    """
    from .engine import sync_column_contents

    print(f"DEBUG: Dealer starting. Deck size: {len(state.LIST_DECK)}")

    for col in state.kup:
        # Clear any old data
        col.contents = []
        col.weight = 0

        num = int(col.num_cards or 0)

        # --- BRANCH 1: draw from shuffled deck ---
        if str(col.shufle_any_cards) == "1":
            for _ in range(num):
                if not state.LIST_DECK:
                    break
                item = state.LIST_DECK.pop(0)
                new_card = item if isinstance(item, Card) else Card(code=item)
                new_card.column_index = col.index
                col.contents.append(new_card)

        # --- BRANCH 2: predefined card list from contents_at_start ---
        else:
            # BUG FIX: Column.__init__ does not initialise contents_at_start,
            # so hasattr() returns False for columns created via Column(index=n).
            # Use getattr with a fallback to "" to be safe regardless.
            at_start = getattr(col, "contents_at_start", "") or ""

            if at_start and at_start.strip().lower() != "next":
                # e.g. contents_at_start=h01   or   contents_at_start=c01,d12
                for code in at_start.split(","):
                    code = code.strip()
                    if code:
                        new_card = Card(code=code)
                        new_card.column_index = col.index
                        col.contents.append(new_card)
            # "next" with shufle_any_cards=0 is unusual but handle it gracefully:
            # treat it the same as shufle_any_cards=1 (draw from deck).
            elif at_start.strip().lower() == "next" and num > 0:
                for _ in range(num):
                    if not state.LIST_DECK:
                        break
                    item = state.LIST_DECK.pop(0)
                    new_card = item if isinstance(item, Card) else Card(code=item)
                    new_card.column_index = col.index
                    col.contents.append(new_card)
            # else: column starts empty — nothing to do

        col.weight = len(col.contents)
        sync_column_contents(state, col)

    #print(f"DEBUG: Dealing finished. Cards left in deck: {len(state.LIST_DECK)}")