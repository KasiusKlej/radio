# ============================================================================
# CLOVEK (LUDO) - Main Module
# ============================================================================
# Factory settings, blueprint setup, and game initialization
# ============================================================================

import os
import uuid
import random
from pathlib import Path
from flask import Blueprint, render_template, session, redirect, url_for, jsonify, request

# =============================================================================
# 🛠️ FACTORY SETTINGS (Admin Scope) - for calibrating animation
# =============================================================================

FACTORY = {
    # Board geometry
    "geometry": {
        "width": 888,           # Canvas width (matches tabla.png)
        "height": 533,          # Canvas height (matches tabla.png)
        "background": "#0B6B2A" # Green board background
    },
    
    # Dice animation settings
    "dice": {
        "size": 48,             # Dice display size in pixels
        "animation_speed": 120, # Animation frame delay (ms)
        "roll_duration": 800,   # Total roll animation time (ms)
        "bounce_count": 3       # Number of bounces during roll
    },
    
    # Dice throw areas (where dice appears during player's turn)
    "dice_throw_area": {
        "red": {
            "x": 100,           # Red player dice position
            "y": 450,
            "width": 60,
            "height": 60
        },
        "blue": {
            "x": 730,           # Blue player dice position
            "y": 50,
            "width": 60,
            "height": 60
        }
    },
    
    # Statistics display areas (overlays on board)
    "stats_display": {
        "red": {
            "x": 50,            # Red player stats panel
            "y": 400,
            "width": 150,
            "height": 120
        },
        "blue": {
            "x": 690,           # Blue player stats panel
            "y": 30,
            "width": 150,
            "height": 120
        }
    },
    
    # Pawn animation settings
    "pawns": {
        "width": 28,            # Pawn display size
        "height": 28,
        "move_speed": 300,      # Movement animation speed (ms per tile)
        "capture_animation": 500, # Capture/return animation time (ms)
        "home_celebration": 1000  # Celebration when reaching goal (ms)
    },
    
    # Asset paths
    "assets": {
        "dice_path": "/static/clovek/dice/",
        "pawn_path": "/static/clovek/pawns/",
        "board_path": "/static/clovek/tabla.png",
        "sound_path": "/static/clovek/sounds/"
    },
    
    # Avatar/profile pictures
    "avatars": {
        "profile_pictures": "/static/clovek/characters/",
        "default_red": "👤",
        "default_blue": "🤖"
    },
    
    # Game modes configuration
    "modes": {
        "HUMAN": {
            "two_players": True,
            "local": True
        },
        "AI": {
            "levels": {
                "AI_EASY": {
                    "think_time": 1000,      # Delay before AI move (ms)
                    "difficulty": 0.3,       # Decision quality (0-1)
                    "random_factor": 0.4     # Randomness in moves
                },
                "AI_MEDIUM": {
                    "think_time": 1500,
                    "difficulty": 0.6,
                    "random_factor": 0.2
                },
                "AI_HARD": {
                    "think_time": 2000,
                    "difficulty": 0.9,
                    "random_factor": 0.05
                }
            }
        },
        "NETWORK": {
            "sync_rate": 30,            # Update frequency (fps)
            "timeout": 60000,           # Move timeout (ms)
            "reconnect_attempts": 3
        }
    },
    
    # Animation timings
    "animation": {
        "dice_roll": 800,        # Dice roll animation
        "pawn_move": 300,        # Single tile movement
        "pawn_capture": 500,     # Capture animation
        "pawn_start": 600,       # Pawn leaving home square
        "pawn_home": 1000,       # Pawn entering goal
        "turn_switch": 500       # Delay between turns
    },
    
    # Sound settings
    "sounds": {
        "enabled": True,
        "volume": 0.7,
        "effects": {
            "dice_roll": "dice_roll.mp3",
            "pawn_move": "pawn_move.mp3",
            "pawn_capture": "pawn_capture.mp3",
            "pawn_home": "pawn_home.mp3",
            "win": "victory.mp3"
        }
    },
    
    # Statistics tracking (9 stats per player)
    "statistics": {
        "tracked": [
            "points",           # stat1: Total points scored
            "dice_average",     # stat2: Average dice roll
            "number_of_rolls",  # stat3: Total dice rolls
            "number_of_steps",  # stat4: Total steps moved
            "pit_starts",       # stat5: Times pawn left home square
            "kills",            # stat6: Enemy pawns captured
            "deaths",           # stat7: Own pawns captured
            "time",             # stat8: Total game time (seconds)
            "games_won"         # stat9: Games won
        ]
    }
}


