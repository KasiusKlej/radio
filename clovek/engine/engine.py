# ============================================================================
# CLOVEK (LUDO) - Game Engine
# ============================================================================
# Core game logic, move validation, and pawn management
# ============================================================================

from typing import List, Dict, Optional, Tuple
from .model import GameState, PlayerColor, Pawn, Player, TileType
import random

# ============================================================================
# PAWN PREPARATION (Moving pawns to home squares before game starts)
# ============================================================================

def prepare_pawns(game: GameState, color: PlayerColor) -> List[Dict]:
    """
    Prepare pawns by moving them to their home squares before game starts.
    This is the setup phase - each pawn moves to its designated home tile.
    
    Args:
        game: Current game state
        color: PlayerColor.RED or PlayerColor.BLUE
    
    Returns:
        List of animation sequences for moving pawns home
    """
    animations = []
    
    # Get the player
    player = game.red_player if color == PlayerColor.RED else game.blue_player
    
    # Move each pawn to its home square
    for pawn in player.pawns:
        # Get current position (might be None or random from initial display)
        current_pos = pawn.position
        
        # Get home square tile ID for this pawn
        home_tile = pawn.get_home_square_id()
        
        # Create animation: pawn moves from wherever it is to its home square
        animations.append({
            "pawn": pawn.id,
            "from": current_pos if current_pos else 0,  # 0 = undefined position
            "to": home_tile,
            "sound": None  # Silent preparation move
        })
        
        # Update pawn position
        pawn.position = None  # In home square = not on board yet
        pawn.is_home = False  # Not at goal
    
    print(f"✅ Prepared {color.value} pawns: {[p.id for p in player.pawns]}")
    
    return animations


def prepare_all_pawns(game: GameState) -> List[Dict]:
    """
    Prepare both red and blue pawns before starting the game.
    
    Returns:
        Combined animation sequence for all 8 pawns
    """
    animations = []
    
    # Prepare red pawns (1-4 → tiles 1-4)
    animations.extend(prepare_pawns(game, PlayerColor.RED))
    
    # Prepare blue pawns (5-8 → tiles 5-8)
    animations.extend(prepare_pawns(game, PlayerColor.BLUE))
    
    print(f"✅ All pawns prepared, ready to start game")
    
    return animations


# ============================================================================
# MOVE VALIDATION
# ============================================================================

def can_start_pawn(game: GameState, pawn: Pawn, dice_value: int) -> bool:
    """
    Check if a pawn can leave home square and enter the board.
    Usually requires rolling a 6.
    
    Args:
        game: Current game state
        pawn: The pawn to check
        dice_value: Result of dice roll
    
    Returns:
        bool: True if pawn can start
    """
    # Must be in home square
    if pawn.position is not None:
        return False
    
    # Must roll a 6 to start
    if dice_value != 6:
        return False
    
    # Check if start tile is blocked by own pawn
    player = game.red_player if pawn.color == PlayerColor.RED else game.blue_player
    start_tile = player.get_start_tile_id()
    
    # Check if any of player's pawns are on start tile
    for p in player.pawns:
        if p.position == start_tile:
            return False  # Start tile blocked
    
    return True



# ============================================================================
# MOVE EXECUTION
# ============================================================================

def start_pawn(game: GameState, pawn: Pawn) -> List[Dict]:
    """
    Move a pawn from home square to start tile.
    
    Returns:
        Animation sequence
    """
    player = game.red_player if pawn.color == PlayerColor.RED else game.blue_player
    start_tile = player.get_start_tile_id()
    
    # Update pawn position
    pawn.position = start_tile
    
    # Create animation with happy sound
    animations = [{
        "pawn": pawn.id,
        "from": pawn.get_home_square_id(),
        "to": start_tile,
        "sound": "GREMO"  # Happy leaving home!
    }]
    
    print(f"🚀 Pawn {pawn.id} started at tile {start_tile}")
    
    return animations


def check_capture(game: GameState, moving_pawn: Pawn, tile_id: int, opponent: Player) -> Optional[Pawn]:
    """
    Check if moving to a tile captures an enemy pawn.
    
    Returns:
        The captured pawn, or None if no capture
    """
    # Check if any opponent pawn is on this tile
    for pawn in opponent.pawns:
        if pawn.position == tile_id and not pawn.is_home:
            return pawn
    
    return None


