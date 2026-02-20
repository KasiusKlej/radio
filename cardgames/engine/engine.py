# engine.py 
from .model import GameState, orig_card_x_size,orig_card_y_size, gap_x, gap_y, LANG_DIR, menu_items_slo, menu_items_eng
from .parser import load_games2, language_parser, load_game_rules, load_game_names, read_gamenames_from_language_files
import random

####################################################
# rewriten functions to accept "State". Or "Game."
####################################################

def moveColumn(game, c_source_idx, c_dest_idx, n):
    """
    VB Port: Function moveColumn
    game: The CardGame instance (The Captain)
    """
    s = game.state
    try:
        if n <= 0:
            return False

        source_col = s.kup[c_source_idx]
        
        # Take the last 'n' cards (The 'Pile')
        cards_to_move = source_col.contents[-n:]
        
        # Important: We must record the IDs because column_click might 
        # modify the list as we iterate.
        card_codes = [c.code for c in cards_to_move]
        
        success = False

        # Simulate the 'Double Click' logic for each card in the pile
        for code in card_codes:
            # --- FIRST CLICK (Select) ---
            s.usermode = 0
            s.simulateClickMode = True
            s.actionMode = True
            
            from .engine import column_click
            # We pass the 'game' controller now!
            column_click(game, c_source_idx, code)

            # --- SECOND CLICK (Move) ---
            s.usermode = 1
            s.simulateClickMode = True
            s.actionMode = True
            column_click(game, c_dest_idx, code)

            if s.cardJustMoved:
                success = True

        # Reset flags after the automated sequence
        s.simulateClickMode = False
        s.actionMode = False
        
        return success

    except Exception as e:
        print(f"CRITICAL ERROR in {s.name} moveColumn: {e}")
        return False


def card_is_face_up(state, card_code):
    """
    VB-style face-up detection.
    Returns True if card is visible (face up).
    """
    # VB: If nextAvailableFaceDown = 0 Then r = True
    # Now we check the specific player's state
    if state.nextAvailableFaceDown == 0:
        return True

    # VB loop: check facedown overlays
    # We iterate only up to the number of face-down cards currently in play
    for i in range(state.nextAvailableFaceDown):
        
        # Access the player's specific FaceDown array
        fd = state.imageFaceDown[i]
        
        # In VB, you used the .Tag property (e.g., fd.Tag = "s13").
        # In your Python model.py, you defined this as either 'card_code' or 'tag'.
        # We will check both just to be safe, but you should standardize it!
        fd_identifier = getattr(fd, 'card_code', getattr(fd, 'tag', None))

        # If the overlay is visible and assigned to this specific card, it's face down
        if fd.visible and fd_identifier == card_code:
            return False

    # If no visible overlay matched this card, it must be face up
    return True


# Core engine event functions
def get_column_of_card(state, card_code):
    """Helper: Finds the index of the column containing the specific card_code."""
    for i, col in enumerate(state.kup):
        for card in col.contents:
            if card.code == card_code:
                return i
    return -1

def card_Click(game, card_code):
    """
    VB: Private Sub card_Click(Index As Integer)
    Handles selecting a card, deselecting, or starting a move.
    """
    state = game.state
    if not card_code:
        return

    # Find which column this card is currently in
    col_idx = get_column_of_card(state, card_code)
    
    if col_idx != -1:
        state.singleClickMode = True
        # Call the heart of the engine
        from .engine import column_click
        column_click(game, col_idx, card_code)
        state.singleClickMode = False


def card_DblClick(game, card_code):
    """
    VB: Private Sub card_DblClick(Index As Integer)
    FIXED: Now takes 'game' parameter to match column_click signature.
    AUTOPLAY - Forces a move to possible destinations.
    """
    s = game.state  # Extract state from game
    
    try:
        if s.singleClickMode:
            return

        csour_idx = get_column_of_card(s, card_code)
        if csour_idx == -1:
            return

        # Check if the game script defines destination columns for double-click
        d_str = s.kup[csour_idx].dblclick_moves_to
        
        if d_str != "-1":
            # Split comma-separated destinations (e.g., "1,2,3")
            destinations = d_str.split(",")
            found_match = False

            for d_val in destinations:
                if not d_val.strip(): 
                    continue
                cdest_idx = int(d_val.strip())

                # Save current state of source column to see if card actually moves
                original_contents = s.kup[csour_idx].contents_str
                
                # --- Simulate Clicks ---
                s.usermode = 0
                s.selectedCard = ""
                s.selectedColumn = -1
                s.simulateClickMode = True
                s.doubleClickMode = True
                
                # Pass 'game' not 'state' ✅
                column_click(game, csour_idx, card_code)
                column_click(game, cdest_idx, card_code)
                
                # Check if move happened
                sync_column_contents(s, s.kup[csour_idx])
                
                if original_contents != s.kup[csour_idx].contents_str:
                    found_match = True
                
                s.simulateClickMode = False
                s.doubleClickMode = False

                if found_match:
                    break

        # Hide selector after action
        s.ShapeSelektor.visible = False

    except Exception as e:
        print(f"Error in {s.GAME_NAME} dblclick: {e}")
        raise RuntimeError(f"{s.GAME_NAME} logic malfunction.")
    

