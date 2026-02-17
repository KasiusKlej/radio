# shuffler_girl a module for CardGames 
import random

def shuffleDeck(state):
    """
    VB-style shuffleDeck
    """

    # ---- default unshuffled deck ----
    state.LIST_DECK.clear()

    for i in range(52):
        if i < 13:
            fname = "c"
        elif i < 26:
            fname = "d"
        elif i < 39:
            fname = "h"
        else:
            fname = "s"

        fname += f"{(i % 13) + 1:02d}"
        state.LIST_DECK.append(fname)

    # ---- find [DECK] section ----
    i = 0
    while i < len(state.LIST_GAME_LINES) and state.LIST_GAME_LINES[i] != "[DECK]":
        i += 1

    if i >= len(state.LIST_GAME_LINES):
        raise RuntimeError(f"{state.GAME_NAME}: [DECK] section not found")

    i += 1
    while i < len(state.LIST_GAME_LINES):
        s = state.LIST_GAME_LINES[i]
        i += 1

        if s == "[END DECK]":
            break

        # set=...
        if s.startswith("set="):
            state.LIST_DECK.clear()
            cards = s[4:]
            while cards:
                state.LIST_DECK.append(cards[:3])
                cards = cards[4:] if len(cards) > 3 else ""

        # shuffle_now=1
        if s.startswith("shuffle_now=1"):
            random.shuffle(state.LIST_DECK)
