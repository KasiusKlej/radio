# engine.py 
# here are the collected constants, variables,functions and procedures that run a state machine for Card Games 
from .model import columnX, columnY, orig_card_x_size, orig_card_y_size, gap_x, gap_y, zoom, zoom2, default_overlap_x, default_overlap_y
from .model import LIST_GAME_LINES, LIST_DECK, GAME_NAME, CURRENT_LANGUAGE, AUTOPLAY_ENABLED, LANG_DIR, DEFAULT_LANG
from .model import timerNumRepeats, parameter, numOfGames, kup, usedColumns, usedFaceDowns, usermode, selectedCard
from .model import selectedColumn, destinationColumn, simulateClickMode, singleClickMode, doubleClickMode, actionMode, youWon, clickModeSuceededSoTryAgain, cardJustMoved, nextAvailableFaceDown
from .model import zap_st_igre
from .model import Column, Card, TableObject
from .model import FaceDownOverlay, SelectionOverlay, ColumnSlot 
from .model import imageFaceDown, ShapeSelektor, ShapeColumns
from .model import menu_items_slo, menu_items_eng, EngineTimer
from .model import lang_app, lang_msg, lang_youwon, lang_youlost, lang_logo1, lang_logo2, lang_logo3, lang_logo4, lang_statWon, lang_statLost, lang_statPlayed, lang_statPct, lang_statPctalfa
from .model import frmc1, frmc2, frmc3, frmc4, frmc5, frmc6, frmc7

from .parser import load_games, language_parser, load_game_rules, load_game_names

import random

# dual representation functions
# String → Cards (during deal)
def parse_contents_str(contents_str, card_lookup):
    if not contents_str:
        return []

    cards = []
    for code in contents_str.split(","):
        cards.append(card_lookup[code])
    return cards

# Cards → String (after moves)
def serialize_contents(cards):
    return ",".join(card.code for card in cards)

# Animal killer, prevents column mismatches, call him: after dealing, after moves, before serialization, after deserialization
def sync_column_contents(col):
    # ---- ENGINE → VB ----
    if isinstance(col.contents, list):
        for i, card in enumerate(col.contents):
            if not hasattr(card, "code"):
                raise RuntimeError(
                    f"CARD CORRUPTION in column {col.cId}: "
                    f"contents[{i}] is {type(card)} ({card!r})"
                )

        col.contents_str = ",".join(card.code for card in col.contents)
        col.weight = len(col.contents)
        return

    if isinstance(col.contents, str):
        raise RuntimeError(
            f"ENGINE INVARIANT VIOLATION: col.contents is str ({col.contents})"
        )

    raise RuntimeError(
        f"ENGINE CORRUPTION: col.contents invalid type {type(col.contents)}"
    )

# Another Animal killer that prevents card type mismatches
def assert_cards_are_objects(col):
    for i, card in enumerate(col.contents):
        if not hasattr(card, "code"):
            raise RuntimeError(
                f"CARD INVARIANT VIOLATION in column {col.cId}: "
                f"contents[{i}] is {type(card)} ({card!r}), expected Card"
            )




#-----------------------------------------------------------
# helper functions
def card_faces_up(self, rule, index):
    """
    Mirrors VB card_faces_up().
    rule: Variant string
    index: 1-based card index
    """

    if rule in ("", None):
        return True

    try:
        return int(rule) >= index
    except ValueError:
        return True


def calcColumnXY():
    """
    VB-compatible column position calculator.
    Must be called once per session.
    """
    global columnX, columnY

    dx = int(orig_card_x_size) + int(gap_x)
    dy = int(orig_card_y_size) + int(gap_y)

    for i in range(10):
        for j in range(5):
            idx = i + j * 10
            if idx >= 69:
                continue

            columnX[idx] = int((i * dx + gap_x) * zoom2)
            columnY[idx] = int((j * dy + gap_y) * zoom2)


