# ============================================================================
# CLOVEK (LUDO) - Game Engine
# ============================================================================
# Core game logic, move validation, and pawn management
# ============================================================================

from typing import List, Dict, Optional, Tuple
from .model import GameState, PlayerColor, Pawn, Player

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


def can_move_pawn(game: GameState, pawn: Pawn, dice_value: int) -> bool:
    """
    Check if a pawn can move the given number of steps.
    
    Args:
        game: Current game state
        pawn: The pawn to check
        dice_value: Number of steps to move
    
    Returns:
        bool: True if move is valid
    """
    # Pawn must be on the board
    if pawn.position is None:
        return False
    
    # Pawn must not be at goal already
    if pawn.is_home:
        return False
    
    # Calculate destination
    destination = calculate_destination(game, pawn, dice_value)
    
    if destination is None:
        return False  # Invalid move (e.g., overshoots goal)
    
    # Check if destination is blocked by own pawn
    player = game.red_player if pawn.color == PlayerColor.RED else game.blue_player
    
    for p in player.pawns:
        if p.position == destination and p.id != pawn.id:
            return False  # Blocked by own pawn
    
    return True


def calculate_destination(game: GameState, pawn: Pawn, steps: int) -> Optional[int]:
    """
    Calculate the destination tile after moving 'steps' from current position.
    
    Args:
        game: Current game state
        pawn: The pawn to move
        steps: Number of steps to move
    
    Returns:
        int: Destination tile ID, or None if move is invalid
    """
    if pawn.position is None:
        return None
    
    current = pawn.position
    destination = current
    
    # Walk through the board step by step
    for _ in range(steps):
        tile = game.board.get(destination)
        if not tile:
            return None  # Invalid tile
        
        # Get next tile for this pawn's color
        next_tile = tile.get_next(pawn.color)
        
        if next_tile is None:
            return None  # No next tile (e.g., at goal)
        
        destination = next_tile
    
    return destination


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


def move_pawn(game: GameState, pawn: Pawn, steps: int) -> List[Dict]:
    """
    Move a pawn the given number of steps.
    Handles captures, teleports, junctions, etc.
    
    Returns:
        Animation sequence (may include multiple steps and captures)
    """
    animations = []
    
    current = pawn.position
    player = game.red_player if pawn.color == PlayerColor.RED else game.blue_player
    opponent = game.blue_player if pawn.color == PlayerColor.RED else game.red_player
    
    # Move step by step
    for step in range(steps):
        tile = game.board.get(current)
        if not tile:
            break
        
        # Get next tile
        next_tile_id = tile.get_next(pawn.color)
        
        if next_tile_id is None:
            break  # Reached end
        
        # Check for teleport
        teleport = tile.get_teleport(pawn.color)
        if teleport:
            next_tile_id = teleport
            print(f"↩️  Pawn {pawn.id} teleported: {current} → {next_tile_id}")
        
        # Check for junction
        junction = tile.get_junction(pawn.color)
        if junction:
            # TODO: Implement junction decision logic
            # For now, always take the junction
            next_tile_id = junction
            print(f"🔀 Pawn {pawn.id} took junction: {current} → {next_tile_id}")
        
        # Add animation step
        is_last_step = (step == steps - 1)
        
        animations.append({
            "pawn": pawn.id,
            "from": current,
            "to": next_tile_id,
            "sound": None if not is_last_step else "FIGURA"
        })
        
        current = next_tile_id
    
    # Update pawn position
    old_position = pawn.position
    pawn.position = current
    
    # Check for capture
    captured_pawn = check_capture(game, pawn, current, opponent)
    
    if captured_pawn:
        # Add capture animation
        capture_anim = capture_enemy_pawn(game, pawn, captured_pawn)
        animations.extend(capture_anim)
        
        # Change last sound to victory sound
        if animations:
            animations[-1]["sound"] = "DA"  # Victory!
    
    # Check if pawn reached goal
    if is_at_goal(game, pawn):
        pawn.is_home = True
        player.score += 1
        print(f"🏁 Pawn {pawn.id} reached goal!")
    
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


def execute_move(game: GameState, pawn_id: int, dice_value: int) -> List[Dict]:
    """
    Execute a move for the given pawn.
    
    Returns:
        Animation sequence
    """
    current_player = game.get_current_player()
    
    # Find the pawn
    pawn = None
    for p in current_player.pawns:
        if p.id == pawn_id:
            pawn = p
            break
    
    if not pawn:
        print(f"❌ Pawn {pawn_id} not found")
        return []
    
    # Check if can start
    if can_start_pawn(game, pawn, dice_value):
        return start_pawn(game, pawn)
    
    # Check if can move
    elif can_move_pawn(game, pawn, dice_value):
        return move_pawn(game, pawn, dice_value)
    
    else:
        print(f"❌ Pawn {pawn_id} cannot move")
        return []


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
