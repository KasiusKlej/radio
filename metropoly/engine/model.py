import random
import string

class Player:
    def __init__(self, id, name, color, is_pc=False):
        self.id = id
        self.name = name
        self.x = 0
        self.y = 0
        self.color = color
        self.is_pc = is_pc
        self.money = 1000
        self.smer = 1        
        self.izobrazba = 0
        self.jobpayment = 0
        self.statland = 0
        self.stathouse = 0
        self.is_bankrupt = False
        # UI options
        self.options = PlayerOptions()

    def get_salary(self):
        # Ported from earn_price in MoneyParameters.bas
        salaries = {0: 50, 1: 80, 2: 100, 3: 150, 4: 250, 5: 300}
        return salaries.get(self.izobrazba, 50)

    def to_dict(self):
        return {
            **self.__dict__,
            "options": self.options.to_dict(),
            "pawn": self.pawn.to_dict()
        }

class PlayerOptions:
    def __init__(self):
        self.fast_mode = False
        self.show_grid = True
        self.auto_end_turn = False
        self.sound = True
        self.graphics = True

    def to_dict(self):
        return self.__dict__


class Tile:
    def __init__(self, index, name, x, y):
        self.index = index
        self.name = name
        self.x = x
        self.y = y
        self.tip = 0         # 0:Road, 1:Prop, 2:School, 3:Job, 4:Jail, 5:Semafor
        self.semafor = 0
        self.price = 0
        self.stage = 0
        self.owner = 0
        self.owner = -1  # -1 if unowned or not buyable
        self.price = 0
        self.rent = 0
        self.square_type = "property" # "property", "start", "jail", "chance"
        self.pawns_present = [] # List of Pawn objects currently here

    def to_dict(self):
        return self.__dict__


class MapCell:
    def __init__(self, tip=1, stage=0, owner=0, price=0):
        self.tip = tip
        self.stage = stage
        self.owner = owner
        self.price = price