def card_is_face_up(card_code):
    """
    VB-style face-up detection.
    Returns True if card is visible (face up).
    """

    # VB: If nextAvailableFaceDown = 0 Then r = True
    if nextAvailableFaceDown == 0:
        return True

    # VB loop: check facedown overlays
    for i in range(nextAvailableFaceDown):
        fd = IMAGE_FACEDOWNS[i]
        if fd.visible and fd.tag == card_code:
            return False

    return True


    from .model import parameter


def _resolve_value(s):
    """
    Resolves VB-style value:
    - number
    - parameterXX
    """
    if isinstance(s, str) and s.startswith("parameter"):
        idx = int(s[9:11])
        return parameter[idx]
    return int(s)


def minmax(mode, s1, s2):
    """
    VB-style min/max with parameter resolution.
    mode: "min" or "max"
    """

    a = _resolve_value(s1)
    b = _resolve_value(s2)

    if mode == "min":
        return a if a < b else b
    else:
        return a if a > b else b

# --------------------------------------------------------
# initial engine routines from VB
# --------------------------------------------------------

def getGameInfo(zap_st_igre, filepath):
    """
    Port of VB getGameInfo.
    zap_st_igre: 1-based game index (FreeCell=1, Golf=4, ...)
    Returns:
        list_game_lines: all lines of the selected game
        list_actions: only action-related lines
    """
    list_game_lines = []
    list_actions = []

    matched = False
    add_action = False
    game_index = 0

    with open(filepath, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]

    i = 0
    while i < len(lines):
        if lines[i] == "[GAMENAME]":
            game_index += 1
            i += 1  # move to name line

            if game_index == zap_st_igre:
                matched = True

                while i < len(lines):
                    s = lines[i]

                    if s == "[GAMENAME]":
                        break  # next game starts

                    list_game_lines.append(s)

                    if s == "[ACTIONS]":
                        add_action = True
                    elif s in ("[FINISH]", "[END ACTIONS]"):
                        add_action = False
                    elif add_action:
                        list_actions.append(s)

                    i += 1

                break  # game found, stop scanning
        i += 1

    if not matched:
        raise ValueError(f"Game with zap_st_igre={zap_st_igre} not found")

    return list_game_lines, list_actions



def move_condition(selectedCard, selectedColumn, col):
    """
    VB port of:
    Function move_condition(selectedCard As Variant, selectedColumn As Variant, col As Variant) As Variant
    Returns True / False
    """

    # player_can_always_put_card option
    cond = (kup[col].player_can_put_card == "yes")

    # allowed on empty column
    cond1 = (
        kup[col].player_can_put_card_if_empty == "yes"
        and kup[col].weight == 0
    )

    # only certain card allowed on empty column
    cond2 = (
        kup[col].player_can_put_card_if_empty not in ("no", "-1", "yes")
        and (selectedCard in kup[col].player_can_put_card_if_empty)
        and kup[col].weight == 0
    )

    # normal matching rules (alternate color, suit, rank, etc.)
    cond3 = match_alternates(col, selectedCard)

    # is move to this column allowed from specific columns
    cond4 = False
    if kup[col].player_can_put_card not in ("yes", "no", "-1"):
        cond4 = match_specificCol(
            kup[col].player_can_put_card,
            selectedColumn
        )
        cond = cond4
    else:
        cond = cond or cond1 or cond2 or cond3

    return cond


def hide_previous_requisites():
    """
    VB: hidePreviousRequsites
    Tear down visuals from a previous game before staging a new one.
    """

    global usermode, usedColumns, nextAvailableFaceDown

    # nothing clicked yet
    usermode = 0

    # reset parameters
    for i in range(len(parameter)):
        parameter[i] = 0

    # unload column shapes
    for i in range(1, usedColumns + 1):
        ShapeColumns[i].visible = False

        if i < len(kup) and kup[i].allways_facedown == "1":
            if i < len(imageFaceDown):
                imageFaceDown[i].visible = False

    # unload any remaining facedowns
    if nextAvailableFaceDown > 0:
        for i in range(1, nextAvailableFaceDown + 1):
            if i < len(imageFaceDown):
                imageFaceDown[i].visible = False
        nextAvailableFaceDown = 0

    usedColumns = 0

    # hide templates
    ShapeSelektor.visible = False
    if imageFaceDown:
        imageFaceDown[0].visible = False

    # (actions / buttons will be handled later)


