# model.py
# ================================================================
# DATA MODEL PORTED FROM VISAL BASIC'S Card Games
# ================================================================
# This module bridges VB's global variable scope environment
# into the web based environment
# GameState represents a thing that was for VB single player 
# one "state of the game" and is here on web many states for many players
# ----------------------------------------------------------------
from pathlib import Path

# ================================================================
# STATIC CONSTANTS (Shared by all players - Thread Safe)
# ================================================================
orig_card_x_size = 80       
orig_card_y_size = 120
gap_x = 20                  
gap_y = 30
LANG_DIR = Path(__file__).parent.parent / "games"

# Shared menu lists (populated once at startup)
menu_items_slo: list[str] = []
menu_items_eng: list[str] = []

# ================================================================
# OBJECT DEFINITIONS (Blueprints)
# ================================================================

class Card:
    def __init__(self, code, face_up=True):
        self.code = code        # e.g. 'c01'
        self.face_up = face_up
        self.column_index = None
        # Position (used for animations)
        self.x = 0
        self.y = 0

    def to_dict(self):
        """This is what the JavaScript sees"""
        return {
            "code": self.code,
            "face_up": self.face_up,
            "x": self.x,
            "y": self.y,
            # FAITHFUL TO YOUR FILENAMES:
            "image": f"1024x768{self.code}.png" 
        }
    

class Column:
    def __init__(self, index=0):
        self.index = index
        self.cId = index
        self.column_name = ""
        self.position = ""
        self.num_cards = 0
        
        # --- The Missing Attribute ---
        # Ensure the spelling matches exactly what prepareRequisites looks for
        self.allways_facedown = "-1" 
        
        # --- Other Defaults to prevent further AttributeErrors ---
        self.player_can_put_card = "-1"
        self.player_can_put_card_if_empty = "-1"
        self.player_can_take_card = "-1"
        self.cards_face_up = ""
        self.backstyle = "-1"
        self.backcolor = "-1"
        self.overlap_x = -1
        self.overlap_y = -1
        self.custom_x = -1
        self.custom_y = -1
        
        # Coordinates (resolved during geometry phase)
        self.x = 0
        self.y = 0
        
        # Card storage
        self.contents = [] # List of Card objects
        self.contents_str = ""
        self.weight = 0

        self.contents_at_start = ""   # e.g. "h01" or "c01,d01" or "next"
        self.shufle_any_cards = "0"   # "1" = draw from deck, "0" = use contents_at_start
        self.dblclick_moves_to = "-1"
        self.after_move_action = "-1"
        self.after_playermove_action = "-1"
        self.attempted_move_action = "-1"
        self.attempted_playermove_action = "-1"
        self.suit = "-1"
        self.card_value = "-1"
        self.alternate = "-1"
        self.suit_or_card = "-1"
        self.max_cards = 0
        self.aces_on_kings = "yes"
        self.use_facedown = "0"

    def to_dict(self):
        # 🛡️ Safety check: ensure cards are objects before serializing
        processed_cards = []
        for c in self.contents:
            if hasattr(c, 'to_dict'):
                processed_cards.append(c.to_dict())
            else:
                # If it's just a string "s13", wrap it in a temporary dict
                processed_cards.append({"code": str(c), "face_up": True})

        return {
            "index": self.index,
            "name": self.column_name,
            "x": self.x,
            "y": self.y,
            "overlap_x": self.overlap_x,
            "overlap_y": self.overlap_y,
            "allways_facedown": self.allways_facedown,
            "cards": processed_cards,
            "weight": self.weight,
            "backstyle": int(self.backstyle) if str(self.backstyle).isdigit() else -1,
            "backcolor": int(self.backcolor) if str(self.backcolor).isdigit() else -1,
            "contents_at_start" : self.contents_at_start, 
            "shufle_any_cards" : self.shufle_any_cards,
            "dblclick_moves_to" : self.dblclick_moves_to,
            "after_move_action" : self.after_move_action,
            "after_playermove_action" : self.after_playermove_action,
            "attempted_move_action" : self.attempted_move_action,
            "attempted_playermove_action" : self.attempted_playermove_action,
            "suit" : self.suit,
            "card_value" : self.card_value,
            "alternate" : self.alternate,
            "suit_or_card" : self.suit_or_card,
            "max_cards" : self.max_cards,
            "aces_on_kings" : self.aces_on_kings,
            "use_facedown" : self.use_facedown
        }


