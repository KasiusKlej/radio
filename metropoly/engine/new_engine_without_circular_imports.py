import os
from pathlib import Path
import random
import string
import traceback

# =============================================================================
# 1. SUPPORTING ENTITIES
# =============================================================================

class PlayerOptions:
    """Stores UI-specific toggles for each player (ported from VB Menu states)."""
    def __init__(self):
        self.fast_mode = False
        self.show_grid = True
        self.auto_end_turn = False
        self.sound = True
        self.graphics = True

    def to_dict(self):
        return self.__dict__


class Tile:
    """VB: Type maptip"""
    def __init__(self, x, y):
        self.x = x  # 1-based
        self.y = y  # 1-based
        self.tip = 0         
        self.semafor = 0     
        self.price = 0       
        self.stage = 0       
        self.owner = 0       
        self.visual_id = 11  
        self.extra_images = []
        self.rent = 0
        self.square_type = "property"

    def to_dict(self):
        return {
            "x": self.x,
            "y": self.y,
            "tip": self.tip,
            "semafor": self.semafor, # Added for logic parity
            "price": self.price,     # Added for logic parity
            "stage": self.stage,
            "owner": self.owner,
            "visual_id": self.visual_id,
            "extra_images": self.extra_images
        }

# =============================================================================
# 2. PLAYER ENTITY
# =============================================================================

class Player:
    """Represents a Metropoly player (Human or PC)."""
    def __init__(self, id, name, color, is_pc=False):
        self.id = id         # 1-7
        self.name = name
        self.color = color   # Hex string (converted from VB Long)
        self.is_pc = is_pc
        
        # Coordinates & Movement
        self.x = 0
        self.y = 0
        self.smer = 1        # Direction: 1:N, 2:S, 3:W, 4:E
        
        # Economy
        self.money = 1000
        self.izobrazba = 0   # 0:Pupil...5:Nobel
        self.jobpayment = 0  # Weekly salary
        self.statland = 0    # Total properties owned
        self.stathouse = 0   # Total houses built
        
        # Status
        self.is_bankrupt = False
        self.options = PlayerOptions()

    def get_salary(self):
        """Port of earn_price in MoneyParameters.bas."""
        salaries = {0: 50, 1: 80, 2: 100, 3: 150, 4: 250, 5: 300}
        return salaries.get(self.izobrazba, 50)

    def to_dict(self):
        """Flattened dictionary for JavaScript consumption."""
        d = self.__dict__.copy()
        d['options'] = self.options.to_dict()
        return d


 

class MetropolyGame:
    """
    The central State Machine. Holds the board, players, and turn logic.
    Consolidates VB globals from Module1.bas and game.frm.
    """
    def __init__(self, map_file="default.map", shortcuts=None):
        # --- A. PATH RESOLUTION (Restored) ---
        # Locates default.map and metropoly.ini in the same folder as this script
        base_path = Path(__file__).parent.resolve()
        self.map_path = base_path / map_file
        self.ini_path = base_path / "metropoly.ini"

        # --- B. 150 LANGUAGE SLOTS ---
        ####self.lngg = [""] * 151 
        self.selectedLanguage = "slo" # File code (e.g. 'slo')
        ####self.CURRENT_LANGUAGE = "slo"  # ISO code (e.g. 'sl')

        # --- C. BOARD & GLOBALS (VB Checklist) ---
        self.dimx = 10
        self.dimy = 11
        self.grid = [] # 2D array of Tile objects
        self.numpl = 0
        self.players = {} # {id: Player object}
        
        # Phase Control (faza 2=Wait for dice, 3=Moving, 4=Interaction)
        self.faza = 0
        self.curpl = 1
        self.kocka = 0
        self.cakajKocko = 0
        self.zoomfaktor = 1.0

        # Time & Education Titles
        self.dayOfWeek = 1
        self.dayOfWeekName = [""] * 8  # 1-7
        self.izobrazbaNaziv = [""] * 7 # 0-6
        self.semaforData = [""] * 82   # 1-81

        # Geometry (Set via load_map and set_startxy)
        self.jailx = 0; self.jaily = 0
        self.startx = 0; self.starty = 0
        self.startsmer = 1

        # Win95 UI Offsets for overlapping pawns
        self.figuraXoffset = [0, 0, 0, 16, 16, 0, 10, 10]
        self.figuraYoffset = [0, 0, 16, 0, 16, 10, 0, 10]
        self.figuraZaRefreshat = 1

        # Logic State
        self.clkMode = 0
        self.status_label = ""
        self.buyDialogAnswer = 0
        self.gameTurnSmer = 0
        self.gameTurnVpadnica = 0
        self.shortcuts = shortcuts or ['r', 's', 'e', 'o', ' '] 
        
        # Audio & Options
        self.audio_queue = []
        self.sound_enabled = True

        # Editor State
        self.is_editor_active = False
        self.mapEditorMode = 0 # 0=Game, 1=New Map, 2=Modified, 3=Opened
        self.mapCurrentTool = 0
        self.pauseGame1 = False # Remembers Dice Timer
        self.pauseGame2 = False # Remembers Jump Timer

        # --- D. BOOTSTRAP SEQUENCE ---
        self.shortcuts = load_metropoly_shortcuts(str(self.ini_path)) # Load shortcuts here
        self._initialize_game()

    def _initialize_game(self):
        """
        The Startup Sequence. Port of VB (game.frm) Form_Load
        Note: load/switch language must happen BEFORE set_data.
        """
        # 1. Determine language from .ini
        ####load_language(self) 

        # 2. Fill the 150 lngg lines from text file
        ####switch_language(self) 

        # 3. Scan for map files (Port of fill_combo)
        fill_combo_logic(self)

        # 4. Initialize logic constants (Semafor rules, Day names from lngg)
        set_data(self) 

        # 5. Load the map grid (sets jailx/y)
        if self.map_path.exists():
            load_metropoly_map(self, str(self.map_path))
        
        # 6. Determine start coordinates next to jail
        set_start_coords(self)

        # 7. Setup active players from .ini
        if self.ini_path.exists():
            config_players = load_metropoly_players(str(self.ini_path))
            init_players_logic(self, config_players)

    def to_dict(self, lang_data):
        #### old
        """Returns the full game state for the JavaScript frontend."""
        # player_data = {str(pid): p.to_dict() for pid, p in self.players.items()}
        # grid_data = [[t.to_dict() for t in row] for row in self.grid]
        # # Deliver and flush audio
        # current_sounds = list(self.audio_queue)
        # self.audio_queue = []
        # return {
        #     "dimx": self.dimx,
        #     "dimy": self.dimy,
        #     "grid": grid_data,
        #     "players": player_data,
        #     "curpl": self.curpl,
        #     "faza": self.faza,
        #     "kocka": self.kocka,
        #     "dayOfWeek": self.dayOfWeek,
        #     "dayName": self.dayOfWeekName[self.dayOfWeek] if 0 < self.dayOfWeek < 8 else "",
        #     "status_label": self.status_label,
        #     "clkMode": self.clkMode,
        #     "is_editor_active": self.is_editor_active,
        #     "mapEditorMode": self.mapEditorMode,
        #     "shortcuts": self.shortcuts,
        #     "audio_queue": current_sounds,
        #     "lang": self.CURRENT_LANGUAGE,
        #     "zoom": self.zoomfaktor,
        #     "dimx": self.dimx,
        #     "dimy": self.dimy,
        #     "map_list": self.map_list, # <--- The "Combo1" data
        #     "players": {str(pid): p.to_dict() for pid, p in self.players.items()}
        # }

        #### ✅ REWRITE to_dict to accept the translation as an external input:
        #### Instead of the engine "knowing" the language, the route hands the language to the engine only during the moment of serialization.
        """
        Serializes the state, using the provided lang_data for UI labels.
        The engine stays language-neutral.
        """
        l = lang_data.get("raw", [""] * 151) # The 150 lines
        
        return {
            "dimx": self.dimx,
            "dimy": self.dimy,
            "faza": self.faza,
            "curpl": self.curpl,
            "status_label": self.status_label, # This is still logic (e.g. "P1 pays P2")
            "players": {str(pid): p.to_dict() for pid, p in self.players.items()},
            "grid": [[t.to_dict() for t in row] for row in self.grid],
            
            # We attach the TRANSLATED menu/UI specifically for this one player
            "m": lang_data.get("menu", {}),
            "turn": lang_data.get("turn", {}),
            "dayName": l[127 + self.dayOfWeek] if hasattr(self, 'dayOfWeek') else ""
        }


    


  
    # -----------------------------------
    # NEW ENGINE WITHOUT CIRCULAR IMPORTS
    # -----------------------------------
   
    MAX_DIM = 100 


# =============================================================================
# STANDALONE ENGINE LOGIC (Ported from VB game.frm)
# =============================================================================
import random
import string

# =============================================================================
# STANDALONE ENGINE HELPERS
# =============================================================================

def next_player(state):
    """
    VB: Logic inside next_player
    Advances the current player index. Returns True if wrapped to Player 1.
    """
    state.curpl += 1
    if state.curpl > state.numpl:
        state.curpl = 1
        return True  # Wrapped around (New day logic usually follows)
    return False

def create_random_property_tile(state, x: int, y: int):
    """
    Consolidated helper for _new_land_tile, default_land, etc.
    Generates a property tile (tip 1) with a VB-style random price (A-Y).
    """
    # VB uses A-Y for prices 20-44
    c = random.choice(string.ascii_uppercase[:25]) 
    price = ord(c) - 45
    
    # Create actual Tile object used in state.grid
    new_tile = Tile(x, y)
    new_tile.tip = 1
    new_tile.price = price
    new_tile.stage = 0
    new_tile.owner = 0
    return new_tile

def get_grid_lines(state):
    """
    VB: Logic for display_grid
    Returns coordinates for rendering grid lines on the web canvas/svg.
    """
    dx = 32 * state.zoomfaktor
    dy = 32 * state.zoomfaktor
    
    vertical = [((i * dx, 0), (i * dx, state.dimy * dy)) for i in range(state.dimx + 1)]
    horizontal = [((0, j * dy), (state.dimx * dx, j * dy)) for j in range(state.dimy + 1)]
    
    return {"vertical": vertical, "horizontal": horizontal}

def display_land_info(state, i: int, j: int):
    """
    VB: Sub display_land_info(i, j)
    Updates state.status_label with tile details using ported financial functions.
    """
    # j-1 (row), i-1 (col) because Python lists are [y][x]
    tile = state.grid[j-1][i-1]
    l = state.lngg # Language lines
    
    res = ""
    if tile.tip == 1: # PROPERTY
        res += f"{l[114]} {buy_land_price(tile.price)} {l[85]}\n"    # Buy price
        res += f"{l[115]} {sell_price(tile.stage, tile.price)} {l[85]}\n" # Sell price
        res += f"{l[116]} {build_houses_price(tile.stage, tile.price)} {l[85]}\n\n"
        
        if tile.owner != 0:
            owner_name = state.players[tile.owner].name
            res += f"Owner: {owner_name}\n"
            
        res += f"{l[117]}\n" # "Rent table:"
        for k in range(6):
            rent_val = calculate_rent(k, tile.price)
            star = "*" if tile.stage == k else " "
            res += f"{star} {l[118]} {k} {l[119]}: {rent_val} {l[85]}\n"

    elif tile.tip in [0, 5]: res = l[120] # Road
    elif tile.tip == 2: res = l[121]      # School
    elif tile.tip == 3: res = l[122]      # Job
    elif tile.tip == 4: res = l[123]      # Jail

    state.status_label = res