def check_allways_facedown_columns():
    """
    VB: check_allways_facedown_columns
    Keeps always-facedown overlays in sync with their columns.
    """

    global usedColumns

    max_i = min(usedColumns, len(kup) - 1, len(imageFaceDown) - 1)

    for i in range(max_i + 1):
        col = kup[i]

        if col.allways_facedown == "1":

            if col.weight > 0:
                # vertical position
                if col.custom_y != -1:
                    imageFaceDown[i].top = col.custom_y
                else:
                    imageFaceDown[i].top = (
                        columnY[int(col.position)]
                        + col.overlap_y * col.weight
                    )

                # horizontal position
                if col.custom_x != -1:
                    imageFaceDown[i].left = col.custom_x
                else:
                    imageFaceDown[i].left = (
                        columnX[int(col.position)]
                        + col.overlap_x * col.weight
                    )

                imageFaceDown[i].bring_to_front()

                # VB: Right(kup(i).contents, 3)
                imageFaceDown[i].tag = col.contents[-3:] if col.contents else ""

                imageFaceDown[i].visible = True

            else:
                imageFaceDown[i].visible = False
                imageFaceDown[i].tag = ""


def match_specificCol(specifCol, col):
    """
    VB: match_specificCol
    specifCol: string ("any", "4", "1,4,5,18")
    col: integer (current column index)
    """

    if not specifCol:
        return False

    if specifCol == "any":
        return True

    try:
        # no commas → single column
        if "," not in specifCol:
            return int(specifCol) == col

        # comma-separated list
        allowed = [int(s.strip()) for s in specifCol.split(",") if s.strip()]
        return col in allowed

    except Exception:
        # VB: MsgBox gamename & lang_msg : End
        raise RuntimeError(f"Game script error: invalid specifCol='{specifCol}'")



# ------------------------------------------------------
# functions that use timer (experimental)
#-------------------------------------------------------
def gather_cards(self):
    if not self.animate_enabled:
        return

    self.timer_repeats = 3 * 24

    def step():
        self._gather_step()

    self.timers.append(
        EngineTimer(
            interval=1/24,
            repeats=self.timer_repeats,
            callback=step
        )
    )


def _gather_step(self):
    self.timer_repeats -= 1

    if self.timer_repeats <= 0:
        self._snap_cards_to_deck()
        return

    r = random.randint(1, 51)
    c0 = self.cards[0]
    c = self.cards[r]

    factor = self.timer_repeats / 72
    c.top = c0.top + (c.top - c0.top) * factor
    c.left = c0.left + (c.left - c0.left) * factor


def _snap_cards_to_deck(self):
    c0 = self.cards[0]
    for c in self.cards[1:]:
        c.top = c0.top
        c.left = c0.left

    self.deck_facedown.top = c0.top
    self.deck_facedown.left = c0.left
    self.deck_facedown.visible = True



# ---------------------------------------------------------------
# engine functions
# ---------------------------------------------------------------
def turn_or_shuffle_column(kup, col_index, mode="turn"):
    """
    mode: "turn" | "shuffle"
    Returns True if operation performed, False otherwise.
    """

    # Safety
    if col_index < 0 or col_index >= len(kup):
        return False

    column = kup[col_index]

    if column.weight == 0:
        return False

    if column.weight == 1:
        return True  # trivial success

    # --- snapshot old order ---
    old_cards = list(column.contents)  # list[Card]
    n = len(old_cards)

    # --- compute new order indices ---
    if mode == "turn":
        new_indices = list(reversed(range(n)))

    elif mode == "shuffle":
        new_indices = list(range(n))
        random.shuffle(new_indices)

    else:
        raise ValueError(f"Unknown mode: {mode}")

    # --- apply new order ---
    new_cards = [old_cards[i] for i in new_indices]
    column.contents = new_cards
    column.weight = len(new_cards)

    # --- rebuild contents_str (VB-compatible semantic) ---
    column.contents_str = ",".join(card.code for card in new_cards)

    # --- z-order semantics (bottom first, VB-style) ---
    for card in new_cards:
        card.z = 0  # or however z-order is represented

    return True