class MetropolyGame:
    """
    Holds the complete mutable state of one Metropoly game.
    Engine functions operate on this object.
    """

    def __init__(self, shortcuts=None):
        # --- Board configuration ---
        self.dimx = 10
        self.dimy = 11
        self.grid = []
        self.map = [[MapCell() for _ in range(self.dimy)] for _ in range(self.dimx)]

        # --- Players ---
        self.players = {}          # {player_id: Player}
        self.numpl = 0
        self.curpl = 1             # current player index (1-based, VB style)

        # --- Turn / phase state ---
        self.faza = 2              # turn phase state machine
        self.kocka = 0             # last dice total
        self.cakajKocko = 0        # waiting-for-dice flag

        # --- Time ---
        self.dayOfWeek = 1         # 1..7

        # --- Special board positions ---
        self.jailx = 0
        self.jaily = 0
        self.startx = 0
        self.starty = 0
        self.startsmer = 1

        # --- Localization ---
        self.CURRENT_LANGUAGE = "eng"
        self.lang_dict = {}


        self.figuraXoffset = [0] * 8
        self.figuraYoffset = [0] * 8
        self.figuraZaRefreshat = 0

        # --- Mouse / click tracking (ported from VB)
        self.whereOnFormClickedX = 0.0
        self.whereOnFormClickedY = 0.0

        # --- Tool selection
        self.mapCurrentTool = 0
        self.OptionSelectedTool = {}  # index -> bool

        # --- Menu toggles / options
        self.autoEndTurn = False

        # --- UI / click state
        self.clkMode = 0            # 0 = normal, 3 = create semafor (VB)
        self.status_label = ""      # replaces LabelStatus.Caption
        self.fast_mode = False
        self.timer_met_kocke_interval = 300
        self.timer_skok_figure_interval = 500
        self.zoomfaktor = 1
        self.tile_draw_queue = []
        self.figuraXoffset = [0] * 8
        self.figuraYoffset = [0] * 8
        self.sound_enabled = True
        self.audio_queue = []
        self.show_grid = False
        self.mapCurrentTool = 0
        self.clkMode = 0
        self.cakajKocko = 10
        self.cakajKocko_start = 10
        self.timer_met_kocke_enabled = False
        self.timer_skok_figure_enabled = False
        self.figuraZaRefreshat = 1
        self.open_save_mode = None
        self.open_save_filename = ""
        self.shortcuts = shortcuts or ['r', 's', 'e', 'o', ' '] 

        self.is_editor_active = False
        self.mapEditorMode = 0
        self.pauseGame1 = False # Dice timer state
        self.pauseGame2 = False # Jump timer state

        # 1. Load the map data
        load_metropoly_map(self, map_file)
        # 2. Find where the road is
        set_start_coords(self)
        # 3. Setup the players from the .ini
        config_players = load_metropoly_config("metropoly.ini")
        init_players_logic(self, config_players)

    # -------------------------
    # Convenience helpers
    # -------------------------

    def next_player(self):
        """Advance current player index safely."""
        self.curpl += 1
        if self.curpl > self.numpl:
            self.curpl = 1
            return True  # wrapped around
        return False

    def to_dict(self):
        """Serialized state sent to frontend."""
        return {
            "dimx": self.dimx,
            "dimy": self.dimy,
            "curpl": self.curpl,
            "faza": self.faza,
            "dayOfWeek": self.dayOfWeek,
            "players": {pid: p.to_dict() for pid, p in self.players.items()},
            "autoEndTurn": self.autoEndTurn,
            "clkMode": self.clkMode,
            "statusLabel": self.status_label,
            "shortcuts": self.shortcuts,
            "status": "ok"
        }


    def expand_teritory(self, x, y):
        """
        Expands the map in the direction of x or y if at the edges.
        Similar to VB6 expand_terit.
        """
        expa = False
        max_dim = 100  # as in VB6 limit

        # Scroll / add left
        if x == 1 and self.dimx < max_dim:
            self.dimx += 1
            expa = True
            self.startx += 1
            self.jailx += 1
            # shift columns right
            for i in range(self.dimx - 1, 0, -1):
                for j in range(self.dimy):
                    self.map[i][j] = self.map[i - 1][j].copy()
            # fill new first column
            for j in range(self.dimy):
                self.map[0][j] = self._new_land_tile()
            # move players
            for p in self.players:
                p.x += 1

        # Add right
        if x == self.dimx and self.dimx < max_dim:
            self.dimx += 1
            expa = True
            i = self.dimx - 1
            for j in range(self.dimy):
                self.map[i][j] = self._new_land_tile()

        # Scroll / add top
        if y == 1 and self.dimy < max_dim:
            self.dimy += 1
            expa = True
            self.starty += 1
            self.jaily += 1
            # shift rows down
            for j in range(self.dimy - 1, 0, -1):
                for i in range(self.dimx):
                    self.map[i][j] = self.map[i][j - 1].copy()
            # fill new first row
            for i in range(self.dimx):
                self.map[i][0] = self._new_land_tile()
            # move players
            for p in self.players:
                p.y += 1

        # Add bottom
        if y == self.dimy and self.dimy < max_dim:
            self.dimy += 1
            expa = True
            j = self.dimy - 1
            for i in range(self.dimx):
                self.map[i][j] = self._new_land_tile()

        # Refresh / redraw (UI layer should handle this)
        return expa

    def _new_land_tile(self):
        """Create a new map tile like VB6 random price tile."""
        import random
        c = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXWZ")
        return {
            "tip": 1,
            "stage": 0,
            "owner": 0,
            "price": ord(c) - 45
        }
    

    def default_land(self):
        """
        Returns a new default land cell, with tip=1, stage=0, owner=0, price random.
        """
        import random, string
        c = random.choice(string.ascii_uppercase[:25])
        return {
            "tip": 1,
            "stage": 0,
            "owner": 0,
            "price": ord(c) - 45
        }   
        
    def display_land_info(self, i: int, j: int) -> dict:
        """
        Returns information about the land at (i, j) for display.
        """
        cell = self.map[i][j]
        info = {
            "image": None,        # placeholder for resource ID or image
            "texts": [],          # list of text lines for display
            "owner_image": None,  # placeholder for owner icon
        }

        if cell["tip"] == 1:  # normal land
            info["image"] = 11 + cell["stage"]  # ImageResource ID
            info["texts"].append(f"{self.lngg(114)} {self.buy_land_price(cell['price'])} {self.lngg(85)}")
            info["texts"].append(f"{self.lngg(115)} {self.sell_price(cell['stage'], cell['price'])} {self.lngg(85)}")
            info["texts"].append(f"{self.lngg(116)} {self.build_houses_price(cell['stage'], cell['price'])} {self.lngg(85)}")

            if cell["owner"] != 0:
                info["owner_image"] = 19 + self.players[cell["owner"] - 1].id  # ImageResource for owner

            info["texts"].append(self.lngg(117))
            for k in range(6):
                s = f"{self.lngg(118)} {k} {self.lngg(119)}"
                ss = f"{self.pay_money_price(k, cell['price'])} {self.lngg(85)}"
                padding = "." * max(0, 25 - len(s) - len(ss))
                line = f"{s}{padding}{ss}"
                info["texts"].append(line)

        elif cell["tip"] in (0, 5):  # road or semaphor
            info["image"] = 2
            info["texts"].append(self.lngg(120))  # "Road"

        elif cell["tip"] == 2:  # school
            info["image"] = 17
            info["texts"].append(self.lngg(121))

        elif cell["tip"] == 3:  # job
            info["image"] = 18
            info["texts"].append(self.lngg(122))

        elif cell["tip"] == 4:  # special?
            info["image"] = 19
            info["texts"].append(self.lngg(123))

        return info
    
    def display_grid(self) -> dict:
        """
        Returns the grid line coordinates for rendering in the UI.
        """
        dx = 32 * self.zoomfaktor
        dy = 32 * self.zoomfaktor
        vertical_lines = []
        horizontal_lines = []

        # vertical lines
        x = 0
        for i in range(self.dimx + 1):
            vertical_lines.append(((x, 0), (x, self.dimy * dy)))
            x += dx

        # horizontal lines
        y = 0
        for j in range(self.dimy + 1):
            horizontal_lines.append(((0, y), (self.dimx * dx, y)))
            y += dy

        return {
            "color": 8,  # QBColor(8) placeholder
            "vertical_lines": vertical_lines,
            "horizontal_lines": horizontal_lines
        }
    
    MAX_DIM = 100

    def expand_terit(self, x: int, y: int):
        """
        Expand the map in the direction indicated by x or y.
        x=1 or x=dimx -> expand left/right
        y=1 or y=dimy -> expand top/bottom
        """
        expa = False

        # Scroll/expand left
        if x == 1 and self.dimx < self.MAX_DIM:
            self.dimx += 1
            expa = True
            self.startx += 1
            self.jailx += 1

            # Shift map right
            for i in range(self.dimx - 1, 0, -1):
                for j in range(self.dimy):
                    self.map[i][j] = self.map[i-1][j]

            # Initialize new left column
            for j in range(self.dimy):
                self.map[0][j] = self._new_land_cell()

            # Move all players right
            for player in self.players:
                player.x += 1

        # Add right column
        if x == self.dimx and self.dimx < self.MAX_DIM:
            self.dimx += 1
            expa = True
            for j in range(self.dimy):
                self.map[self.dimx - 1][j] = self._new_land_cell()

        # Scroll/expand top
        if y == 1 and self.dimy < self.MAX_DIM:
            self.dimy += 1
            expa = True
            self.starty += 1
            self.jaily += 1

            # Shift map down
            for j in range(self.dimy - 1, 0, -1):
                for i in range(self.dimx):
                    self.map[i][j] = self.map[i][j-1]

            # Initialize new top row
            for i in range(self.dimx):
                self.map[i][0] = self._new_land_cell()

            # Move all players down
            for player in self.players:
                player.y += 1

        # Add bottom row
        if y == self.dimy and self.dimy < self.MAX_DIM:
            self.dimy += 1
            expa = True
            for i in range(self.dimx):
                self.map[i][self.dimy - 1] = self._new_land_cell()

        if expa:
            self.draw_map()
            if self.mapEditorMode == 0:
                self.draw_players()
            if self.showGrid:
                self.display_grid()

    def _new_land_cell(self):
        """Helper to generate a new land cell like VB6 code."""
        c = random.choice(string.ascii_uppercase[:25])  # A-Y
        return {
            "tip": 1,
            "stage": 0,
            "owner": 0,
            "price": ord(c) - 45
        }
    
    def display_land_info(self, i: int, j: int) -> dict:
        """
        Return info about a land cell at (i, j) for display.
        This replaces VB6 form operations with a structured dictionary.
        """
        cell = self.map[i][j]
        info = {}

        if cell["tip"] == 1:  # Land
            info["image"] = 11 + cell["stage"]       # ImageResource index
            info["owner_image"] = None
            if cell["owner"] != 0:
                info["owner_image"] = 19 + self.players[cell["owner"]-1].id

            # Prices
            info["buy_price"] = self.buy_land_price(cell["price"])
            info["sell_price"] = self.sell_price(cell["stage"], cell["price"])
            info["build_price"] = self.build_houses_price(cell["stage"], cell["price"])

            # Rent table
            info["rent_table"] = []
            for k in range(6):
                price = self.pay_money_price(k, cell["price"])
                info["rent_table"].append({
                    "houses": k,
                    "rent": price,
                    "highlight": (cell["stage"] == k)
                })

        elif cell["tip"] in (0, 5):  # Road or semaphore
            info["image"] = 2
            info["type"] = "Road"

        elif cell["tip"] == 2:  # School
            info["image"] = 17
            info["type"] = "School"

        elif cell["tip"] == 3:  # Job
            info["image"] = 18
            info["type"] = "Job"

        elif cell["tip"] == 4:  # Special
            info["image"] = 19
            info["type"] = "Special"

        return info
    
    def get_grid_lines(self, zoom_factor=1):
        """
        Return the positions of vertical and horizontal grid lines.
        Each line is represented as ((x1, y1), (x2, y2)).
        """
        dx = 32 * zoom_factor
        dy = 32 * zoom_factor

        vertical_lines = [((i * dx, 0), (i * dx, self.dimy * dy)) for i in range(self.dimx + 1)]
        horizontal_lines = [((0, j * dy), (self.dimx * dx, j * dy)) for j in range(self.dimy + 1)]

        return {"vertical": vertical_lines, "horizontal": horizontal_lines}
    

    def new_random_cell(self):
        import random
        c = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXWZ")
        price = ord(c) - 45
        return MapCell(tip=1, stage=0, owner=0, price=price)
    

    def display_land_info(self, i, j):
        """
        Returns structured information about a map tile
        (replacement for VB6 display_land_info drawing code)
        """
        tile = self.map[i][j]

        info = {
            "type": None,
            "image": None,
            "lines": [],
            "owner_player_id": None,
            "rent_table": []
        }

        # ----------------------------
        # LAND
        # ----------------------------
        if tile["tip"] == 1:
            info["type"] = "land"
            info["image"] = 11 + tile["stage"]

            buy_price = self.buy_land_price(tile["price"])
            sell_price = self.sell_price(tile["stage"], tile["price"])
            build_price = self.build_houses_price(tile["stage"], tile["price"])

            info["lines"].append({
                "text": f"{self.lngg(114)} {buy_price}{self.lngg(85)}",
                "bold": False
            })
            info["lines"].append({
                "text": f"{self.lngg(115)} {sell_price}{self.lngg(85)}",
                "bold": False
            })
            info["lines"].append({
                "text": f"{self.lngg(116)} {build_price}{self.lngg(85)}",
                "bold": False
            })

            if tile["owner"] != 0:
                info["owner_player_id"] = self.players[tile["owner"] - 1].id

            # Rent table (stage 0–5)
            info["lines"].append({
                "text": self.lngg(117),
                "bold": False
            })

            for k in range(6):
                rent = self.pay_money_price(k, tile["price"])
                info["rent_table"].append({
                    "stage": k,
                    "rent": rent,
                    "active": (tile["stage"] == k)
                })

            return info

        # ----------------------------
        # ROAD / SEMAPHORE
        # ----------------------------
        if tile["tip"] in (0, 5):
            info["type"] = "road"
            info["image"] = 2
            info["lines"].append({
                "text": self.lngg(120),
                "bold": False
            })
            return info

        # ----------------------------
        # SCHOOL
        # ----------------------------
        if tile["tip"] == 2:
            info["type"] = "school"
            info["image"] = 17
            info["lines"].append({
                "text": self.lngg(121),
                "bold": False
            })
            return info

        # ----------------------------
        # JOB
        # ----------------------------
        if tile["tip"] == 3:
            info["type"] = "job"
            info["image"] = 18
            info["lines"].append({
                "text": self.lngg(122),
                "bold": False
            })
            return info

        # ----------------------------
        # OTHER
        # ----------------------------
        if tile["tip"] == 4:
            info["type"] = "other"
            info["image"] = 19
            info["lines"].append({
                "text": self.lngg(123),
                "bold": False
            })
            return info

        return info

    
    def display_grid(self, zoom_factor=1):
        """
        Returns a list of horizontal and vertical lines for the grid.
        Each line is ((x1, y1), (x2, y2)).
        zoom_factor scales the size of the cells.
        """
        lines = []
        dx = 32 * zoom_factor
        dy = 32 * zoom_factor

        # vertical lines
        for i in range(self.dimx + 1):
            x = i * dx
            lines.append(((x, 0), (x, self.dimy * dy)))

        # horizontal lines
        for j in range(self.dimy + 1):
            y = j * dy
            lines.append(((0, y), (self.dimx * dx, y)))

        return lines
    

    def get_land_info(self, i, j):
        """
        Returns a dictionary of all relevant land info for map tile (i,j),
        replacing VB6 display_land_info sub.
        """
        tile = self.map[i][j]
        info = {}

        if tile["tip"] == 1:  # property
            info["image"] = 11 + tile["stage"]  # ImageResource index
            info["buy_price"] = self.buy_land_price(tile["price"])
            info["sell_price"] = self.sell_price(tile["stage"], tile["price"])
            info["build_price"] = self.build_houses_price(tile["stage"], tile["price"])
            info["owner_id"] = tile["owner"] if tile["owner"] != 0 else None
            # Rent table
            rent_table = []
            for k in range(6):
                rent_table.append({
                    "stage": k,
                    "rent": self.pay_money_price(k, tile["price"]),
                    "highlight": tile["stage"] == k
                })
            info["rent_table"] = rent_table

        elif tile["tip"] in [0, 5]:  # road / semaphore
            info["image"] = 2
            info["type"] = "Road"

        elif tile["tip"] == 2:  # school
            info["image"] = 17
            info["type"] = "School"

        elif tile["tip"] == 3:  # job
            info["image"] = 18
            info["type"] = "Job"

        elif tile["tip"] == 4:  # bonus / special
            info["image"] = 19
            info["type"] = "Special"

        return info
    

    def prepare_buy_dialog(self, sx: int, sy: int, price: int, land_or_house: int):
        """
        Prepares data for buy dialog.
        land_or_house: 0 = land, 1 = house
        """
        # display_land_info is still engine-side
        land_info = self.get_land_info(sx, sy)

        if land_or_house == 0:
            question = f"{self.lngg(124)} {price}{self.lngg(101)}"
        else:
            question = f"{self.lngg(125)} {price}{self.lngg(101)}"

        # decide vertical placement hint (top/bottom half of map)
        placement = "top" if sy <= self.dimy / 2 else "bottom"

        return {
            "question": question,
            "land_info": land_info,
            "placement": placement,
            "x": sx,
            "y": sy,
        }

    def turn_semaphores(self):
        """Rotate all semaphores (called on Wed/Sat)."""
        self.status_message = self.lngg(126)

        for x in range(1, self.dimx + 1):
            for y in range(1, self.dimy + 1):
                tile = self.map[x][y]
                if tile.tip == 5:
                    self.turn_semaphore(x, y)
                    self.draw_road(x, y)

        self.gameTurnVpadnica = (self.gameTurnVpadnica + 1) % 4
        self.gameTurnSmer = (self.gameTurnSmer + 1) % 3

    def turn_semaphore(self, x: int, y: int):
        """
        Rotate a single semaphore according to game turn rules.
        """
        smr = self.gameTurnVpadnica   # which approach (0–3)
        nsmr = self.gameTurnSmer      # direction variant (0–2)

        sosed = self.kje_so_sosednje_ceste(x, y)
        if sosed[smr] == "0":
            return  # cannot rotate

        s = self.semaforData[self.map[x][y].semafor][:4]
        ss = ""

        if smr == 0:
            nova = "234"[nsmr]
            if sosed[int(nova) - 1] == "1":
                ss = nova + s[1:]
        elif smr == 1:
            nova = "134"[nsmr]
            if sosed[int(nova) - 1] == "1":
                ss = s[0] + nova + s[2:]
        elif smr == 2:
            nova = "124"[nsmr]
            if sosed[int(nova) - 1] == "1":
                ss = s[:2] + nova + s[3]
        elif smr == 3:
            nova = "123"[nsmr]
            if sosed[int(nova) - 1] == "1":
                ss = s[:3] + nova

        if not ss:
            return

        for i, data in self.semaforData.items():
            if data.startswith(ss):
                self.map[x][y].semafor = i
                break

    def rotate_semaphores_if_possible(self):
        p = self.rotateSemafor_price
        player = self.players[self.curpl]

        if player.tip != 0:
            return False

        if player.money < p:
            return False

        self.turn_semaphores()
        player.money -= p
        self.update_status()

        return True
            
    def someone_already_stands_here(self, x: int, y: int, pid: int) -> bool:
        for player in self.players[1:self.numpl + 1]:
            if player.id != pid and player.x == x and player.y == y:
                return True
        return False


    def build_road_at(self, x, y):
        tile = self.grid[y][x]
        tile.tip = 0 # Road
        # ... logic to update neighbors ...
        from .engine import add_random_semafor
        add_random_semafor(self, x, y)



from enum import IntEnum

class OpenSaveMode(IntEnum):
    OPEN = 1
    SAVE = 2

    