# engine/engine.py

def column_click(game, col_idx, card_code):
    """
    VB Port: Sub column_click
    Receives 'game' (the CardGame instance) to access class methods.
    """

    # 1. Imports from the current module (Local Math/Rule Helpers)
    from .engine import (
        move_condition, match_specificCol, 
        sync_column_contents, check_allways_facedown_columns
    )

    s = game.state  
    target_col = s.kup[col_idx]

    #print("column_click. usermode= {s.usermode} ")
    
    # ---------------------------------------------------------
    # MODE 0: SELECT CARD
    # ---------------------------------------------------------
    if s.usermode == 0:
        # Check if column is not empty and allows taking cards
        cond = (target_col.weight > 0)
        cond = cond and (target_col.player_can_take_card == "yes")
        
        # VB: can only select top card
        if target_col.contents:
            top_card = target_col.contents[-1]
            cond = cond and (top_card.code == card_code)

        if cond or s.actionMode:
            if not s.simulateClickMode:
                s.ShapeSelektor.visible = True
                s.ShapeSelektor.target_column = col_idx

            s.usermode = 1
            s.selectedCard = card_code
            s.selectedColumn = col_idx
            s.destinationColumn = -1

    # ---------------------------------------------------------
    # MODE 1: DESELECT OR MOVE
    # ---------------------------------------------------------
    else:
        # A. DESELECT
        if s.usermode == 1 and s.selectedColumn == col_idx:
            if not s.simulateClickMode:
                s.ShapeSelektor.visible = False
                s.usermode = 0
                s.selectedCard = ""
                s.selectedColumn = -1

        # B. MOVE
        elif s.usermode == 1 and s.selectedColumn != col_idx and s.selectedCard != "":
            
            # Use standalone helper from this module
            cond = move_condition(s, s.selectedCard, s.selectedColumn, col_idx)
            s.destinationColumn = col_idx
            
            sc_idx = s.selectedColumn
            success = False

            # --- PRE-MOVE ACTIONS (Attempted Move) ---
            action_key = "attempted_playermove_action" if not s.actionMode else "attempted_move_action"
            action_val = getattr(target_col, action_key, "-1")

            if action_val != "-1":
                parts = action_val.split("-")
                specifCol, ac_name = parts[0], parts[1]
                if match_specificCol(s, specifCol, sc_idx):
                    # CALL THE CAPTAIN: use game.do_whole_action (the class method)
                    success = game.do_whole_action(ac_name)
                    if success:
                        cond = False # Action overrode the move

            s.cardJustMoved = cond

            # --- EXECUTE ACTUAL MOVE ---
            if (cond or s.actionMode) and s.selectedCard != "":
                source_col = s.kup[sc_idx]
                
                moving_card = None
                for i, c in enumerate(source_col.contents):
                    if c.code == s.selectedCard:
                        moving_card = source_col.contents.pop(i)
                        break
                
                if moving_card:
                    target_col.contents.append(moving_card)
                    s.cardJustMoved = True
                    
                    source_col.weight = len(source_col.contents)
                    target_col.weight = len(target_col.contents)
                    
                    # Sync list to VB strings
                    sync_column_contents(s, source_col)
                    sync_column_contents(s, target_col)

                # --- POST-MOVE PROCESSING (Call class methods) ---
                game.try_seek_Parameter_actions()
                
                s.usermode = 0
                prev_selected_col = s.selectedColumn
                s.selectedCard = ""
                s.selectedColumn = -1
                s.ShapeSelektor.visible = False
                
                if s.simulateClickMode:
                    s.clickModeSuceededSoTryAgain = True

                # --- IMMEDIATELY AFTER MOVE ACTIONS ---
                post_action_key = "after_playermove_action" if not s.actionMode else "after_move_action"
                post_action_val = getattr(target_col, post_action_key, "-1")

                if post_action_val != "-1":
                    parts = post_action_val.split("-")
                    specifCol, ac_name = parts[0], parts[1]
                    if match_specificCol(s, specifCol, prev_selected_col):
                        game.do_whole_action(ac_name)

                # Chain reactions (Autoplay, Win checks)
                if not s.actionMode:
                    game.try_every_turn_actions()
                    check_allways_facedown_columns(s)
                    game.check_end_of_game()
                
            else:
                if s.simulateClickMode:
                    s.usermode = 0
                    s.selectedCard = ""
                    s.selectedColumn = -1

    # Argonauts don't need to call sync_visual_actors here anymore
    # because the Route calls it once at the end of the voyage.


def Form_MouseDown(game, col_idx):
    """
    VB: Private Sub Form_MouseDown(...)
    FIXED: Now takes 'game' parameter to match column_click signature.
    """
    s = game.state  # Extract state from game
    
    if not (len(s.ShapeColumns) > 0):
        return

    if col_idx == -1:
        return
    
    # Pass 'game' not 'state' ✅
    column_click(game, col_idx, s.selectedCard)