def do_action(self, act: str) -> bool:
    """
    Execute an action DSL string.
    Returns success of the action.
    """

    success = False

    # ----------------------------
    # movecolumn=X-Y
    # ----------------------------
    if act.startswith("movecolumn="):
        ac = act[len("movecolumn="):]
        csource, cdest = map(int, ac.split("-"))

        self.actionMode = True
        self.simulateClickMode = True

        if self.kup[csource].weight > 0:
            success = self.moveColumn(
                csource,
                cdest,
                self.kup[csource].weight
            )

        self.actionMode = False
        self.simulateClickMode = False

    # ----------------------------
    # turncolumn=X
    # ----------------------------
    elif act.startswith("turncolumn="):
        col = int(act[len("turncolumn="):])
        success = turn_or_shuffle_column(self.kup, col, mode="turn")

    # ----------------------------
    # shufflecolumn=X
    # ----------------------------
    elif act.startswith("shufflecolumn="):
        col = int(act[len("shufflecolumn="):])
        success = turn_or_shuffle_column(self.kup, col, mode="shuffle")

    # ----------------------------
    # movepile=N,X-Y
    # ----------------------------
    elif act.startswith("movepile="):
        ac = act[len("movepile="):]
        n_str, rest = ac.split(",", 1)
        n = int(n_str)

        csource, cdest = map(int, rest.split("-"))

        self.actionMode = True
        self.simulateClickMode = True

        n = min(n, self.kup[csource].weight)
        if n > 0:
            success = self.moveColumn(csource, cdest, n)

        self.actionMode = False
        self.simulateClickMode = False

    # ----------------------------
    # trymovepile=...
    # ----------------------------
    elif act.startswith("trymovepile="):
        ac = act[len("trymovepile="):]

        max_part, cols = ac.split(",", 1)
        max_cards = (
            self.parameter[int(max_part[9:])]
            if max_part.startswith("parameter")
            else int(max_part)
        )

        src, dest = cols.split("-")
        csource = self.selectedColumn if src == "selected" else int(src)
        cdest = int(dest)

        success = False

        if self.kup[csource].weight > 1:
            how_many = 0
            cards = list(self.kup[csource].contents)

            for i in range(min(len(cards), max_cards)):
                card = cards[-(i + 1)]
                if (
                    move_condition(card.code, csource, cdest)
                    and card.face_up
                ):
                    how_many = i + 1
                else:
                    break

            if how_many > 1:
                self.do_action(
                    f"movepile={how_many},{csource}-{cdest}"
                )
                success = True

    # ----------------------------
    # parameter / setparameter
    # ----------------------------
    elif act.startswith("parameter") or act.startswith("setparameter="):
        if act.startswith("setparameter="):
            act = act[len("setparameter="):]

        p = int(act[9:11])
        expr = act[12:]

        success = True

        if expr.isdigit():
            self.parameter[p] = int(expr)

        elif expr.startswith("countempty"):
            self.parameter[p] = param_count_empty(expr[10:])

        elif expr.startswith("cardsrowed("):
            col = (
                self.selectedColumn
                if expr[11:-1] == "selected"
                else int(expr[11:-1])
            )
            self.parameter[p] = param_cards_rowed(col)

        elif expr.startswith("min(") or expr.startswith("max("):
            fn = expr[:3]
            a, b = expr[4:-1].split(",")
            self.parameter[p] = minmax(fn, a, b)

        elif expr.startswith("source_column"):
            self.parameter[p] = self.selectedColumn

        elif expr.startswith("weight_of"):
            self.parameter[p] = param_count_weight(expr[9:])

        else:
            success = False

    # ----------------------------
    # increase(parameterX)
    # ----------------------------
    elif act.startswith("increase(parameter"):
        p = int(act[18:-1])
        self.parameter[p] += 1
        success = True

    # ----------------------------
    # ifduringaction(...)
    # ----------------------------
    elif act.startswith("ifduringaction("):
        cond, subact = act[15:].split(")", 1)
        subact = subact.lstrip(",")

        if check_ifduringaction_condition(cond):
            success = self.do_action(subact)

    # ----------------------------
    # autoplay
    # ----------------------------
    elif act.startswith("autoplay"):
        self.try_every_turn_actions()
        success = True

    # ----------------------------
    # whole action block
    # ----------------------------
    elif act.startswith("["):
        self.do_whole_action(act)
        success = True

    # ----------------------------
    # post-action maintenance
    # ----------------------------
    if success:
        self.check_allways_facedown_columns()

    return success


