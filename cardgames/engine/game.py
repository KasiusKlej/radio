# game.py 
# here are the collected constants, variables,functions and procedures that run a state machine for Card Games 
from .model import columnX, columnY, orig_card_x_size, orig_card_y_size, gap_x, gap_y, zoom, zoom2, default_overlap_x, default_overlap_y
from .model import LIST_GAME_LINES, LIST_DECK, GAME_NAME, CURRENT_LANGUAGE, AUTOPLAY_ENABLED, LANG_DIR, DEFAULT_LANG
from .model import timerNumRepeats, parameter, numOfGames, kup, usedColumns, usedFaceDowns, usermode, selectedCard
from .model import selectedColumn, destinationColumn, simulateClickMode, singleClickMode, doubleClickMode, actionMode, youWon, clickModeSuceededSoTryAgain, cardJustMoved, nextAvailableFaceDown
from .model import zap_st_igre
from .model import Column, Card, TableObject
from .model import FaceDownOverlay, SelectionOverlay, ColumnSlot 
from .model import imageFaceDown, ShapeSelektor, ShapeColumns
from .model import menu_items_slo, menu_items_eng
from .model import lang_app, lang_msg, lang_youwon, lang_youlost, lang_logo1, lang_logo2, lang_logo3, lang_logo4, lang_statWon, lang_statLost, lang_statPlayed, lang_statPct, lang_statPctalfa
from .model import frmc1, frmc2, frmc3, frmc4, frmc5, frmc6, frmc7

# engine incorporated...
from .engine import parse_contents_str, serialize_contents, sync_column_contents, assert_cards_are_objects
from .engine import card_faces_up, calcColumnXY, card_is_face_up, minmax, param_count_empty, param_count_weight, param_cards_rowed
from .engine import getGameInfo, hide_previous_requisites, check_allways_facedown_columns, match_specificCol, gather_cards
from .engine import turn_or_shuffle_column, do_action, check_ifduringaction_condition, do_whole_action
from .engine import match_alternates, card_faces_up, cardId, cardname, match_crds_suit, match_crds_alternate
from .engine import try_every_turn_actions, try_if_actions, try_seek_Parameter_actions, check_end_of_game

from .parser import load_games, language_parser, load_game_rules, load_game_names, parse_all_games

from .shuffler_girl import shuffleDeck
from .card_dealer import dealCards

from flask import session
import random
from .layout_heuristics import apply_game_layout_heuristics
from pathlib import Path


def load_default_language():
    try:
        return language_parser(LANG_DIR, DEFAULT_LANG)
    except Exception as e:
        # LAST LINE OF DEFENSE — app must not crash because of language
        print("Language load failed:", e)
        return {
            "lang": {
                "app": "Card Games for One",
                "msg": " malfunction.",
                "youwon": "You won!",
                "youlost": "You lost!",
            },
            "menu": {},
            "dialog": {"ok": "OK", "cancel": "Cancel"},
            "statistics": {},
            "meta": {},
        }

#out of phase
CURRENT_LANGUAGE = load_default_language()      # this is out of phase, should be phase 0

class CardGame:
    """
    Single source of truth for:
    - column semantics (role)
    - layout metadata (row, overlap)
    - card state
    """
    #TICK_INTERVAL = 1 / 24  # seconds