def expand_terit(state, x: int, y: int):
    """
    VB: Sub expand_terit(x, y)
    Dynamically grows the grid when building on the edge.
    """
    expa = False
    max_dim = 100 

    # --- EXPAND LEFT ---
    if x == 1 and state.dimx < max_dim:
        state.dimx += 1
        expa = True
        state.startx += 1
        state.jailx += 1
        for r_idx in range(state.dimy):
            # Create random property at the new x=1
            new_t = create_random_property_tile(state, 1, r_idx + 1)
            state.grid[r_idx].insert(0, new_t)
            # Re-sync X coordinates for the rest of the row
            for col_idx, tile in enumerate(state.grid[r_idx]):
                tile.x = col_idx + 1
        for p in state.players.values(): p.x += 1

    # --- EXPAND RIGHT ---
    elif x == state.dimx and state.dimx < max_dim:
        state.dimx += 1
        expa = True
        for r_idx in range(state.dimy):
            new_t = create_random_property_tile(state, state.dimx, r_idx + 1)
            state.grid[r_idx].append(new_t)

    # --- EXPAND TOP ---
    if y == 1 and state.dimy < max_dim:
        state.dimy += 1
        expa = True
        state.starty += 1
        state.jaily += 1
        new_row = [create_random_property_tile(state, c + 1, 1) for c in range(state.dimx)]
        state.grid.insert(0, new_row)
        # Re-sync Y coordinates for all tiles
        for row_idx, row in enumerate(state.grid):
            for tile in row: tile.y = row_idx + 1
        for p in state.players.values(): p.y += 1

    # --- EXPAND BOTTOM ---
    elif y == state.dimy and state.dimy < max_dim:
        state.dimy += 1
        expa = True
        new_row = [create_random_property_tile(state, c + 1, state.dimy) for c in range(state.dimx)]
        state.grid.append(new_row)

    if expa:
        state.status_label = state.lngg[103] # "Territory expanded"
    
    return expa

def prepare_buy_dialog(state, sx: int, sy: int, price: int, land_or_house: int):
    """
    VB: Logic prep for frmBuyDialog.
    land_or_house: 0 = land, 1 = house
    """
    # Use our standalone display function to update status_label
    display_land_info(state, sx, sy)

    if land_or_house == 0:
        # VB: lngg(124) "Do you want to buy land for..."
        question = f"{state.lngg[124]} {price}{state.lngg[101]}"
    else:
        # VB: lngg(125) "Do you want to build houses for..."
        question = f"{state.lngg[125]} {price}{state.lngg[101]}"

    # Decide vertical placement hint (Win95 logic)
    placement = "top" if sy <= state.dimy / 2 else "bottom"

    return {
        "question": question,
        "placement": placement,
        "x": sx,
        "y": sy,
    }

def turn_semaphore(state, x: int, y: int):
    """
    VB: Sub turn_semaphore(x, y)
    Rotate a single semaphore according to game turn rules.
    """
    smr = state.gameTurnVpadnica   # Approach (0–3)
    nsmr = state.gameTurnSmer      # Direction variant (0–2)

    sosed = kje_so_sosednje_ceste(state, x, y)
    if sosed[smr] == "0":
        return  # Road doesn't exist from this approach

    tile = state.grid[y-1][x-1]
    # Get the 4-digit prefix of the semaphore rule
    s = state.semaforData[tile.semafor][:4]
    ss = ""

    # Logic for finding the new direction string
    if smr == 0:
        nova = "234"[nsmr]
        if sosed[int(nova) - 1] == "1": ss = nova + s[1:]
    elif smr == 1:
        nova = "134"[nsmr]
        if sosed[int(nova) - 1] == "1": ss = s[0] + nova + s[2:]
    elif smr == 2:
        nova = "124"[nsmr]
        if sosed[int(nova) - 1] == "1": ss = s[:2] + nova + s[3:]
    elif smr == 3:
        nova = "123"[nsmr]
        if sosed[int(nova) - 1] == "1": ss = s[:3] + nova

    if not ss:
        return

    # Find the new rule index in the 81 presets
    for i in range(1, 82):
        if state.semaforData[i].startswith(ss):
            tile.semafor = i
            break

def turn_semaphores(state):
    """
    VB: Sub turn_semaphores()
    Iterates the whole map and rotates every traffic light.
    Usually called on Wednesday and Saturday.
    """
    state.status_label = state.lngg[126] # "Turning semaphores..."
    
    for y in range(1, state.dimy + 1):
        for x in range(1, state.dimx + 1):
            tile = state.grid[y-1][x-1]
            if tile.tip == 5: # It's a semaphore
                # Call the individual rotation function we wrote earlier
                turn_semaphore(state, x, y)
                # Update the visual IDs for the JS
                risi_cesto(state, x, y)
                
    # Update global semaphore cycle state
    state.gameTurnVpadnica = (state.gameTurnVpadnica + 1) % 4
    state.gameTurnSmer = (state.gameTurnSmer + 1) % 3

def rotate_semaphores_if_possible(state):
    """VB: Logic for mnuRotateSemaphors_Click"""
    p_cost = rotate_semafor_price()
    player = state.players[state.curpl]

    if player.is_pc or player.money < p_cost:
        return False

    turn_semaphores(state)
    player.money -= p_cost
    # Equivalent to display_status in VB
    state.status_label = state.lngg[126] # "Turning semaphores"
    return True

def someone_already_stands_here(state, x: int, y: int, pid: int) -> bool:
    """VB: Function nekdo_ze_stoji_tle"""
    for player in state.players.values():
        if player.id != pid and player.x == x and player.y == y:
            return True
    return False

def build_road_at(state, x: int, y: int):
    """Logic for converting land to road in editor or via AI."""
    tile = state.grid[y-1][x-1]
    tile.tip = 0 # Road
    tile.stage = 0
    tile.owner = 0
    # Update visuals and neighboring roads
    risi_cesto(state, x, y)
    popravi_sosednje_ceste(state, x, y)
    add_random_semafor(state, x, y)

def process_move_sequence(state):
    """
    VB Port: TimerSkokFigure_Timer()
    Returns full path for JS animation and triggers landing interaction.
    """
    p = state.players[state.curpl]
    steps_path = []
    steps_remaining = state.kocka
    
    while steps_remaining > 0:
        kamx, kamy = state.jailx, state.jaily 
        newsmer = 0
        
        # 1. Jail Logic
        if p.x == state.jailx and p.y == state.jaily:
            kamx, kamy = state.startx, state.starty
            p.smer = state.startsmer
        else:
            # 2. Road Adjacency
            sosed = kje_so_sosednje_ceste(state, p.x, p.y)
            if sosed[p.smer - 1] == "1":
                kamx, kamy = p.x, p.y
                if p.smer == 1: kamy -= 1
                elif p.smer == 2: kamy += 1
                elif p.smer == 3: kamx -= 1
                elif p.smer == 4: kamx += 1
            else:
                # 3. Corner Logic
                kamx, kamy, newsmer = find_alternative_road_logic(state, sosed, p.smer, p.x, p.y)
        
        if newsmer != 0: p.smer = newsmer
            
        # 4. Semaphore Entry logic
        target_tile = state.grid[kamy-1][kamx-1]
        if target_tile.tip == 5:
            rule_str = state.semaforData[target_tile.semafor]
            if p.y - kamy == -1: p.smer = int(rule_str[0])
            elif p.y - kamy == 1: p.smer = int(rule_str[1])
            elif p.x - kamx == -1: p.smer = int(rule_str[2])
            elif p.x - kamx == 1: p.smer = int(rule_str[3])

        # 5. Finalize Step
        p.x, p.y = kamx, kamy
        sviraj(state, "figura.wav")
        steps_path.append({"x": p.x, "y": p.y, "smer": p.smer})
        steps_remaining -= 1

    state.faza = 4
    pristanek(state) 
    return steps_path

def roll_dice(state):
    """VB: TimerMetKocke equivalent"""
    d1 = random.randint(1, 6)
    d2 = random.randint(1, 6)
    state.kocka = d1 + d2
    state.faza = 3 # Moving
    sviraj(state, "kocka.wav")
    return {"dice": [d1, d2], "total": state.kocka}

def next_player(state):
    """VB: Sub next_player()"""
    state.curpl += 1
    if state.curpl > state.numpl:
        state.curpl = 1
        # Day increment happens in mnu_end_turn_click

    p = state.players[state.curpl]
    
    # Bankruptcy skip
    if p.money < 0:
        eliminate_player(state, p.id)
        return next_player(state)

    state.faza = 2 # Waiting for roll
    state.status_label = f"{state.lngg[141]} {p.name}{state.lngg[142]}"

def pc_emergency_funds(state):
    player = state.players[state.curpl]
    if player.money >= 90:
        return

    # Get a list of all tiles owned by this player
    owned_tiles = [tile for row in state.grid for tile in row if tile.owner == player.id]
    random.shuffle(owned_tiles)

    for tile in owned_tiles:
        if player.money > 160:
            break
            
        if tile.stage > 0:
            # 70% chance to sell a house
            if random.random() < 0.7:
                refund = calculate_sell_price(tile.stage, tile.price)
                player.money += refund
                tile.stage -= 1
                player.stathouse -= 1
        else:
            # 50% chance to sell land or convert to road
            if random.random() < 0.5:
                # Sell Land
                refund = calculate_sell_price(0, tile.price)
                player.money += refund
                tile.owner = 0
                player.statland -= 1
            else:
                # Convert to Road
                tile.owner = 0
                tile.tip = 0 # Convert to road
                tile.stage = 0
                # Recalculate road tiling for this and neighbors
                update_road_visuals(state, tile.x, tile.y)
                player.money += 100 # refund

def metropoly_language_parser(lang_dir, filename):
    """
    Unified Parser: Always returns a dict with 151 items in 'raw'.
    No more KeyErrors or NoneType crashes.
    """
    path = Path(lang_dir) / filename
    # 151 slots of empty strings (index 0 to 150)
    raw_lines = [""] * 151 

    if path.exists():
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                for i, line in enumerate(f, 1):
                    if i > 150: break
                    raw_lines[i] = line.strip().replace("&", "")
        except Exception as e:
            print(f"⚓ Parser File Error: {e}")

    # Helper function to prevent empty values in HTML
    l = lambda idx, default: raw_lines[idx] if raw_lines[idx] else default

    return {
        "raw": raw_lines,
        "menu": {
            "file": l(17, "File"), "new": l(18, "New"), "open": l(19, "Open"),
            "save": l(20, "Save"), "save_map": l(21, "Save map"),
            "exit_map_editor": l(22, "Exit map editor"), "exit": l(23, "Exit"),
            "orders": l(25, "Orders"), "build_road": l(26, "Build road"),
            "sell": l(27, "Sell"), "semaphores": l(28, "Semaphores"),
            "create_semaphore": l(29, "Create semaphore"),
            "remove_semaphore": l(30, "Remove semaphore"),
            "rotate_semaphores": l(31, "Rotate semaphores"),
            "end_turn": l(32, "End turn"),
            "options": l(34, "Options"), "fast": l(35, "Fast"),
            "show_grid": l(36, "Show grid"), "auto_end_turn": l(37, "Automatic end turn"),
            "sound": l(38, "Sound"), "graphics": l(39, "Graphics"),
            "tools": l(41, "Tools"), "map_editor": l(42, "Map editor"),
            "help": l(44, "Help"), "contents": l(45, "Contents"),
            "about": l(46, "About"), "register": l(47, "Register")
        },
        "phrases": {
            "currency": l(85, "$"),
            "pays": l(91, "pays"),
            "buys_land": l(93, "buys land for")
        },
        "turn": {
            "prefix": l(141, "It is"),
            "suffix": l(142, "'s turn"),
            "yes": l(144, "Yes"),
            "no": l(145, "No")
        }
    }