class TableObject:
    def __init__(self):
        self.left = 0
        self.top = 0
        self.visible = False
        self.enabled = True

    def to_dict(self):
        return {"left": self.left, "top": self.top, "visible": self.visible, "enabled": self.enabled}
    

class ColumnSlot(TableObject):
    def __init__(self, column_index=0):
        super().__init__()
        self.column_index = column_index
        self.backstyle = -1         # -1 means "Not Set / Use Default Green"
        self.backcolor = -1
    def to_dict(self):
        d = super().to_dict()
        d["backstyle"] = self.backstyle
        d["backcolor"] = self.backcolor
        return d

class FaceDownOverlay(TableObject):
    def __init__(self):
        super().__init__()
        self.card_code = ""

class SelectionOverlay(TableObject):
    def __init__(self):
        super().__init__()
        self.target_column = -1

class EngineTimer:
    def __init__(self, interval, repeats, callback):
        self.interval = interval
        self.repeats = repeats
        self.callback = callback
        self.accum = 0.0
        self.enabled = True

# ================================================================
# THE BIG MOVE: GameState Encapsulation
# ================================================================

class GameState:
    def __init__(self, game_id, session_id):
        # Identity
        self.game_id = game_id
        self.session_id = session_id
        self.GAME_NAME = ""
        
        # VB GLOBALS moved to INSTANCE variables
        self.zap_st_igre = 1
        self.CURRENT_LANGUAGE = "eng"
        self.zoom = 1.0
        self.animate_enabled = True
        self.autoplay_enabled = False
        self.is_busy = False
        
        # Logic Structures
        # This is the "kup" move: it belongs to the player
        self.kup = [Column(i) for i in range(70)] 
        
        # Visual/Interface Objects
        self.ShapeSelektor = SelectionOverlay()
        self.imageFaceDown = [FaceDownOverlay() for _ in range(53)]
        
        # Lists and Buffers
        self.LIST_GAME_LINES = []
        self.LIST_DECK = []
        self.animation_queue = []
        self.timers = []
        self.parameter = [0] * 21
        
        # VB Engine Flags
        self.columnX = [0] * 70
        self.columnY = [0] * 70
        self.usermode = 0
        self.selectedCard = None
        self.selectedColumn = None
        self.destinationColumn = None
        self.youWon = False
        self.timer_repeats = 0

        # UI Language Constants
        self.lang_app = "Card Games for One"
        self.lang_youwon = "You won!"
        self.default_overlap_x = 0
        self.default_overlap_y = 25

        # --- THE LATEST PATCH: Engine State Flags ---
        self.usermode = 0           # 0=Selecting, 1=Moving
        self.simulateClickMode = False 
        self.actionMode = False     # Enforce move regardless of rules
        self.cardJustMoved = False
        self.clickModeSuceededSoTryAgain = False
        
        # The Brazilian Guy's Wish
        self.rules_of_currently_played_game = "No rules loaded."


    # ----------------------------------------------------------------
    # TIMER ENGINE (Ported into Class)
    # ----------------------------------------------------------------
    def tick(self, dt):
        """Processes any active backend timers for this specific player."""
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

    def gather_cards(self):
        """Prepares animation sequence based on player's animation setting."""
        if not self.animate_enabled:
            self._gather_instant()
            return

        self.timer_repeats = 3 * 24
        for _ in range(self.timer_repeats):
            # This logic would be moved into a method that modifies self
            move_data = self._calculate_one_gather_step()
            self.animation_queue.append(move_data)

    def _calculate_one_gather_step(self):
        # Placeholder for your physics logic
        return {"card": "s13", "x": 10, "y": 10}

    def _gather_instant(self):
        # Logic to skip animation and just update kup positions
        pass

    def to_dict(self):
        """
        THE FULL SNAPSHOT: Includes cards AND visual actors (Requisites).
        REMINDER: Every time you add a variable to __init__, 
        it MUST be added here so the Frontend can see it.
        """
        return {
            "game_id": self.game_id,
            "name": self.GAME_NAME,
            "usermode": self.usermode,
            "simulateClickMode": self.simulateClickMode,
            "actionMode": self.actionMode,
            "rules": self.rules_of_currently_played_game,
            "selected_card_code": self.selectedCard if self.selectedCard != -1 else None,
            # ... cards and actors as before ...
            "kup": [col.to_dict() for col in self.kup if col.column_name != "" or col.weight > 0],
            "actors": {
                "slots": [s.to_dict() for s in self.ShapeColumns],
                "selector": self.ShapeSelektor.to_dict()
            }
        }