# =============================================================================
# 📂 PATH RESOLUTION
# =============================================================================

# ASSETS: Points to .../mywebsite/static/clovek/
BASE = Path(__file__).resolve().parent
STATIC_DIR = BASE.parent / "static" / "clovek"

# Ensure directories exist
STATIC_DIR.mkdir(parents=True, exist_ok=True)
(STATIC_DIR / "dice").mkdir(exist_ok=True)
(STATIC_DIR / "pawns").mkdir(exist_ok=True)
(STATIC_DIR / "characters").mkdir(exist_ok=True)
(STATIC_DIR / "sounds").mkdir(exist_ok=True)


# =============================================================================
# 🛰️ BLUEPRINT SETUP
# =============================================================================

clovek_bp = Blueprint(
    "clovek",
    __name__,
    template_folder="templates",
    static_folder=str(STATIC_DIR),
    static_url_path="/static/clovek"
)


# =============================================================================
# 🔧 SHARED HELPERS
# =============================================================================

def ensure_sid():
    """
    Identical to Metropoly/CardGames to maintain cross-app compatibility.
    Ensures session has a unique session ID and default language.
    """
    if "user_sid" not in session:
        session["user_sid"] = str(uuid.uuid4())
    
    if "lang" not in session:
        session["lang"] = "slo"
    
    return session["user_sid"]


# =============================================================================
# 🎮 ACTIVE MATCHES STORAGE
# =============================================================================

# Global in-memory store for active matches (Player SIDs)
# In production, use Redis or database
active_matches = {}


# =============================================================================
# 📊 STATISTICS HELPER FUNCTIONS
# =============================================================================

def init_player_stats():
    """Initialize statistics dictionary for a new player."""
    return {
        "stat1": 0.0,  # points
        "stat2": 0.0,  # dice_average
        "stat3": 0.0,  # number_of_rolls
        "stat4": 0.0,  # number_of_steps
        "stat5": 0.0,  # pit_starts
        "stat6": 0.0,  # kills
        "stat7": 0.0,  # deaths
        "stat8": 0.0,  # time
        "stat9": 0.0   # games_won
    }


def update_stat(player_stats, stat_name, value):
    """
    Update a specific statistic for a player.
    
    Args:
        player_stats (dict): Player's statistics dictionary
        stat_name (str): Name of statistic (e.g., "kills", "dice_average")
        value (float): New value or increment
    """
    stat_mapping = {
        "points": "stat1",
        "dice_average": "stat2",
        "number_of_rolls": "stat3",
        "number_of_steps": "stat4",
        "pit_starts": "stat5",
        "kills": "stat6",
        "deaths": "stat7",
        "time": "stat8",
        "games_won": "stat9"
    }
    
    if stat_name in stat_mapping:
        stat_key = stat_mapping[stat_name]
        player_stats[stat_key] = value


def increment_stat(player_stats, stat_name, increment=1.0):
    """Increment a statistic by a given amount."""
    stat_mapping = {
        "points": "stat1",
        "dice_average": "stat2",
        "number_of_rolls": "stat3",
        "number_of_steps": "stat4",
        "pit_starts": "stat5",
        "kills": "stat6",
        "deaths": "stat7",
        "time": "stat8",
        "games_won": "stat9"
    }
    
    if stat_name in stat_mapping:
        stat_key = stat_mapping[stat_name]
        player_stats[stat_key] = player_stats.get(stat_key, 0.0) + increment


def get_stat(player_stats, stat_name):
    """Get a specific statistic value."""
    stat_mapping = {
        "points": "stat1",
        "dice_average": "stat2",
        "number_of_rolls": "stat3",
        "number_of_steps": "stat4",
        "pit_starts": "stat5",
        "kills": "stat6",
        "deaths": "stat7",
        "time": "stat8",
        "games_won": "stat9"
    }
    
    if stat_name in stat_mapping:
        stat_key = stat_mapping[stat_name]
        return player_stats.get(stat_key, 0.0)
    
    return 0.0


