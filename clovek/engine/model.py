# ============================================================================
# CLOVEK (LUDO) - Complete Game Data Model
# ============================================================================
# A Slovenian Ludo game for 2 players (Red vs Blue)
# Board: 125 tiles with teleports, shortcuts, and home stretches
# ============================================================================

from dataclasses import dataclass, field
from typing import Optional, List, Dict
from enum import Enum

# ============================================================================
# ENUMS & CONSTANTS
# ============================================================================

class PlayerColor(Enum):
    RED = "red"
    BLUE = "blue"

class GameMode(Enum):
    AI_EASY = "ai_easy"
    AI_MEDIUM = "ai_medium"
    AI_HARD = "ai_hard"
    HOTSEAT = "hotseat"
    NETWORK = "network"

class TileType(Enum):
    START = "start"              # Starting position (9 for red, 57 for blue)
    HOME_SQUARE = "home_square"  # Starting houses (1-4 for red, 5-8 for blue)
    HOME_STRETCH = "home_stretch" # Final stretch to home (119-122 red, 123-126 blue)
    NORMAL = "normal"            # Regular path
    CORNER = "corner"            # Corner tiles (38, 52, 87, 101)
    TELEPORT = "teleport"        # Teleport tiles (25→18, 73→66)
    JUNCTION = "junction"        # Fork in road (21→106, 69→118)
    CENTER_STOP = "center_stop"  # Stop tile (111)
    CENTER_DEATH = "center_death" # Death tile (112)
    RETURN = "return"            # Return tile (18, 66)

# ============================================================================
# BOARD TILE DATA
# ============================================================================

@dataclass
class Tile:
    """Represents a single tile on the board."""
    id: int
    x: int
    y: int
    next_red: Optional[int]   # Next tile for red player (None = 'x')
    next_blue: Optional[int]  # Next tile for blue player (None = 'x')
    teleport_red: Optional[int] = None   # Teleport destination for red
    teleport_blue: Optional[int] = None  # Teleport destination for blue
    junction_red: Optional[int] = None   # Junction path for red
    junction_blue: Optional[int] = None  # Junction path for blue
    description: str = ""
    tile_type: TileType = TileType.NORMAL
    
    def get_next(self, color: PlayerColor) -> Optional[int]:
        """Get next tile for given player color."""
        return self.next_red if color == PlayerColor.RED else self.next_blue
    
    def get_teleport(self, color: PlayerColor) -> Optional[int]:
        """Get teleport destination for given player color."""
        return self.teleport_red if color == PlayerColor.RED else self.teleport_blue
    
    def get_junction(self, color: PlayerColor) -> Optional[int]:
        """Get junction destination for given player color."""
        return self.junction_red if color == PlayerColor.RED else self.junction_blue


# ============================================================================
# BOARD MAP - Encoded from CSV
# ============================================================================