def imageFaceDown_Click(game, fd_index):
    """
    VB: Private Sub imageFaceDown_Click(Index As Integer)
    Handles clicking a face-down overlay.
    """
    state = game.state
    fd = state.imageFaceDown[fd_index]
    card_code = fd.card_code
    
    col_idx = get_column_of_card(state, card_code)
    if col_idx == -1: 
        return
    
    if state.kup[col_idx].allways_facedown == "1":
        # Card is in 'playable' face-down mode
        card_Click(game, card_code)  # ✅ Pass game
    else:
        # Cannot play this yet
        pass


def imageFaceDown_DblClick(game, fd_index):
    """
    VB: Private Sub imageFaceDown_DblClick(Index As Integer)
    Handles double-clicking to flip a card or auto-play a face-down card.
    """
    state = game.state
    fd = state.imageFaceDown[fd_index]
    card_code = fd.card_code
    col_idx = get_column_of_card(state, card_code)
    if col_idx == -1: 
        return
    
    if state.kup[col_idx].allways_facedown == "1":
        # Redirect to standard double-click logic
        card_DblClick(game, card_code)  # ✅ Pass game
    else:
        # Check if the dbl-clicked card is the top card of the column
        # and flip it if the rules allow.
        source_col = state.kup[col_idx]
        
        if source_col.contents:
            top_card_code = source_col.contents[-1].code
            
            if top_card_code == card_code:
                # Flip the card!
                fd.visible = False
                source_col.contents[-1].face_up = True
                
                # Trigger game rules
                game.try_every_turn_actions()  # ✅ This is why we need game


from .model import orig_card_x_size, orig_card_y_size, gap_x, gap_y

# ================================================================
# DUAL REPRESENTATION & INTEGRITY
# ================================================================
def sync_column_contents(state, col):
    """
    The 'Animal Killer': Prevents column mismatches.
    """
    # Safety: get session ID if state exists, otherwise use 'Unknown'
    sid = getattr(state, 'session_id', 'Unknown_Session')

    # ---- ENGINE (List) → VB (String) ----
    if isinstance(col.contents, list):
        for i, card in enumerate(col.contents):
            # Check if it's a real Card object
            if not hasattr(card, "code"):
                raise RuntimeError(
                    f"CARD CORRUPTION in session {sid}, column {getattr(col, 'index', '?')}: "
                    f"contents[{i}] is {type(card)} ({card!r})"
                )

        # Update the serialized string and the weight count
        col.contents_str = ",".join(card.code for card in col.contents)
        col.weight = len(col.contents)
        return

    raise RuntimeError(
        f"ENGINE CORRUPTION: col.contents in session {sid} is invalid type {type(col.contents)}"
    )


def assert_cards_are_objects(state, col):
    """Safety check to ensure cards haven't been downgraded to strings."""
    for i, card in enumerate(col.contents):
        if not hasattr(card, "code"):
            raise RuntimeError(
                f"CARD INVARIANT VIOLATION in session {state.session_id}: "
                f"Column {col.index}, card {i} is {type(card)}, expected Card object"
            )

def parse_contents_str(state, contents_str, card_lookup):
    """Converts a VB comma-separated string into a list of Card objects."""
    if not contents_str:
        return []

    cards = []
    for code in contents_str.split(","):
        # We find the card object from the state's master deck/lookup
        if code in card_lookup:
            cards.append(card_lookup[code])
    return cards

def serialize_contents(state, cards):
    """Pure utility to convert card objects back to 's10,h12' format."""
    return ",".join(card.code for card in cards)


# ================================================================
# RULES & LOGIC
# ================================================================

def card_faces_up(state, rule_str, card_index):
    """
    Mirrors VB card_faces_up().
    Determines if a card at a certain depth should be visible.
    """
    if rule_str in ("", None):
        return True

    try:
        # VB Logic: If rule is "3", then cards 1, 2, and 3 are face up.
        return int(rule_str) >= card_index
    except ValueError:
        # If it's a binary string like '0011', handle it here or default to True
        return True


# ================================================================
# GEOMETRY & MATH
# ================================================================

def calcColumnXY(state):
    """
    VB-compatible column position calculator.
    Updated to write into the player-specific state arrays.
    """
    # Use module-level constants (shared) to calculate state-level geometry (private)
    dx = int(orig_card_x_size) + int(gap_x)
    dy = int(orig_card_y_size) + int(gap_y)

    for i in range(10): # 10 columns wide
        for j in range(5): # 5 rows deep
            idx = i + j * 10
            if idx >= 69:
                continue

            # We write into the state's private memory
            # zoom2 is obsolete (1.0), so we multiply by 1
            state.columnX[idx] = int((i * dx + gap_x) * 1)
            state.columnY[idx] = int((j * dy + gap_y) * 1)


