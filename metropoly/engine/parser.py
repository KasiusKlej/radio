def load_metropoly_map(file_path):
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
    
    dimx = int(lines[0])
    dimy = int(lines[1])
    
    # Initialize a grid of Tile objects
    grid = [[Tile(x, y) for x in range(dimx)] for y in range(dimy)]
    
    cursor = 2
    # 1. Parse Types & Semafors
    for y in range(dimy):
        row_str = lines[cursor]
        for x, char in enumerate(row_str):
            val = ord(char)
            if val < 53: # '0' through '4'
                grid[y][x].tip = int(char)
            else:
                grid[y][x].tip = 5
                grid[y][x].semafor = val - 52
        cursor += 1
        
    # 2. Parse Prices ('A'-'Z')
    for y in range(dimy):
        row_str = lines[cursor]
        for x, char in enumerate(row_str):
            grid[y][x].price = ord(char) - 45
        cursor += 1
        
    # 3. Parse Stages
    for y in range(dimy):
        row_str = lines[cursor]
        for x, char in enumerate(row_str):
            grid[y][x].stage = int(char)
        cursor += 1
        
    # 4. Parse Owners
    for y in range(dimy):
        row_str = lines[cursor]
        for x, char in enumerate(row_str):
            grid[y][x].owner = int(char)
        cursor += 1
        
    return grid, dimx, dimy

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


import os
from pathlib import Path

def metropoly_language_parser(lang_dir: Path, filename: str) -> dict:
    """
    Parses Metropoly line-based language files.
    Renames 3-letter codes internally and strips '&' mnemonics.
    """
    if not filename.lower().endswith(".txt"):
        filename += ".txt"

    path = lang_dir / filename
    if not path.exists():
        # Fallback to eng.txt if requested language is missing
        path = lang_dir / "eng.txt"

    with path.open("r", encoding="utf-8", errors="ignore") as f:
        # We keep the raw list to access by index (Metropoly style)
        # but we strip the '&' from every line immediately.
        raw_lines = [line.strip().replace("&", "") for line in f]

    # Helper to safely get a line by index (1-based to match VB logic)
    def get_l(idx):
        return raw_lines[idx-1] if 0 < idx <= len(raw_lines) else ""

    lang = {}

    # --- A. Menu & UI (Lines 1-50) ---
    lang["menu"] = {
        "language_title": get_l(14),
        "app_title": get_l(15),
        "file": get_l(17),
        "new": get_l(18),
        "open": get_l(19),
        "save": get_l(20),
        "exit": get_l(23),
        "orders": get_l(25),
        "road": get_l(26),
        "sell": get_l(27),
        "semafors": get_l(28),
        "end_turn": get_l(32),
    }

    # --- B. Game Phrases (Lines 83-125) ---
    lang["phrases"] = {
        "currency": get_l(85),         # "$"
        "per_week": get_l(89),         # "$/week"
        "ask_end_turn": get_l(90),     # "End turn?"
        "pays": get_l(91),             # "pays"
        "buys_land": get_l(93),        # "buys land for"
        "visit_school": get_l(98),     # "Do you want visit school for"
        "out": get_l(106),             # "is out"
        "winner": get_l(107),          # "The winner is"
        "week_end": get_l(127),        # "End of the week"
    }

    # --- C. Time & Education (Lines 128-140) ---
    lang["days"] = [
        get_l(128), get_l(129), get_l(130), get_l(131), 
        get_l(132), get_l(133), get_l(134)
    ]
    
    lang["education"] = [
        get_l(135), get_l(136), get_l(137), get_l(138), get_l(139)
    ]

    # --- D. Interaction (Lines 141-145) ---
    lang["turn"] = {
        "prefix": get_l(141),          # "It is"
        "suffix": get_l(142),          # "'s turn"
        "yes": get_l(144),
        "no": get_l(145)
    }

    return lang

import configparser

def load_metropoly_config(ini_path):
    """Parses metropoly.ini for default players and language."""
    players = []
    # Using a simple text parser because .ini has custom formatting
    with open(ini_path, 'r') as f:
        content = f.read()
    
    # Simple extraction for players
    import re
    player_matches = re.findall(r'(\d)(\d)([^\n]+)', content)
    for i, (active, is_ai, name) in enumerate(player_matches):
        if active == "1":
            players.append({
                "id": i + 1,
                "is_pc": is_ai == "1",
                "name": name.strip()
            })
    return players

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

# metropoly/engine/parser.py

def load_metropoly_config(ini_path):
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

# metropoly/engine/parser.py

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

import random
import string

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

# metropoly/engine/parser.py
####from .model import Tile

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

# metropoly/engine/parser.py

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