def create_board() -> Dict[int, Tile]:
    """Create the complete board with all 125 tiles."""
    
    board = {}
    
    # Helper to parse CSV 'x' as None
    def parse_id(val):
        return None if val == 'x' or val == '' else int(val)
    
    # RED HOME SQUARES (1-4) - Starting houses
    board[1] = Tile(1, 166, 378, 9, None, tile_type=TileType.HOME_SQUARE, description="Začetna hiška RED")
    board[2] = Tile(2, 200, 378, 9, None, tile_type=TileType.HOME_SQUARE, description="Začetna hiška RED")
    board[3] = Tile(3, 166, 412, 9, None, tile_type=TileType.HOME_SQUARE, description="Začetna hiška RED")
    board[4] = Tile(4, 200, 412, 9, None, tile_type=TileType.HOME_SQUARE, description="Začetna hiška RED")
    
    # BLUE HOME SQUARES (5-8) - Starting houses
    board[5] = Tile(5, 629, 88, None, 57, tile_type=TileType.HOME_SQUARE, description="Začetna hiška BLUE")
    board[6] = Tile(6, 665, 88, None, 57, tile_type=TileType.HOME_SQUARE, description="Začetna hiška BLUE")
    board[7] = Tile(7, 629, 124, None, 57, tile_type=TileType.HOME_SQUARE, description="Začetna hiška BLUE")
    board[8] = Tile(8, 665, 123, None, 57, tile_type=TileType.HOME_SQUARE, description="Začetna hiška BLUE")
    
    # MAIN PATH - Bottom row (9-38)
    board[9] = Tile(9, 147, 479, 10, 10, tile_type=TileType.START, description="START rdeči")
    board[10] = Tile(10, 171, 479, 11, 11, description="")
    board[11] = Tile(11, 197, 479, 12, 12, description="")
    board[12] = Tile(12, 221, 479, 13, 13, description="")
    board[13] = Tile(13, 244, 479, 14, 14, description="")
    board[14] = Tile(14, 268, 479, 15, 15, description="")
    board[15] = Tile(15, 291, 479, 16, 16, description="")
    board[16] = Tile(16, 314, 479, 17, 17, description="")
    board[17] = Tile(17, 338, 479, 18, 18, description="")
    board[18] = Tile(18, 360, 479, 19, 19, tile_type=TileType.RETURN, description="Polje vračanja")
    board[19] = Tile(19, 384, 479, 20, 20, description="")
    board[20] = Tile(20, 407, 479, 21, 21, description="")
    board[21] = Tile(21, 431, 479, 22, 22, junction_red=106, tile_type=TileType.JUNCTION, description="Kretnica spodaj")
    board[22] = Tile(22, 455, 479, 23, 23, description="")
    board[23] = Tile(23, 479, 479, 24, 24, description="")
    board[24] = Tile(24, 504, 479, 25, 25, description="")
    board[25] = Tile(25, 529, 479, 26, 26, teleport_red=18, teleport_blue=18, tile_type=TileType.TELEPORT, description="Vrni se 7 polj")
    board[26] = Tile(26, 554, 479, 27, 27, description="")
    board[27] = Tile(27, 578, 479, 28, 28, description="")
    board[28] = Tile(28, 602, 479, 29, 29, description="")
    board[29] = Tile(29, 626, 479, 30, 30, description="")
    board[30] = Tile(30, 650, 479, 31, 31, description="")
    board[31] = Tile(31, 674, 479, 32, 32, description="")
    board[32] = Tile(32, 699, 479, 33, 33, description="")
    board[33] = Tile(33, 723, 479, 34, 34, description="")
    board[34] = Tile(34, 747, 479, 35, 35, description="")
    board[35] = Tile(35, 771, 479, 36, 36, description="")
    board[36] = Tile(36, 795, 479, 37, 37, description="")
    board[37] = Tile(37, 819, 479, 38, 38, description="")
    board[38] = Tile(38, 843, 479, 39, 39, teleport_red=52, teleport_blue=52, tile_type=TileType.CORNER, description="VOGAL desno spodaj")
    
    # RIGHT VERTICAL PATH (39-52)
    board[39] = Tile(39, 843, 443, 40, 40, description="Desna navpična pot")
    board[40] = Tile(40, 843, 408, 41, 41, description="Desna navpična pot")
    board[41] = Tile(41, 843, 377, 42, 42, description="Desna navpična pot")
    board[42] = Tile(42, 843, 345, 43, 43, description="Desna navpična pot")
    board[43] = Tile(43, 843, 314, 44, 44, description="Desna navpična pot")
    board[44] = Tile(44, 843, 283, 45, 45, description="Desna navpična pot")
    board[45] = Tile(45, 843, 251, 46, 46, description="Desna navpična pot")
    board[46] = Tile(46, 843, 220, 47, 47, description="Desna navpična pot")
    board[47] = Tile(47, 843, 189, 48, 48, description="Desna navpična pot")
    board[48] = Tile(48, 843, 157, 49, 49, description="Desna navpična pot")
    board[49] = Tile(49, 843, 126, 50, 50, description="Desna navpična pot")
    board[50] = Tile(50, 843, 95, 51, 51, description="Desna navpična pot")
    board[51] = Tile(51, 843, 62, 52, 52, description="Desna navpična pot")
    board[52] = Tile(52, 843, 31, 53, 53, tile_type=TileType.CORNER, description="VOGAL desno zgoraj")
    
    # TOP ROW (53-87)
    board[53] = Tile(53, 803, 31, 54, 54, description="")
    board[54] = Tile(54, 780, 31, 55, 55, description="")
    board[55] = Tile(55, 751, 31, 56, 56, description="")
    board[56] = Tile(56, 724, 31, 57, 123, description="KONČNO polje za v hišo MODRI")
    board[57] = Tile(57, 697, 31, 58, 58, tile_type=TileType.START, description="START modri")
    board[58] = Tile(58, 674, 31, 59, 59, description="")
    board[59] = Tile(59, 650, 31, 60, 60, description="")
    board[60] = Tile(60, 625, 31, 61, 61, description="")
    board[61] = Tile(61, 600, 31, 62, 62, description="")
    board[62] = Tile(62, 578, 31, 63, 63, description="")
    board[63] = Tile(63, 553, 31, 64, 64, description="")
    board[64] = Tile(64, 530, 31, 65, 65, description="")
    board[65] = Tile(65, 515, 31, 66, 66, description="")
    board[66] = Tile(66, 491, 31, 67, 67, tile_type=TileType.RETURN, description="Vračilo")
    board[67] = Tile(67, 468, 31, 68, 68, description="")
    board[68] = Tile(68, 448, 31, 69, 69, description="")
    board[69] = Tile(69, 427, 31, 70, 70, junction_blue=118, tile_type=TileType.JUNCTION, description="Kretnica zgoraj")
    board[70] = Tile(70, 406, 31, 71, 71, description="")
    board[71] = Tile(71, 380, 31, 72, 72, description="")
    board[72] = Tile(72, 359, 31, 73, 73, description="")
    board[73] = Tile(73, 332, 33, 74, 74, teleport_red=66, teleport_blue=66, tile_type=TileType.TELEPORT, description="Vrni se 7 polj")
    board[74] = Tile(74, 311, 31, 75, 75, description="")
    board[75] = Tile(75, 291, 31, 76, 76, description="")
    board[76] = Tile(76, 263, 31, 77, 77, description="")
    board[77] = Tile(77, 247, 31, 78, 78, description="")
    board[78] = Tile(78, 214, 31, 79, 79, description="")
    board[79] = Tile(79, 195, 31, 80, 80, description="")
    board[80] = Tile(80, 171, 31, 81, 81, description="")
    board[81] = Tile(81, 147, 31, 82, 82, description="")
    board[82] = Tile(82, 125, 31, 83, 83, description="")
    board[83] = Tile(83, 103, 31, 84, 84, description="")
    board[84] = Tile(84, 75, 31, 85, 85, description="")
    board[85] = Tile(85, 54, 31, 87, 87, description="")
    board[87] = Tile(87, 26, 31, 88, 88, teleport_red=101, teleport_blue=101, tile_type=TileType.CORNER, description="VOGAL levo zgoraj")
    
    # LEFT VERTICAL PATH (88-101)
    board[88] = Tile(88, 31, 62, 89, 89, description="Navpična pot levo")
    board[89] = Tile(89, 31, 95, 90, 90, description="Navpična pot levo")
    board[90] = Tile(90, 31, 126, 91, 91, description="Navpična pot levo")
    board[91] = Tile(91, 31, 157, 92, 92, description="Navpična pot levo")
    board[92] = Tile(92, 31, 189, 93, 93, description="Navpična pot levo")
    board[93] = Tile(93, 31, 220, 94, 94, description="Navpična pot levo")
    board[94] = Tile(94, 31, 251, 95, 95, description="Navpična pot levo")
    board[95] = Tile(95, 31, 283, 96, 96, description="Navpična pot levo")
    board[96] = Tile(96, 31, 314, 97, 97, description="Navpična pot levo")
    board[97] = Tile(97, 31, 345, 98, 98, description="Navpična pot levo")
    board[98] = Tile(98, 31, 377, 99, 99, description="Navpična pot levo")
    board[99] = Tile(99, 31, 408, 100, 100, description="Navpična pot levo")
    board[100] = Tile(100, 31, 443, 101, 101, description="Navpična pot levo")
    board[101] = Tile(101, 31, 479, 102, 102, tile_type=TileType.CORNER, description="VOGAL levo spodaj")
    board[102] = Tile(102, 54, 479, 103, 103, description="")
    board[103] = Tile(103, 78, 479, 104, 104, description="")
    board[104] = Tile(104, 101, 479, 105, 105, description="")
    board[105] = Tile(105, 125, 479, 119, 9, description="KONČNO polje za v hišo RDEČI")
    
    # CENTER PATH (106-118) - Shortcut through middle
    board[106] = Tile(106, 432, 443, 107, 21, description="Srednja pot")
    board[107] = Tile(107, 432, 408, 108, 106, description="Srednja pot")
    board[108] = Tile(108, 432, 377, 109, 107, description="Srednja pot")
    board[109] = Tile(109, 432, 345, 110, 108, description="Srednja pot")
    board[110] = Tile(110, 432, 314, 111, 109, description="Srednja pot")
    board[111] = Tile(111, 432, 283, 112, 110, teleport_red=9, teleport_blue=57, tile_type=TileType.CENTER_STOP, description="STOP")
    board[112] = Tile(112, 432, 251, 113, 111, teleport_red=1234, teleport_blue=5678, tile_type=TileType.CENTER_DEATH, description="SMRT")
    board[113] = Tile(113, 432, 220, 114, 112, teleport_red=9, teleport_blue=57, tile_type=TileType.CENTER_STOP, description="STOP")
    board[114] = Tile(114, 432, 189, 115, 113, description="Srednja pot")
    board[115] = Tile(115, 432, 157, 116, 114, description="Srednja pot")
    board[116] = Tile(116, 432, 126, 117, 115, description="Srednja pot")
    board[117] = Tile(117, 432, 95, 118, 116, description="Srednja pot")
    board[118] = Tile(118, 432, 62, 69, 117, description="Srednja pot")
    
    # RED HOME STRETCH (119-122) - Final path to goal
    board[119] = Tile(119, 125, 450, 120, None, tile_type=TileType.HOME_STRETCH, description="Hiše rdeči")
    board[120] = Tile(120, 125, 410, 121, None, tile_type=TileType.HOME_STRETCH, description="Hiše rdeči")
    board[121] = Tile(121, 125, 379, 122, None, tile_type=TileType.HOME_STRETCH, description="Hiše rdeči")
    board[122] = Tile(122, 125, 349, None, None, tile_type=TileType.HOME_STRETCH, description="Hiše rdeči GOAL")
    
    # BLUE HOME STRETCH (123-126) - Final path to goal
    board[123] = Tile(123, 724, 63, None, 124, tile_type=TileType.HOME_STRETCH, description="Hiše modri")
    board[124] = Tile(124, 724, 91, None, 125, tile_type=TileType.HOME_STRETCH, description="Hiše modri")
    board[125] = Tile(125, 724, 126, None, 126, tile_type=TileType.HOME_STRETCH, description="Hiše modri")
    board[126] = Tile(126, 724, 157, None, None, tile_type=TileType.HOME_STRETCH, description="Hiše modri GOAL")
    
    return board


