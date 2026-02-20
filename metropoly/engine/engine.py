# engine/engine.py

def next_player(state):
    """Moves the turn to the next active player."""
    state.curpl += 1
    if state.curpl > state.numpl:
        state.curpl = 1
    
    # Check if player is bankrupt/inactive (to be implemented)
    # If state.players[state.curpl].is_bankrupt: return next_player(state)
    
    return state.curpl

def get_road_adjacency(state, x, y):
    """
    Equivalent to VB 'kje_so_sosednje_ceste'.
    Returns a string 'NSWE' where 1 is road/semafor, 0 is empty.
    """
    res = ""
    # North (y-1)
    res += "1" if y > 0 and state.grid[y-1][x].tip in [0, 5] else "0"
    # South (y+1)
    res += "1" if y < state.dimy-1 and state.grid[y+1][x].tip in [0, 5] else "0"
    # West (x-1)
    res += "1" if x > 0 and state.grid[y][x-1].tip in [0, 5] else "0"
    # East (x+1)
    res += "1" if x < state.dimx-1 and state.grid[y][x+1].tip in [0, 5] else "0"
    
    return res

# engine/engine.py
import random

def roll_dice(state):
    """
    Calculates the outcome of a turn.
    Returns the two dice values and the total.
    """
    d1 = random.randint(1, 6)
    d2 = random.randint(1, 6)
    
    state.kocka = d1 + d2
    state.faza = 3 # Ready to move
    
    return {
        "dice": [d1, d2],
        "total": state.kocka,
        "frames": 10 # Tell JS to animate for 10 frames
    }

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

def process_move(state):
    """
    Simulates the entire movement phase for the current player.
    Returns a list of 'steps' for the JS frontend to animate.
    """
    player = state.players[state.curpl]
    steps = []
    
    for _ in range(state.kocka):
        # 1. Determine next coordinate
        next_x, next_y = player.x, player.y
        sosed = get_road_adjacency(state, player.x, player.y) # NSWE string
        
        # Try to move in current direction
        can_move = False
        if sosed[player.smer - 1] == "1":
            can_move = True
            if player.smer == 1: next_y -= 1
            elif player.smer == 2: next_y += 1
            elif player.smer == 3: next_x -= 1
            elif player.smer == 4: next_x += 1
        
        # 2. If road ends, find alternative (port of find_alternative_road)
        if not can_move:
            next_x, next_y, new_smer = find_alternative(state, sosed, player.smer, player.x, player.y)
            player.smer = new_smer
            
        # 3. Apply Semafor logic if landing on tip=5
        tile = state.grid[next_y][next_x]
        if tile.tip == 5:
            # Map entry direction to semaphorData index
            if player.y - next_y == -1: idx = 0 # Came from North
            elif player.y - next_y == 1: idx = 1 # Came from South
            elif player.x - next_x == -1: idx = 2 # Came from West
            else: idx = 3 # Came from East
            
            # Lookup direction from semaforData (81 presets)
            rule = state.semaforData[tile.semafor]
            player.smer = int(rule[idx])

        # Update player position
        player.x, player.y = next_x, next_y
        steps.append({"x": player.x, "y": player.y})

    return steps

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

def turn_semaphore_tile(state, x, y):
    """Port of turn_semaphore(x, y)"""
    tile = state.grid[y][x]
    vpadnica = state.gameTurnVpadnica  # 0:N, 1:S, 2:W, 3:E
    smer_idx = state.gameTurnSmer     # 0, 1, 2
    
    sosed = get_road_adjacency(state, x, y)
    if sosed[vpadnica] == "0":
        return # No road coming from this direction
    
    # Get the current 4-digit rule (e.g., "2341")
    current_rule = state.semaforData[tile.semafor][:4]
    
    # Mapping table for the "Mid" logic in VB
    options = ["234", "134", "124", "123"]
    new_dir = options[vpadnica][smer_idx]
    
    # Check if the exit road actually exists
    if sosed[int(new_dir)-1] == "1":
        # Build the new 4-digit string
        rule_list = list(current_rule)
        rule_list[vpadnica] = new_dir
        new_rule_str = "".join(rule_list)
        
        # Find the index of this rule in semaphorData
        for i, data in enumerate(state.semaforData):
            if data.startswith(new_rule_str):
                tile.semafor = i
                break

