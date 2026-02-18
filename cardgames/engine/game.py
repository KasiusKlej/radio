# game.py 
from flask import session
import random
import uuid
from pathlib import Path

# --- Internal Engine Tools ---
from .engine import sync_column_contents, check_allways_facedown_columns, getGameInfo, column_click, card_DblClick
# --- Data Models & Constants ---
from .model import GameState, Card, Column, ColumnSlot, FaceDownOverlay, SelectionOverlay, LANG_DIR, orig_card_x_size, orig_card_y_size, gap_x, gap_y
# --- Parsers & Shufflers ---
from .parser import load_games2, language_parser, load_game_rules, load_game_names, parse_all_games, load_gamesVB, read_gamenames_from_language_files
from .shuffler_girl import shuffleDeck
from .card_dealer import dealCards



# movable part
def load_default_language():
    try:
        return language_parser(LANG_DIR, "eng")
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

CURRENT_LANGUAGE = load_default_language()      # this is out of phase, should be phase 0




# Game manager - a way to store these objects in the server memory, separated by a unique "Session ID."
active_games = {} # Key: SessionID, Value: GameState object
def get_my_game():
    session_id = session.get('user_sid')
    if session_id not in active_games:
        # Create a new instance specifically for this user
        active_games[session_id] = GameState(game_id="default", player_id=session_id)
    return active_games[session_id]

def to_px(value):
    """
    Converts a game-data overlap/position value to pixels.

    The game file is a mixed bag:
      - Large values (200, 350, 1500...) are VB Twips → divide by 15
      - Small values (0, 1, 2 ... up to ~15) are already pixels → keep as-is

    Threshold history:
      > 24  — original threshold; let values like 20 and 50 through as raw
               pixels, causing wildly spread cards in games like Auld Lang Syne
               whose reserve columns use overlap_x=20, overlap_y=50 (twips).
      > 15  — new threshold; 15 is exactly 1 twip = 1 pixel, so anything
               above 15 is unambiguously a twip value and must be divided.
               Genuine sub-pixel or 1-pixel overlaps (0..15) are kept intact.
    """
    try:
        v_str = str(value).strip()
        if not v_str or v_str == "-1":
            return -1

        val = int(v_str)
        if val == 0:
            return 0

        # Use absolute value for threshold check so negative spreads
        # (e.g. overlap_x=-200 for rightward fans) are handled correctly.
        if abs(val) > 15:
            return int(val / 15)

        # Small value — already in pixels, return unchanged.
        return val

    except (ValueError, TypeError):
        return 0
        

# -------------------------------------------------
# PHASE 0: Language Handling (Session-Safe)
# -------------------------------------------------

def get_language_dict(lang_code="eng"):
    """
    Retrieves language strings. No longer uses a global variable.
    """
    try:
        return language_parser(LANG_DIR, lang_code)
    except Exception as e:
        print(f"Language load failed for {lang_code}, falling back to English: {e}")
        return {
            "lang": {"app": "Card Games", "youwon": "You Won!", "youlost": "You Lost!"},
            "menu": {}, "dialog": {"ok": "OK", "cancel": "Cancel"}
        }

# -------------------------------------------------
# CardGame Controller
# -------------------------------------------------