# ============================================================================
# GAME ENTITIES
# ============================================================================

@dataclass
class Pawn:
    """Represents a single pawn."""
    id: int                      # 1-4 for red, 5-8 for blue
    color: PlayerColor
    position: Optional[int] = None  # Current tile ID (None = in starting house)
    is_home: bool = False        # Has reached goal
    
    def get_home_square_id(self) -> int:
        """Get the starting house tile ID for this pawn."""
        return self.id
    
    def is_in_home_square(self) -> bool:
        """Check if pawn is in starting house."""
        return self.position is None
    
    def get_start_tile_id(self) -> int:
        """
        Get the start tile ID for this pawn's color.
        Red: tile 9, Blue: tile 57
        """
        if self.color == PlayerColor.RED:
            return 9
        else:  # BLUE
            return 57

@dataclass
class Player:
    """Represents a player."""
    color: PlayerColor
    name: str
    pawns: List[Pawn] = field(default_factory=list)
    score: int = 0
    avatar: str = ""
    is_ai: bool = False
    ai_difficulty: Optional[str] = None
    stat1: float = 0
    stat2: float = 0
    stat3: float = 0
    stat4: float = 0
    stat5: float = 0
    stat6: float = 0
    stat7: float = 0
    stat8: float = 0
    stat9: float = 0

    def __post_init__(self):
        if not self.pawns:
            # Create 4 pawns
            start_id = 1 if self.color == PlayerColor.RED else 5
            self.pawns = [
                Pawn(id=start_id + i, color=self.color)
                for i in range(4)
            ]
    
    def get_start_tile_id(self) -> int:
        """Get the start tile ID for this player."""
        return 9 if self.color == PlayerColor.RED else 57
    
    # def get_home_entry_tile_id(self) -> int:
    #     """Get the tile ID that leads to home stretch."""
    #     return 105 if self.color == PlayerColor.RED else 56
    
    def get_home_stretch_start_id(self) -> int:
        """Get first tile of home stretch."""
        return 119 if self.color == PlayerColor.RED else 123
    
    def pawns_at_goal(self) -> int:
        """Count how many pawns have reached the goal."""
        return sum(1 for pawn in self.pawns if pawn.is_home)
    
    def has_won(self) -> bool:
        """Check if player has won (all 4 pawns home)."""
        return self.pawns_at_goal() == 4
    
    def get_home_entry_tile_id(self) -> int:
        """
        Get the tile where pawns enter the home stretch.
        Red: tile 118 (enters home stretch at 119-122)
        Blue: tile 106 (enters home stretch at 123-126)
        """
        if self.color == PlayerColor.RED:
            return 118
        else:  # BLUE
            return 106
    
    def get_goal_tile_id(self) -> int:
        """
        Get the final goal tile ID.
        Red: tile 122 (last of home stretch 119-122)
        Blue: tile 126 (last of home stretch 123-126)
        """
        if self.color == PlayerColor.RED:
            return 122
        else:  # BLUE
            return 126
    
        
    