def _resolve_value(state, val_input):
    """
    Resolves VB-style values.
    Supports raw numbers or 'parameterXX' looking up state.parameter[XX].
    """
    if isinstance(val_input, str) and val_input.startswith("parameter"):
        try:
            # Extract index from 'parameter05' -> 5
            idx = int(val_input[9:11])
            return state.parameter[idx]
        except (ValueError, IndexError):
            return 0
    
    try:
        return int(val_input)
    except (ValueError, TypeError):
        return 0


def minmax(state, mode, val1, val2):
    """
    VB-style min/max with parameter resolution.
    """
    a = _resolve_value(state, val1)
    b = _resolve_value(state, val2)

    if mode == "min":
        return a if a < b else b
    else:
        return a if a > b else b
    

from .model import orig_card_x_size, orig_card_y_size, gap_x, gap_y

# ================================================================
# DUAL REPRESENTATION & INTEGRITY
# ================================================================

def sync_column_contents(state, col):
    """
    The 'Animal Killer': Prevents column mismatches between the 
    object-oriented list and the VB-style string.
    """
    # ---- ENGINE (List) → VB (String) ----
    if isinstance(col.contents, list):
        for i, card in enumerate(col.contents):
            if not hasattr(card, "code"):
                raise RuntimeError(
                    f"CARD CORRUPTION in session {state.session_id}, column {col.index}: "
                    f"contents[{i}] is {type(card)} ({card!r})"
                )

        # Update the serialized string and the weight count
        col.contents_str = ",".join(card.code for card in col.contents)
        col.weight = len(col.contents)
        return

    raise RuntimeError(
        f"ENGINE CORRUPTION: col.contents in session {state.session_id} is invalid type {type(col.contents)}"
    )

def assert_cards_are_objects(state, col):
    """Safety check to ensure cards haven't been downgraded to strings."""
    for i, card in enumerate(col.contents):
        if not hasattr(card, "code"):
            raise RuntimeError(
                f"CARD INVARIANT VIOLATION in session {state.session_id}: "
                f"Column {col.index}, card {i} is {type(card)}, expected Card object"
            )

def parse_contents_str(state, contents_str, card_lookup):
    """Converts a VB comma-separated string into a list of Card objects."""
    if not contents_str:
        return []

    cards = []
    for code in contents_str.split(","):
        # We find the card object from the state's master deck/lookup
        if code in card_lookup:
            cards.append(card_lookup[code])
    return cards

def serialize_contents(state, cards):
    """Pure utility to convert card objects back to 's10,h12' format."""
    return ",".join(card.code for card in cards)


# ================================================================
# RULES & LOGIC
# ================================================================

def card_faces_up(state, rule_str, card_index):
    """
    Mirrors VB card_faces_up().
    Determines if a card at a certain depth should be visible.
    """
    if rule_str in ("", None):
        return True

    try:
        # VB Logic: If rule is "3", then cards 1, 2, and 3 are face up.
        return int(rule_str) >= card_index
    except ValueError:
        # If it's a binary string like '0011', handle it here or default to True
        return True


# ================================================================
# GEOMETRY & MATH
# ================================================================

def calcColumnXY(state):
    """
    VB-compatible column position calculator.
    Updated to write into the player-specific state arrays.
    """
    # Use module-level constants (shared) to calculate state-level geometry (private)
    dx = int(orig_card_x_size) + int(gap_x)
    dy = int(orig_card_y_size) + int(gap_y)

    for i in range(10): # 10 columns wide
        for j in range(5): # 5 rows deep
            idx = i + j * 10
            if idx >= 69:
                continue

            # We write into the state's private memory
            # zoom2 is obsolete (1.0), so we multiply by 1
            state.columnX[idx] = int((i * dx + gap_x) * 1)
            state.columnY[idx] = int((j * dy + gap_y) * 1)


def _resolve_value(state, val_input):
    """
    Resolves VB-style values.
    Supports raw numbers or 'parameterXX' looking up state.parameter[XX].
    """
    if isinstance(val_input, str) and val_input.startswith("parameter"):
        try:
            # Extract index from 'parameter05' -> 5
            idx = int(val_input[9:11])
            return state.parameter[idx]
        except (ValueError, IndexError):
            return 0
    
    try:
        return int(val_input)
    except (ValueError, TypeError):
        return 0


def minmax(state, mode, val1, val2):
    """
    VB-style min/max with parameter resolution.
    """
    a = _resolve_value(state, val1)
    b = _resolve_value(state, val2)

    if mode == "min":
        return a if a < b else b
    else:
        return a if a > b else b


# ================================================================
# INITIAL ENGINE ROUTINES (STATE-AWARE PORT)
# ================================================================