def capture_enemy_pawn(game: GameState, attacker: Pawn, victim: Pawn) -> List[Dict]:
    """
    Capture an enemy pawn and send it back home.
    
    Returns:
        Animation sequence
    """
    animations = []
    
    # Send victim home
    victim_home = victim.get_home_square_id()
    
    animations.append({
        "pawn": victim.id,
        "from": victim.position,
        "to": victim_home,
        "sound": "NE"  # Sad going home!
    })
    
    # Update victim position
    victim.position = None  # Back in home square
    
    print(f"💥 Pawn {attacker.id} captured pawn {victim.id}!")
    
    # Update statistics
    attacker_player = game.red_player if attacker.color == PlayerColor.RED else game.blue_player
    victim_player = game.blue_player if attacker.color == PlayerColor.RED else game.red_player
    
    # TODO: Update stats (kills/deaths)
    
    return animations


def is_at_goal(game: GameState, pawn: Pawn) -> bool:
    """Check if pawn has reached the goal tile."""
    player = game.red_player if pawn.color == PlayerColor.RED else game.blue_player
    goal_tile = player.get_goal_tile_id()
    
    return pawn.position == goal_tile


# ============================================================================
# TURN MANAGEMENT
# ============================================================================

def can_player_move_at_all(game: GameState, dice_value: int) -> bool:
    """
    Check if current player has ANY valid moves with the given dice value.
    
    This checks:
    - Can any pawn start (if rolled 6)?
    - Can any pawn move on the board?
    
    Special Ludo rule (simplified for now):
    - If all pawns are home or at goal, player gets extra rolls
    - For now, we just return False to test turn passing
    
    Args:
        game: Current game state
        dice_value: Result of dice roll
    
    Returns:
        bool: True if player has at least one valid move
    """
    current_player = game.get_current_player()
    
    # Check each pawn
    for pawn in current_player.pawns:
        # Check if can start (leave home square)
        if can_start_pawn(game, pawn, dice_value):
            return True
        
        # Check if can move on board
        if can_move_pawn(game, pawn, dice_value):
            return True
    
    # No valid moves found
    return False


def get_valid_moves(game: GameState, dice_value: int) -> List[Tuple[Pawn, str]]:
    """
    Get all valid moves for the current player.
    
    Returns:
        List of (pawn, move_type) tuples where move_type is "start" or "move"
    """
    current_player = game.get_current_player()
    valid_moves = []
    
    for pawn in current_player.pawns:
        # Check if can start
        if can_start_pawn(game, pawn, dice_value):
            valid_moves.append((pawn, "start"))
        
        # Check if can move
        elif can_move_pawn(game, pawn, dice_value):
            valid_moves.append((pawn, "move"))
    
    return valid_moves


def end_turn(game: GameState, rolled_six: bool):
    """
    End the current turn and switch to next player.
    
    Args:
        rolled_six: If True, player gets another turn
    """
    if not rolled_six:
        game.switch_turn()
    
    # Clear dice value
    game.dice_value = None
    
    print(f"🔄 Turn ended, now: {game.current_turn.value}")


def pass_turn(game: GameState):
    """
    Pass turn to opponent when no valid moves are available.
    """
    print(f"⏭️  {game.current_turn.value} passes (no valid moves)")
    game.switch_turn()
    game.dice_value = None
    print(f"🔄 Now: {game.current_turn.value}'s turn")


# ============================================================================
# GAME STATE CHECKS
# ============================================================================

def check_victory(game: GameState) -> bool:
    """
    Check if current player has won (all pawns at goal).
    
    Returns:
        bool: True if game is over
    """
    current_player = game.get_current_player()
    
    if current_player.has_won():
        game.game_over = True
        game.winner = current_player.color
        print(f"🏆 {current_player.name} wins!")
        return True
    
    return False


# ============================================================================
# EXPORTS
# ============================================================================

__all__ = [
    "prepare_pawns",
    "prepare_all_pawns",
    "can_start_pawn",
    "can_move_pawn",
    "calculate_destination",
    "start_pawn",
    "move_pawn",
    "execute_move",
    "end_turn",
    "check_victory",
    "get_valid_moves"
]