@dataclass
class GameState:
    """Represents the complete game state."""
    mode: GameMode
    board: Dict[int, Tile]
    red_player: Player
    blue_player: Player
    current_turn: PlayerColor = PlayerColor.RED
    dice_value: Optional[int] = None
    game_over: bool = False
    winner: Optional[PlayerColor] = None
    move_history: List[Dict] = field(default_factory=list)
    clovek_paused: bool = True          # when waiting for other player to join game
    
    def get_current_player(self) -> Player:
        """Get the player whose turn it is."""
        return self.red_player if self.current_turn == PlayerColor.RED else self.blue_player
    
    def get_opponent(self) -> Player:
        """Get the opponent player."""
        return self.blue_player if self.current_turn == PlayerColor.RED else self.red_player
    
    def switch_turn(self):
        """Switch to the other player's turn."""
        self.current_turn = PlayerColor.BLUE if self.current_turn == PlayerColor.RED else PlayerColor.RED
        self.dice_value = None


# ============================================================================
# GAME CONSTANTS
# ============================================================================

GAME_RULES = {
    "pawns_per_player": 4,
    "dice_sides": 6,
    "start_bonus": True,  # Roll 6 to start
    "capture_returns_home": True,  # Capturing sends opponent pawn home
    "exact_finish": True,  # Must land exactly on goal
}