def getGameInfo(zap_st_igre, filepath):
    """
    Pure data loader. Extracts game definition lines from the master file.
    Does not modify state directly, but returns data for state initialization.
    """
    target_index = int(zap_st_igre)
    list_game_lines = []
    list_actions = []

    matched = False
    add_action = False
    current_game_counter = 0

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = [line.rstrip("\n") for line in f]
    except FileNotFoundError:
        raise FileNotFoundError(f"Game definition file not found at: {filepath}")

    i = 0
    while i < len(lines):
        line_content = lines[i].strip()

        if line_content == "[GAMENAME]":
            current_game_counter += 1

            if current_game_counter == target_index:
                matched = True
                list_game_lines.append(lines[i])
                if (i + 1) < len(lines):
                    list_game_lines.append(lines[i + 1])
                
                i += 2
                while i < len(lines):
                    line_val = lines[i]
                    line_stripped = line_val.strip()

                    if line_stripped == "[GAMENAME]":
                        break 

                    list_game_lines.append(line_val)

                    if line_stripped == "[ACTIONS]":
                        add_action = True
                    elif line_stripped in ("[FINISH]", "[END ACTIONS]"):
                        add_action = False
                    elif add_action:
                        list_actions.append(line_val)
                    i += 1
                break
        i += 1

    if not matched:
        raise ValueError(f"Game with index {target_index} not found.")
    
    return list_game_lines, list_actions


def move_condition(state, selectedCard, selectedColumn_idx, target_col_idx):
    """
    VB Port: Function move_condition
    The Brain's Logic: Determines if a move is legal based on the game script.
    """
    # Import inside to prevent circular dependency
    from .engine import match_alternates, match_specificCol
    
    # Get reference to the specific column the player is trying to drop onto
    target_col = state.kup[target_col_idx]

    # Rule: player_can_always_put_card
    cond = (target_col.player_can_put_card == "yes")

    # Rule: allowed on empty column
    cond1 = (
        target_col.player_can_put_card_if_empty == "yes"
        and target_col.weight == 0
    )

    # Rule: only certain card allowed on empty column (e.g. King only)
    cond2 = (
        target_col.player_can_put_card_if_empty not in ("no", "-1", "yes")
        and (selectedCard in target_col.player_can_put_card_if_empty)
        and target_col.weight == 0
    )

    # Rule: normal matching rules (alternate color, suit, rank, etc.)
    # We pass 'state' down so match_alternates knows which player's rules to use
    cond3 = match_alternates(state, target_col_idx, selectedCard)

    # Rule: is move allowed from specific columns (e.g. Foundation only from Tableau)
    cond4 = False
    if target_col.player_can_put_card not in ("yes", "no", "-1"):
        # Here, player_can_put_card holds a string like "1,2,3"
        cond4 = match_specificCol(
            state,
            target_col.player_can_put_card,
            selectedColumn_idx
        )
        # If specific column rule exists, it usually overrides general rules
        cond = cond4
    else:
        # Standard logic: it's legal if ANY of these conditions are met
        cond = cond or cond1 or cond2 or cond3

    return cond


def hide_previous_requisites(state):
    """
    VB: hidePreviousRequsites
    Resets the player's private table state before starting a new game.
    """
    # Reset interaction mode
    state.usermode = 0

    # Reset parameters (VB: parameter(20))
    for i in range(len(state.parameter)):
        state.parameter[i] = 0

    # Reset visual column slots (ShapeColumns)
    for slot in state.ShapeColumns:
        slot.visible = False
        slot.enabled = True

    # Reset visual face-down overlays
    for fd in state.imageFaceDown:
        fd.visible = False
        fd.enabled = True
    
    # Reset counters
    state.nextAvailableFaceDown = 0
    # Note: 'usedColumns' is now derived from len(state.ShapeColumns)
    
    # Hide the selection indicator
    state.ShapeSelektor.visible = False


# def check_allways_facedown_columns(state):
#     """
#     VB: check_allways_facedown_columns
#     Syncs facedown overlays with the current position of the columns.
#     """
#     s = state  # Short reference

#     # We iterate through all columns in the player's private 'kup'
#     for i, col in enumerate(s.kup):
#         # We only care about columns tagged as "always facedown" (usually the deck)
#         if col.allways_facedown == "1":
            
#             # If the column has cards, the overlay must be visible and correctly positioned
#             if col.weight > 0:
#                 # 1. Resolve Column Position (VB Index)
#                 pos_idx = int(col.position) if col.position else 0
                
#                 # 2. Vertical Position (Y)
#                 if col.custom_y not in (-1, None, ""):
#                     # Specific override in script
#                     s.imageFaceDown[i].top = int(col.custom_y)
#                 else:
#                     # Standard grid position + fan overlap
#                     s.imageFaceDown[i].top = (
#                         s.columnY[pos_idx] + (col.overlap_y * col.weight)
#                     )

#                 # 3. Horizontal Position (X)
#                 if col.custom_x not in (-1, None, ""):
#                     s.imageFaceDown[i].left = int(col.custom_x)
#                 else:
#                     s.imageFaceDown[i].left = (
#                         s.columnX[pos_idx] + (col.overlap_x * col.weight)
#                     )

#                 # 4. Update the card reference (VB .Tag)
#                 # Since col.contents is a list of Card objects, we take the last one's code
#                 if col.contents:
#                     s.imageFaceDown[i].card_code = col.contents[-1].code
                
#                 s.imageFaceDown[i].visible = True
#             else:
#                 # Column is empty, hide the facedown image
#                 s.imageFaceDown[i].visible = False
#                 s.imageFaceDown[i].card_code = ""