def check_ifduringaction_condition(self, condit: str) -> bool:
    """
    Evaluate a condition used inside ifduringaction(...).
    Returns True or False.
    """

    r = False

    # ---------------------------------
    # destination_card=...
    # ---------------------------------
    if condit.startswith("destination_card="):
        allowed = condit[len("destination_card="):]

        if self.kup[self.destinationColumn].weight > 0:
            # top card of destination column
            dest_card = self.kup[self.destinationColumn].contents[-1].code
            if dest_card in allowed:
                r = True

    # ---------------------------------
    # parameterXX comparisons
    # ---------------------------------
    elif condit.startswith("parameter"):
        # parameterXX<value / >value / =value
        p = int(condit[9:11])
        expr = condit[11:]

        if expr.startswith("<"):
            value = int(expr[1:])
            if self.parameter[p] < value:
                r = True

        elif expr.startswith(">"):
            value = int(expr[1:])
            if self.parameter[p] > value:
                r = True

        elif expr.startswith("="):
            value = int(expr[1:])
            if self.parameter[p] == value:
                r = True

        else:
            # implicit equality: parameterXX5
            if self.parameter[p] == int(expr):
                r = True

    return r


def do_whole_action(self, actionname: str) -> bool:
    """
    Execute a named action block like "[myaction]"
    or a standalone action like "trymovepile=52,10-8".
    """

    success = False

    # ---------------------------------
    # Block action: [actionname]
    # ---------------------------------
    if actionname.startswith("["):
        if not self.list_actions:
            return False

        i = 0
        count = len(self.list_actions)

        # find action header
        while i < count and self.list_actions[i] != actionname:
            i += 1

        # action not found
        if i >= count:
            return False

        i += 1  # move past [actionname]

        # execute until next block or end
        while i < count:
            s = self.list_actions[i]
            if s.startswith("["):
                break
            success = self.do_action(s)
            i += 1

    # ---------------------------------
    # Single action
    # ---------------------------------
    else:
        success = self.do_action(actionname)

    return success


def _parse_cols_arg(self, cols):
    """
    Parse column argument like:
    "3", "1,4,7", "(1,4,7)"
    → [1, 4, 7]
    """
    if cols is None:
        return []

    s = str(cols).strip()

    if s.startswith("("):
        s = s[1:]
    if s.endswith(")"):
        s = s[:-1]

    if not s:
        return []

    if "," in s:
        return [int(c.strip()) for c in s.split(",") if c.strip().isdigit()]
    else:
        return [int(s)]


def param_count_empty(self, cols):
    """
    Count how many of the given columns are empty.
    """
    r = 0
    for c in self._parse_cols_arg(cols):
        if 0 <= c < len(self.kup):
            if self.kup[c].weight == 0:
                r += 1
    return r


def param_count_weight(self, cols):
    """
    Count total number of cards in the given columns.
    """
    r = 0
    for c in self._parse_cols_arg(cols):
        if 0 <= c < len(self.kup):
            r += self.kup[c].weight
    return r