# -------------------------------------------------
# entry point somewhere between phase 1 and 2
# -------------------------------------------------
    def __init__(self, game_id):

        # ---- PHASE 2: pre-Form_Load (VB global setup) ----
        global zap_st_igre, GAME_NAME, LIST_GAME_LINES

        zap_st_igre = game_id
        self.game_id = game_id
        self.name = ""
        self.timers = []

        # STATIC GAME DATA (read once per game start, not per action)
        LIST_GAME_LINES = load_games()          # ZERO arguments, single source

        # Extract this game's definition
        self.load_game()                        # sets GAME_NAME, trims LIST_GAME_LINES

        # Initialize VB-style globals
        self._vb_init_globals()

        # ---- PHASE 3: start game (VB Form_Load) ----
        self.autoplay_enabled = False
        self._start_new_game()


    # inside class CardGame

    # def _start_new_game(self):
    #     global (
    #         simulateClickMode, singleClickMode, doubleClickMode, actionMode,
    #         youWon, nextAvailableFaceDown,
    #         zoom, zoom2,
    #         numOfGames
    #     )

    #     # input modes
    #     simulateClickMode = False
    #     singleClickMode = False
    #     doubleClickMode = False
    #     actionMode = False

    #     # game state
    #     youWon = False
    #     nextAvailableFaceDown = 0

    #     # zoom
    #     zoom = 1
    #     zoom2 = 1

    #     # hourglass equivalent could be frontend later

    #     # deck + statistics
    #     initDeck()
    #     statistics("no game started", "load", 0, 0, 0)

    #     # gather cards (VB semantics)
    #     gather_cards()

    #     # menu/game counters
    #     numOfGames = 0

    #     # autoplay default
    #     self.autoplay_enabled = False


    def _vb_init_globals(self):
        global kup, parameter, youWon
        global selectedCard, selectedColumn, destinationColumn
        global simulateClickMode, singleClickMode, doubleClickMode
        global actionMode, clickModeSuceededSoTryAgain
        global cardJustMoved, nextAvailableFaceDown

        kup.clear()
        parameter.clear()

        youWon = False
        selectedCard = -1
        selectedColumn = -1
        destinationColumn = -1

        simulateClickMode = False
        singleClickMode = False
        doubleClickMode = False
        actionMode = False
        clickModeSuceededSoTryAgain = False
        cardJustMoved = False
        nextAvailableFaceDown = 0

    def prepareRequisites(self):
        """
        VB: prepareRequisites
        Initializes visual table actors:
        - column slots
        - selection overlay
        - persistent face-down overlays
        """

        # reset globals (VB-style shared visual actors)
        ShapeColumns.clear()
        imageFaceDown.clear()

        # reset facedown tracking
        global nextAvailableFaceDown, usedColumns
        nextAvailableFaceDown = 0

        # selector hidden at start
        ShapeSelektor.visible = False

        # --- create column slots ---
        for i, col in enumerate(self.kup):
            slot = ColumnSlot(column_index=i)

            pos = int(col.position)

            slot.top = col.custom_y if col.custom_y != -1 else columnY[pos]
            slot.left = col.custom_x if col.custom_x != -1 else columnX[pos]

            slot.visible = True

            # appearance overrides
            if col.backstyle != "-1":
                slot.backstyle = col.backstyle
            if col.backcolor != "-1":
                slot.backcolor = col.backcolor

            ShapeColumns.append(slot)

        usedColumns = len(ShapeColumns) - 1

        # --- persistent face-down columns ---
        for i, col in enumerate(self.kup):
            if col.allways_facedown == "1":
                fd = FaceDownOverlay()
                fd.visible = True
                fd.top = ShapeColumns[i].top
                fd.left = ShapeColumns[i].left

                imageFaceDown.append(fd)
                nextAvailableFaceDown += 1

        # ensure facedowns are stacked correctly
        check_allways_facedown_columns()





    # -------------------------------------------------
    # Load & semantics
    # -------------------------------------------------
    # def load_game_definition(game_id):
    #     current_name = None
    #     buffer = []
    #     games = {}

    #     with open(LANG_DIR / "CardGames-utf8.txt", encoding="utf-8") as f:
    #         for line in f:
    #             line = line.rstrip()

    #             if line == "[GAMENAME]":
    #                 if current_name:
    #                     gid = normalize_game_id(current_name)
    #                     games[gid] = buffer
    #                 current_name = next(f).strip()
    #                 buffer = []
    #             else:
    #                 buffer.append(line)

    #         if current_name:
    #             gid = normalize_game_id(current_name)
    #             games[gid] = buffer

    #     if game_id not in games:
    #         raise ValueError(f"Game definition not found for id '{game_id}'")

    #     return games[game_id], current_name


    def load_game(self):
        global LIST_GAME_LINES, GAME_NAME

        lines = LIST_GAME_LINES
        i = 0
        found = False
        game_lines = []

        while i < len(lines):
            line = lines[i].strip()
            i += 1

            if line == "[GAMENAME]":
                name = lines[i].strip()
                i += 1

                if name == zap_st_igre:
                    GAME_NAME = name
                    self.name = name
                    found = True

                    # collect game block
                    while i < len(lines):
                        s = lines[i].strip()
                        if s.startswith("[") and s.endswith("]"):
                            break
                        game_lines.append(s)
                        i += 1
                    break

        if not found:
            raise ValueError(f"Game not found: {zap_st_igre}")

        # Replace LIST_GAME_LINES with this game's definition
        LIST_GAME_LINES = game_lines



    def _start_new_game(self):
        global youWon, cardJustMoved, zap_st_igre
        """
        VB Form_Load equivalent.
        Called exactly once.
        """
        
        
        # ------------------------------------------------------------
        # VB → Python Migration Tracker
        # #### irrelevant / intentionally not ported
        # ###  ported & working
        # ##   planned, not ported yet
        # #    decision pending
        # ------------------------------------------------------------

        #### statistics(gamename, "modify", 0, 0, 1)
        # (statistics system will be ported later)

        ### gamename
        # Already mapped → game.name

        ### youWon
        youWon = 0  # VB Boolean → int/boolean (global model citizen)

        ### Form1.Caption
        # Ported → HTML <title> (via Flask template)

        #### menu enabling
        # mnuStatistics.Enabled, mnuRules.Enabled
        # (menus handled by web navigation, not state)

        #### TimerAnimate
        # Web animations handled via CSS/JS

        ### cardJustMoved
        # Will be used by engine for move validation
        cardJustMoved = 0

        ## Screen.MousePointer
        # Ported conceptually → CSS cursor: wait
        # Future usage:
        # setBusy(true);
        # // start animation / fetch / deal
        # setBusy(false);
        # self.gather_cards()         # experimental
        
        ### hidePreviousRequsites
        # Not applicable (DOM handles visibility)
        hide_previous_requisites()

        ### getGameInfo
        GAMES_FILE = Path(__file__).parent.parent / "games" / "CardGames-utf8.txt"
        getGameInfo(zap_st_igre, GAMES_FILE)        # zap_st_igre is set within session

        ### calcColumnXY
        calcColumnXY()

        ### prepareColumns
        self._prepare_columns()
                
        ### prepareRequisites
        # sets up visual actors
        self.prepareRequisites()
        
        ### shuffleDeck
        shuffleDeck()
        
        ### dealCards
        dealCards(self)
        
        #debug
        print("Deck size after deal:", len(LIST_DECK))        
        total_cards_on_table = sum(len(col.contents) for col in self.kup)
        print("Total cards on table:", total_cards_on_table)
        for i, col in enumerate(self.kup):
            print(
                f"Column {i}:",
                [card.code if hasattr(card, "code") else card for card in col.contents]
            )



        # 🔒 critical invariant enforcement
        for col in self.kup:
            sync_column_contents(col)
      
        ## check_allways_facedown_columns
        # Needed for strict VB rule enforcement
        check_allways_facedown_columns()

        ## do_whole_action("[autostart]")
        # Engine-driven automation (future)



        


    
    

    # -------------------------------------------------
    # Slot geometry
    # -------------------------------------------------
    #def _column_base_xy(self):
    def _column_base_xy(self, position):
        """
        Convert VB slot position (e.g. "03") into (x, y).
        """

        if not isinstance(position, str) or len(position) != 2:
            raise ValueError(f"Invalid position '{position}'")

        col = int(position[0])
        row = int(position[1])

        x = self.TABLE_INSET_X + col * self.SLOT_W
        y = self.TABLE_INSET_Y + row * self.SLOT_H

        return x, y
            

    def _assert_only_real_columns(self):
        for idx, col in enumerate(self.kup):
            col_id = col.cId or f"#{idx}"
            if col.position in ("", None):
                raise RuntimeError(
                    f"Synthetic column detected: {col_id} (no position)"
                )
  

    def _resolve_overlap_values(self):
        for idx, col in enumerate(self.kup):
            col_id = col.cId or f"#{idx}"

            if getattr(col, "_is_placeholder", False):
                continue

            # Normalize overlap values (VB style: empty means default)
            if col.overlap_x in ("", None):
                col.overlap_x = self.DEFAULT_OVERLAP_X

            if col.overlap_y in ("", None):
                col.overlap_y = self.DEFAULT_OVERLAP_Y
  
    
    def _assert_columns_are_well_formed(self):
        for idx, col in enumerate(self.kup):
            col_id = col.cId or f"#{idx}"

            # position is mandatory for layout
            if col.position in ("", None):
                raise RuntimeError(
                    f"Column {col_id} missing position"
                )

            # contents must always exist (VB ListBox equivalent)
            if col.contents is None:
                raise RuntimeError(
                    f"Column {col_id} missing contents list"
                )
        
    

    

    def _apply_slot_geometry(self):
        """
        VB-style slot geometry.
        Resolves base x/y from columnX/Y and applies custom overrides.
        """

        for idx, col in enumerate(self.kup):

            # position is VB string ("00", "12", ...)
            if col.position in ("", None):
                raise RuntimeError(f"Column #{idx} missing position")

            try:
                pos = int(col.position)
            except ValueError:
                raise RuntimeError(
                    f"Invalid column position '{col.position}' in column #{idx}"
                )

            if pos < 0 or pos >= len(columnX):
                raise RuntimeError(
                    f"Column position {pos} out of range in column #{idx}"
                )

            # base geometry (VB columnX / columnY)
            col.x = columnX[pos]
            col.y = columnY[pos]

            # custom overrides (VB: -1 means ignore)
            if col.custom_x not in (-1, None, ""):
                col.x = int(col.custom_x)

            if col.custom_y not in (-1, None, ""):
                col.y = int(col.custom_y)




    def _init_geometry_constants(self):
        """
        Single source of truth for all geometry.
        MUST match CSS and renderer assumptions.
        """

        # --- Card dimensions ---
        self.CARD_W = 80
        self.CARD_H = 120

        # --- Table padding / inset ---
        self.TABLE_INSET_X = 6
        self.TABLE_INSET_Y = 6

        # --- Slot spacing (VB legacy grid) ---
        self.SLOT_GAP_X = 12
        self.SLOT_GAP_Y = 20

        self.SLOT_W = self.CARD_W + self.SLOT_GAP_X
        self.SLOT_H = self.CARD_H + self.SLOT_GAP_Y

        # --- Default overlaps (VB semantics) ---
        self.DEFAULT_OVERLAP_X = 20
        self.DEFAULT_OVERLAP_Y = 30

        # --- Modern helpers (optional, but consistent) ---
        self.card_width = self.CARD_W
        self.card_height = self.CARD_H

        self.table_padding_x = self.TABLE_INSET_X
        self.table_padding_y = self.TABLE_INSET_Y


    def _position_to_xy(self, pos):
        """
        Factory position resolver (VB-faithful).
        Converts position like '00', '01', '12' into base (x, y).
        """
        try:
            row = int(pos[0])
            col = int(pos[1])
        except Exception:
            raise RuntimeError(f"Invalid position '{pos}'")

        x = self.TABLE_INSET_X + col * self.SLOT_W
        y = self.TABLE_INSET_Y + row * self.SLOT_H
        return x, y



    # helper functions
    def _iter_columns(self):
        return self.columns

    
    # Column overlap normalization (VB-faithful, GOLDEN)
    def _normalize_column_overlaps(self):
        for col in self.kup:

            if getattr(col, "_is_placeholder", False):
                col.overlap_x = 0
                col.overlap_y = 0
                continue

            ox = col.overlap_x
            oy = col.overlap_y

            if ox in ("", None) and oy in ("", None):
                col.overlap_x = self.DEFAULT_OVERLAP_X
                col.overlap_y = self.DEFAULT_OVERLAP_Y






    

    




    # -------------------------------------------------
    # Deck & dealing  (temporary variant until we find VB version)
    # -------------------------------------------------
    def _create_deck(self):
        suits = {
            "c": ("clubs", "black"),
            "d": ("diamonds", "red"),
            "h": ("hearts", "red"),
            "s": ("spades", "black"),
        }
        deck = []
        for s, (name, color) in suits.items():
            for rank in range(1, 14):
                code = f"{s}{rank:02}"
                deck.append({
                    "code": code,
                    "suit": name,
                    "rank": rank,
                    "color": color,
                    "face_up": True,
                    "image": f"1024x768{code}.bmp",
                })
        return deck

    
    # def shuffle_and_deal(self):
    #     # temporary not VB version (a function just to simulate card dealings at the start of a card game)
    #     deck = self._create_deck()
    #     random.shuffle(deck)

    #     for col in self.kup:
    #         col.contents.clear()
    #         col.weight = 0

    #         n = int(col.num_cards or 0)
    #         if n <= 0:
    #             continue

    #         face_mask = col.cards_face_up or []
    #         always_fd = col.allways_facedown == "1"
    #         use_fd = col.use_facedown == "1"

    #         for i in range(n):
    #             card = deck.pop(0)

    #             if always_fd:
    #                 card.face_up = False
    #             elif use_fd and i == n - 1:
    #                 card.face_up = False
    #             elif i < len(face_mask):
    #                 card.face_up = bool(int(face_mask[i]))
    #             else:
    #                 card.face_up = True

    #             col.contents.append(card)

    #         col.weight = len(col.contents)




    # -------------------------------------------------
    # Moves (under reconstruction)
    # -------------------------------------------------
    def move_card(self, from_col, to_col, card_code):
        if from_col not in self.columns or to_col not in self.columns:
            return False

        src = self.columns[from_col]["cards"]
        for i, card in enumerate(src):
            if card["code"] == card_code:
                self.columns[to_col]["cards"].append(src.pop(i))
                return True
        return False


    # -------------------------------------------------
    # Serialization
    # -------------------------------------------------
    def to_dict(self):
        # --- ensure column duality before save ---
        for col in self.kup:
            sync_column_contents(col)

        return {
            "game_id": self.game_id,

            # ----------------
            # COLUMNS + CARDS
            # ----------------
            "kup": [
                {
                    "cId": col.cId,
                    "column_name": col.column_name,
                    "position": col.position,
                    "num_cards": col.num_cards,
                    "shufle_any_cards": col.shufle_any_cards,

                    "custom_x": col.custom_x,
                    "custom_y": col.custom_y,
                    "overlap_x": col.overlap_x,
                    "overlap_y": col.overlap_y,

                    "cards": [
                        {
                            "code": card.code,
                            "face_up": card.face_up,
                            "image": card.image,
                        }
                        for card in col.contents
                    ],

                    "contents_str": col.contents_str,
                }
                for col in self.kup
            ],

            # ----------------
            # ACTORS (VISUALS)
            # ----------------
            "actors": {
                "ShapeColumns": [
                    {
                        "top": s.top,
                        "left": s.left,
                        "visible": s.visible,
                        "enabled": s.enabled,
                        "backstyle": s.backstyle,
                        "backcolor": s.backcolor,
                    }
                    for s in ShapeColumns
                ],

                "imageFaceDown": [
                    {
                        "top": fd.top,
                        "left": fd.left,
                        "visible": fd.visible,
                        "enabled": fd.enabled,
                        "tag": fd.tag,
                    }
                    for fd in imageFaceDown
                ],

                "ShapeSelektor": {
                    "top": ShapeSelektor.top,
                    "left": ShapeSelektor.left,
                    "visible": ShapeSelektor.visible,
                    "enabled": ShapeSelektor.enabled,
                },
            }
        }


    @staticmethod
    def from_dict(data):
        if not isinstance(data.get("kup"), list):
            raise RuntimeError(
                f"Session corruption detected: kup must be list, got {type(data.get('kup'))}"
            )

        g = CardGame(data["game_id"], shuffle=False)
        g.kup = []

        # ----------------
        # COLUMNS
        # ----------------
        for col_data in data["kup"]:
            col = Column()

            col.cId = col_data.get("cId", "")
            col.column_name = col_data.get("column_name", "")
            col.position = col_data.get("position", "")
            col.num_cards = col_data.get("num_cards", "")
            col.shufle_any_cards = col_data.get("shufle_any_cards", "")

            col.custom_x = col_data.get("custom_x", "")
            col.custom_y = col_data.get("custom_y", "")
            col.overlap_x = col_data.get("overlap_x", "")
            col.overlap_y = col_data.get("overlap_y", "")

            col.contents = []
            for card_data in col_data.get("cards", []):
                col.contents.append(
                    Card(
                        code=card_data["code"],
                        face_up=card_data.get("face_up", True),
                        image=card_data.get("image"),
                    )
                )

            col.contents_str = col_data.get(
                "contents_str",
                ",".join(card.code for card in col.contents),
            )

            col.weight = len(col.contents)

            sync_column_contents(col)
            g.kup.append(col)

        # ----------------
        # ACTORS
        # ----------------
        actors = data.get("actors", {})

        ShapeColumns.clear()
        for s in actors.get("ShapeColumns", []):
            slot = ColumnSlot()
            slot.top = s.get("top", 0)
            slot.left = s.get("left", 0)
            slot.visible = s.get("visible", False)
            slot.enabled = s.get("enabled", True)
            slot.backstyle = s.get("backstyle", 0)
            slot.backcolor = s.get("backcolor", 0)
            ShapeColumns.append(slot)

        imageFaceDown.clear()
        for fd in actors.get("imageFaceDown", []):
            f = FaceDownOverlay()
            f.top = fd.get("top", 0)
            f.left = fd.get("left", 0)
            f.visible = fd.get("visible", False)
            f.enabled = fd.get("enabled", True)
            f.tag = fd.get("tag", "")
            imageFaceDown.append(f)

        sel = actors.get("ShapeSelektor")
        if sel:
            ShapeSelektor.top = sel.get("top", 0)
            ShapeSelektor.left = sel.get("left", 0)
            ShapeSelektor.visible = sel.get("visible", False)
            ShapeSelektor.enabled = sel.get("enabled", True)
            ShapeSelektor.tag = sel.get("tag", "")

        return g


    # Frontend Wiring 5️⃣ Frontend Layout Formula (Canonical)
    def card_position(col, index):
        base_x = col.custom_x if col.custom_x != -1 else columnX[col.position]
        base_y = col.custom_y if col.custom_y != -1 else columnY[col.position]

        return (
            base_x + col.overlap_x * index,
            base_y + col.overlap_y * index,
            index  # z-order
        )







    # -------------------------------------------------
    # Session helpers
    # -------------------------------------------------
    @staticmethod
    def load_from_session():
        session.pop("game", None)
        return None


    def save_to_session(self):
        session["game"] = self.to_dict()


    #-------------------------------------------------
    # porting some VB functions here
    #-------------------------------------------------

    # prepareColumns
    def _prepare_columns(self):
        i = 0

        # ---- [COLUMNS DEFAULTS] ----
        while i < len(LIST_GAME_LINES) and LIST_GAME_LINES[i] != "[COLUMNS DEFAULTS]":
            i += 1

        if i < len(LIST_GAME_LINES):
            i += 1
            while i < len(LIST_GAME_LINES):
                s = LIST_GAME_LINES[i]
                i += 1

                if s == "[END COLUMNS DEFAULTS]":
                    break

                if s.startswith("overlap_x="):
                    default_overlap_x = int(s[10:])
                elif s.startswith("overlap_y="):
                    default_overlap_y = int(s[10:])
                elif s.startswith("zoom="):
                    zoom = float(s[5:])

        # ---- [COLUMNS] ----
        i = 0
        while i < len(LIST_GAME_LINES) and LIST_GAME_LINES[i] != "[COLUMNS]":
            i += 1

        if i >= len(LIST_GAME_LINES):
            raise RuntimeError("No [COLUMNS] section")

        i += 1
        c = 0

        while i < len(LIST_GAME_LINES):
            s = LIST_GAME_LINES[i]
            i += 1

            if s == "[END COLUMNS]":
                break

            col = Column()
            col.cId = c

            parts = s.split(",")
            col.column_name = parts[0]
            col.position = parts[1].strip()[:2]
            col.num_cards = parts[2].strip()
            col.shufle_any_cards = s[-1]

            # defaults (VB faithfully)
            col.max_cards = 0
            col.suit = -1
            col.card_value = -1
            col.alternate = -1
            col.suit_or_card = -1
            col.always_allowed_from_columns = -1
            col.custom_x = -1
            col.custom_y = -1
            col.overlap_x = 0
            col.overlap_y = 0
            col.player_can_put_card = "-1"
            col.player_can_put_card_if_empty = "-1"
            col.player_can_take_card = "-1"
            col.contents_at_start = ""
            col.cards_face_up = ""
            col.use_facedown = "-1"
            col.weight = 0

            self.kup.append(col)
            c += 1