def check_allways_facedown_columns(state):
    s = state
    fd_idx = 0  # <-- separate counter for imageFaceDown

    for i, col in enumerate(s.kup):
        if col.allways_facedown == "1":

            # Guard: don't exceed the imageFaceDown array
            if fd_idx >= len(s.imageFaceDown):
                break

            if col.weight > 0:
                # Safe position resolution
                try:
                    pos_idx = int(str(col.position).strip()) if col.position else 0
                except (ValueError, TypeError):
                    pos_idx = 0

                # Vertical position
                if col.custom_y not in (-1, None, ""):
                    s.imageFaceDown[fd_idx].top = int(col.custom_y)
                else:
                    s.imageFaceDown[fd_idx].top = (
                        s.columnY[pos_idx] + (col.overlap_y * col.weight)
                    )

                # Horizontal position
                if col.custom_x not in (-1, None, ""):
                    s.imageFaceDown[fd_idx].left = int(col.custom_x)
                else:
                    s.imageFaceDown[fd_idx].left = (
                        s.columnX[pos_idx] + (col.overlap_x * col.weight)
                    )

                # Card reference
                if col.contents:
                    s.imageFaceDown[fd_idx].card_code = col.contents[-1].code

                s.imageFaceDown[fd_idx].visible = True

            else:
                s.imageFaceDown[fd_idx].visible = False
                s.imageFaceDown[fd_idx].card_code = ""

            fd_idx += 1  # <-- only advance when we've consumed one overlay


def match_specificCol(state, specifCol, col_idx):
    """
    VB: match_specificCol
    Checks if 'col_idx' is allowed based on a string rule (e.g. "any", "1,2,5").
    """
    if not specifCol or specifCol == "-1":
        return False

    if specifCol == "any":
        return True

    try:
        # Check for comma-separated list
        if "," in str(specifCol):
            # Parse list: "1, 2, 4" -> [1, 2, 4]
            allowed = [int(x.strip()) for x in str(specifCol).split(",") if x.strip()]
            return col_idx in allowed
        else:
            # Single value check
            return (int(specifCol) if specifCol else 0) == col_idx

    except Exception as e:
        # If the script has a typo (like '1, 2, abc'), we fail safely
        print(f"Logic Error in specificCol check: {specifCol} for player {state.session_id}")
        return False


def turn_or_shuffle_column(state, col_index, mode="turn"):
    """
    VB Port: turncolumn / shufflecolumn
    Rotates or randomizes the cards within a specific column.
    """
    s = state
    if col_index < 0 or col_index >= len(s.kup):
        return False

    column = s.kup[col_index]

    if column.weight <= 1:
        return True  # Nothing to shuffle or turn

    # --- Snapshot old order ---
    old_cards = list(column.contents)
    n = len(old_cards)

    # --- Compute new order indices ---
    if mode == "turn":
        # Reverse the list of cards
        new_indices = list(reversed(range(n)))
    elif mode == "shuffle":
        # Randomize the list
        new_indices = list(range(n))
        random.shuffle(new_indices)
    else:
        raise ValueError(f"Unknown column transformation mode: {mode}")

    # --- Apply new order ---
    column.contents = [old_cards[i] for i in new_indices]
    
    # --- Sync Duality ---
    from .engine import sync_column_contents
    sync_column_contents(state, column)

    return True


def check_ifduringaction_condition(state, condit_str):
    """
    VB Port: check_ifduringaction_condition
    Evaluates conditional logic inside an action script.
    """
    s = state
    result = False

    # ---------------------------------
    # destination_card=s01,h13...
    # ---------------------------------
    if condit_str.startswith("destination_card="):
        allowed_list = condit_str[len("destination_card="):]
        dest_idx = s.destinationColumn
        
        if dest_idx != -1 and s.kup[dest_idx].contents:
            # Top card of destination column
            dest_card_code = s.kup[dest_idx].contents[-1].code
            if dest_card_code in allowed_list:
                result = True

    # ---------------------------------
    # parameterXX comparisons (e.g., parameter01<5)
    # ---------------------------------
    elif condit_str.startswith("parameter"):
        p_idx = int(condit_str[9:11])
        expr = condit_str[11:]
        current_val = s.parameter[p_idx]

        if expr.startswith("<"):
            result = current_val < int(expr[1:])
        elif expr.startswith(">"):
            result = current_val > int(expr[1:])
        elif expr.startswith("="):
            result = current_val == int(expr[1:])
        elif expr[0].isdigit():
            # Implicit equality: parameter015
            result = current_val == int(expr)

    return result