# ============================================================================
# MOVE VALIDATION
# ============================================================================

def can_move_pawn(game: GameState, pawn: Pawn, dice_value: int) -> bool:
    if pawn.position is None or pawn.is_home:
        return False
    
    if pawn.color != game.current_turn:
        return False

    # Get the ACTUAL final spot (after teleports/stops)
    final_dest = get_final_destination(game, pawn, dice_value)

    # If final_dest is None, it means the pawn is going back to Hiška. 
    # Usually, multiple pawns are allowed in the Hiška, so this is always legal.
    if final_dest is None:
        return True

    # RULE: Check if ANY friendly pawn is already at that specific final tile
    player = game.red_player if pawn.color == PlayerColor.RED else game.blue_player
    for p in player.pawns:
        if p.position == final_dest and p.id != pawn.id:
            print(f"🚫 Move blocked: Friendly pawn {p.id} is at the final destination {final_dest}")
            return False
            
    return True

def calculate_destination(game: GameState, pawn: Pawn, steps: int) -> Optional[int]:
    """
    Calculates the final tile ID. 
    Rule: Junctions only trigger if starting the move FROM that tile.
    """
    current_id = pawn.position
    
    for i in range(steps):
        tile = game.board.get(current_id)
        if not tile: return None
        
        # Rule: Junctions trigger ONLY on the first step of the move
        if i == 0:
            junction_id = tile.get_junction(pawn.color)
            if junction_id:
                current_id = junction_id
                continue
        
        # Standard move
        current_id = tile.get_next(pawn.color)
        if current_id is None: return None
        
    return current_id

# ============================================================================
# MOVE EXECUTION
# ============================================================================

def move_pawn(game: GameState, pawn: Pawn, steps: int) -> List[Dict]:
    animations = []
    player = game.red_player if pawn.color == PlayerColor.RED else game.blue_player
    opponent = game.blue_player if pawn.color == PlayerColor.RED else game.red_player
    
    current_id = pawn.position

    # --- STEP 1: CALCULATE THE PATH (Walking) ---
    for i in range(steps):
        tile = game.board.get(current_id)
        if i == 0:
            next_id = tile.get_junction(pawn.color) or tile.get_next(pawn.color)
        else:
            next_id = tile.get_next(pawn.color)

        animations.append({
            "pawn": pawn.id, "from": current_id, "to": next_id,
            "sound": "FIGURA" if i == steps - 1 else None
        })
        current_id = next_id

    # Sync position to the primary landing spot
    pawn.position = current_id

    # --- STEP 2: APPLY LANDING EFFECTS ---
    # We use our logic to find the final target
    landing_tile = game.board.get(pawn.position)
    
    # Check effects in priority order
    teleport_target = landing_tile.get_teleport(pawn.color)
    
    if landing_tile.tile_type == TileType.CENTER_STOP:
        teleport_target = player.get_start_tile_id()
    
    is_deadly = (landing_tile.tile_type == TileType.CENTER_DEATH)
    if is_deadly:
        teleport_target = pawn.get_home_square_id()

    # If an effect triggered, add the secondary jump animation
    if teleport_target is not None:
        animations.append({
            "pawn": pawn.id,
            "from": pawn.position,
            "to": teleport_target,
            "sound": "NE" 
        })
        
        # Update logical position
        if is_deadly:
            pawn.position = None # Back to Hiška
        else:
            pawn.position = teleport_target

    # --- STEP 3: CAPTURES & GOALS ---
    # Now that pawn.position is definitively the final square:
    if pawn.position is not None:
        captured_pawn = check_capture(game, pawn, pawn.position, opponent)
        if captured_pawn:
            animations.extend(capture_enemy_pawn(game, pawn, captured_pawn))
            animations[-1]["sound"] = "DA" 

    if is_at_goal(game, pawn):
        pawn.is_home = True
        player.score += 1

    return animations

# ============================================================================
# TURN MANAGEMENT
# ============================================================================