class CardGame:
    """
    The Engine Controller. 
    It 'owns' a GameState and provides methods to manipulate it.
    """
    def __init__(self, game_id, session_id=None, from_snapshot=None):
        # 1. Initialize the State (The container for all Brazilian/Korean data)
        # We ensure the session ID is linked immediately.
        sid = session_id or session.get('user_sid')
        self.state = GameState(game_id, sid)
        
        print(f"DEBUG: Initializing game controller for ID: {game_id}")

        if from_snapshot:
            # Reconstruct from browser save
            self._load_from_dict(from_snapshot)
        else:
            # This is the ONLY entry point for a fresh game.
            # We call the faithful VB port directly.
            self._start_new_game(game_id)
   

    def _load_game_definition(self, game_id):
        """
        Equivalent to VB Phase 2. 
        Loads specific lines for the chosen game into self.state.
        """
        filepath = LANG_DIR / "CardGames-utf8.txt"
        # We reuse the logic we wrote earlier to find the N-th game
        lines, actions = getGameInfo(game_id, filepath)
        
        self.state.LIST_GAME_LINES = lines
        if lines:
            # Usually the name is on the second line of the block
            self.state.GAME_NAME = lines[1].strip()
            self.state.name = self.state.GAME_NAME

    def _vb_init_globals(self):
        """
        Sets all engine flags inside self.state.
        Replaces 'global' variables with instance variables.
        """
        s = self.state
        s.youWon = False
        s.selectedCard = -1
        s.selectedColumn = -1
        s.destinationColumn = -1
        s.usermode = 0
        s.actionMode = False          #patched
        s.nextAvailableFaceDown = 0
        s.parameter = [0] * 21
        s.autoplay_enabled = False

    
    def prepareRequisites(self):
        """
        VB: prepareRequisites. 
        Stages the visual 'actors' (slots and overlays) based on column data.
        """
        s = self.state
        s.ShapeColumns = []
        s.imageFaceDown = []
        s.ShapeSelektor.visible = False
        s.nextAvailableFaceDown = 0 # Reset counter

        for i, col in enumerate(s.kup):
            # 1. Skip columns that don't have a valid position
            if not col.position:
                continue

            slot = ColumnSlot(column_index=i)
            
            # 2. Geometry Resolution (The 'Big Move' fix)
            try:
                pos = int(col.position)
            except ValueError:
                pos = 0

            # Use the state's calculated X/Y grid or the custom override
            slot.left = col.custom_x if col.custom_x != -1 else s.columnX[pos]
            slot.top = col.custom_y if col.custom_y != -1 else s.columnY[pos]
            slot.visible = True
            # THE COSTUME CHECK
            # Transfer settings from the Column (Data) to the Slot (Actor)
            slot.backstyle = col.backstyle
            slot.backcolor = col.backcolor
        
            s.ShapeColumns.append(slot)

            # 3. Handle Face-Down Overlays (Spelling check: allways_facedown)
            if col.allways_facedown == "1":
                fd = FaceDownOverlay()
                fd.visible = True
                fd.left = slot.left
                fd.top = slot.top
                # Link it to the card logic
                fd.card_code = col.contents[-1].code if col.contents else ""
                
                s.imageFaceDown.append(fd)
                s.nextAvailableFaceDown += 1

                


    # ------------------------------------------------------
    # Animation Ticks (Server-side simulation)
    # ------------------------------------------------------
    
    def gather_cards(self):
        """Initializes the gather sequence."""
        if not self.state.animate_enabled:
            self._snap_cards_to_deck()
            return

        # 3 seconds at 24 frames per second
        self.state.timer_repeats = 3 * 24

        # Instead of self.timers, we use our state's timer list
        from .model import EngineTimer
        self.state.timers.append(
            EngineTimer(
                interval=1/24,
                repeats=self.state.timer_repeats,
                callback=self._gather_step # Passing the method as a callback
            )
        )

    def _gather_step(self):
        """
        VB: TimerAnimate_Timer() logic.
        Calculates one frame of cards flying toward the deck.
        """
        s = self.state
        s.timer_repeats -= 1

        if s.timer_repeats <= 0:
            self._snap_cards_to_deck()
            return

        # Move one random card per tick (Faithful to your VB code)
        import random
        r = random.randint(0, 51)
        
        # We need access to the actual Card objects to update their coordinates
        # assuming all cards are stored in a master list for animation
        # (This would be your list of 52 card objects)
        all_cards = [] 
        for col in s.kup: all_cards.extend(col.contents)

        if len(all_cards) > r:
            card = all_cards[r]
            target_x = s.columnX[0] # Usually position 0 is the deck
            target_y = s.columnY[0]

            factor = s.timer_repeats / 72
            # The math: CurrentPos = Target + (Start - Target) * Factor
            # This makes the card "slide" into the deck
            # Note: Card coordinates must be in the Card object or GameState
            # We will assume they are in card.x and card.y
            if hasattr(card, 'x'):
                card.x = target_x + (card.x - target_x) * factor
                card.y = target_y + (card.y - target_y) * factor


    def _snap_cards_to_deck(self):
        """Finalizes the animation by snapping everything to (0,0)."""
        s = self.state
        target_x = s.columnX[0]
        target_y = s.columnY[0]

        for col in s.kup:
            for card in col.contents:
                card.x = target_x
                card.y = target_y

        # Sync the facedown overlay (The deck back)
        if len(s.imageFaceDown) > 0:
            s.imageFaceDown[0].left = target_x
            s.imageFaceDown[0].top = target_y
            s.imageFaceDown[0].visible = True


    def do_action(self, act: str) -> bool:
        """
        VB Port: do_action
        The interpreter for the game's script language. 
        Operates exclusively on self.state.
        """
        s = self.state
        success = False
        
        # Import engine tools needed for these actions
        from .engine import (
            turn_or_shuffle_column, move_condition, 
            param_count_empty, param_cards_rowed, 
            param_count_weight, minmax, 
            check_ifduringaction_condition
        )

        # ----------------------------
        # movecolumn=X-Y (Move whole column)
        # ----------------------------
        if act.startswith("movecolumn="):
            ac_body = act[len("movecolumn="):]
            csource, cdest = map(int, ac_body.split("-"))

            s.actionMode = True
            s.simulateClickMode = True

            if s.kup[csource].weight > 0:
                # We call the move_column method we ported earlier
                success = self.move_column(csource, cdest, s.kup[csource].weight)

            s.actionMode = False
            s.simulateClickMode = False

        # ----------------------------
        # turncolumn=X / shufflecolumn=X
        # ----------------------------
        elif act.startswith("turncolumn="):
            col_idx = int(act[len("turncolumn="):])
            success = turn_or_shuffle_column(s, col_idx, mode="turn")

        elif act.startswith("shufflecolumn="):
            col_idx = int(act[len("shufflecolumn="):])
            success = turn_or_shuffle_column(s, col_idx, mode="shuffle")

        # ----------------------------
        # movepile=N,X-Y (Move top N cards)
        # ----------------------------
        elif act.startswith("movepile="):
            ac_body = act[len("movepile="):]
            n_str, rest = ac_body.split(",", 1)
            n = int(n_str)
            csource, cdest = map(int, rest.split("-"))

            s.actionMode = True
            s.simulateClickMode = True

            actual_n = min(n, s.kup[csource].weight)
            if actual_n > 0:
                success = self.move_column(csource, cdest, actual_n)

            s.actionMode = False
            s.simulateClickMode = False

        # ----------------------------
        # trymovepile=MAX,SRC-DEST
        # ----------------------------
        elif act.startswith("trymovepile="):
            ac_body = act[len("trymovepile="):]
            max_part, col_range = ac_body.split(",", 1)
            
            # Resolve if max is a raw number or a parameter
            if max_part.startswith("parameter"):
                p_idx = int(max_part[9:11])
                max_cards = s.parameter[p_idx]
            else:
                max_cards = int(max_part)

            src_str, dest_str = col_range.split("-")
            csource = s.selectedColumn if src_str == "selected" else int(src_str)
            cdest = int(dest_str)

            if s.kup[csource].weight > 0:
                how_many = 0
                cards = list(s.kup[csource].contents)

                # Look for a sequence of cards that can move together
                for i in range(min(len(cards), max_cards)):
                    card = cards[-(i + 1)]
                    # Logic: Is the i-th card allowed to land on cdest?
                    if move_condition(s, card.code, csource, cdest) and card.face_up:
                        how_many = i + 1
                    else:
                        # In many card games, if the 3rd card can't move, 
                        # the 4th card behind it certainly can't.
                        break

                if how_many > 0:
                    success = self.do_action(f"movepile={how_many},{csource}-{cdest}")

        # ----------------------------
        # parameter management (The Game's Variables)
        # ----------------------------
        elif act.startswith("parameter") or act.startswith("setparameter="):
            # Clean the string
            clean_act = act[len("setparameter="):] if act.startswith("setparameter=") else act
            
            p_idx = int(clean_act[9:11])
            expr = clean_act[12:]
            success = True

            if expr.isdigit():
                s.parameter[p_idx] = int(expr)
            elif expr.startswith("countempty"):
                s.parameter[p_idx] = param_count_empty(s, expr[10:])
            elif expr.startswith("cardsrowed("):
                col = s.selectedColumn if "selected" in expr else int(expr[11:-1])
                s.parameter[p_idx] = param_cards_rowed(s, col)
            elif expr.startswith("min(") or expr.startswith("max("):
                fn = expr[:3]
                val_a, val_b = expr[4:-1].split(",")
                s.parameter[p_idx] = minmax(s, fn, val_a, val_b)
            elif expr.startswith("source_column"):
                s.parameter[p_idx] = s.selectedColumn
            elif expr.startswith("weight_of"):
                s.parameter[p_idx] = param_count_weight(s, expr[9:])
            else:
                success = False

        # ----------------------------
        # Logic: increase(parameterX)
        # ----------------------------
        elif act.startswith("increase(parameter"):
            p_idx = int(act[18:-1])
            s.parameter[p_idx] += 1
            success = True

        # ----------------------------
        # Conditionals: ifduringaction(COND, ACTION)
        # ----------------------------
        elif act.startswith("ifduringaction("):
            content = act[15:]
            cond_str, subact = content.split(")", 1)
            subact = subact.lstrip(",")

            if check_ifduringaction_condition(s, cond_str):
                success = self.do_action(subact)

        # ----------------------------
        # Recursion: whole action block [ActionName]
        # ----------------------------
        elif act.startswith("["):
            self.do_whole_action(act)
            success = True

        # ----------------------------
        # post-action maintenance
        # ----------------------------
        if success:
            from .engine import check_allways_facedown_columns
            check_allways_facedown_columns(s)

        return success


    def do_whole_action(self, action_name: str) -> bool:
        """
        VB Port: do_whole_action
        Executes a sequence of commands labeled in the script as [action_name].
        """
        s = self.state
        success = False

        if action_name.startswith("["):
            # We look into the player's private list of script lines
            lines = s.LIST_GAME_LINES
            i = 0
            
            # 1. Find the header
            while i < len(lines) and lines[i].strip() != action_name:
                i += 1
            
            if i >= len(lines):
                return False # Action not found in this game's definition

            i += 1 # Move past the header
            
            # 2. Execute lines until we hit another [header] or the end
            while i < len(lines):
                line = lines[i].strip()
                if not line or line.startswith("#"): 
                    i += 1
                    continue
                if line.startswith("["): 
                    break
                
                # Execute individual DSL command
                success = self.do_action(line)
                i += 1
        else:
            # Standalone action (e.g., movepile=1,0-1)
            success = self.do_action(action_name)

        return success

    def _parse_cols_arg(self, cols_input):
        """Helper: Parses '(1,2,3)' or '5' into a list of integers."""
        if not cols_input: return []
        s = str(cols_input).replace("(", "").replace(")", "").strip()
        if "," in s:
            return [int(c.strip()) for c in s.split(",") if c.strip().isdigit()]
        return [int(s)] if s.isdigit() else []

    def param_count_empty(self, cols_input):
        """Action: countempty(cols)"""
        count = 0
        for c_idx in self._parse_cols_arg(cols_input):
            if 0 <= c_idx < len(self.state.kup):
                if self.state.kup[c_idx].weight == 0:
                    count += 1
        return count

    def param_count_weight(self, cols_input):
        """Action: weight_of(cols)"""
        count = 0
        for c_idx in self._parse_cols_arg(cols_input):
            if 0 <= c_idx < len(self.state.kup):
                count += self.state.kup[c_idx].weight
        return count

    def param_cards_rowed(self, col_idx):
        """
        Action: cardsrowed(col)
        Checks how many cards at the top of a column follow the sequence rules.
        """
        s = self.state
        if not (0 <= col_idx < len(s.kup)): return 0
        
        column = s.kup[col_idx]
        if column.weight <= 1: return column.weight

        # Check from top down
        cards = list(column.contents)
        cards.reverse() # Top is now at index 0
        
        row_count = 1
        for i in range(len(cards) - 1):
            # Check if card i can be placed on card i+1 (the card under it)
            # using the column's specific suit/alternate rules
            if self.match_alternates(col_idx, cards[i].code):
                row_count += 1
            else:
                break
        return row_count
    
    def try_every_turn_actions(self):
        """
        VB Port: try_every_turn_actions
        The 'Autoplay' engine. It loops as long as it finds valid automatic moves.
        """
        s = self.state
        # We limit loops to prevent potential infinite script loops
        max_loops = 50 
        
        while max_loops > 0:
            s.clickModeSuceededSoTryAgain = False
            lines = s.LIST_GAME_LINES # Our script block

            for line in lines:
                line = line.strip()
                if line.startswith("every_turn=") and s.autoplay_enabled:
                    action_cmd = line[11:]

                    if action_cmd.startswith("["):
                        self.do_whole_action(action_cmd)
                    elif action_cmd.startswith("parameter"):
                        self.do_action(action_cmd)
                    else:
                        # Standard x-y move (e.g., 0-1)
                        try:
                            src_idx, dst_idx = map(int, action_cmd.split("-"))
                            source_col = s.kup[src_idx]
                            
                            if source_col.contents:
                                top_card = source_col.contents[-1]
                                
                                # Simulate clicks to move the card
                                s.simulateClickMode = True
                                self.column_click(src_idx, top_card.code)
                                self.column_click(dst_idx, top_card.code)
                                s.simulateClickMode = False
                        except Exception:
                            continue
                
                if line == "[FINISH]": break
            
            if not s.clickModeSuceededSoTryAgain:
                break
            max_loops -= 1

        self.try_if_actions()

    def try_if_actions(self):
        """
        VB Port: try_if_actions
        Evaluates 'if(condition)then[Action]' blocks.
        """
        s = self.state
        for line in s.LIST_GAME_LINES:
            line = line.strip()
            if not line.startswith("if("):
                if line == "[FINISH]": break
                continue

            # Parsing: if(empty_columns=1,2,3)then[MoveToFound]
            try:
                cond_part = line[line.find("(")+1 : line.find(")")]
                then_part = line[line.find(")then")+5 :]
                
                met = False
                if cond_part.startswith("empty_columns="):
                    met = (self.param_count_empty(cond_part[14:]) == 0) # Wait, logic check: VB usually meant 'all these are empty'
                    # If you want 'Are ALL these empty?', use count_empty == len(cols)
                    
                elif cond_part.startswith("parameter"):
                    p_idx = int(cond_part[9:11])
                    expr = cond_part[cond_part.find("=")+1:]
                    val = s.parameter[p_idx]
                    if expr.startswith(">"): met = val >= int(expr[1:])
                    elif expr.startswith("<"): met = val <= int(expr[1:])
                    else: met = val == int(expr)

                if met:
                    self.do_whole_action(then_part)
            except:
                continue

    def check_end_of_game(self):
        """
        VB Port: check_end_of_game
        Checks [VICTORY] and [DEFEAT] conditions.
        """
        s = self.state
        if s.youWon: return # Only win once per game

        lines = s.LIST_GAME_LINES
        
        # Helper to find a block and check its 'empty_columns' rule
        def check_block(header):
            i = 0
            while i < len(lines) and lines[i].strip() != header:
                i += 1
            if i < len(lines) - 1:
                cond_line = lines[i+1].strip()
                if cond_line.startswith("empty_columns="):
                    # If the specified columns are all empty, condition is met
                    col_str = cond_line[14:]
                    cols = [int(c.strip()) for c in col_str.split(",")]
                    return all(s.kup[c].weight == 0 for c in cols)
            return False

        # Check Victory
        if check_block("[VICTORY]"):
            s.youWon = True
            s.game_message = s.lang_youwon
            print(f"Victory detected for player {s.session_id}")
            # statistics(s.name, "win") logic here

        # Check Defeat
        elif check_block("[DEFEAT]"):
            s.youWon = True # Mark as game over
            s.game_message = "You lost!"
            print(f"Defeat detected for player {s.session_id}")














    # -------------------------------------------------
    # State Serialization (to/from Frontend)
    # -------------------------------------------------

    def to_dict(self):
        """Calls the GameState's to_dict to package data for JS."""
        # Ensure cards are synced with strings before sending
        for col in self.state.kup:
            sync_column_contents(self.state, col)
        return self.state.to_dict()
   

    @staticmethod
    def from_dict(data, session_id):
        """
        RECONSTRUCTION: Rebuilds the engine from a JSON snapshot.
        """
        # 1. Create a skeleton game
        g = CardGame(data["game_id"], session_id=session_id)
        s = g.state
        
        s.GAME_NAME = data.get("name", "")
        s.autoplay_enabled = data.get("autoplay_enabled", False)
        s.selectedCard = data.get("selected_card_code", -1)
        s.usermode = data.get("usermode", 0)
        s.actionMode = data.get("actionMode", False)
        s.rules_of_currently_played_game = data.get("rules", "")

        # 2. Rebuild Columns and Cards
        s.kup = []
        for col_data in data.get("kup", []):
            col = Column(index=col_data["index"])
            col.column_name = col_data["name"]
            col.x, col.y = col_data["x"], col_data["y"]
            col.overlap_x = col_data["overlap_x"]
            col.overlap_y = col_data["overlap_y"]
            col.allways_facedown = col_data.get("allways_facedown", "-1")
            
            for c_data in col_data.get("cards", []):
                card = Card(c_data["code"], face_up=c_data["face_up"])
                col.contents.append(card)
            
            col.weight = len(col.contents)
            s.kup.append(col)
            
        return g


    # -------------------------------------------------
    # Engine Actions
    # -------------------------------------------------

    def move_card(self, from_col_idx, to_col_idx, card_code):
        """
        The main entry point for a player's 'wish'.
        Checks conditions and executes movement.
        """
        # Example of calling an engine function with the state
        # if move_condition(self.state, card_code, from_col_idx, to_col_idx):
        #     execute_move(self.state, ...)
        #     return True
        return False






    # -------------------------------------------------
    # Load & semantics
    # -------------------------------------------------

    def load_game(self):
        """
        Extracts the specific game definition from the master list.
        Uses self.state to store results.
        """
        # Get local reference to the player's specific state data
        lines = self.state.LIST_GAME_LINES
        target_id = str(self.state.zap_st_igre) 
        
        i = 0
        current_game_index = 0
        found = False
        game_lines = []

        while i < len(lines):
            line = lines[i].strip()

            if line == "[GAMENAME]":
                current_game_index += 1  # Increment game counter (1, 2, 3...)

                if str(current_game_index) == target_id:
                    # We found the N-th game!
                    name = lines[i + 1].strip()
                    self.state.GAME_NAME = name
                    self.state.name = name
                    found = True

                    # --- START CAPTURING THE GAME BLOCK ---
                    game_lines.append(lines[i])
                    game_lines.append(lines[i+1])
                    i += 2

                    while i < len(lines):
                        if lines[i].strip() == "[GAMENAME]":
                            break
                        game_lines.append(lines[i])
                        i += 1
                    break
            i += 1

        if not found:
            raise ValueError(f"Numeric game index {target_id} not found in file.")

        # Replace player's LIST_GAME_LINES with only their game's definition
        self.state.LIST_GAME_LINES = game_lines


    # load game rules
    def _load_rules_to_state(self):
        """
        Reads the rules from the language file and stores them 
        directly in the player's state.
        """
        from .parser import load_game_rules
        from .model import LANG_DIR
        
        # Get session language
        lang = self.state.CURRENT_LANGUAGE 
        
        # We need the language dictionary for the 'logos'
        lang_data = get_language_dict(lang)
        lang_vars = lang_data.get('lang', {})

        rules_text = load_game_rules(
            gamename=self.state.GAME_NAME,
            language=lang,
            lang_dir=LANG_DIR,
            list_game=self.state.LIST_GAME_LINES,
            lang_vars=lang_vars
        )
        
        self.state.rules_of_currently_played_game = rules_text
        

    def _start_new_game(self, game_id):
        """
        VB Form_Load equivalent.
        This is the MASTER function where the game logic river flows.
        """
        s = self.state 
        
        # --- STEP 1: SETUP MEMORY & SCRIPT (Old Phase 1 & 2) ---
        s.zap_st_igre = game_id
        s.CURRENT_LANGUAGE = session.get("lang", "eng")
        
        # Load the specific text lines for this game into s.LIST_GAME_LINES
        self._load_game_definition(game_id) 
        
        # --- STEP 2: INITIALIZE GLOBALS (VB-style) ---
        self._vb_init_globals() # Sets s.youWon = False, s.usermode = 0, etc.
        s.cardJustMoved = False
        s.name = s.GAME_NAME # Map the loaded name
        self._load_rules_to_state() #game rules

        # --- STEP 3: GEOMETRY & PARSING ---
        from .engine import calcColumnXY, check_allways_facedown_columns, sync_column_contents
        
        # Calculate X/Y grid based on the constants
        calcColumnXY(s)
        
        print(f"DEBUG: prepare columns")
        # Parse the [COLUMNS] section from the script into s.kup
        self._prepare_columns() 
                
        # Setup visual actors (overlays, selectors)
        self.prepareRequisites()
        
        # --- STEP 4: CARDS IN MOTION ---
        # 1. Create the physical deck objects
        self._create_deck() 
        
        # 2. Shuffle
        shuffleDeck(s)

        # 3. Deal
        dealCards(s)

        # --- THE FIX: The Quick Hand Trickery ---
        from .engine import apply_facedown_masks
        apply_facedown_masks(s)

        # Enforce duality (Cards <-> Strings)
        for col in s.kup:
            sync_column_contents(s, col)
      
        # Set facedown positions
        check_allways_facedown_columns(s)

        # Optional: Run start-of-game automation
        # self.do_whole_action("[autostart]")
















    




    # # -------------------------------------------------
    # # Moves (under reconstruction)
    # # -------------------------------------------------
    # def move_card(self, from_col, to_col, card_code):
    #     if from_col not in self.columns or to_col not in self.columns:
    #         return False

    #     src = self.columns[from_col]["cards"]
    #     for i, card in enumerate(src):
    #         if card["code"] == card_code:
    #             self.columns[to_col]["cards"].append(src.pop(i))
    #             return True
    #     return False


    



   

    def _init_geometry_constants(self):
        """
        Single source of truth for all geometry.
        These are stored in the engine instance, but defaults come from self.state.
        """
        # --- Card dimensions (Standard) ---
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

    # -------------------------------------------------
    # Slot geometry
    # -------------------------------------------------
    
    def _apply_slot_geometry(self):
        """
        VB-style slot geometry.
        Resolves base x/y from shared constants and applies custom overrides.
        """
        for idx, col in enumerate(self.state.kup):
            if col.position in ("", None):
                continue

            try:
                # VB position index (e.g. "01" -> 1)
                pos = int(col.position)
            except ValueError:
                continue

            if pos < 0 or pos >= len(self.state.columnX):
                continue

            # 1. Start with base geometry (Global columnX / columnY)
            col.custom_x = self.state.columnX[pos]
            col.custom_y = self.state.columnY[pos]

            # 2. Check for manual overrides in the game script (VB: -1 means ignore)
            # Note: We use the values parsed during _prepare_columns
            # col.x/y are the final resolved coordinates for the renderer
            col.x = col.custom_x
            col.y = col.custom_y

    
    def _normalize_column_overlaps(self):
        """
        Improved Normalizer: Prevents 'Leaking Axis' bugs.
        """
        s = self.state
        for col in s.kup:
            # Case A: Column specified NOTHING (-1, -1)
            # Use the game-wide defaults.
            if col.overlap_x == -1 and col.overlap_y == -1:
                col.overlap_x = s.default_overlap_x
                col.overlap_y = s.default_overlap_y

            # Case B: Column specified horizontal ONLY
            # Assume vertical is 0.
            elif col.overlap_x != -1 and col.overlap_y == -1:
                col.overlap_y = 0

            # Case C: Column specified vertical ONLY
            # Assume horizontal is 0.
            elif col.overlap_y != -1 and col.overlap_x == -1:
                col.overlap_x = 0
            
            # Case D: Both already set (e.g. by behaviour or Stage 2)
            # Do nothing.





    # -------------------------------------------------
    # Deck & dealing
    # -------------------------------------------------

    def _create_deck(self):
        suits = ['c', 'd', 'h', 's']
        self.state.LIST_DECK = []
        for s in suits:
            for v in range(1, 14):
                # Format to match your filenames: e.g. "s13"
                code = f"{s}{v:02d}" 
                self.state.LIST_DECK.append(code)

    # -------------------------------------------------
    # Moves (Web Context)
    # -------------------------------------------------
    
    def move_card(self, from_col_idx, to_col_idx, card_code):
        """
        Web entry point for moving a card. 
        Works on self.state.kup indexed by current player.
        """
        s = self.state
        try:
            from_idx = int(from_col_idx)
            to_idx = int(to_col_idx)
            src_col = s.kup[from_idx]
            dst_col = s.kup[to_idx]
        except (ValueError, IndexError):
            return False

        # Find the card in the source column
        for i, card in enumerate(src_col.contents):
            if card.code == card_code:
                # Move the card object
                moving_card = src_col.contents.pop(i)
                dst_col.contents.append(moving_card)
                
                # Update weights and strings (Duality check)
                from .engine import sync_column_contents
                sync_column_contents(src_col)
                sync_column_contents(dst_col)
                return True
        return False

    # -------------------------------------------------
    # Column Preparation (The Script Parser)
    # -------------------------------------------------

    


    def _prepare_columns(self):
        """
        VB: prepareColumns
        Full 3-stage parser: Defaults -> Layout -> Behaviour
        
        Now fully synchronized with Column.__init__ to handle all attributes.
        """
        s = self.state
        lines = s.LIST_GAME_LINES
        i = 0

        # ═══════════════════════════════════════════════════════════════════════
        # STAGE 1: [COLUMNS DEFAULTS]
        # ═══════════════════════════════════════════════════════════════════════
        while i < len(lines):
            line = lines[i].strip()
            if line == "[COLUMNS DEFAULTS]":
                i += 1
                while i < len(lines) and lines[i].strip() != "[END COLUMNS DEFAULTS]":
                    l = lines[i].strip()
                    
                    # Note: Check 'l' not 'line' (bug fix)
                    if l.startswith("overlap_x="):
                        s.default_overlap_x = to_px(l.split("=")[1])
                    elif l.startswith("overlap_y="):
                        s.default_overlap_y = to_px(l.split("=")[1])
                    elif l.startswith("zoom="):
                        try:
                            s.zoom = float(l.split("=")[1])
                        except ValueError:
                            s.zoom = 1.0
                    
                    i += 1
            if line == "[COLUMNS]": 
                break
            i += 1

        # ═══════════════════════════════════════════════════════════════════════
        # STAGE 2: [COLUMNS] — Create Column objects
        # ═══════════════════════════════════════════════════════════════════════
        i = 0
        while i < len(lines) and lines[i].strip() != "[COLUMNS]": 
            i += 1
        i += 1  # Skip past [COLUMNS] header
        
        c_idx = 0
        s.kup = [] 
        
        while i < len(lines):
            line = lines[i].strip()
            if line == "[END COLUMNS]": 
                break
            if not line or line.startswith("#"): 
                i += 1
                continue
            
            # Create new Column with all defaults from __init__
            col = Column(index=c_idx)
            
            # Parse the compact format: "name, position, num_cards, shuffle_flag"
            parts = [p.strip() for p in line.split(",")]
            col.column_name = parts[0]
            col.position = parts[1][:2] if len(parts) > 1 else ""
            col.num_cards = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 0
            col.shufle_any_cards = parts[-1] if len(parts) > 3 else "0"
            
            # Keep overlap as -1 (unset) so Stage 3 can override or normalize can apply defaults
            # col.overlap_x and col.overlap_y already = -1 from __init__
            
            s.kup.append(col)
            c_idx += 1
            i += 1

        # ═══════════════════════════════════════════════════════════════════════
        # STAGE 3: [COLUMNS BEHAVIOUR] — Apply per-column settings
        # ═══════════════════════════════════════════════════════════════════════
        i = 0
        current_col = None
        
        while i < len(lines):
            line = lines[i].strip()
            if line == "[COLUMNS BEHAVIOUR]":
                i += 1
                while i < len(lines):
                    line = lines[i].strip()
                    if line == "[END COLUMNS BEHAVIOUR]":
                        break
                    
                    # Column header: [column_name]
                    if line.startswith("[") and line.endswith("]"):
                        col_name = line[1:-1]
                        current_col = next((c for c in s.kup if c.column_name == col_name), None)
                        if not current_col:
                            print(f"Warning: Column '{col_name}' not found in kup")
                    
                    # Key=Value pairs
                    elif current_col and "=" in line:
                        key, val = [p.strip() for p in line.split("=", 1)]
                        
                        # ───────────────────────────────────────────────────────
                        # GEOMETRY & POSITIONING
                        # ───────────────────────────────────────────────────────
                        if key == "overlap_x":
                            if val == "default":
                                current_col.overlap_x = s.default_overlap_x
                            else:
                                current_col.overlap_x = to_px(val)
                        
                        elif key == "overlap_y":
                            if val == "default":
                                current_col.overlap_y = s.default_overlap_y
                            else:
                                current_col.overlap_y = to_px(val)
                        
                        elif key == "custom_x":
                            current_col.custom_x = to_px(val)
                        
                        elif key == "custom_y":
                            current_col.custom_y = to_px(val)
                        
                        # ───────────────────────────────────────────────────────
                        # PLAYER INTERACTION PERMISSIONS
                        # ───────────────────────────────────────────────────────
                        elif key == "player_can_take_card":
                            current_col.player_can_take_card = val
                        
                        elif key == "player_can_put_card":
                            current_col.player_can_put_card = val
                        
                        elif key == "player_can_put_card_if_empty":
                            current_col.player_can_put_card_if_empty = val
                        
                        # ───────────────────────────────────────────────────────
                        # VISUAL SETTINGS
                        # ───────────────────────────────────────────────────────
                        elif key == "backstyle":
                            current_col.backstyle = val  # Store as string, will convert in prepareRequisites
                        
                        elif key == "backcolor":
                            current_col.backcolor = val  # Store as string, will convert in prepareRequisites
                        
                        elif key == "allways_facedown":
                            current_col.allways_facedown = val
                        
                        elif key == "cards_face_up":
                            current_col.cards_face_up = val
                        
                        elif key == "use_facedown":
                            current_col.use_facedown = val
                        
                        # ───────────────────────────────────────────────────────
                        # CARD DEALING
                        # ───────────────────────────────────────────────────────
                        elif key == "contents_at_start":
                            current_col.contents_at_start = val
                        
                        # ───────────────────────────────────────────────────────
                        # GAME RULES (card matching logic)
                        # ───────────────────────────────────────────────────────
                        elif key == "suit":
                            current_col.suit = val
                        
                        elif key == "card_value":
                            current_col.card_value = val
                        
                        elif key == "alternate":
                            current_col.alternate = val
                        
                        elif key == "suit_or_card":
                            current_col.suit_or_card = val
                        
                        elif key == "max_cards":
                            current_col.max_cards = int(val) if val.isdigit() else 0
                        
                        elif key == "aces_on_kings":
                            current_col.aces_on_kings = val
                        
                        # ───────────────────────────────────────────────────────
                        # PLAYER ACTIONS
                        # ───────────────────────────────────────────────────────
                        elif key == "dblclick_moves_to":
                            current_col.dblclick_moves_to = val
                        
                        elif key == "after_move_action":
                            current_col.after_move_action = val
                        
                        elif key == "after_playermove_action":
                            current_col.after_playermove_action = val
                        
                        elif key == "attempted_move_action":
                            current_col.attempted_move_action = val
                        
                        elif key == "attempted_playermove_action":
                            current_col.attempted_playermove_action = val
                        
                        # ───────────────────────────────────────────────────────
                        # ADDITIONAL RULES (if any new ones appear in game data)
                        # ───────────────────────────────────────────────────────
                        elif key == "always_allowed_from_columns":
                            # Not in Column.__init__, but might be used by engine
                            setattr(current_col, key, val)
                        
                        elif key == "overlap":
                            # Legacy VB attribute, store it if present
                            setattr(current_col, key, val)
                        
                        else:
                            # Future-proofing: store any unknown keys
                            # print(f"Info: Unknown column attribute '{key}' for column '{current_col.column_name}'")
                            setattr(current_col, key, val)
                    
                    i += 1
                break
            i += 1

        # ═══════════════════════════════════════════════════════════════════════
        # FINALIZE: Apply geometry and normalize overlaps
        # ═══════════════════════════════════════════════════════════════════════
        self._apply_slot_geometry()
        self._normalize_column_overlaps()