def param_cards_rowed(self, col):
    """
    Count how many top cards in a column form a valid row
    according to suit / alternate rules.
    """
    r = 0

    if not (0 <= col < len(self.kup)):
        return 0

    column = self.kup[col]

    if column.weight == 0:
        return 0

    if column.weight == 1:
        return 1

    # work on a copy of contents, top-first
    cards = list(column.contents)  # bottom -> top
    cards.reverse()                # top -> bottom

    rowed = True

    for i in range(len(cards)):
        ctop = cards[i].code
        r += 1

        if i + 1 >= len(cards):
            break

        cunder = cards[i + 1].code

        # suit rule
        if column.suit != "-1":
            rowed = self.match_crds_suit(column.suit, ctop, cunder)

        # alternate color rule
        if rowed and column.alternate != "-1":
            rowed = self.match_crds_alternate(column.alternate, ctop, cunder)

        if not rowed:
            break

        if r >= column.weight:
            break

    return r


def match_alternates(self, col, selectedCard):
    """
    Check if a single card may be placed onto destination column `col`.
    """
    cardcango = False

    if not (0 <= col < len(self.kup)):
        return False

    dest_col = self.kup[col]

    # destination must have a card to match against
    if dest_col.weight > 0:
        c = dest_col.contents[-1].code  # top card on destination

        sc_suit = selectedCard[0]
        sc_val = int(selectedCard[1:])
        c_suit = c[0]
        c_val = int(c[1:])

        # --------------------------------------------------
        # ALTERNATE rules
        # --------------------------------------------------
        if dest_col.alternate != "-1":

            def is_alternate(a, b):
                return (
                    (a == "c" and b in ("h", "d")) or
                    (a == "d" and b in ("c", "s")) or
                    (a == "h" and b in ("c", "s")) or
                    (a == "s" and b in ("h", "d"))
                )

            if dest_col.alternate == "1":  # ascending
                cond1 = (sc_val - c_val) == 1
                if dest_col.aces_on_kings != "no":
                    if sc_val == 1 and c_val == 13:
                        cond1 = True
                cond2 = is_alternate(sc_suit, c_suit)
                cardcango = cond1 and cond2

            elif dest_col.alternate == "0":  # descending
                cond1 = (c_val - sc_val) == 1
                if dest_col.aces_on_kings != "no":
                    if sc_val == 13 and c_val == 1:
                        cond1 = True
                cond2 = is_alternate(sc_suit, c_suit)
                cardcango = cond1 and cond2

            elif dest_col.alternate == "any":
                cardcango = is_alternate(sc_suit, c_suit)

        # --------------------------------------------------
        # SUIT rules
        # --------------------------------------------------
        if dest_col.suit != "-1":

            same_suit = sc_suit == c_suit

            if dest_col.suit == "1":  # ascending
                cond1 = (sc_val - c_val) == 1
                if dest_col.aces_on_kings != "no":
                    if sc_val == 1 and c_val == 13:
                        cond1 = True
                cardcango = cond1 and same_suit

            elif dest_col.suit == "0":  # descending
                cond1 = (c_val - sc_val) == 1
                if dest_col.aces_on_kings != "no":
                    if sc_val == 13 and c_val == 1:
                        cond1 = True
                cardcango = cond1 and same_suit

            elif dest_col.suit == "10":  # next_in_rank
                cond1 = abs(c_val - sc_val) == 1
                if dest_col.aces_on_kings != "no":
                    if (sc_val, c_val) in ((13, 1), (1, 13)):
                        cond1 = True
                cardcango = cond1 and same_suit

            elif dest_col.suit == "any":
                cardcango = same_suit

        # --------------------------------------------------
        # CARD VALUE rules
        # --------------------------------------------------
        if dest_col.card_value != "-1":

            if dest_col.card_value == "1":  # same value
                cardcango = sc_val == c_val

            elif dest_col.card_value == "2":  # ascending
                cardcango = (sc_val - c_val) == 1
                if dest_col.aces_on_kings != "no":
                    if sc_val == 1 and c_val == 13:
                        cardcango = True

            elif dest_col.card_value == "3":  # descending
                cardcango = (c_val - sc_val) == 1
                if dest_col.aces_on_kings != "no":
                    if sc_val == 13 and c_val == 1:
                        cardcango = True

            elif dest_col.card_value == "23":  # adjacent regardless of suit
                cardcango = abs(c_val - sc_val) == 1
                if dest_col.aces_on_kings != "no":
                    if (sc_val, c_val) in ((13, 1), (1, 13)):
                        cardcango = True

        # --------------------------------------------------
        # SUIT OR CARD rules
        # --------------------------------------------------
        if dest_col.suit_or_card != "-1":

            if dest_col.suit_or_card == "1":
                same_value = sc_val == c_val
                same_suit = sc_suit == c_suit
                cardcango = same_value or same_suit

            elif dest_col.suit_or_card == "any":
                cardcango = True

    # --------------------------------------------------
    # ALWAYS ALLOWED FROM COLUMNS
    # --------------------------------------------------
    if dest_col.always_allowed_from_columns != "-1":
        if self.match_specificCol(
            dest_col.always_allowed_from_columns,
            self.selectedColumn
        ):
            cardcango = True
        if dest_col.always_allowed_from_columns == "any":
            cardcango = True

    return cardcango


