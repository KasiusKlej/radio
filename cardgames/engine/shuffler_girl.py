# shuffler_girl a module for CardGames 
import random
from .model import LIST_GAME_LINES, LIST_DECK, GAME_NAME

def shuffleDeck():
    """
    VB-style shuffleDeck:
    operates entirely on global LIST_GAME_LINES and LIST_DECK
    """

    # ---- default unshuffled deck ----
    LIST_DECK.clear()

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
        LIST_DECK.append(fname)

    # ---- find [DECK] section ----
    i = 0
    while i < len(LIST_GAME_LINES) and LIST_GAME_LINES[i] != "[DECK]":
        i += 1

    if i >= len(LIST_GAME_LINES):
        raise RuntimeError(f"{GAME_NAME}: [DECK] section not found")

    i += 1
    while i < len(LIST_GAME_LINES):
        s = LIST_GAME_LINES[i]
        i += 1

        if s == "[END DECK]":
            break

        # set=...
        if s.startswith("set="):
            LIST_DECK.clear()
            cards = s[4:]
            while cards:
                LIST_DECK.append(cards[:3])
                cards = cards[4:] if len(cards) > 3 else ""

        # shuffle_now=1
        if s.startswith("shuffle_now=1"):
            random.shuffle(LIST_DECK)