SPECIAL_TILES = {
    "red_start": 9,
    "blue_start": 57,
    "red_home_entry": 105,
    "blue_home_entry": 56,
    "red_goal": 122,
    "blue_goal": 126,
    "teleports": [25, 73],  # Tiles with teleport ability
    "junctions": [21, 69],  # Tiles with junction/shortcut
    "death_tile": 112,       # Center death tile
    "stop_tiles": [111, 113] # Center stop tiles
}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

# def initialize_game(mode: GameMode, 
#                    red_name: str = "Red Player", 
#                    blue_name: str = "Blue Player") -> GameState:
#     """Initialize a new game."""
#     board = create_board()
    
#     red_player = Player(
#         color=PlayerColor.RED,
#         name=red_name,
#         is_ai=False
#     )
    
#     blue_player = Player(
#         color=PlayerColor.BLUE,
#         name=blue_name,
#         is_ai=mode in [GameMode.AI_EASY, GameMode.AI_MEDIUM, GameMode.AI_HARD],
#         ai_difficulty=mode.value if mode != GameMode.HOTSEAT and mode != GameMode.NETWORK else None
#     )
    
#     return GameState(
#         mode=mode,
#         board=board,
#         red_player=red_player,
#         blue_player=blue_player
#     )

def initialize_game(mode: GameMode, 
                    red_name: str = "Red Player", 
                    blue_name: str = "Blue Player") -> GameState:
    """Initialize a new game based on chosen mode."""
    board = create_board()
    
    # Red is always Human in this version
    red_player = Player(
        color=PlayerColor.RED,
        name=red_name,
        is_ai=False
    )
    
    # Blue is AI if the mode is one of the AI levels
    is_blue_ai = mode in [GameMode.AI_EASY, GameMode.AI_MEDIUM, GameMode.AI_HARD]
    
    blue_player = Player(
        color=PlayerColor.BLUE,
        name=blue_name,
        is_ai=is_blue_ai,
        # Ensure the string "AI_HARD" etc. is stored here for the select_ai_move switch
        ai_difficulty=mode.name if is_blue_ai else None 
    )
    
    return GameState(
        mode=mode,
        board=board,
        red_player=red_player,
        blue_player=blue_player
    )

