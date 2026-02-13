# card_dealer.py
# VB-style card dealer (no parameters, uses globals)
# here are the colleed constants, variables,functions and procedures that run a state machine for Card Games 
from .model import columnX, columnY, orig_card_x_size, orig_card_y_size, gap_x, gap_y, zoom, zoom2, default_overlap_x, default_overlap_y
from .model import LIST_GAME_LINES, LIST_DECK, GAME_NAME
from .model import timerNumRepeats, parameter, numOfGames, kup, usedColumns, usedFaceDowns, usermode, selectedCard
from .model import selectedColumn, destinationColumn, simulateClickMode, singleClickMode, doubleClickMode, actionMode, youWon, clickModeSuceededSoTryAgain, cardJustMoved, nextAvailableFaceDown
from .model import zap_st_igre
from .model import Column, Card, TableObject
from .model import FaceDownOverlay, SelectionOverlay, ColumnSlot 
from .model import imageFaceDown, ShapeSelektor, ShapeColumns
#from .model import ... languages (obsolete)

# engine incorporated...
from .engine import parse_contents_str, serialize_contents, sync_column_contents, assert_cards_are_objects
from .engine import card_faces_up, calcColumnXY, card_is_face_up, minmax


###from .model import Card

def dealCards(game):
    """
    VB-style dealCards
    - consumes LIST_DECK (list[str] like 's13')
    - populates col.contents with Card objects ONLY
    """

    for col in game.kup:
        col.contents = []
        col.weight = 0

        num = int(col.num_cards or 0)
        if num <= 0:
            continue

        # VB: shufle_any_cards = 1 → deal from deck
        if str(col.shufle_any_cards) == "1":
            for _ in range(num):
                if not LIST_DECK:
                    break
                code = LIST_DECK.pop(0)
                col.contents.append(Card(code=code))

        else:
            # VB: predefined contents_at_start (string)
            if col.contents_at_start:
                for code in col.contents_at_start.split(","):
                    col.contents.append(Card(code=code))

        col.weight = len(col.contents)

        # 🔐 sync VB string after dealing
        sync_column_contents(col)


# def dealCards(game):
#     """
#     VB-style dealCards()

#     - uses global LIST_DECK
#     - modifies game.kup(c)
#     - sets contents, weight, face_up
#     """

#     kup = game.kup

#     # -------------------------------------------------
#     # PHASE 1: prepare cards (deal from deck)
#     # -------------------------------------------------
#     for i, col in enumerate(kup):

#         num = int(col.num_cards or 0)
#         if num <= 0:
#             continue

#         if str(col.shufle_any_cards) == "1":
#             cards = []

#             for _ in range(num):
#                 if not LIST_DECK:
#                     break
#                 cards.append(LIST_DECK.pop(0))

#             col.contents_at_start = ",".join(cards)
#             col.contents = cards[:]

#         else:
#             # Predefined contents
#             if isinstance(col.contents_at_start, str):
#                 col.contents = (
#                     col.contents_at_start.split(",")
#                     if col.contents_at_start
#                     else []
#                 )
#             else:
#                 col.contents = list(col.contents_at_start or [])

#         col.weight = 0  # VB resets before placement

#     # -------------------------------------------------
#     # PHASE 2: logical placement & face-up logic
#     # -------------------------------------------------
#     for i, col in enumerate(kup):

#         num = int(col.num_cards or 0)
#         if num <= 0:
#             continue

#         for j, card_code in enumerate(col.contents, start=1):

#             # increase stack
#             col.weight += 1

#             # facedown logic
#             if str(col.use_facedown) == "1":
#                 cfu = col.cards_face_up
#                 face_up = card_faces_up(cfu, j)
#             else:
#                 face_up = True

#             # store per-card metadata (renderer will use this later)
#             game.card_state[card_code] = {
#                 "column": i,
#                 "face_up": face_up,
#                 "z": col.weight,
#             }