def load_metropoly_players(ini_path):
    """
    Parses metropoly.ini. 
    Converts lines like '11Bugs' into {'id': 1, 'active': True, 'is_pc': True, 'name': 'Bugs'}
    """
    players_to_init = []
    try:
        with open(ini_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        found_section = False
        p_count = 0
        for line in lines:
            line = line.strip()
            if not line: continue
            
            if line == "[DefaultPlayers]":
                found_section = True
                continue
            
            # If we hit the next section, stop
            if found_section and line.startswith("["):
                break
                
            if found_section:
                p_count += 1
                # Line format: '1' (active), '1' (is_pc), 'Name'
                # Example: '11Bugs' -> active='1', pc='1', name='Bugs'
                if len(line) >= 2:
                    active = line[0] == "1"
                    is_pc = line[1] == "1"
                    name = line[2:]
                    
                    if active:
                        # WE CREATE THE DICTIONARY HERE
                        players_to_init.append({
                            'id': p_count,
                            'is_pc': is_pc,
                            'name': name
                        })
                
                if p_count >= 7: break # Metropoly only supports 7 slots
                
    except Exception as e:
        print(f"Error parsing .ini: {e}")
        
    return players_to_init # Now returns a list of DICTS

def parse_map_file(map_path):
    """Parses the 4-layer default.map file."""
    with open(map_path, 'r') as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    dimx = int(lines[0])
    dimy = int(lines[1])
    
    # Initialize 2D array
    grid = [[{"x": x, "y": y} for x in range(dimx)] for y in range(dimy)]

    # Layer 1: Types & Semafors (lines 2 to 2+dimy)
    for y in range(dimy):
        row_str = lines[2 + y]
        for x in range(dimx):
            char = row_str[x]
            val = ord(char)
            if val < 53: # '0'-'4'
                grid[y][x]["tip"] = int(char)
            else:
                grid[y][x]["tip"] = 5 # Semafor
                grid[y][x]["semafor_idx"] = val - 52

    # Layer 2: Prices (lines 2+dimy to 2+2*dimy)
    cursor = 2 + dimy
    for y in range(dimy):
        row_str = lines[cursor + y]
        for x in range(dimx):
            grid[y][x]["price"] = ord(row_str[x]) - 45

    # Layer 3: Stage
    cursor = 2 + 2 * dimy
    for y in range(dimy):
        row_str = lines[cursor + y]
        for x in range(dimx):
            grid[y][x]["stage"] = int(row_str[x])

    # Layer 4: Owner
    cursor = 2 + 3 * dimy
    for y in range(dimy):
        row_str = lines[cursor + y]
        for x in range(dimx):
            grid[y][x]["owner"] = int(row_str[x])

    return grid, dimx, dimy

def load_metropoly_shortcuts(ini_path):
    with open(ini_path, 'r') as f:
        lines = f.readlines()

    shortcuts = []
    found_section = False
    for line in lines:
        line = line.strip()
        if line == "[OrdersKeyboardShortcuts]":
            found_section = True
            continue
        if found_section and line and not line.startswith("["):
            shortcuts.append(line.lower()) # e.g., ['r', 's', 'e', 'o', ' ']
        if len(shortcuts) >= 5: break
            
    return shortcuts

def load_keyboard_shortcuts(ini_path):
    """
    VB: Sub load_keyboard_shortcuts()
    Reads the 5 specific lines for keyboard shortcuts from metropoly.ini.
    """
    shortcuts = []
    try:
        with open(ini_path, 'r') as f:
            lines = f.readlines()
        
        found_section = False
        for i, line in enumerate(lines):
            clean_line = line.strip()
            if clean_line == "[OrdersKeyboardShortcuts]":
                found_section = True
                # Read the next 5 lines
                for offset in range(1, 6):
                    if i + offset < len(lines):
                        shortcuts.append(lines[i + offset].strip())
                    else:
                        shortcuts.append("")
                break
    except Exception as e:
        print(f"Error loading shortcuts: {e}")
        return ["r", "s", "e", "o", " "] # Defaults

    return shortcuts

def put_road(s, x, c):
    """
    VB: Function put_road(s, x, c)
    Helper to inject a character into a string at a specific 1-based index.
    """
    # Adjust 1-based VB index to 0-based Python index
    idx = x - 1
    return s[:idx] + str(c) + s[idx+1:]

def generate_default_map_content(x, y):
    """
    VB: Sub generate_default_map(x, y)
    Generates the 4-layer ASCII map data.
    """
    lines = []
    
    # --- LAYER 0: Dimensions ---
    lines.append(str(x))
    lines.append(str(y))
    
    # --- LAYER 1: Roads & Types ---
    sema = ":" 
    semb = "X"
    xs1 = 3 + random.randint(1, x - 6)
    
    # Row 1: Top boundary + School
    s = "1" * x
    # random offset for school: xs1 + Rnd(4) - 2
    school_pos = xs1 + random.randint(1, 4) - 2
    s = put_road(s, school_pos, "2")
    lines.append(s)
    
    # Row 2: Jail + Semaphore
    s = "4" + ("0" * (x - 2)) + "1" # Jail at start, Property at end
    s = put_road(s, xs1, sema)
    lines.append(s)
    
    # Rows 3 to Y-2: Vertical Road with "Wiggles"
    for i in range(3, y - 1):
        s = "10" + ("1" * (x - 4)) + "01"
        s = put_road(s, xs1, "0")
        
        # Ovinek (Wiggle) logic: 40% chance to shift road left/right
        if random.random() > 0.6:
            if 3 < xs1 < (x - 3):
                pm = 1 if random.random() > 0.5 else -1
                xs1 += pm
                s = put_road(s, xs1, "0")
        lines.append(s)
        
    # Penultimate Row: Job + Semaphore
    s = "1" + ("0" * (x - 2)) + "3"
    s = put_road(s, xs1, semb)
    lines.append(s)
    
    # Last Row: Bottom boundary
    lines.append("1" * x)
    
    # --- LAYER 2: Prices (A-Z) ---
    alphabet = string.ascii_uppercase # ABCDEFGHIJKLMNOPQRSTUVWXYZ
    for i in range(1, y + 1):
        char_idx = (i - 1) % 25
        lines.append(alphabet[char_idx] * x)
        
    # --- LAYER 3: Stage (All '0') ---
    for i in range(y):
        lines.append("0" * x)
        
    # --- LAYER 4: Owner (All '0') ---
    for i in range(y):
        lines.append("0" * x)
        
    return lines

def load_metropoly_map(state, file_path):
    """
    VB: Sub load_map(fn)
    Parses the 4-layer map file into the state grid.
    """
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = [line.rstrip('\n') for line in f.readlines()]

    state.dimx = int(lines[0])
    state.dimy = int(lines[1])
    dx, dy = state.dimx, state.dimy

    # Initialize empty grid
    state.grid = [[Tile(x+1, y+1) for x in range(dx)] for y in range(dy)]

    # Layer 1: Tip & Semaphore
    for i in range(dy):
        row_str = lines[2 + i]
        for j in range(dx):
            char = row_str[j]
            code = ord(char)
            if code < 53: # '0'-'4'
                state.grid[i][j].tip = int(char)
                if int(char) == 4: # Jail
                    state.jailx, state.jaily = j + 1, i + 1
            else:
                state.grid[i][j].tip = 5 # Semaphore
                state.grid[i][j].semafor = code - 52

    # Layer 2: Price (ASCII - 45)
    offset = 2 + dy
    for i in range(dy):
        row_str = lines[offset + i]
        for j in range(dx):
            state.grid[i][j].price = ord(row_str[j]) - 45

    # Layer 3: Stage (Houses)
    offset = 2 + (2 * dy)
    for i in range(dy):
        row_str = lines[offset + i]
        for j in range(dx):
            state.grid[i][j].stage = int(row_str[j])

    # Layer 4: Owner
    offset = 2 + (3 * dy)
    for i in range(dy):
        row_str = lines[offset + i]
        for j in range(dx):
            state.grid[i][j].owner = int(row_str[j])

def save_metropoly_defaults(ini_path, player_data_list):
    """
    VB: Sub save_frm_defaults()
    Updates metropoly.ini with the current player names and types (Human/PC).
    player_data_list: List of dicts [{'active': bool, 'is_pc': bool, 'name': str}, ...]
    """
    try:
        with open(ini_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        new_content = []
        skip_mode = False
        
        for line in lines:
            if line.strip() == "[DefaultPlayers]":
                new_content.append(line)
                # Generate the 7 player lines based on the UI data
                for i in range(7):
                    p = player_data_list[i] if i < len(player_data_list) else {'active': False, 'is_pc': False, 'name': ''}
                    s = "1" if p['active'] else "0"
                    s += "1" if p['is_pc'] else "0"
                    s += p['name']
                    new_content.append(s + "\n")
                skip_mode = True # We are now in the zone we are overwriting
                continue
            
            # If we hit the next section, stop skipping
            if skip_mode and line.startswith("["):
                skip_mode = False
            
            if not skip_mode:
                new_content.append(line)

        with open(ini_path, 'w', encoding='utf-8') as f:
            f.writelines(new_content)
            
    except Exception as e:
        print(f"Error saving ini defaults: {e}")





######################################### engine #################################################
# engine/engine.py

def next_player(state):
    """Moves the turn to the next active player."""
    state.curpl += 1
    if state.curpl > state.numpl:
        state.curpl = 1
    
    # Check if player is bankrupt/inactive (to be implemented)
    # If state.players[state.curpl].is_bankrupt: return next_player(state)
    
    return state.curpl

def get_player_stats(state):
    total_land = sum(p.statland for p in state.players.values())
    total_houses = sum(p.stathouse for p in state.players.values())
    
    stats = []
    for pid, p in state.players.items():
        # Gauge calculation from VB: 45 + Int((stat / total) * 9)
        land_gauge = 0
        if total_land > 0:
            land_gauge = int((p.statland / total_land) * 9)
            
        stats.append({
            "name": p.ime,
            "money": p.money,
            "land_gauge": f"GAUG{land_gauge}.png",
            "is_current": (pid == state.curpl)
        })
    return stats

def run_landing_logic(state):
    """Handles neighbors (Pay, Buy, Build, Learn)."""
    p = state.players[state.curpl]
    neighbors = [(p.x-1, p.y), (p.x+1, p.y), (p.x, p.y-1), (p.x, p.y+1)]
    
    events = []
    for nx, ny in neighbors:
        if not (0 <= nx < state.dimx and 0 <= ny < state.dimy):
            continue
            
        tile = state.grid[ny][nx]
        
        # Logic: Pay Rent
        if tile.tip == 1 and tile.owner != 0 and tile.owner != p.id:
            rent = calculate_rent(tile)
            p.money -= rent
            state.players[tile.owner].money += rent
            events.append(f"Paid {rent} to {state.players[tile.owner].name}")

        # Logic: School (Education)
        if tile.tip == 2:
            events.append({"type": "offer_learn", "price": calculate_learn_price(p)})
            
        # Logic: Job (Salary)
        if tile.tip == 3:
            p.jobpayment = calculate_salary(p)
            events.append(f"New job payment: {p.jobpayment}")
            
    return events

def eliminate_player(state, player_id):
    p = state.players[player_id]
    p.is_active = False
    
    # Reset all tiles owned by this player
    for row in state.grid:
        for tile in row:
            if tile.owner == player_id:
                tile.owner = 0
                tile.stage = 0
    
    return f"{p.name} has been eliminated!"

def expand_map(state, edge):
    """
    edge: 'top', 'bottom', 'left', 'right'
    """
    if edge == 'left' and state.dimx < 100:
        state.dimx += 1
        # Shift all existing tiles right and insert new col at index 0
        for y in range(state.dimy):
            new_tile = Tile(0, y)
            new_tile.tip = 1 # Property
            state.grid[y].insert(0, new_tile)
        # Update player coordinates
        for p in state.players.values():
            p.x += 1
            
    elif edge == 'right' and state.dimx < 100:
        state.dimx += 1
        for y in range(state.dimy):
            new_tile = Tile(state.dimx-1, y)
            new_tile.tip = 1
            state.grid[y].append(new_tile)
            
    # Similar logic for top (insert row at 0) and bottom (append row)

def get_turn_message(state):
    player_name = state.players[state.curpl].name
    # Equivalent to VB: lngg(141) & " " & player(curpl).ime & lngg(142)
    prefix = state.lang_dict['turn']['prefix']
    suffix = state.lang_dict['turn']['suffix']
    return f"{prefix} {player_name}{suffix}"

def find_jail_and_start(state):
    # Find the '4' in the grid
    for y in range(state.dimy):
        for x in range(state.dimx):
            if state.grid[y][x]["tip"] == 4:
                state.jailx, state.jaily = x + 1, y + 1 # 1-based to match VB
                
    # Logic to find adjacent road (simplified port of your VB code)
    # Check 4 neighbors...
    neighbors = [(0,1), (0,-1), (1,0), (-1,0)]
    for dx, dy in neighbors:
        nx, ny = state.jailx + dx, state.jaily + dy
        # If it's a road (0), set that as startx, starty
        # and set startsmer based on where the road continues...
        

#############################################################
# game.frm porting from Visual Basic 5.0
#############################################################

SOUND_MAP = {
    "kocka": "KOCKA",
    "figua": "FIGURA",
}

def init_game(state):
    """
    Port of VB6 Form_Load from game.frm
    Initializes game state.
    """
    random.seed()  # VB: Randomize

    state.numpl = 0

    load_language(state)
    switch_language(state)
    set_data(state)

    state.zoomfaktor = 1  # must be 1

    # --- Pawn drawing offsets (VB figuraXoffset / figuraYoffset)
    # Index 0 intentionally unused (VB arrays are 1-based)

    twx = 1  # Screen.TwipsPerPixelX → pixels in web version
    twy = 1  # Screen.TwipsPerPixelY

    state.figuraXoffset[1] = 0 * twx
    state.figuraYoffset[1] = 0 * twy

    state.figuraXoffset[2] = 0 * twx
    state.figuraYoffset[2] = 16 * twy

    state.figuraXoffset[3] = 16 * twx
    state.figuraYoffset[3] = 0 * twy

    state.figuraXoffset[4] = 16 * twx
    state.figuraYoffset[4] = 16 * twy

    state.figuraXoffset[5] = 0 * twx
    state.figuraYoffset[5] = 10 * twy

    state.figuraXoffset[6] = 10 * twx
    state.figuraYoffset[6] = 0 * twy

    state.figuraXoffset[7] = 10 * twx
    state.figuraYoffset[7] = 10 * twy

    state.figuraZaRefreshat = 1

    load_resources(state)

    # --- Custom graphics (metropoly.ini)
    mustCustomize = False
    ini_path = os.path.join(state.app_path, "metropoly.ini")

    try:
        with open(ini_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip() == "[Graphics]":
                    # Read next 3 lines like VB did
                    try:
                        next(f)
                        next(f)
                        next(f)
                        mustCustomize = True
                    except StopIteration:
                        pass
                    break
    except FileNotFoundError:
        pass

    if mustCustomize:
        load_graphics_from_ini(state)

    load_keyboard_shortcuts(state)

#####################
# game menu functions
#####################
def display_status(state):
    """
    Port of VB display_status
    Clears land info and shows general status.
    """
    state.selected_land = None
    state.status_mode = "default"

def image_land_info_click(state):
    """
    Port of ImageLandInfo_Click
    """
    display_status(state)

def image_selected_tool_click(state, index):
    """
    Port of ImageSelectedTool_Click(Index)
    """
    state.mapCurrentTool = index

    # Reset all tool selections
    for k in state.OptionSelectedTool.keys():
        state.OptionSelectedTool[k] = False

    state.OptionSelectedTool[index] = True

def mnu_about_click(state):
    """
    VB: frmAbout.Show vbModal
    Web: route will render frmAbout.html
    """
    # No state mutation required
    return

def mnu_auto_end_turn_click(state):
    """
    VB: mnuAutoEndTurn.Checked = Not mnuAutoEndTurn.Checked
    """
    state.autoEndTurn = not state.autoEndTurn

def mnu_contents_click(state):
    """
    VB: Help.Show vbModal
    Web: route renders help page
    """
    return

def mnu_register_click(state):
    state.ui.show_modal("register")

def mnu_sound_click(state):
    state.sound_enabled = not state.sound_enabled

def option_selected_tool_click(state, index):
    state.mapCurrentTool = int(index)

def picture_status_click(state):
    display_status(state)


###################
# logic
###################



def mnu_fast_click(state):
    state.fast_mode = not state.fast_mode
    if state.fast_mode:
        state.timer_met_kocke_interval = 30
        state.timer_skok_figure_interval = 50
    else:
        state.timer_met_kocke_interval = 300
        state.timer_skok_figure_interval = 500


##############
# drawing
##############
def draw_players(state):
    # Hide all pawns
    for pawn in state.pawns:   # assume state.pawns exists, max 7
        pawn.is_visible = False
    
    # Show active players
    for i in range(1, state.numpl+1):
        player = state.players[i]
        pawn = state.pawns[player.id]  # mapping VB figura(i).Visible
        pawn.is_visible = True
        pawn.x = player.x
        pawn.y = player.y
        draw_player(state, player.x, player.y, player.id)

def draw_player(state, x, y, player_id):
    dx = 32 * state.zoomfaktor
    dy = 32 * state.zoomfaktor
    
    x1 = (x - 1) * dx
    y1 = (y - 1) * dy
    
    pawn = state.pawns[player_id]
    
    if nekdo_ze_stoji_tle(state, x, y, player_id):
        pawn.top = y1 + state.figuraYoffset[player_id]
        pawn.left = x1 + state.figuraXoffset[player_id]
    else:
        pawn.top = y1 + 8
        pawn.left = x1 + 8

def kje_so_sosednje_ceste(state, x, y):
    """Return 'nswe' adjacency string of roads/semaphores"""
    s1 = s2 = s3 = s4 = "0"
    
    # North
    if y - 1 > 0:
        t = state.grid[x][y-1].tip
        if t in (0, 5):
            s1 = "1"
    
    # South
    if y + 1 <= state.dimy:
        t = state.grid[x][y+1].tip
        if t in (0, 5):
            s2 = "1"
    
    # West
    if x - 1 > 0:
        t = state.grid[x-1][y].tip
        if t in (0, 5):
            s3 = "1"
    
    # East
    if x + 1 <= state.dimx:
        t = state.grid[x+1][y].tip
        if t in (0, 5):
            s4 = "1"
    
    return s1 + s2 + s3 + s4

def risipolje(state, x, y, tile_id):
    """Mark a tile to be painted. tile_id corresponds to image."""
    dx = 32 * state.zoomfaktor
    dy = 32 * state.zoomfaktor
    x1 = (x - 1) * dx
    y1 = (y - 1) * dy
    
    # In Python, we store this info to render in JS
    state.tile_draw_queue.append({
        "tile_id": tile_id,
        "x": x1,
        "y": y1
    })

def draw_map(state):
    state.tile_draw_queue.clear()
    
    for y in range(1, state.dimy + 1):
        for x in range(1, state.dimx + 1):
            tile = state.grid[x][y]
            
            # Base ground
            risipolje(state, x, y, 11)
            
            # Roads
            if tile.tip in (0, 5):
                risi_cesto(state, x, y)
            
            # Special tiles
            if tile.tip == 2: risipolje(state, x, y, 17)  # school
            if tile.tip == 3: risipolje(state, x, y, 18)  # job
            if tile.tip == 4: risipolje(state, x, y, 19)  # jail
            
            # House stage
            if tile.stage > 0:
                risipolje(state, x, y, 11 + int(tile.stage))
            
            # Owner flag
            if tile.owner > 0:
                owner_id = state.players[tile.owner].id
                risipolje(state, x, y, 19 + owner_id)

def mnu_remove_semaphor_click(state):
    player = state.players[state.curpl]
    
    if player.is_pc == False: # tip 0
        # Re-use your display_land_info port
        display_land_info(state, player.x, player.y) 
        
        # ACCESSING THE LIST:
        state.status_label = state.lngg[84] 
        state.clkMode = 4

def mnu_show_grid_click(state):
    state.show_grid = not state.show_grid
    
    if state.show_grid:
        display_grid(state)
    else:
        draw_map(state)

def play_sound(state, sound_id, volume=0.4):
    if not state.sound_enabled:
        return
    
    state.audio_queue.append({
        "sound": sound_id,
        "volume": min(volume, 0.5)  # hard cap
    })

##########
# timer
########

def timer_refresh_figure_tick(state):
    if state.numpl == 0:
        return
    
    pid = state.figuraZaRefreshat
    
    if state.pawns[pid].visible:
        state.pawns[pid].z += 1  # logical z-index
    
    state.figuraZaRefreshat += 1
    if state.figuraZaRefreshat > 7:
        state.figuraZaRefreshat = 1

def play_sound(state, sound_key, volume=0.4):
    if not state.sound_enabled:
        return
    
    sound_id = SOUND_MAP.get(sound_key)
    if not sound_id:
        return
    
    state.audio_queue.append({
        "id": sound_id,
        "volume": min(volume, 0.5)
    })

def get_status_panel(state):
    total_land = sum(p.statland for p in state.players.values())
    total_house = sum(p.stathouse for p in state.players.values())

    players = []
    for pid, p in state.players.items():
        players.append({
            "id": pid,
            "name": p.name,
            "money": p.money,
            "land": p.statland,
            "house": p.stathouse,
            "is_current": pid == state.curpl,
            "color": p.color,
            "land_ratio": (p.statland / total_land) if total_land else 0,
            "house_ratio": (p.stathouse / total_house) if total_house else 0,
            "tooltip": (
                f"{p.name} "
                f"{state.lang['land']} {p.statland} "
                f"{state.lang['house']} {p.stathouse} "
                f"{state.lang['salary']} {p.jobpayment}"
            )
        })

    return {
        "players": players
    }

def step_player_movement(state):
    p = state.players[state.curpl]

    next_x, next_y, new_dir = compute_next_position(state, p)

    if new_dir:
        p.smer = new_dir

    p.x = next_x
    p.y = next_y

    state.kocka -= 1

    return {
        "move": {
            "player": p.id,
            "x": p.x,
            "y": p.y
        },
        "sound": "jump",
        "done": state.kocka <= 0
    }

def pay_money(state, sx, sy, multiPay):
    tile = state.map[sx][sy]
    cur = state.curpl

    if tile.tip != 1:
        return

    if tile.owner == 0 or tile.owner == cur:
        return

    p = calculate_rent(tile.stage, tile.price)

    payer = state.players[cur]
    receiver = state.players[tile.owner]

    payer.money -= p
    receiver.money += p

    msg_part = f"{p} {state.lang_dict['pay']['to']} {receiver.name}"

    if not multiPay:
        multiPay.append(
            f"{payer.name} {state.lang_dict['pay']['paid']} {msg_part}"
        )
    else:
        multiPay.append(msg_part)

def buy_land(state, sx, sy):
    tile = state.map[sx][sy]
    player = state.players[state.curpl]

    if tile.tip != 1 or tile.owner != 0:
        return None

    price = buy_land_price(tile.price)

    if player.money < price:
        return None

    # default PC logic
    auto_ok = True
    if player.money < 200:
        auto_ok = False

    if player.tip == 1:  # PC
        if not auto_ok:
            return None
        confirm = True
    else:
        return {
            "action": "confirm_buy_land",
            "x": sx,
            "y": sy,
            "price": price
        }

    if confirm:
        player.money -= price
        player.statland += 1
        tile.owner = state.curpl

        return {
            "action": "land_bought",
            "player": player.name,
            "price": price
        }

def build_houses(state, sx, sy):
    tile = state.map[sx][sy]
    player = state.players[state.curpl]

    if tile.tip != 1 or tile.owner != state.curpl:
        return None

    if tile.stage >= 5:
        return None

    price = build_houses_price(tile.stage, tile.price)

    if player.money < price:
        return None

    auto_ok = True
    if player.money < 300:
        auto_ok = False

    if player.tip == 1:
        if not auto_ok:
            return None
        confirm = True
    else:
        return {
            "action": "confirm_build_house",
            "x": sx,
            "y": sy,
            "price": price,
            "next_stage": tile.stage + 1
        }

    if confirm:
        player.money -= price
        player.stathouse += 1
        tile.stage += 1

        return {
            "action": "house_built",
            "stage": tile.stage,
            "price": price
        }

def earn_learn(state, sx, sy):
    tile = state.map[sx][sy]
    player = state.players[state.curpl]

    # JOB
    if tile.tip == 3:
        p = earn_price(player.izobrazba)
        player.jobpayment = p
        return {
            "action": "job_assigned",
            "weekly_pay": p
        }

    # SCHOOL
    if tile.tip == 2 and player.izobrazba < 5:
        p = learn_price(player.izobrazba)

        if player.money < p:
            return None

        if player.tip == 1:
            if random.random() > 0.75:
                return None
            confirm = True
        else:
            return {
                "action": "confirm_learn",
                "price": p,
                "level": player.izobrazba + 1
            }

        if confirm:
            player.money -= p
            player.izobrazba += 1
            return {
                "action": "learned",
                "new_level": player.izobrazba
            }

def is_semafor_possible(state, x, y):
    """
    VB: Function semafor_je_mozen(x, y)
    Checks if there are more than 2 roads connecting to this tile.
    (Semaphors only appear at T-junctions or Crossroads).
    """
    # We defined this in our previous session
    sosed = kje_so_sosednje_ceste(state, x, y)
    
    # Sum up the '1's in the string
    road_count = sum(int(c) for c in sosed)
    
    return road_count > 2

def create_semafor(state, x, y):
    """
    VB: Sub create_semaphor(x, y)
    Sets the tile as a semaphor and 'spins' it to find a valid rule.
    """
    if is_semafor_possible(state, x, y):
        tile = state.grid[y][x]
        tile.tip = 5
        tile.semafor = 22  # Default index from VB code
        
        # This loop replicates the VB logic of iterating through 
        # vpadnica (entry) and smer (exit) to find a valid road match
        for _ in range(4): # 1 To 4
            for _ in range(3): # 1 To 3
                state.gameTurnVpadnica = (state.gameTurnVpadnica + 1) % 4
                state.gameTurnSmer = (state.gameTurnSmer + 1) % 3
                turn_semaphore(state, x, y)
        
        # In the web version, the frontend will redraw this 
        # based on the updated tile.tip and tile.semafor
        return True
    return False

def add_random_semafor(state, x, y):
    """
    VB: Sub dodaj_kak_semafor(x, y)
    33% chance to create a semaphor (used when a new road is built).
    """
    if random.random() > 0.66:
        create_semafor(state, x, y)

def pc_intelig_moves(state):
    """
    VB: Sub pc_intelig_moves()
    The 'Emergency AI' logic that sells assets when money is low.
    """
    player = state.players[state.curpl]
    
    # Only triggers if money is low
    if player.money < 90:
        attempts = 0
        # Loop until either we've tried 55 times or we have enough cash
        while attempts < 55 and player.money <= 160:
            attempts += 1
            
            # Randomly pick coordinates (0-based)
            x = random.randint(0, state.dimx - 1)
            y = random.randint(0, state.dimy - 1)
            
            tile = state.grid[y][x]
            
            # Check if current player owns the tile and it's a property
            if tile.owner == state.curpl and tile.tip == 1:
                
                if tile.stage > 0:
                    # --- SCENARIO A: SELL HOUSE ---
                    # 70% chance to sell a house
                    if random.random() > 0.3:
                        p = sell_price(tile.stage, tile.price)
                        
                        player.money += p
                        player.stathouse -= 1
                        tile.stage -= 1
                        
                        # In Web Port, we don't 'risipolje', 
                        # we just let the JSON update the client.
                        
                else:
                    # --- SCENARIO B: SELL LAND OR CONVERT TO ROAD ---
                    # 50% chance to sell land, 50% to convert to road
                    if random.random() > 0.5:
                        # 1. Sell Land
                        
                        p = sell_price(tile.stage, tile.price)
                        
                        player.money += p
                        player.statland -= 1
                        tile.owner = 0
                        # Reset stage just in case
                        tile.stage = 0 
                    else:
                        # 2. Convert to Road (The 'Scorched Earth' move)
                        # VB: road_price returns -100, so player.money - (-100) = +100
                        p = road_price(x, y) 
                        
                        player.money -= p # Usually adds 100
                        player.statland -= 1
                        # Note: VB subtracts tile.stage from player.stathouse here
                        player.stathouse -= tile.stage
                        
                        tile.owner = 0
                        tile.stage = 0
                        tile.tip = 0 # Convert to Road
                        
                        # Update neighbors and handle visual logic
                        
                        update_road_visuals(state, x, y)
                        expand_territory(state, x, y)

def begin_map_editor(state):
    """
    VB: Sub begin_map_editor()
    Transitions the engine into Map Editor mode.
    """
    # Store the 'timer' states (Equivalent to pauseGame1/2)
    # This prevents the dice or figures from moving while editing
    state.pauseGame1 = (state.faza == 2) # Dice rolling faza
    state.pauseGame2 = (state.faza == 3) # Pawn moving faza
    
    # Force 'timers' off
    state.faza = 0 # Idle/Paused
    
    # Set modes
    state.clkMode = 33 # Map Editor Click Mode
    state.is_editor_active = True
    
    return state.to_dict()

def end_map_editor(state):
    """
    VB: Sub end_map_editor()
    Resumes game or triggers a new game depending on how the map was edited.
    """
    # 1. Capture the editor mode before clearing
    # 1: New Map, 2: Modified Current, 3: Opened/Modified
    mode = state.mapEditorMode 
    
    # 2. Reset Editor-specific flags
    state.is_editor_active = False
    state.clkMode = 0 
    
    # 3. Restore the "Timer" logic (Game Phase)
    # pauseGame1/2 were set in begin_map_editor to remember what was happening
    if state.pauseGame1:
        state.faza = 2  # Roll Dice phase
    elif state.pauseGame2:
        state.faza = 3  # Moving/Jumping phase
    else:
        state.faza = 4  # Interaction/End Turn phase
    
    # 4. Handle Mode Transitions
    if mode == 1 or mode == 3:
        # Re-initialize the session on the new map (Reset positions, players, day)
        # This calls the helper we ported earlier
        finalize_new_game_setup(state)
        
    elif mode == 2:
        # Mode 2 means we just edited the current map while playing.
        # We simply resume exactly where we were.
        pass
        
    # 5. Final Cleanup
    state.mapEditorMode = 0
    state.pauseGame1 = False
    state.pauseGame2 = False

    # Return the state object. 
    # The Route will handle to_dict(lang_data).
    return state

def edit_map_tile(state, x, y, tool_index):
    """
    VB: Sub edit_map(x, y)
    Modifies the map grid based on the currently selected editor tool.
    """
    # 1. Protect the Jail (VB: If map(x, y).tip <> 4 Then)
    # We don't want the editor to accidentally delete the starting point!
    tile = state.grid[y][x]
    if tile.tip == 4:
        return False

    # 2. Logic based on mapCurrentTool
    if tool_index == 1: # TOOL: LAND
        tile.tip = 1
        tile.stage = 0
        tile.owner = 0
        # Update surrounding roads in case this land broke a road connection
        update_neighboring_roads(state, x, y)

    elif tool_index == 0: # TOOL: ROAD
        tile.tip = 0
        tile.stage = 0
        tile.owner = 0
        # Determine which road texture to show (Corner, Straight, etc.)
        update_road_visuals(state, x, y)
        # Check if neighbors need to change their texture now
        update_neighboring_roads(state, x, y)
        # Check if we built on the edge and need to grow the 100x100 map
        expand_territory(state, x, y)

    elif tool_index == 2: # TOOL: SCHOOL
        tile.tip = 2
        tile.stage = 0
        tile.owner = 0

    elif tool_index == 3: # TOOL: JOB
        tile.tip = 3
        tile.stage = 0
        tile.owner = 0

    elif tool_index == 4: # TOOL: SEMAPHORE
        # Semaphores can only be placed on existing roads
        if tile.tip == 0:
            tile.tip = 5
            create_semafor(state, x, y)

    return True

def start_new_game_logic(state, map_choice="Random", custom_x=None, custom_y=None, player_settings=None):
    """
    VB: Sub CommandOK_Click() from newgame.frm
    Handles the full initialization of a new session.
    """
    import random
    try:
        if custom_x: custom_x = int(custom_x)
        if custom_y: custom_y = int(custom_y)
    except:
        custom_x, custom_y = None, None

    # 1. Update the metropoly.ini with the new player names/types from the UI
    # This ensures the 'defaults' are saved for the next time the app opens.
    if player_settings:
        save_metropoly_defaults(str(state.ini_path), player_settings)
    
    # 2. Handle Map Dimensions
    # VB: x = 6 + Int((15 - 1 + 1) * Rnd + 1)
    rand_x = 6 + random.randint(1, 15)
    rand_y = 5 + random.randint(1, 10)

    # 3. Initialize Map (The "Map Decision Tree")
    # If mapEditorMode is 1 (New) or 3 (Opened/Modified), we don't reload.
    if state.mapEditorMode in [1, 3]:
        # Keep current grid, just re-scan for jail/start
        set_start_coords(state)
    
    else:
        # Check if we are doing a Procedural Random map or Loading a file
        is_random = (map_choice == "Random" or not map_choice)
        
        if is_random:
            # Enforce minimums (VB: If x < 7 Then x = 7)
            x = max(7, custom_x if custom_x else rand_x)
            y = max(7, custom_y if custom_y else rand_y)
            
            # Generate procedural content (the 4-layer ASCII lines)
            map_content = generate_default_map_content(x, y)
            
            # Write to default.map (overwrite)
            with open(state.map_path, 'w', encoding='utf-8') as f:
                f.write("\n".join(map_content))
            
            # Load this newly created map into the state grid
            load_metropoly_map(state, str(state.map_path))
        
        else:
            # Load a specific map file (e.g., "city.map")
            # Map choice usually comes from the dropdown in NewGame.frm
            target_map = state.map_path.parent / map_choice
            if target_map.exists():
                load_metropoly_map(state, str(target_map))
            else:
                # Fallback to default if file is missing
                load_metropoly_map(state, str(state.map_path))

    # 4. Sync Special Coordinates (Find Jail and set startsmer)
    set_start_coords(state)

    # 5. Initialize Players
    # If no player_settings passed from UI, reload from the .ini we just saved
    if not player_settings:
        player_settings = load_metropoly_players(str(state.ini_path))
    
    # Places players at jail, sets starting money, color, and direction
    init_players_logic(state, player_settings)
    
    # 6. Reset Game Timing & Phase
    state.faza = 2          # Phase: Waiting for dice roll
    state.curpl = 1         # Start with Player 1
    state.dayOfWeek = 1     # Set to Monday
    state.buyDialogAnswer = 0
    state.status_label = state.lngg[141] + " " + state.players[1].name + state.lngg[142] # "It is Bugs's turn"

    return state.to_dict()

def set_start_coords(state):
    """
    VB: Sub set_startxy(...)
    Finds a road adjacent to the jail and sets the player's starting direction.
    1=North, 2=South, 3=West, 4=East
    """
    jx, jy = state.jailx, state.jaily
    # Convert to 0-based for grid access
    gx, gy = jx - 1, jy - 1
    
    # Directions to check: [dx, dy, smer_id]
    checks = [
        (0, 1, 2),  # South
        (0, -1, 1), # North
        (1, 0, 4),  # East
        (-1, 0, 3)  # West
    ]

    found_start = False
    for dx, dy, _ in checks:
        nx, ny = gx + dx, gy + dy
        
        # Boundary check
        if 0 <= nx < state.dimx and 0 <= ny < state.dimy:
            tile = state.grid[ny][nx]
            if tile.tip == 0 or tile.tip == 5: # Road or Semaphore
                state.startx = nx + 1
                state.starty = ny + 1
                
                # Now find which way the road continues from this spot
                # to set the 'startsmer' (Starting Direction)
                for ddx, ddy, dsmer in checks:
                    nnx, nny = nx + ddx, ny + ddy
                    if 0 <= nnx < state.dimx and 0 <= nny < state.dimy:
                        # Don't look back at the jail
                        if nnx + 1 == state.jailx and nny + 1 == state.jaily:
                            continue
                        
                        target = state.grid[nny][nnx]
                        if target.tip == 0 or target.tip == 5:
                            state.startsmer = dsmer
                            found_start = True
                            break
                if found_start: break
    
    if not found_start:
        state.startsmer = 1 # Fallback to North

def init_players_logic(state, config_players):
    """
    VB: Sub init_players()
    FIXED: Manually parses strings like '11Bugs' to avoid TypeError.
    """
    state.players = {}
    state.numpl = 0
    
    # Standard Win95 colors for the players
    colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF", "#FFFFFF"]
    
    # config_players is likely a list of strings: ["11Bugs", "11Donald", "00Elvis"...]
    for i, p_data in enumerate(config_players):
        
        # --- START OF FIX ---
        # Check if the data is a string (e.g., "11Bugs")
        if isinstance(p_data, str):
            if len(p_data) < 2: 
                continue # Skip empty or malformed lines
                
            is_active = p_data[0] == "1"
            is_pc = p_data[1] == "1"
            name = p_data[2:] # Everything after the first two digits
            pid = i + 1       # Use the loop index as the ID
            
            if not is_active:
                continue # Skip players that aren't marked as playing
        
        # If it's already a dictionary, handle it this way
        elif isinstance(p_data, dict):
            pid = p_data.get('id', i + 1)
            name = p_data.get('name', f"Player {pid}")
            is_pc = p_data.get('is_pc', False)
        # --- END OF FIX ---

        state.numpl += 1
        
        # Create the Player object
        # Ensure we don't crash if pid is high
        color_idx = (pid - 1) % len(colors)
        
        # This calls your Player class defined at the top of the file
        new_p = Player(id=pid, name=name, color=colors[color_idx], is_pc=is_pc)
        
        # Set starting positions (must have loaded map first!)
        new_p.x = state.jailx
        new_p.y = state.jaily
        new_p.smer = state.startsmer
        
        # Store in the state dictionary
        state.players[pid] = new_p

def kje_so_sosednje_ceste(state, x, y):
    """
    VB: Function kje_so_sosednje_ceste(x, y)
    Returns a string 'NSWE' where '1' means a road/semaphore neighbor exists.
    """
    # Initialize directions (North, South, West, East)
    s1, s2, s3, s4 = "0", "0", "0", "0"
    
    # Coordinates in VB are 1-based, Grid in Python is 0-based.
    # North (y-1)
    if (y - 1) > 0:
        if state.grid[y-2][x-1].tip in [0, 5]: s1 = "1"
    # South (y+1)
    if (y + 1) <= state.dimy:
        if state.grid[y][x-1].tip in [0, 5]: s2 = "1"
    # West (x-1)
    if (x - 1) > 0:
        if state.grid[y-1][x-2].tip in [0, 5]: s3 = "1"
    # East (x+1)
    if (x + 1) <= state.dimx:
        if state.grid[y-1][x].tip in [0, 5]: s4 = "1"
        
    return s1 + s2 + s3 + s4

def risi_cesto(state, x, y):
    """
    VB: Sub risi_cesto(x, y)
    Calculates which road graphic ID (0-10) to use and handles semaphore markers.
    """
    tile = state.grid[y-1][x-1]
    sosed = kje_so_sosednje_ceste(state, x, y)
    
    # Default graphic is '11' (Ground)
    kaj = 11
    
    # The Road Tiling Logic (Select Case sosed)
    mapping = {
        "1100": 3, "0011": 2, "0110": 0, "0101": 1,
        "1010": 4, "1001": 5, "0111": 6, "1011": 9,
        "1101": 8, "1110": 7, "1111": 10,
        "1000": 3, "0100": 3, "0010": 2, "0001": 2
    }
    
    if sosed == "0000":
        kaj = 2 if state.mapEditorMode > 0 else 11
    else:
        kaj = mapping.get(sosed, 11)

    # Update the Tile's primary visual ID
    tile.visual_id = kaj
    
    # Handle Semaphores (tip 5)
    # VB calls risipolje multiple times. We store these in a list for JS to layer.
    tile.extra_images = []
    
    if tile.tip == 5:
        # Get the semaphore string (e.g., "211133363942")
        s = state.semaforData[tile.semafor]
        
        # VB peels from Right to Left: East, West, South, North
        # Each marker is a 2-digit ID in the string.
        
        # East
        if sosed[3] == "1":
            tile.extra_images.append(int(s[-2:]))
        s = s[:-2]
        
        # West
        if sosed[2] == "1":
            tile.extra_images.append(int(s[-2:]))
        s = s[:-2]
        
        # South
        if sosed[1] == "1":
            tile.extra_images.append(int(s[-2:]))
        s = s[:-2]
        
        # North
        if sosed[0] == "1":
            tile.extra_images.append(int(s[-2:]))

    # Note: 'display_grid' is handled by the frontend CSS/JS in the web port.

def set_data(state):
    """
    VB: Sub set_data()
    Initializes logical game constants and semaphore rules.
    NOTE: Language-specific names (Days, Education) are now handled 
    by the Context Processor and to_dict(lang_data).
    """
    # 1. Reset Modes & Time Counters (Pure Logic)
    state.clkMode = 0
    state.dayOfWeek = 1
    state.gameTurnVpadnica = 0
    state.gameTurnSmer = 0
    state.mapEditorMode = 0
    
    # 2. The Semafor Rule Table (81 Logical Presets)
    # We use a list of 82 to allow 1-based indexing (1..81) to match VB
    state.semaforData = [""] * 82
    
    # These strings are directions (NSWE), not text. They stay in the engine.
    state.semaforData[1] = "211133363942"
    state.semaforData[2] = "211233363943"
    state.semaforData[3] = "211333363944"
    state.semaforData[4] = "212133364042"
    state.semaforData[5] = "212233364043"
    state.semaforData[6] = "212333364044"
    state.semaforData[7] = "214133364142"
    state.semaforData[8] = "214233364143"
    state.semaforData[9] = "214333364144"
    state.semaforData[10] = "231133373942"
    state.semaforData[11] = "231233373943"
    state.semaforData[12] = "231333373944"
    state.semaforData[13] = "232133374042"
    state.semaforData[14] = "232233374043"
    state.semaforData[15] = "232333374044"
    state.semaforData[16] = "234133374142"
    state.semaforData[17] = "234233374143"
    state.semaforData[18] = "234333374144"
    state.semaforData[19] = "241133383942"
    state.semaforData[20] = "241233383943"
    state.semaforData[21] = "241333383944"
    state.semaforData[22] = "242133384042"
    state.semaforData[23] = "242233384043"
    state.semaforData[24] = "242333384044"
    state.semaforData[25] = "244133384142"
    state.semaforData[26] = "244233384143"
    state.semaforData[27] = "244333384144"
    state.semaforData[28] = "311134363942"
    state.semaforData[29] = "311234363943"
    state.semaforData[30] = "311334363944"
    state.semaforData[31] = "312134364042"
    state.semaforData[32] = "312234364043"
    state.semaforData[33] = "312334364044"
    state.semaforData[34] = "314134364142"
    state.semaforData[35] = "314234364143"
    state.semaforData[36] = "314334364144"
    state.semaforData[37] = "331134373942"
    state.semaforData[38] = "331234373943"
    state.semaforData[39] = "331334373944"
    state.semaforData[40] = "332134374042"
    state.semaforData[41] = "332234374043"
    state.semaforData[42] = "332334374044"
    state.semaforData[43] = "334134374142"
    state.semaforData[44] = "334234374143"
    state.semaforData[45] = "334334374144"
    state.semaforData[46] = "341134383942"
    state.semaforData[47] = "341234383943"
    state.semaforData[48] = "341334383944"
    state.semaforData[49] = "342134384042"
    state.semaforData[50] = "342234384043"
    state.semaforData[51] = "342334384044"
    state.semaforData[52] = "344134384142"
    state.semaforData[53] = "344234384143"
    state.semaforData[54] = "344334384144"
    state.semaforData[55] = "411135363942"
    state.semaforData[56] = "411235363943"
    state.semaforData[57] = "411335363944"
    state.semaforData[58] = "412135364042"
    state.semaforData[59] = "412235364043"
    state.semaforData[60] = "412335364044"
    state.semaforData[61] = "414135364142"
    state.semaforData[62] = "414235364143"
    state.semaforData[63] = "414335364144"
    state.semaforData[64] = "431135373942"
    state.semaforData[65] = "431235373943"
    state.semaforData[66] = "431335373944"
    state.semaforData[67] = "432135374042"
    state.semaforData[68] = "432235374043"
    state.semaforData[69] = "432335374044"
    state.semaforData[70] = "434135374142"
    state.semaforData[71] = "434235374143"
    state.semaforData[72] = "434335374144"
    state.semaforData[73] = "441135383942"
    state.semaforData[74] = "441235383943"
    state.semaforData[75] = "441335383944"
    state.semaforData[76] = "442135384042"
    state.semaforData[77] = "442235384043"
    state.semaforData[78] = "442335384044"
    state.semaforData[79] = "444135384142"
    state.semaforData[80] = "444235384143"
    state.semaforData[81] = "444335384144"

def sviraj(state, fn):
    """
    VB: Sub sviraj(fn)
    Instead of playing sound, we add it to a queue for the frontend.
    """
    # In your calculate_path or move logic, call it just like VB:
    # sviraj(state, "FIGURA.WAV")
    if state.sound_enabled:
        state.audio_queue.append(fn)

def find_alternative_road_logic(state, sosed, smer, x, y):
    """
    VB: Sub find_alternative_road(sosed, smer, x, y, ByRef kamx, ByRef kamy, ByRef newsmer)
    Logic for following a road around a corner or a T-junction.
    Returns: (kamx, kamy, newsmer)
    """
    import random
    
    found = False
    kamx, kamy, newsmer = x, y, 0

    # sosed mapping (NSWE): index 0=N, 1=S, 2=W, 3=E
    
    if smer == 1: # WAS GOING NORTH
        if sosed[2] == "1": # Can turn West (Left)?
            kamx, newsmer, found = x - 1, 3, True
        
        # Desno pravilo (Right-turn probability)
        if found:
            # If we already found a left turn, 25% chance to "prefer" the right turn if available
            if random.random() > 0.75 and sosed[3] == "1":
                kamx, newsmer = x + 1, 4
        elif sosed[3] == "1": # Only right turn available
            kamx, newsmer, found = x + 1, 4, True
            
        if not found and sosed[1] == "1": # Forced to go back South
            kamy, newsmer = y + 1, 2

    elif smer == 2: # WAS GOING SOUTH
        if sosed[2] == "1": # Can turn West (Right)?
            kamx, newsmer, found = x - 1, 3, True
        if found:
            if random.random() > 0.75 and sosed[3] == "1":
                kamx, newsmer = x + 1, 4
        elif sosed[3] == "1":
            kamx, newsmer, found = x + 1, 4, True
        if not found and sosed[0] == "1": # Forced back North
            kamy, newsmer = y - 1, 1

    elif smer == 3: # WAS GOING WEST
        if sosed[0] == "1": # Can turn North (Right)?
            kamy, newsmer, found = y - 1, 1, True
        if found:
            if random.random() > 0.75 and sosed[1] == "1":
                kamy, newsmer = y + 1, 2
        elif sosed[1] == "1":
            kamy, newsmer, found = y + 1, 2, True
        if not found and sosed[3] == "1": # Forced back East
            kamx, newsmer = x + 1, 4

    elif smer == 4: # WAS GOING EAST
        if sosed[0] == "1": # Can turn North (Left)?
            kamy, newsmer, found = y - 1, 1, True
        if found:
            if random.random() > 0.75 and sosed[1] == "1":
                kamy, newsmer = y + 1, 2
        elif sosed[1] == "1":
            kamy, newsmer, found = y + 1, 2, True
        if not found and sosed[2] == "1": # Forced back West
            kamx, newsmer = x - 1, 3

    return kamx, kamy, newsmer

def pristanek(state):
    """
    VB: Sub pristanek()
    Handles interactions with neighboring tiles (Rent, Buy, School, Job).
    This is the Web-compatible version that supports async popups.
    """
    p = state.players[state.curpl]
    x, y = p.x, p.y
    
    # 1. Identify valid neighbor coordinates (1-based)
    neighbors = []
    if x > 1: neighbors.append((x - 1, y))
    if x < state.dimx: neighbors.append((x + 1, y))
    if y > 1: neighbors.append((x, y - 1))
    if y < state.dimy: neighbors.append((x, y + 1))
    
    # 2. Handle Rent (Automatic Money Transfer)
    multi_pay_msg = ""
    for nx, ny in neighbors:
        tile = state.grid[ny-1][nx-1]
        if tile.tip == 1 and tile.owner != 0 and tile.owner != p.id:
            # Transfer money (VB: pay_money logic)
            rent = calculate_rent(tile) 
            p.money -= rent
            state.players[tile.owner].money += rent
            multi_pay_msg += f"{p.name} pays {rent} to {state.players[tile.owner].name}. "

    state.status_label = multi_pay_msg if multi_pay_msg else state.lngg[90] # "End turn?"

    # 3. Handle Actions (Queue them for the JavaScript UI)
    state.pending_actions = []
    for nx, ny in neighbors:
        tile = state.grid[ny-1][nx-1]
        
        # JOB: Automatic salary update
        if tile.tip == 3:
            p.jobpayment = p.get_salary()
            
        # SCHOOL / BUY / BUILD: Requires a "Yes/No" from the player
        if tile.tip == 2 and p.izobrazba < 5:
            state.pending_actions.append({"type": "learn", "x": nx, "y": ny, "price": learn_price(p.izobrazba)})
        
        if tile.tip == 1 and tile.owner == 0:
            state.pending_actions.append({"type": "buy_land", "x": nx, "y": ny, "price": buy_land_price(tile.price)})
            
        if tile.tip == 1 and tile.owner == p.id and tile.stage < 5:
            state.pending_actions.append({"type": "build_house", "x": nx, "y": ny, "price": build_houses_price(tile.stage, tile.price)})

    # 4. Handle PC Turn
    if p.is_pc:
        pc_intelig_moves(state)

def load_language(state):
    """
    VB: Sub load_language()
    Reads metropoly.ini to find the active language and menu visibility.
    """
    if not state.ini_path.exists():
        state.selectedLanguage = "slo"
        return

    try:
        with open(state.ini_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            
        for i, line in enumerate(lines):
            if "[Language]" in line and i + 1 < len(lines):
                # VB: selectedLanguage = Left(s, Len(s) - 4) -> removes .txt
                fn = lines[i+1].strip()
                state.selectedLanguage = fn.replace(".txt", "").replace(".TXT", "")
                
                # Logic for line i+2 (the visibility mask 1111110001010)
                # In the web version, we use this to filter the dropdown in Jinja
                if i + 2 < len(lines):
                    state.language_visibility_mask = lines[i+2].strip()
                break
    except Exception as e:
        print(f"⚓ ERROR load_language: {e}")

def switch_language(state):
    """
    VB: Sub switch_language()
    Reads the selected language TXT file and constructs state.lang_dict.
    """
    # 1. Path resolution
    root_folder = Path(__file__).parent.parent.parent
    lang_file = root_folder / "static" / "metropoly" / "assets" / "languages" / f"{state.selectedLanguage}.txt"

    # 2. Read the first 150 lines into a 1-indexed list (Safe from KeyErrors)
    # Using a list of 151 empty strings ensures state.lngg[70] always exists
    state.lngg = [""] * 151
    try:
        with open(lang_file, 'r', encoding='utf-8', errors='ignore') as f:
            for i, line in enumerate(f, 1):
                if i > 150: break
                state.lngg[i] = line.strip().replace("&", "")
    except Exception as e:
        print(f"⚓ ERROR switch_language: {e}")

    l = state.lngg # Shortcut helper

    # 3. Build the lang_dict COMPLETELY in one assignment
    # This prevents the AttributeError: 'MetropolyGame' has no attribute 'lang_dict'
    state.lang_dict = {
        "menu": {
            "language_title": l[14] or "Language",
            "app_title": l[15] or "Metropoly",
            "file": l[17], "new": l[18], "open": l[19], "save": l[20], 
            "save_map": l[21], "exit_map_editor": l[22], "exit": l[23],
            "orders": l[25], "build_road": l[26], "sell": l[27], 
            "semaphores": l[28], "create_semaphore": l[29], 
            "remove_semaphore": l[30], "rotate_semaphores": l[31], "end_turn": l[32],
            "options": l[34], "fast": l[35], "show_grid": l[36], 
            "auto_end_turn": l[37], "sound": l[38], "graphics": l[39],
            "tools": l[41], "map_editor": l[42],
            "help": l[44], "contents": l[45], "about": l[46], "register": l[47],
            
            # --- INJECT HELP LABELS HERE (Indices 70-81) ---
            "help_title": l[70],
            "help_l0": l[71], "help_l1": l[72], "help_l2": l[73],
            "help_l3": l[74], "help_l4": l[75], "help_l5": l[76],
            "help_l6": l[77], "help_l7": l[78], "help_l8": l[79],
            "help_l9": l[80], "help_l10": l[81],
            "ok": l[53]
        },
        "dialog": {
            "new_game": l[49], "x": l[50], "y": l[51], "map": l[52],
            "ok": l[53], "cancel": l[54], "filename_label": l[59]
        },
        "turn": {
            "msg_turn_prefix": l[141], 
            "msg_turn_suffix": l[142],
            "yes": l[144], "no": l[145]
        }
    }

    # 4. Final step: link 'm' for the template context
    state.m = state.lang_dict["menu"]

def calculate_rent(stage: int, price: int) -> int:
    """VB: Function pay_money_price(stage, price)"""
    if stage == 0:
        return int(price / 5 * 2)
    return (stage + 1) * price

def buy_land_price(price: int) -> int:
    """VB: Function buy_land_price(price)"""
    return price * 2

def build_houses_price(stage: int, price: int) -> int:
    """VB: Function build_houses_price(stage, price)"""
    return price * 2

def earn_price(izobrazba: int) -> int:
    """VB: Function earn_price(izobrazba)"""
    # Map for Select Case izobrazba
    salaries = {
        0: 50,
        1: 80,
        2: 100,
        3: 150,
        4: 250,
        5: 300
    }
    return salaries.get(izobrazba, 50)

def learn_price(izobrazba: int) -> int:
    """VB: Function learn_price(izobrazba)"""
    return 50 + izobrazba * 20

def sell_price(stage: int, price: int) -> int:
    """VB: Function sell_price(stage, price)"""
    pl = buy_land_price(price)
    ph = build_houses_price(stage, price)
    
    if stage == 0:
        return int(1.5 * pl)  # VB: Int(3 / 2 * pl)
    elif stage == 1:
        return int(0.5 * ph)  # VB: Int(1 / 2 * ph)
    elif stage == 2:
        return int(0.75 * ph) # VB: Int(3 / 4 * ph)
    elif stage == 3:
        return ph
    elif stage == 4:
        return int(1.25 * ph) # VB: Int(5 / 4 * ph)
    elif stage == 5:
        return int(1.5 * ph)  # VB: Int(6 / 4 * ph)
    return 0

def road_price(x: int, y: int) -> int:
    """VB: Function road_price(x, y)"""
    return -100

def rotate_semafor_price() -> int:
    """VB: Function rotateSemafor_price()"""
    return 5

def create_semaphor_price(x: int, y: int) -> int:
    """VB: Function create_semaphor_price(x, y)"""
    return 15

def delete_semaphor_price(x: int, y: int) -> int:
    """VB: Function delete_semaphor_price(x, y)"""
    return 50

def fill_combo_logic(state):
    """
    VB: Sub fill_combo()
    Scans the engine directory for all available .map files.
    """
    
    # We look in the same folder where the engine script lives
    engine_dir = state.map_path.parent
    
    # Get all files ending in .map
    # Replicates File1.Pattern = "*.map"
    try:
        map_files = [f for f in os.listdir(engine_dir) if f.lower().endswith(".map")]
        # Replicates the loop adding items to Combo1
        state.map_list = sorted(map_files)
    except Exception as e:
        print(f"⚓ ERROR fill_combo_logic: {e}")
        state.map_list = ["default.map"]

def mnu_end_turn_click(state):
    """
    VB: Private Sub mnuEndTurn_Click()
    Handles the transition to the next player and the global weekly cycle.
    """
    # 🔒 PHASE GUARD: Only allow ending turn if move is finished
    if state.faza == 4:
        state.curpl += 1
        
        if state.curpl > state.numpl:
            # --- NOV DAN (New Day Logic) ---
            state.curpl = 1
            state.dayOfWeek += 1
            
            if state.dayOfWeek > 7:
                state.dayOfWeek = 1
            
            # Update UI Status with Day Name (Monday, etc.)
            # VB: LabelStatus.Caption = dayOfWeekName(dayOfWeek)
            if 0 < state.dayOfWeek < 8:
                state.status_label = state.dayOfWeekName[state.dayOfWeek]
            
            # Wednesday (3) or Saturday (6): Rotate all traffic lights
            if state.dayOfWeek == 3 or state.dayOfWeek == 6:
                turn_semaphores(state)
                
            # Sunday (7): Distribute weekly wages
            if state.dayOfWeek == 7:
                pay_wages(state)
        
        # Final Step: Initialize the next player's phase (roll dice)
        next_player(state)

def shift_map_owners(state, i: int, o: int):
    """
    VB: Sub shift_map_owners(i, o)
    Re-assigns ownership of all tiles owned by player 'o' to player 'i'.
    """
    for row in state.grid:
        for tile in row:
            # tip 1 is a property
            if tile.tip == 1 and tile.owner == o:
                tile.owner = i
            
def pay_wages(state):
    """
    VB: Sub pay_wages()
    Distributes job payments every Sunday and builds a summary report.
    """
    summary = []
    # VB: For i = 1 To numpl
    for pid, p in state.players.items():
        # Update money
        p.money += p.jobpayment
        
        # Build the summary line using lngg indices
        # VB: player(i).statland & lngg(109) & player(i).stathouse & lngg(110) & player(i).ime
        line = (f"{p.statland}{state.lngg[109]} "
                f"{p.stathouse}{state.lngg[100]} " # Note: check if 100 or 110 matches house suffix
                f"{p.name}")
        
        if p.jobpayment > 0:
            # VB: lngg(111) & player(i).jobpayment & lngg(89)
            line += f" {state.lngg[111]} {p.jobpayment}{state.lngg[89]}"
            
        summary.append(line)
    
    # Store the result in status_label to be displayed in the sidebar
    # VB: ok = MsgBox(s, vbOKOnly, lngg(112))
    header = state.lngg[112] # "End of the week" or "Wages"
    state.status_label = f"--- {header} ---\n" + "\n".join(summary)

def mnu_road_click(state):
    """
    VB: Private Sub mnuRoad_Click()
    Enables the mode where clicking a property converts it to a road.
    """
    p = state.players[state.curpl]
    
    # tip 0 means human player
    if p.is_pc == False:
        # Re-use our previously ported display function
        display_land_info(state, p.x, p.y)
        
        # VB: LabelStatus.Caption = lngg(113)
        state.status_label = state.lngg[113]
        
        # Set click mode to 2 (Build Road)
        state.clkMode = 2

def popravi_sosednje_ceste(state, x: int, y: int):
    """
    VB: Sub popravi_sosednje_ceste(x, y)
    Triggers visual updates for neighbors when a road is created/changed.
    """
    # Get NSWE road adjacency for current tile
    sosed = kje_so_sosednje_ceste(state, x, y)
    
    # 1. Check North (Mid index 1)
    if y > 1 and sosed[0] == "1":
        risi_cesto(state, x, y - 1)
        add_random_semafor(state, x, y - 1)
        
    # 2. Check South (Mid index 2)
    if y < state.dimy and sosed[1] == "1":
        risi_cesto(state, x, y + 1)
        add_random_semafor(state, x, y + 1)
        
    # 3. Check West (Mid index 3)
    if x > 1 and sosed[2] == "1":
        risi_cesto(state, x - 1, y)
        add_random_semafor(state, x - 1, y)
        
    # 4. Check East (Mid index 4)
    if x < state.dimx and sosed[3] == "1":
        risi_cesto(state, x + 1, y)
        add_random_semafor(state, x + 1, y)

def handle_map_click(state, x, y):
    """
    VB: Combined Logic of Form_MouseUp and Form_Click.
    Handles clicking on the board based on the current 'clkMode'.
    """
    # 1. Boundary Check (1-based logic)
    if x < 1 or x > state.dimx or y < 1 or y > state.dimy:
        return

    p = state.players[state.curpl]
    # Grid access (0-based)
    tile = state.grid[y-1][x-1]
    l = state.lngg # Language lines shortcut

    # --- Case 0: Land Info ---
    if state.clkMode == 0:
        display_land_info(state, x, y)
        # Note: display_land_info updates state.status_label

    # --- Case 1: Sell (House or Land) ---
    elif state.clkMode == 1:
        if tile.owner == state.curpl:
            p_value = sell_price(tile.stage, tile.price)
            
            # Since we can't 'MsgBox' and wait on the server, we send 
            # a 'pending_action' to the browser to show the Yes/No dialog.
            # The JS will send back a 'confirm_sell' event if user clicks Yes.
            msg = f"{l[100]} {p_value}{l[101]}" # "Do you want to sell...?"
            state.pending_actions.append({
                "type": "confirm_sell",
                "x": x, "y": y,
                "price": p_value,
                "msg": msg
            })
        else:
            # VB: Beep
            state.clkMode = 0
            state.status_label = ""

    # --- Case 2: Build Road ---
    elif state.clkMode == 2:
        state.status_label = ""
        # Only build on owned property
        if tile.owner == state.curpl and tile.tip == 1:
            p_cost = road_price(x, y) # returns -100
            
            # Record houses lost before clearing tile
            houses_lost = tile.stage
            
            # Convert tile back to road
            tile.stage = 0
            tile.owner = 0
            tile.tip = 0
            
            # Update visuals and connections
            risi_cesto(state, x, y)
            popravi_sosednje_ceste(state, x, y)
            
            # Update player stats (VB: money - (-100) = +100)
            p.money -= p_cost
            p.statland -= 1
            p.stathouse -= houses_lost
            
            state.status_label = l[103] # "Road was built"
            expand_terit(state, x, y)
            
        state.clkMode = 0 # Reset mode

    # --- Case 3: Create Semaphore ---
    elif state.clkMode == 3:
        state.status_label = ""
        if tile.tip == 0: # Road
            p_cost = create_semaphor_price(x, y)
            if p.money >= p_cost:
                if semafor_je_mozen(state, x, y):
                    create_semaphor(state, x, y)
                    p.money -= p_cost
                    state.status_label = l[104] # "Semaphore was built"
        state.clkMode = 0

    # --- Case 4: Remove Semaphore ---
    elif state.clkMode == 4:
        state.status_label = ""
        if tile.tip == 5: # Semaphore
            p_cost = delete_semaphor_price(x, y)
            if p.money >= p_cost:
                tile.tip = 0
                tile.semafor = 0
                risi_cesto(state, x, y)
                p.money -= p_cost
                state.status_label = l[105] # "Semaphore was removed"
        state.clkMode = 0

    # --- Case 33: Map Editor Tool ---
    elif state.clkMode == 33:
        # Re-use the editor logic we ported earlier
        edit_map_tile(state, x, y, state.mapCurrentTool)

def finalize_new_game_setup(state):
    """
    VB: Final part of mnuNew_Click()
    Selects starting player and begins turn.
    """
    # 1. Reset logic modes
    state.clkMode = 0
    state.dayOfWeek = 1
    state.gameTurnVpadnica = 0
    state.gameTurnSmer = 0
    
    # 2. Pick random starting player (VB: Int(numpl * Rnd + 1))
    if state.numpl > 0:
        state.curpl = random.randint(1, state.numpl)
        
        # 3. Trigger next_player logic to start the first dice roll phase
        # This sets faza = 2
        next_player(state) 
    
    return state.to_dict()



# frmBuyDialog.frm
def execute_pending_action(state, action_data):
    """
    VB: The logic that ran after 'If ok = vbYes Then'
    Processes the actual money transaction and property update.
    """
    p = state.players[state.curpl]
    a_type = action_data.get("type")
    x, y = action_data.get("x"), action_data.get("y")
    tile = state.grid[y-1][x-1]
    
    if a_type == "buy_land":
        price = buy_land_price(tile.price)
        if p.money >= price:
            p.money -= price
            p.statland += 1
            tile.owner = p.id
            state.status_label = f"{p.name} {state.lngg[93]} {price}{state.lngg[85]}."

    elif a_type == "build_house":
        price = build_houses_price(tile.stage, tile.price)
        if p.money >= price:
            p.money -= price
            p.stathouse += 1
            tile.stage += 1
            # Update visual_id to show the house (h1, h2...)
            tile.visual_id = 11 + tile.stage 
            state.status_label = f"{p.name} {state.lngg[94]} {tile.stage} {state.lngg[95]} {price}{state.lngg[85]}."

    elif a_type == "learn":
        price = learn_price(p.izobrazba)
        if p.money >= price:
            p.money -= price
            p.izobrazba += 1
            state.status_label = f"{p.name} level up to {state.izobrazbaNaziv[p.izobrazba]}."

    # After any purchase, clear the queue and show status
    state.pending_actions = [] 
    return state.to_dict()

def save_map_to_disk(state, filename):
    """
    VB: Sub save_game(fn, True)
    Writes the current grid into a 4-layer .map file.
    """
    if not filename.endswith(".map"):
        filename += ".map"
        
    path = state.map_path.parent / filename
    lines = []

    # Layer 0: Dimensions
    lines.append(str(state.dimx))
    lines.append(str(state.dimy))

    # Layer 1: Tip & Semaphore
    for row in state.grid:
        row_str = ""
        for tile in row:
            if tile.tip == 5:
                row_str += chr(tile.semafor + 52)
            else:
                row_str += str(tile.tip)
        lines.append(row_str)

    # Layer 2: Price (ASCII mapping)
    for row in state.grid:
        row_str = "".join(chr(tile.price + 45) for tile in row)
        lines.append(row_str)

    # Layer 3: Stage
    for row in state.grid:
        row_str = "".join(str(tile.stage) for tile in row)
        lines.append(row_str)

    # Layer 4: Owner
    for row in state.grid:
        row_str = "".join(str(tile.owner) for tile in row)
        lines.append(row_str)

    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))
        return True
    except Exception as e:
        print(f"⚓ ERROR saving map: {e}")
        return False

def mnu_sell_click(state):
    """
    VB: Private Sub mnuSell_Click()
    Enables Sell Mode for the current human player.
    """
    p = state.players[state.curpl]
    
    # tip 0 = Human Player
    if not p.is_pc:
        # VB: LabelStatus.Caption = lngg(100) -> "Click on land you want to sell"
        state.status_label = state.lngg[100]
        # Set click mode to 1 (Sell)
        state.clkMode = 1

def execute_sell_logic(state, x, y):
    """
    Handles the actual sale when a tile is clicked while clkMode == 1.
    """
    tile = state.grid[y-1][x-1]
    p = state.players[state.curpl]
    
    # 1. THE JAIL SHIELD: Tip 4 cannot be sold
    if tile.tip == 4:
        state.status_label = "Cannot sell the Jail!"
        state.clkMode = 0
        return False

    # 2. Ownership Check
    if tile.owner != state.curpl:
        state.status_label = "You don't own this!"
        state.clkMode = 0
        return False

    # 3. Calculate Refund (using the sell_price function we ported earlier)
    refund = sell_price(tile.stage, tile.price)

    # 4. Sell Houses First (VB Logic)
    if tile.stage > 0:
        tile.stage -= 1
        p.stathouse -= 1
        state.status_label = f"Sold house for {refund}{state.lngg[85]}"
    else:
        # 5. Sell Land if no houses are left
        tile.owner = 0
        p.statland -= 1
        state.status_label = f"Sold land for {refund}{state.lngg[85]}"

    # Update Wallet
    p.money += refund
    
    # Reset mode to Info (Mode 0)
    state.clkMode = 0
    return True