def get_tile_at_position(board: Dict[int, Tile], x: int, y: int, tolerance: int = 20) -> Optional[Tile]:
    """Find tile at given screen coordinates."""
    for tile in board.values():
        if abs(tile.x - x) <= tolerance and abs(tile.y - y) <= tolerance:
            return tile
    return None


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

# if __name__ == "__main__":
#     # Create a new game
#     game = initialize_game(GameMode.AI_MEDIUM, "Janez", "Computer")
    
#     print(f"Game Mode: {game.mode.value}")
#     print(f"Red Player: {game.red_player.name}")
#     print(f"Blue Player: {game.blue_player.name} (AI: {game.blue_player.is_ai})")
#     print(f"Board tiles: {len(game.board)}")
#     print(f"Current turn: {game.current_turn.value}")
    
#     # Show some special tiles
#     print("\nSpecial Tiles:")
#     print(f"Red Start: Tile {game.board[9].id} at ({game.board[9].x}, {game.board[9].y})")
#     print(f"Blue Start: Tile {game.board[57].id} at ({game.board[57].x}, {game.board[57].y})")
#     print(f"Death Tile: Tile {game.board[112].id} - {game.board[112].description}")
#     print(f"Red Goal: Tile {game.board[122].id} - {game.board[122].description}")
    
#     # Show teleport example
#     teleport_tile = game.board[25]
#     print(f"\nTeleport: Tile {teleport_tile.id} → {teleport_tile.get_teleport(PlayerColor.RED)}")
    