def calculate_dice_average(player_stats):
    """
    Calculate and update dice average.
    Should be called after each dice roll.
    """
    total_rolls = get_stat(player_stats, "number_of_rolls")
    if total_rolls > 0:
        # This assumes you're tracking total dice sum elsewhere
        # For now, just return current average
        return get_stat(player_stats, "dice_average")
    return 0.0


def format_stats_for_display(player_stats, language="slo"):
    """
    Format statistics for display in UI.
    
    Returns:
        dict: Formatted statistics with labels
    """
    from .engine.labels import get_stat_label, Language
    
    lang = Language.SLOVENIAN if language == "slo" else Language.ENGLISH
    
    return {
        get_stat_label("points", lang): f"{get_stat(player_stats, 'points'):.0f}",
        get_stat_label("dice_average", lang): f"{get_stat(player_stats, 'dice_average'):.2f}",
        get_stat_label("number_of_rolls", lang): f"{get_stat(player_stats, 'number_of_rolls'):.0f}",
        get_stat_label("number_of_steps", lang): f"{get_stat(player_stats, 'number_of_steps'):.0f}",
        get_stat_label("pit_starts", lang): f"{get_stat(player_stats, 'pit_starts'):.0f}",
        get_stat_label("kills", lang): f"{get_stat(player_stats, 'kills'):.0f}",
        get_stat_label("deaths", lang): f"{get_stat(player_stats, 'deaths'):.0f}",
        get_stat_label("time", lang): f"{get_stat(player_stats, 'time'):.0f}s"
    }


# =============================================================================
# 🌍 CONTEXT PROCESSOR (Win95 Menu Integration)
# =============================================================================

@clovek_bp.context_processor
def inject_clovek_ui():
    """
    Inject common variables into all templates.
    This makes FACTORY and other settings available in templates.
    """
    return {
        "FACTORY": FACTORY,
        "lang": session.get("lang", "slo"),
        "user_sid": session.get("user_sid", "")
    }


# =============================================================================
# 🎲 GAME HELPER FUNCTIONS
# =============================================================================

def roll_dice():
    """Roll a six-sided dice."""
    return random.randint(1, 6)


def can_move_pawn(game_state, pawn_id, dice_value):
    """
    Check if a pawn can be moved with the given dice value.
    
    Args:
        game_state: Current game state
        pawn_id: ID of the pawn to move
        dice_value: Result of dice roll
    
    Returns:
        bool: True if move is valid
    """
    # TODO: Implement actual move validation logic
    # This is a placeholder
    return True


def calculate_new_position(current_position, dice_value, player_color):
    """
    Calculate new position after moving dice_value steps.
    
    Args:
        current_position: Current tile ID
        dice_value: Number of steps to move
        player_color: "red" or "blue"
    
    Returns:
        int: New tile ID
    """
    # TODO: Implement actual position calculation with board logic
    # This is a placeholder
    return current_position + dice_value if current_position else None


# =============================================================================
# 🎯 MATCH MANAGEMENT
# =============================================================================

def create_match(host_sid, mode="NETWORK"):
    """Create a new match and return match ID."""
    match_id = str(uuid.uuid4())
    active_matches[match_id] = {
        "host": host_sid,
        "guest": None,
        "mode": mode,
        "status": "waiting",
        "created": "now"  # TODO: Use actual timestamp
    }
    return match_id


def join_match(match_id, guest_sid):
    """Join an existing match."""
    if match_id in active_matches:
        active_matches[match_id]["guest"] = guest_sid
        active_matches[match_id]["status"] = "active"
        return True
    return False


def get_match(match_id):
    """Get match by ID."""
    return active_matches.get(match_id)


def end_match(match_id):
    """End and remove a match."""
    if match_id in active_matches:
        del active_matches[match_id]


# =============================================================================
# 📦 EXPORTS
# =============================================================================

__all__ = [
    "clovek_bp",
    "FACTORY",
    "ensure_sid",
    "active_matches",
    "init_player_stats",
    "update_stat",
    "increment_stat",
    "get_stat",
    "calculate_dice_average",
    "format_stats_for_display",
    "roll_dice",
    "can_move_pawn",
    "calculate_new_position",
    "create_match",
    "join_match",
    "get_match",
    "end_match"
]