@staticmethod
def card_faces_up(cards_face_up: str, j: int) -> bool:
    """
    cards_face_up: "1,1,1,0,1"
    j: 1-based position
    """
    if not cards_face_up:
        return True

    # single value
    if len(cards_face_up) == 1:
        return bool(int(cards_face_up))

    parts = cards_face_up.split(",")
    if 1 <= j <= len(parts):
        return bool(int(parts[j - 1]))

    return False


@staticmethod
def cardId(c: str) -> int:
    """
    c = "c04" -> 0..51
    """
    suit_map = {
        "c": 0,
        "d": 1,
        "h": 2,
        "s": 3,
    }

    suit = c[0]
    value = int(c[1:])

    return suit_map[suit] * 13 + value - 1


@staticmethod
def cardname(k: int) -> str:
    """
    k = 0..51 -> "c01".."s13"
    """
    suit_map = {
        0: "c",
        1: "d",
        2: "h",
        3: "s",
    }

    suit = suit_map[k // 13]
    value = (k % 13) + 1

    return f"{suit}{value:02d}"


@staticmethod
def match_crds_suit(mode: str, ctop: str, cunder: str) -> bool:
    """
    Check suit-based matching between two cards.
    Single-deck assumption.
    """
    # suits must match
    if ctop[0] != cunder[0]:
        return False

    top_val = int(ctop[1:])
    under_val = int(cunder[1:])

    if mode == "1":
        return (top_val - under_val) == 1
    elif mode == "0":
        return (top_val - under_val) == 1
    elif mode == "any":
        return True

    return False


@staticmethod
def match_crds_alternate(mode: str, ctop: str, cunder: str) -> bool:
    """
    Check alternate-color matching between two cards.
    Single-deck assumption.
    """
    black = {"c", "s"}
    red = {"d", "h"}

    top_suit = ctop[0]
    under_suit = cunder[0]

    # alternate colors required
    alt = (
        (top_suit in black and under_suit in red) or
        (top_suit in red and under_suit in black)
    )

    if not alt:
        return False

    top_val = int(ctop[1:])
    under_val = int(cunder[1:])

    if mode == "1":
        return (top_val - under_val) == 1
    elif mode == "0":
        return (under_val - top_val) == 1
    elif mode == "any":
        return True

    return False


def try_every_turn_actions(self):
    """
    Execute actions defined as every_turn=x-y or every_turn=[action].
    """
    while True:
        self.clickModeSuceededSoTryAgain = False

        if not self.ListActions:
            break

        i = 0
        while i < len(self.ListActions):
            s = self.ListActions[i]
            i += 1

            if s.startswith("every_turn=") and self.autoplay_enabled:
                ac = s[11:]  # after 'every_turn='

                if ac.startswith("["):
                    self.do_whole_action(ac)

                elif ac.startswith("parameter"):
                    self.do_action(ac)

                else:
                    # x-y move
                    try:
                        csource = int(ac.split("-")[0])
                        cdest = int(ac.split("-")[1])
                    except (ValueError, IndexError):
                        continue

                    if self.kup[csource].weight == 0:
                        continue

                    crd = self.kup[csource].contents[-3:]
                    crd_id = self.cardId(crd)

                    if crd_id is not None and self.card_is_face_up(self.cardname(crd_id)):
                        # simulate click mode
                        self.simulateClickMode = True
                        self.column_click(csource, crd_id)
                        self.column_click(cdest, crd_id)
                        self.simulateClickMode = False

            if s == "[FINISH]":
                break

        if not self.clickModeSuceededSoTryAgain:
            break

    # also execute conditional actions every turn
    self.try_if_actions()


def try_if_actions(self):
    """
    Execute conditional actions defined as if(condition)then[action].
    """
    if not self.ListActions:
        return

    i = 0
    while i < len(self.ListActions):
        s = self.ListActions[i]
        i += 1

        if not s.startswith("if("):
            if s == "[FINISH]":
                break
            continue

        # extract condition and action block name
        cond_expr = s[s.find("(") + 1 : s.find(")")]
        ac = s[s.find(")then") + 5 :]

        cond = False

        # empty_columns condition
        if cond_expr.startswith("empty_columns="):
            cols = cond_expr[14:]
            sum_weights = 0

            for part in cols.split(","):
                c = int(part)
                sum_weights += self.kup[c].weight

            cond = (sum_weights == 0)

        # parameter condition
        elif cond_expr.startswith("parameter"):
            pnum = int(cond_expr[9:11])
            expr = cond_expr[cond_expr.find("=") + 1 :]

            val = self.parameter[pnum]

            if expr.startswith(">"):
                cond = val >= int(expr[1:])
            elif expr.startswith("<"):
                cond = val <= int(expr[1:])
            else:
                cond = val == int(expr)

        # execute action block
        if cond:
            j = 0
            while j < len(self.ListActions):
                if self.ListActions[j] == ac:
                    break
                j += 1

            if j >= len(self.ListActions):
                raise RuntimeError("Action block not found")

            j += 1
            while j < len(self.ListActions):
                act = self.ListActions[j]
                j += 1
                if act.startswith("["):
                    break
                self.do_action(act)

        if s == "[FINISH]":
            break


def try_seek_Parameter_actions(self):
    """
    Execute seek_parameter actions.
    """
    if not self.ListActions:
        return

    for s in self.ListActions:
        if s.startswith("seek_parameter="):
            ac = s[15:]
            if ac.startswith("parameter"):
                self.do_action(ac)
        if s == "[FINISH]":
            break


def check_end_of_game(self):
    """
    Checks [VICTORY] and [DEFEAT] blocks in ListGame.
    Emits end-of-game events exactly once.
    """
    try:
        # ---------- VICTORY ----------
        i = 0
        sum_weights = 0

        while i < len(self.ListGame) and self.ListGame[i] != "[VICTORY]":
            i += 1

        if i < len(self.ListGame):
            i += 1  # first condition
            s = self.ListGame[i]

            if s.startswith("empty_columns="):
                cols = s[14:]

                for part in cols.split(","):
                    c = int(part)
                    sum_weights += self.kup[c].weight

                if sum_weights == 0 and not self.youWon:
                    self.statistics(self.gamename, "modify", 1, 0, 1)

                    # engine signal (UI will react later)
                    self.game_result = "victory"
                    self.game_message = lang_youwon

                    self.youWon = True

        # ---------- DEFEAT ----------
        i = 0
        sum_weights = 0

        while i < len(self.ListGame) and self.ListGame[i] != "[DEFEAT]":
            i += 1

        if i < len(self.ListGame) and not self.youWon:
            i += 1  # first condition
            s = self.ListGame[i]

            if s.startswith("empty_columns="):
                cols = s[14:]

                for part in cols.split(","):
                    c = int(part)
                    sum_weights += self.kup[c].weight

                if sum_weights == 0 and not self.youWon:
                    self.statistics(self.gamename, "modify", 0, 1, 1)

                    self.game_result = "defeat"
                    self.game_message = lang_youlost

                    self.youWon = True

    except Exception:
        raise RuntimeError(self.gamename + lang_msg)