def match_alternates(state, col_idx, selected_card_code):
    """
    VB Port: match_alternates
    The core rule-checker for moving a card onto a pile.
    Checks Alternate Color, Suit, and Rank rules.
    """
    s = state
    card_can_go = False
    dest_col = s.kup[col_idx]

    # If the column is not empty, we match against the top card
    if dest_col.contents:
        target_card = dest_col.contents[-1].code
        
        # Parse Moving Card (sc) and Target Card (c)
        sc_suit, sc_val = selected_card_code[0], int(selected_card_code[1:])
        c_suit, c_val = target_card[0], int(target_card[1:])

        def is_alternate(suit_a, suit_b):
            """Internal helper for red/black logic."""
            reds = ('h', 'd')
            blacks = ('c', 's')
            return (suit_a in blacks and suit_b in reds) or (suit_a in reds and suit_b in blacks)

        # --- ALTERNATE rules ---
        if dest_col.alternate != "-1":
            # 1 = Ascending, 0 = Descending
            rank_match = False
            if dest_col.alternate == "1":
                rank_match = (sc_val - c_val == 1) or (dest_col.aces_on_kings != "no" and sc_val == 1 and c_val == 13)
            elif dest_col.alternate == "0":
                rank_match = (c_val - sc_val == 1) or (dest_col.aces_on_kings != "no" and sc_val == 13 and c_val == 1)
            elif dest_col.alternate == "any":
                rank_match = True
            
            card_can_go = rank_match and is_alternate(sc_suit, c_suit)

        # --- SUIT rules ---
        if dest_col.suit != "-1":
            same_suit = (sc_suit == c_suit)
            rank_match = False
            if dest_col.suit == "1": # Ascending same suit
                rank_match = (sc_val - c_val == 1) or (dest_col.aces_on_kings != "no" and sc_val == 1 and c_val == 13)
            elif dest_col.suit == "0": # Descending same suit
                rank_match = (c_val - sc_val == 1) or (dest_col.aces_on_kings != "no" and sc_val == 13 and c_val == 1)
            elif dest_col.suit == "10": # Next in rank (either way) same suit
                rank_match = abs(c_val - sc_val) == 1 or (dest_col.aces_on_kings != "no" and sorted((sc_val, c_val)) == [1, 13])
            elif dest_col.suit == "any":
                rank_match = True
            
            card_can_go = rank_match and same_suit

        # --- CARD VALUE rules (Regardless of suit) ---
        if dest_col.card_value != "-1":
            if dest_col.card_value == "1": # Same rank
                card_can_go = (sc_val == c_val)
            elif dest_col.card_value == "2": # Ascending
                card_can_go = (sc_val - c_val == 1) or (dest_col.aces_on_kings != "no" and sc_val == 1 and c_val == 13)
            elif dest_col.card_value == "3": # Descending
                card_can_go = (c_val - sc_val == 1) or (dest_col.aces_on_kings != "no" and sc_val == 13 and c_val == 1)
            elif dest_col.card_value == "23": # Adjacent
                card_can_go = abs(c_val - sc_val) == 1 or (dest_col.aces_on_kings != "no" and sorted((sc_val, c_val)) == [1, 13])

        # --- SUIT OR CARD rules ---
        if dest_col.suit_or_card != "-1":
            if dest_col.suit_or_card == "1":
                card_can_go = (sc_val == c_val or sc_suit == c_suit)
            elif dest_col.suit_or_card == "any":
                card_can_go = True

    # --- ALWAYS ALLOWED FROM COLUMNS ---
    if dest_col.always_allowed_from_columns != "-1":
        from .engine import match_specificCol
        if match_specificCol(state, dest_col.always_allowed_from_columns, s.selectedColumn):
            card_can_go = True

    return card_can_go

def card_faces_up(rule_str, pos_idx):
    """
    Determines if a card at a certain index is visible.
    Example rule: "1,0,1" -> pos 1 is Up, pos 2 is Down.
    """
    if not rule_str: return True
    if len(rule_str) == 1: return rule_str == "1"
    
    parts = rule_str.split(",")
    # pos_idx is 1-based from VB
    if 1 <= pos_idx <= len(parts):
        return parts[pos_idx - 1].strip() == "1"
    return False


def cardId(card_code):
    """
    Converts card code ('c04') to 0..51.
    """
    suit_map = {"c": 0, "d": 1, "h": 2, "s": 3}
    try:
        suit = card_code[0]
        value = int(card_code[1:])
        return suit_map[suit] * 13 + value - 1
    except (KeyError, ValueError, IndexError):
        return None

