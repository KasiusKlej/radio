# model.py
# ----------------------------------------------------------------
# VB GLOBAL DATA MODEL
# ----------------------------------------------------------------
# This module mirrors VB's global variable scope.
# All values here are first-class citizens and may be read/written
# by any module (engine, dealer, shuffler, renderer, UI).
# ----------------------------------------------------------------
from pathlib import Path

# ================================================================
# GEOMETRY & LAYOUT (VB globals)
# ================================================================

# Reserve 69 possible column positions (VB: columnX(), columnY())
columnX = [0] * 69
columnY = [0] * 69

# Card graphics (pixels)
orig_card_x_size = 80
orig_card_y_size = 120

# Gaps between cards / columns
gap_x = 20
gap_y = 30

# Zoom factors (obsolete but preserved for VB compatibility)
zoom = 1.0
zoom2 = 1.0

# Default overlaps (VB system values)
default_overlap_x = 20
default_overlap_y = 30


# ================================================================
# GAME SCRIPT & DECK (VB ListBox equivalents)
# ================================================================

# Loaded game script lines (VB: ListGame)
LIST_GAME_LINES = []

# Deck of cards (VB: ListDeck) – list of card codes ("c01", "h13", ...)
LIST_DECK = []

# Current game name (VB: gamename)
GAME_NAME = ""


# ================================================================
# GAME STATE / ENGINE FLAGS (FIRST-CLASS CITIZENS)
# ================================================================

# Tutorial / animation
timerNumRepeats = 0

# Generic parameter array (VB: parameter(20))
parameter = [0] * 21

# Statistics
numOfGames = 0

# Column / card usage
usedColumns = 0
usedFaceDowns = 0           # facedown cards currently used

# User interaction modes
usermode = 0                # 1=column selected, 2=move to column
selectedCard = None
selectedColumn = None
destinationColumn = None

simulateClickMode = False   # autoplay (hides selector)
singleClickMode = True      # usual mode
doubleClickMode = False     # trying move
actionMode = False          # enforce move

# Game outcome flags
youWon = False              # report win only once
clickModeSuceededSoTryAgain = False
cardJustMoved = False

# Facedown card handling
# VB: imageFaceDown(), ShapeSelektor
imageFaceDown = []      # list[FaceDownOverlay]
nextAvailableFaceDown = 0
ShapeColumns = []        # list[ColumnSlot]



# ================================================================
# OBSOLETE / UI / LANGUAGE RESOURCES (PRESERVED)
# ================================================================

# model.py
# ===============================
# Language / UI constants
# ===============================

# application
lang_app = "Card Games for One"
lang_msg = " malfunction."

# game result messages
lang_youwon = "You won!"
lang_youlost = "You lost!"

# logos / splash
lang_logo1 = "Card Games for One Player"
lang_logo2 = "           for Windows"
lang_logo3 = "  (c) september 2000"
lang_logo4 = "  (p) miha11@yahoo.com"

# statistics labels
lang_statWon = "Won: "
lang_statLost = "Lost: "
lang_statPlayed = "Played: "
lang_statPct = "Percent: "
lang_statPctalfa = "Percent alfa: "

# form / popup captions
frmc1 = "OK"
frmc2 = "Cancel"
frmc3 = "OK"
frmc4 = "Legend:"
frmc5 = "won"
frmc6 = "unfinished"
frmc7 = "lost"

# (reserved for future use)
# lang_filename = "\\cardgame - eng.txt"

# interface related
zap_st_igre: int = 1

# unused (statistics page?)
lang_Legend = ""
lang_won = ""
lang_unf = ""
lang_lost = ""

# bridge
menu_items_slo: list[str] = []
menu_items_eng: list[str] = []

CURRENT_LANGUAGE = "eng"
AUTOPLAY_ENABLED = False
LANG_DIR = Path(__file__).parent.parent / "games"
DEFAULT_LANG = "eng"

# types

# This mirrors VB's columnType exactly
class Column:
    def __init__(self):
        # identity
        self.cId = ""
        self.column_name = ""
        self.position = ""
        self.num_cards = ""
        self.shufle_any_cards = ""

        # rules
        self.max_cards = ""
        self.suit = ""
        self.card_value = ""
        self.alternate = ""
        self.suit_or_card = ""
        self.always_allowed_from_columns = ""

        # geometry
        self.custom_x = ""
        self.custom_y = ""
        self.overlap_x = ""
        self.overlap_y = ""
        self.overlap = ""

        # cards in this column
        self.contents_str = ""          # VB-style serialized form  "c01,c02,c13"
        self.contents = []              # Engine/runtime form       list[Card]
        self.contents_at_start = ""     # Legacy                    VB semantics

        # permissions
        self.player_can_put_card = ""
        self.player_can_put_card_if_empty = ""
        self.player_can_take_card = ""

        # state
        self.contents_at_start = ""
        self.cards_face_up = ""

        # actions
        self.dblclick_moves_to = ""
        self.allways_facedown = ""
        self.after_move_action = ""
        self.attempted_move_action = ""
        self.after_playermove_action = ""
        self.attempted_playermove_action = ""
        self.use_facedown = ""
        self.aces_on_kings = ""

        # visuals
        self.backstyle = ""
        self.backcolor = ""

        # runtime
        self.contents = []   # actual cards
        self.weight = 0


class Card:
    """
    Runtime card entity.
    Replaces VB card(i).
    """
    def __init__(self, code, face_up=True, image=None):
        self.code = code        # e.g. 's13'
        self.face_up = face_up
        self.image = image
        self.column_index = None


class TableObject:
    """
    Base class for all visual / interactive objects on the table.
    Mirrors VB Image / Shape controls.
    """
    def __init__(self):
        self.left = 0
        self.top = 0
        self.visible = False
        self.enabled = True
        self.image = None     # path or image id
        self.z_index = 0      # rendering order (optional)

    def to_dict(self):
        return {
            "left": self.left,
            "top": self.top,
            "visible": self.visible,
            "enabled": self.enabled,
            "image": self.image,
            "z": self.z_index,
        }


class FaceDownOverlay(TableObject):
    """
    Visual overlay that hides a card (VB imageFaceDown).
    """
    def __init__(self):
        super().__init__()
        self.card_code = None   # VB Tag = crd (e.g. "s13")

    def to_dict(self):
        d = super().to_dict()
        d["card_code"] = self.card_code
        return d


class SelectionOverlay(TableObject):
    """
    Visual selector (VB ShapeSelektor).
    """
    def __init__(self):
        super().__init__()
        self.target_column = None
        self.target_card_code = None

ShapeSelektor = SelectionOverlay()


class ColumnSlot(TableObject):
    """
    Visual representation of a column slot (VB ShapeColumn).
    """
    def __init__(self, column_index):
        super().__init__()
        self.column_index = column_index
        self.backstyle = 0
        self.backcolor = None


kup: list[ColumnSlot] = []  # VB: Dim kup() As columnType


# -------------------------------------------------        
# Timer            
# -------------------------------------------------
class EngineTimer:
    def __init__(self, interval, repeats, callback):
        self.interval = interval
        self.repeats = repeats
        self.callback = callback
        self.accum = 0.0
        self.enabled = True

def tick(self, dt):
    for timer in self.timers:
        if not timer.enabled:
            continue

        timer.accum += dt
        while timer.accum >= timer.interval:
            timer.accum -= timer.interval
            timer.callback()
            timer.repeats -= 1
            if timer.repeats <= 0:
                timer.enabled = False