def end_turn(state):
    state.curpl += 1
    if state.curpl > state.numpl:
        state.curpl = 1
        state.dayOfWeek += 1
        
        if state.dayOfWeek > 7:
            state.dayOfWeek = 1
            
        # Weekly Events
        if state.dayOfWeek in [3, 6]: # Wednesday, Saturday
            rotate_all_semaphores(state)
            
        if state.dayOfWeek == 7: # Sunday
            distribute_weekly_wages(state)

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

import random
import os

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

def mnu_exit_click(state):
    """
    VB: End
    Web: handled by route via redirect
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

def mnu_create_semafors_click(state):
    """
    Port of mnuCreateSemafors_Click
    """
    player = state.players[state.curpl]

    if player.tip == 0:  # road
        display_land_info(state, player.x, player.y)
        state.status_label = state.lang_dict.get("83", "")
        state.clkMode = 3

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
    
    if player.tip == 0:
        display_land_info(state, player.x, player.y)
        state.status_text = lngg(84)
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
import random

def timer_met_kocke_tick(state):
    display_status(state)  # dice background
    
    kocka1 = random.randint(1, 6)
    kocka2 = random.randint(1, 6)
    
    x1 = 35 * 3
    y1 = (state.curpl - 1) * 35
    x2 = 35 * 4
    
    state.tile_draw_queue.append({
        "tile_id": 26 + kocka1,
        "x": x1,
        "y": y1
    })
    
    state.tile_draw_queue.append({
        "tile_id": 26 + kocka2,
        "x": x2,
        "y": y1
    })
    
    # Play dice sound once
    if state.cakajKocko == state.cakajKocko_start:
        play_sound(state, "KOCKA", volume=0.35)
    
    state.cakajKocko -= 1
    
    if state.cakajKocko <= 0:
        state.timer_met_kocke_enabled = False
        state.kocka = kocka1 + kocka2
        state.faza = 3
        state.timer_skok_figure_enabled = True

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

import random

def find_alternative_road(sosed, smer, x, y):
    """
    Returns (kamx, kamy, newsmer) or (None, None, 0) if not found
    smer: 1=up, 2=down, 3=left, 4=right
    sosed: string "nswe"
    """
    found = False
    kamx = kamy = None
    newsmer = 0

    def has(i):
        return sosed[i - 1] == "1"

    if smer == 1:  # up
        if has(3):  # left
            kamx, kamy, newsmer = x - 1, y, 3
            found = True
        if found:
            if random.random() > 0.25 and has(4):
                kamx, kamy, newsmer = x + 1, y, 4
        elif has(4):
            kamx, kamy, newsmer = x + 1, y, 4
            found = True
        if not found and has(2):  # back
            kamx, kamy, newsmer = x, y + 1, 2

    elif smer == 2:  # down
        if has(3):
            kamx, kamy, newsmer = x - 1, y, 3
            found = True
        if found:
            if random.random() > 0.25 and has(4):
                kamx, kamy, newsmer = x + 1, y, 4
        elif has(4):
            kamx, kamy, newsmer = x + 1, y, 4
            found = True
        if not found and has(1):
            kamx, kamy, newsmer = x, y - 1, 1

    elif smer == 3:  # left
        if has(1):
            kamx, kamy, newsmer = x, y - 1, 1
            found = True
        if found:
            if random.random() > 0.25 and has(2):
                kamx, kamy, newsmer = x, y + 1, 2
        elif has(2):
            kamx, kamy, newsmer = x, y + 1, 2
            found = True
        if not found and has(4):
            kamx, kamy, newsmer = x + 1, y, 4

    elif smer == 4:  # right
        if has(1):
            kamx, kamy, newsmer = x, y - 1, 1
            found = True
        if found:
            if random.random() > 0.25 and has(2):
                kamx, kamy, newsmer = x, y + 1, 2
        elif has(2):
            kamx, kamy, newsmer = x, y + 1, 2
            found = True
        if not found and has(3):
            kamx, kamy, newsmer = x - 1, y, 3

    return kamx, kamy, newsmer


def next_player(state):
    state.faza = 1  # next player

    # bankruptcy check
    if state.players[state.curpl].money < 0:
        eliminate_player(state)
        state.faza = 1

    if state.numpl > 1:
        state.faza = 2  # dice roll
        state.kocka = 0
        state.cakajKocko = 5 + random.randint(1, 6)

        return {
            "action": "roll_dice",
            "sound": "dice"
        }

    return {"action": "idle"}


def try_end_turn(state):
    if state.faza != 4:
        return {"error": "not_ready"}

    end_turn(state)
    return next_player(state)

def pristanek(state):
    p = state.players[state.curpl]
    x, y = p.x, p.y

    multiPay = []

    def visit(sx, sy):
        pay_money(state, sx, sy, multiPay)
        earn_learn(state, sx, sy)
        build_houses(state, sx, sy)
        buy_land(state, sx, sy)

    if x > 1: visit(x - 1, y)
    if x < state.dimx: visit(x + 1, y)
    if y > 1: visit(x, y - 1)
    if y < state.dimy: visit(x, y + 1)

    state.faza = 4

    return {
        "status": "landed",
        "multiPay": ". ".join(multiPay) if multiPay else None,
        "auto_end": (
            p.tip == 1 or state.options.auto_end_turn
        )
    }

def pay_money(state, sx, sy, multiPay):
    tile = state.map[sx][sy]
    cur = state.curpl

    if tile.tip != 1:
        return

    if tile.owner == 0 or tile.owner == cur:
        return

    p = pay_money_price(tile.stage, tile.price)

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

import random

def is_semafor_possible(state, x, y):
    """
    VB: Function semafor_je_mozen(x, y)
    Checks if there are more than 2 roads connecting to this tile.
    (Semaphors only appear at T-junctions or Crossroads).
    """
    # Assuming get_road_adjacency returns "NSWE" string like "1101"
    # We defined this in our previous session
    from .engine import get_road_adjacency 
    sosed = get_road_adjacency(state, x, y)
    
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
        
        # We need the turn_semaphore_tile function we wrote earlier
        from .engine import turn_semaphore_tile
        
        # This loop replicates the VB logic of iterating through 
        # vpadnica (entry) and smer (exit) to find a valid road match
        for _ in range(4): # 1 To 4
            for _ in range(3): # 1 To 3
                state.gameTurnVpadnica = (state.gameTurnVpadnica + 1) % 4
                state.gameTurnSmer = (state.gameTurnSmer + 1) % 3
                turn_semaphore_tile(state, x, y)
        
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


import random

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
                        from .model import sell_price # Assuming logic from MoneyParameters.bas
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
                        from .model import sell_price
                        p = sell_price(tile.stage, tile.price)
                        
                        player.money += p
                        player.statland -= 1
                        tile.owner = 0
                        # Reset stage just in case
                        tile.stage = 0 
                    else:
                        # 2. Convert to Road (The 'Scorched Earth' move)
                        # VB: road_price returns -100, so player.money - (-100) = +100
                        from .model import road_price
                        p = road_price(x, y) 
                        
                        player.money -= p # Usually adds 100
                        player.statland -= 1
                        # Note: VB subtracts tile.stage from player.stathouse here
                        player.stathouse -= tile.stage
                        
                        tile.owner = 0
                        tile.stage = 0
                        tile.tip = 0 # Convert to Road
                        
                        # Update neighbors and handle visual logic
                        from .engine import update_road_visuals, expand_territory
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
    mode = state.mapEditorMode # 1=New, 2=Modified, 3=Opened/Modified
    
    # Reset modes
    state.is_editor_active = False
    state.clkMode = 0 
    
    # Restore 'timer' logic (faza)
    if state.pauseGame1: state.faza = 2
    elif state.pauseGame2: state.faza = 3
    else: state.faza = 4 # Default to waiting for turn end
    
    # VB Logic for MapEditorMode transitions
    if mode == 1 or mode == 3:
        # Trigger 'New Game' logic on the newly edited map
        from .engine import reset_game_state
        reset_game_state(state)
    elif mode == 2:
        # Simply continue where we left off
        pass
        
    state.mapEditorMode = 0
    return state.to_dict()

# metropoly/engine/engine.py
#from .engine import update_road_visuals, update_neighboring_roads, create_semafor, expand_territory

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

# metropoly/engine/engine.py
import random
####from .parser import load_metropoly_map, generate_default_map, load_metropoly_config
####from .engine import set_start_coords, init_players

def start_new_game_logic(state, map_choice="Random", custom_x=None, custom_y=None):
    """
    VB: Sub CommandOK_Click()
    Handles the initialization of a new game session.
    """
    
    # 1. Random dimension logic (VB: 6 + Rnd(15) and 5 + Rnd(10))
    rand_x = 6 + random.randint(1, 15)
    rand_y = 5 + random.randint(1, 10)

    # 2. Check if we are coming from the Map Editor (Mode 1 or 3)
    if state.mapEditorMode in [1, 3]:
        # No need to load a file; the map is already in state.grid
        # Just find the start/jail coordinates
        set_start_coords(state)
    
    else:
        # 3. Handle Map Loading / Generation
        if map_choice == "Random" or not map_choice:
            # Enforce minimums (VB: x < 7 Then x = 7)
            x = custom_x if (custom_x and custom_x >= 7) else rand_x
            y = custom_y if (custom_y and custom_y >= 7) else rand_y
            
            # Generate the procedural map and load it
            generate_default_map(state, x, y) 
            load_metropoly_map(state, "default.map")
        
        else:
            # Load the specific map file chosen from the "Combo1" dropdown
            # (e.g., "city.map")
            load_metropoly_map(state, map_choice)

    # 4. Finalize Setup
    set_start_coords(state)
    init_players(state) # Pulls names/types from metropoly.ini
    
    # 5. Reset Game State for a fresh start
    state.faza = 2      # Phase: Waiting for dice roll
    state.curpl = 1     # Start with player 1
    state.dayOfWeek = 1 # Monday
    
    return state.to_dict()


def create_random_game_map(state, x, y):
    from .parser import generate_default_map_content, parse_map_from_lines
    
    # 1. Generate the ASCII lines
    map_lines = generate_default_map_content(x, y)
    
    # 2. (Optional) Save to default.map so it persists
    with open("metropoly/engine/default.map", "w") as f:
        f.write("\n".join(map_lines))
    
    # 3. Load these lines into the current game state
    grid, dimx, dimy = parse_map_from_lines(map_lines)
    state.grid = grid
    state.dimx = dimx
    state.dimy = dimy


# metropoly/engine/engine.py

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

####from .model import Player

def init_players_logic(state, config_players):
    """
    VB: Sub init_players()
    config_players is a list of dicts from the .ini parser
    """
    state.players = {}
    state.numpl = 0
    
    for p_data in config_players:
        state.numpl += 1
        new_p = Player(
            id=p_data['id'],
            name=p_data['name'],
            color="#FF0000", # We'll handle VB long colors later
            is_pc=p_data['is_pc']
        )
        
        # Default starting stats
        new_p.money = 1000
        new_p.smer = state.startsmer
        new_p.x = state.jailx
        new_p.y = state.jaily
        new_p.izobrazba = 0
        
        state.players[new_p.id] = new_p



# metropoly/engine/engine.py
import random
from .parser import generate_default_map_content, load_metropoly_map, save_metropoly_defaults
from .engine import set_start_coords, init_players_logic

def start_new_game(state, map_choice, custom_x, custom_y, player_settings, ini_path):
    """
    VB: Sub CommandOK_Click()
    """
    # 1. Update the .ini file with the names/types entered in the menu
    save_metropoly_defaults(ini_path, player_settings)
    
    # 2. Random size calculation (VB: 6 + Rnd(15) and 5 + Rnd(10))
    rand_x = 6 + random.randint(1, 15)
    rand_y = 5 + random.randint(1, 10)

    # 3. Map Initialization Logic
    if state.mapEditorMode in [1, 3]:
        # User just finished editing a map, keep the current grid
        set_start_coords(state)
    else:
        # Check if they want a random map or a specific file
        # 'Random' is the default if fields are empty
        is_random = (not map_choice or map_choice == "Random") and not custom_x and not custom_y
        
        if is_random:
            # Generate procedural map
            content = generate_default_map_content(rand_x, rand_y)
            # Use a temporary file or update state directly
            # For simplicity, we write to default.map
            with open("metropoly/engine/default.map", "w") as f:
                f.write("\n".join(content))
            load_metropoly_map(state, "metropoly/engine/default.map")
        else:
            if map_choice and map_choice != "Random":
                # Load existing map file
                load_metropoly_map(state, f"metropoly/engine/{map_choice}")
            else:
                # Custom dimensions provided
                x = max(7, custom_x or rand_x)
                y = max(7, custom_y or rand_y)
                content = generate_default_map_content(x, y)
                with open("metropoly/engine/default.map", "w") as f:
                    f.write("\n".join(content))
                load_metropoly_map(state, "metropoly/engine/default.map")

    # 4. Finalizing
    set_start_coords(state)
    init_players_logic(state, player_settings) # Initialize player objects at Jail
    
    state.faza = 2 # Set to "Waiting for roll"
    state.curpl = 1 # Player 1 starts