def card_name(idx):
    """
    Converts 0..51 back to card code ('c01').
    """
    suit_map = {0: "c", 1: "d", 2: "h", 3: "s"}
    suit = suit_map[idx // 13]
    value = (idx % 13) + 1
    return f"{suit}{value:02d}"

def match_crds_suit(state, mode, c_top, c_under):
    """
    Checks suit-based rank matching (Same suit).
    """
    if c_top[0] != c_under[0]:
        return False
    
    val_top = int(c_top[1:])
    val_under = int(c_under[1:])

    # VB Logic: 1 = Ascending, 0 = Descending
    if mode == "1": return (val_top - val_under) == 1
    if mode == "0": return (val_under - val_top) == 1
    if mode == "any": return True
    return False

def match_crds_alternate(state, mode, c_top, c_under):
    """
    Checks alternate-color matching (Red on Black, etc).
    """
    blacks, reds = {"c", "s"}, {"d", "h"}
    top_s, und_s = c_top[0], c_under[0]

    alt = (top_s in blacks and und_s in reds) or (top_s in reds and und_s in blacks)
    if not alt: return False

    val_top, val_under = int(c_top[1:]), int(c_under[1:])
    if mode == "1": return (val_top - val_under) == 1
    if mode == "0": return (val_under - val_top) == 1
    if mode == "any": return True
    return False







# # ------------------------------------------------------
# # functions that use timer (experimental)
# #-------------------------------------------------------
# def gather_cards(self):
#     if not self.animate_enabled:
#         return

#     self.timer_repeats = 3 * 24

#     def step():
#         self._gather_step()

#     self.timers.append(
#         EngineTimer(
#             interval=1/24,
#             repeats=self.timer_repeats,
#             callback=step
#         )
#     )


# def _gather_step(self):
#     self.timer_repeats -= 1

#     if self.timer_repeats <= 0:
#         self._snap_cards_to_deck()
#         return

#     r = random.randint(1, 51)
#     c0 = self.cards[0]
#     c = self.cards[r]

#     factor = self.timer_repeats / 72
#     c.top = c0.top + (c.top - c0.top) * factor
#     c.left = c0.left + (c.left - c0.left) * factor


# def _snap_cards_to_deck(self):
#     c0 = self.cards[0]
#     for c in self.cards[1:]:
#         c.top = c0.top
#         c.left = c0.left

#     self.deck_facedown.top = c0.top
#     self.deck_facedown.left = c0.left
#     self.deck_facedown.visible = True




# ================================================================
# ADDITIONAL ENGINE ROUTINES 
# ================================================================

def apply_facedown_masks(state):
    """
    VB: Logic usually found in prepareColumns or dealCards.
    Sets card.face_up=False for any card that should be hidden at deal time,
    and activates the corresponding imageFaceDown overlay.

    Two independent mechanisms can hide cards:

      1. allways_facedown == "1"
            The entire column is a face-down pile (e.g. the draw deck).
            ALL cards in it are hidden, regardless of cards_face_up.
            The overlay is managed by check_allways_facedown_columns, but
            we still must set card.face_up=False here so the renderer
            doesn't show card faces underneath.

      2. cards_face_up = "0,0,1,1,..."
            Individual cards within a normal column are hidden (e.g. tableau
            piles in Klondike where only the top card is revealed).
            card.face_up is set per-card according to the list.

    BUG THAT WAS HERE:
      Auld Lang Syne's [1deck] has allways_facedown=1 but cards_face_up=1,1,1...
      (all ones). apply_facedown_masks only checked cards_face_up, so it saw
      "all face up" and left every card visible. The deck appeared face-up
      because the column-level allways_facedown flag was never consulted.
    """
    s = state
    s.nextAvailableFaceDown = 0

    # Reset all masks first
    for fd in s.imageFaceDown:
        fd.visible = False

    for col in s.kup:

        # ── MECHANISM 1: allways_facedown column ─────────────────────────
        # The whole column is a face-down pile. Mark every card hidden.
        # check_allways_facedown_columns handles the overlay positioning;
        # we only need to set the card flags here.
        if col.allways_facedown == "1":
            for card in col.contents:
                card.face_up = False
            # Don't also process cards_face_up for this column — skip to next.
            continue

        # ── MECHANISM 2: per-card cards_face_up mask ─────────────────────
        if not col.cards_face_up or col.cards_face_up == "-1":
            continue

        # Parse "0,0,1,1" → [False, False, True, True]
        rules = [r.strip() == "1" for r in str(col.cards_face_up).split(",")]

        for i, card in enumerate(col.contents):
            # If the rule list is shorter than the column, remaining cards
            # default to face-up (safe assumption).
            should_be_face_up = rules[i] if i < len(rules) else True

            if not should_be_face_up:
                card.face_up = False

                # Activate a mask overlay at this card's position
                if s.nextAvailableFaceDown < len(s.imageFaceDown):
                    mask = s.imageFaceDown[s.nextAvailableFaceDown]
                    mask.visible = True
                    mask.card_code = card.code
                    mask.left = col.x + (i * col.overlap_x)
                    mask.top  = col.y + (i * col.overlap_y)
                    s.nextAvailableFaceDown += 1


def sync_visual_actors(state):
    """
    The Master Wire. Call this once at the end of ANY engine action.
    It ensures masks (imageFaceDown) match the Card.face_up state.
    """
    s = state
    s.nextAvailableFaceDown = 0
    
    # Reset all masks
    for fd in s.imageFaceDown:
        fd.visible = False

    for col in s.kup:
        for i, card in enumerate(col.contents):
            # If the card is face down, we need a mask
            if not card.face_up:
                if s.nextAvailableFaceDown < len(s.imageFaceDown):
                    mask = s.imageFaceDown[s.nextAvailableFaceDown]
                    mask.visible = True
                    mask.card_code = card.code
                    
                    # Position mask exactly on top of the card
                    mask.left = col.x + (i * col.overlap_x)
                    mask.top = col.y + (i * col.overlap_y)
                    
                    s.nextAvailableFaceDown += 1