def execute_move(game: GameState, pawn_id: int, dice_value: int) -> List[Dict]:
    """
    Main entry point for a move.
    Ensures turn synchronization.
    """
    # 1. Get the current player object
    current_player = game.get_current_player()
    
    # 2. Find the pawn and verify ownership
    pawn = next((p for p in current_player.pawns if p.id == pawn_id), None)
    
    if not pawn:
        print(f"❌ Illegal: Player {game.current_turn} tried to move a pawn they don't own.")
        return []
    
    # 3. Validation
    if can_start_pawn(game, pawn, dice_value):
        return start_pawn(game, pawn)
    elif can_move_pawn(game, pawn, dice_value):
        return move_pawn(game, pawn, dice_value)
    
    return []

def get_final_destination(game: GameState, pawn: Pawn, steps: int) -> Optional[int]:
    """
    Predicts the absolute final tile ID, including teleports/traps.
    Returns: tile_id (int) or None if the pawn goes back to the 'Hiška'
    """
    player = game.red_player if pawn.color == PlayerColor.RED else game.blue_player
    
    # 1. Simulate the dice movement
    primary_dest = calculate_destination(game, pawn, steps)
    if primary_dest is None:
        return None
    
    tile = game.board.get(primary_dest)
    
    # 2. Check for Teleport/Stop/Death effects
    # Teleport
    tp = tile.get_teleport(pawn.color)
    if tp:
        return tp
        
    # Stop (Go to Start)
    if tile.tile_type == TileType.CENTER_STOP:
        return player.get_start_tile_id()
        
    # Death (Go back to Hiška)
    if tile.tile_type == TileType.CENTER_DEATH:
        return None # None represents the home square/hiška
        
    return primary_dest

def get_steps_to_finish(game: GameState, pawn: Pawn) -> int:
    """Calculates how many steps are left until the goal tile."""
    if pawn.position is None:
        return 100 # Very far (in home)
    
    steps = 0
    current_id = pawn.position
    # Walk the path until we hit the end
    while current_id is not None:
        tile = game.board.get(current_id)
        if not tile: break
        current_id = tile.get_next(pawn.color)
        if current_id:
            steps += 1
        else:
            break
    return steps





def select_ai_move(game: GameState, dice_value: int) -> Optional[int]:
    """
    The switch that chooses the pawn based on difficulty.
    """
    valid_moves = get_valid_moves(game, dice_value)
    if not valid_moves:
        return None

    player = game.get_current_player()
    difficulty = player.ai_difficulty # e.g., "AI_HARD"

    # --- LEVEL 1: AI_EASY ---
    # Just move the first pawn that can move.
    if difficulty == "AI_EASY":
        return valid_moves[0][0].id

    # --- LEVEL 2 & 3: EVALUATION ---
    scores = []
    opponent = game.blue_player if player.color == PlayerColor.RED else game.red_player

    for pawn, move_type in valid_moves:
        score = 0
        # Basic Medium weights
        if move_type == "start": score += 10
        
        final_pos = get_final_destination(game, pawn, dice_value)
        if final_pos is None: # Deadly tile
            score -= 15
        else:
            # Capture bonus
            if check_capture(game, pawn, final_pos, opponent):
                score += 12
            # Stop tile penalty
            if game.board[final_pos].tile_type == TileType.CENTER_STOP:
                score -= 5

        # --- LEVEL 3: AI_HARD (The Distance Factor) ---
        if difficulty == "AI_HARD":
            # How far from finish (0 to ~40 steps)
            dist = get_steps_to_finish(game, pawn)
            # Higher weight for pawns near the end
            # (40 / 100) = 0.4 penalty vs (2 / 100) = 0.02 penalty
            score -= (dist / 100.0)

        scores.append((pawn.id, score))

    # Pick the pawn with the highest score
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[0][0]


#new
def start_turn(game: GameState):
    """Call at the beginning of every turn."""
    player = game.get_current_player()
    
    if player.is_pc:
        # 1. Auto Roll Dice
        dice = random.randint(1, 6)
        game.dice_value = dice
        
        # 2. Select Move using the new brain
        pawn_id = select_ai_move(game, dice)
        
        if pawn_id:
            return execute_move(game, pawn_id, dice)
        else:
            return pass_turn(game)


