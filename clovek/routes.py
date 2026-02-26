# clovek/routes.py
import uuid
import random
from flask import render_template, session, request, jsonify, redirect, url_for, current_app, Response
from .clovek import clovek_bp

# Import game model and labels
from .engine.model import GameState, GameMode, PlayerColor, initialize_game
from .engine.labels import Language, get_all_labels, set_language

# =============================================================================
# 🎮 ACTIVE GAMES STORAGE
# =============================================================================
# In production, use Redis or database
active_games = {}

# =============================================================================
# 🧠 SESSION SETUP
# =============================================================================
def ensure_session():
    """Initialize session with default values."""
    session.setdefault("sid", str(uuid.uuid4()))
    session.setdefault("mode", "NETWORK")
    session.setdefault("clovek_paused", True)
    session.setdefault("language", "slo")
    session.setdefault("red_player_name", "Rdeči igralec")
    session.setdefault("blue_player_name", "Modri igralec")
    session.setdefault("options", {
        "fast": False,
        "sound": True,
        "save_result": True
    })


def get_or_create_game() -> GameState:
    """Get existing game or create new one for this session."""
    ensure_session()
    sid = session["sid"]
    
    if sid not in active_games:
        # Create new game with current mode
        mode_str = session.get("mode", "NETWORK")
        
        # Convert string to GameMode enum
        try:
            mode = GameMode[mode_str]
        except KeyError:
            mode = GameMode.NETWORK
        
        # Create game
        active_games[sid] = initialize_game(
            mode=mode,
            red_name=session.get("red_player_name", "Rdeči igralec"),
            blue_name=session.get("blue_player_name", "Modri igralec")
        )
    
    return active_games[sid]


def build_clovek_context():
    """Explicit context – never merged globally."""
    ensure_session()
    game = get_or_create_game()
    language = set_language(session.get("language", "slo"))

    # Import factory settings
    from .clovek import FACTORY

    return {
        "factory": FACTORY,
        "state": {
            "mode": session["mode"],
            "paused": session["clovek_paused"],
            "language": session["language"],
            "options": session.get("options", {}),
            "current_turn": game.current_turn.value,
            "dice_value": game.dice_value,
            "game_over": game.game_over,
            "winner": game.winner.value if game.winner else None,
            "red_player": {
                "name": game.red_player.name,
                "score": game.red_player.score,
                "pawns_home": game.red_player.pawns_at_goal(),
                "is_ai": game.red_player.is_ai,
                "avatar": session.get("red_avatar", "👤")
            },
            "blue_player": {
                "name": game.blue_player.name,
                "score": game.blue_player.score,
                "pawns_home": game.blue_player.pawns_at_goal(),
                "is_ai": game.blue_player.is_ai,
                "avatar": session.get("blue_avatar", "🤖" if game.blue_player.is_ai else "👤")
            }
        },
        "labels": get_all_labels(language),
        "modes": [
            "HUMAN",
            "AI_EASY",
            "AI_MEDIUM",
            "AI_HARD",
            "NETWORK",
        ],
    }


# =============================================================================
# MAIN PAGE
# =============================================================================
from flask import current_app, Response
@clovek_bp.route("/")
def index():
    context = {
        "CLOVEK": build_clovek_context()
    }

    template = current_app.jinja_env.get_template("clovek_game.html")
    html = template.render(context)

    return Response(html)

# =============================================================================
# API
# =============================================================================
@clovek_bp.route("/api/state", methods=["POST"])
@clovek_bp.route("/api/state/", methods=["POST"])
def api_state():
    ensure_session()

    data = request.get_json(silent=True) or {}
    mode = data.get("mode")

    if mode in {
        "HUMAN",
        "AI_EASY",
        "AI_MEDIUM",
        "AI_HARD",
        "NETWORK",
    }:
        session["mode"] = mode

    return jsonify(ok=True, mode=session["mode"])









# =============================================================================
# 🎮 MENU ROUTES - GAME
# =============================================================================
@clovek_bp.route("/start")
@clovek_bp.route("/start/")
def start_game():
    """Start a new game based on current mode."""
    ensure_session()
    sid = session["sid"]
    mode = session.get("mode", "NETWORK")
    
    # Network mode: Can't start until other player joins
    if mode == "NETWORK":
        # Keep paused until matched with opponent
        session["clovek_paused"] = True
        return jsonify({
            "success": False,
            "message": "Waiting for opponent to join..."
        })
    
    # AI/Human modes: Start immediately
    if mode in ["HUMAN", "AI_EASY", "AI_MEDIUM", "AI_HARD"]:
        # Clear any existing game
        if sid in active_games:
            del active_games[sid]
        
        # Create fresh game
        game = get_or_create_game()
        
        # Unpause game
        session["clovek_paused"] = False
        
        return redirect(url_for("clovek.index"))
    
    return redirect(url_for("clovek.index"))


@clovek_bp.route("/api/game/new", methods=["POST"])
def api_new_game():
    """API endpoint to start new game."""
    ensure_session()
    sid = session["sid"]
    
    # Remove old game
    if sid in active_games:
        del active_games[sid]
    
    # Create fresh game
    game = get_or_create_game()
    
    # Start game unless in network mode waiting for opponent
    if session["mode"] != "NETWORK":
        session["clovek_paused"] = False
    
    return jsonify({
        "success": True,
        "message": "Nova igra začeta",
        "paused": session["clovek_paused"]
    })


@clovek_bp.route("/api/game/end", methods=["POST"])
def api_end_game():
    """End current game."""
    ensure_session()
    sid = session["sid"]
    
    if sid in active_games:
        game = active_games[sid]
        game.game_over = True
        
        # Save statistics if enabled
        if session.get("options", {}).get("save_result", False):
            # TODO: Save to database
            pass
        
        # Pause game
        session["clovek_paused"] = True
    
    return jsonify({
        "success": True,
        "message": "Igra končana"
    })


@clovek_bp.route("/exit")
@clovek_bp.route("/exit/")
def exit_game():
    """Exit game and clear session."""
    sid = session.get("sid")
    
    # Remove game from active games
    if sid and sid in active_games:
        del active_games[sid]
    
    # Remove only clovek-related session keys
    clovek_keys = [k for k in session.keys() if k.startswith("clovek_") or k in ["sid", "mode"]]
    for k in clovek_keys:
        session.pop(k, None)
    
    # Redirect to homepage instead of clovek index
    return redirect("/")  


# =============================================================================
# 🎮 MENU ROUTES - OPTIONS
# =============================================================================
@clovek_bp.route("/api/options/toggle", methods=["POST"])
def api_toggle_option():
    """Toggle boolean options (fast, sound, save_result)."""
    ensure_session()
    
    data = request.get_json() or {}
    option = data.get("option")
    
    if option in ["fast", "sound", "save_result"]:
        options = session.get("options", {})
        current_value = options.get(option, False)
        options[option] = not current_value
        session["options"] = options
        session.modified = True
        
        return jsonify({
            "success": True,
            "option": option,
            "value": options[option]
        })
    
    return jsonify({
        "success": False,
        "error": "Invalid option"
    }), 400


@clovek_bp.route("/api/statistics")
def api_statistics():
    """Get player statistics."""
    ensure_session()
    game = get_or_create_game()
    
    # TODO: Load from database for persistent stats
    # For now, return current game stats
    
    return jsonify({
        "red_player": {
            "name": game.red_player.name,
            "score": game.red_player.score,
            "pawns_home": game.red_player.pawns_at_goal(),
            "games_won": session.get("red_games_won", 0),
            "games_played": session.get("red_games_played", 0),
            "total_moves": session.get("red_total_moves", 0)
        },
        "blue_player": {
            "name": game.blue_player.name,
            "score": game.blue_player.score,
            "pawns_home": game.blue_player.pawns_at_goal(),
            "games_won": session.get("blue_games_won", 0),
            "games_played": session.get("blue_games_played", 0),
            "total_moves": session.get("blue_total_moves", 0)
        }
    })


# MENU OPTIONS
# ✓ Hitro (Fast) - Toggle
# ✓ Zvok (Sound) - Toggle
# ✓ Shrani rezultat (Save Result) - Toggle
# ───────
# Statistika (Statistics) - Action
# Tabla (Board) - Action


# =============================================================================
# 🎮 MENU ROUTES - OPPONENT SETTINGS
# =============================================================================
@clovek_bp.route("/human")
@clovek_bp.route("/human/")
def set_human():
    """Set mode to two human players (hotseat)."""
    ensure_session()
    sid = session["sid"]
    
    # If switching modes, end current game
    if session.get("mode") != "HUMAN" and sid in active_games:
        del active_games[sid]
    
    session["mode"] = "HUMAN"
    session["red_player_name"] = session.get("red_player_name", "Rdeči igralec")
    session["blue_player_name"] = session.get("blue_player_name", "Modri igralec")
    session["clovek_paused"] = True
    session.modified = True
    
    return redirect(url_for("clovek.index"))

# --- AI LEVELS ---
@clovek_bp.route("/computer1")
@clovek_bp.route("/computer1/")
def set_level1():
    """Set mode to Easy AI."""
    ensure_session()
    sid = session["sid"]
    
    # If switching modes, end current game
    if session.get("mode") != "AI_EASY" and sid in active_games:
        del active_games[sid]
    
    session["mode"] = "AI_EASY"
    session["red_player_name"] = session.get("red_player_name", "Rdeči igralec")
    session["blue_player_name"] = "Računalnik (Slab)"
    session["clovek_paused"] = True
    session.modified = True
    
    return redirect(url_for("clovek.index"))

@clovek_bp.route("/computer2")
@clovek_bp.route("/computer2/")
def set_level2():
    """Set mode to Medium AI."""
    ensure_session()
    sid = session["sid"]
    
    # If switching modes, end current game
    if session.get("mode") != "AI_MEDIUM" and sid in active_games:
        del active_games[sid]
    
    session["mode"] = "AI_MEDIUM"
    session["red_player_name"] = session.get("red_player_name", "Rdeči igralec")
    session["blue_player_name"] = "Računalnik (Dober)"
    session["clovek_paused"] = True
    session.modified = True
    
    return redirect(url_for("clovek.index"))

@clovek_bp.route("/computer3")
@clovek_bp.route("/computer3/")
def set_level3():
    """Set mode to Hard AI."""
    ensure_session()
    sid = session["sid"]
    
    # If switching modes, end current game
    if session.get("mode") != "AI_HARD" and sid in active_games:
        del active_games[sid]
    
    session["mode"] = "AI_HARD"
    session["red_player_name"] = session.get("red_player_name", "Rdeči igralec")
    session["blue_player_name"] = "Računalnik (Zelo dober)"
    session["clovek_paused"] = True
    session.modified = True
    
    return redirect(url_for("clovek.index"))

@clovek_bp.route("/network")
@clovek_bp.route("/network/")
def set_network():
    """Set mode to network multiplayer."""
    ensure_session()
    sid = session["sid"]
    
    # If switching to network mode, end current game
    if session.get("mode") != "NETWORK" and sid in active_games:
        del active_games[sid]
    
    session["mode"] = "NETWORK"
    session["clovek_paused"] = True  # Always paused until matched
    session.modified = True
    
    return redirect(url_for("clovek.index"))


@clovek_bp.route("/api/opponent", methods=["POST"])
def api_set_opponent():
    """API endpoint to set opponent mode."""
    ensure_session()
    sid = session["sid"]
    
    data = request.get_json() or {}
    mode = data.get("mode")
    
    if mode not in ["HUMAN", "AI_EASY", "AI_MEDIUM", "AI_HARD", "NETWORK"]:
        return jsonify({
            "success": False,
            "error": "Invalid mode"
        }), 400
    
    # If switching modes, end current game
    if session.get("mode") != mode and sid in active_games:
        del active_games[sid]
    
    # Update session
    session["mode"] = mode
    session["clovek_paused"] = True
    
    # Update blue player name based on mode
    if mode == "AI_EASY":
        session["blue_player_name"] = "Računalnik (Slab)"
    elif mode == "AI_MEDIUM":
        session["blue_player_name"] = "Računalnik (Dober)"
    elif mode == "AI_HARD":
        session["blue_player_name"] = "Računalnik (Zelo dober)"
    else:
        session["blue_player_name"] = session.get("blue_player_name", "Modri igralec")
    
    session.modified = True
    
    return jsonify({
        "success": True,
        "mode": mode,
        "paused": session["clovek_paused"]
    })


# =============================================================================
# 🎮 MENU ROUTES - LANGUAGE
# =============================================================================
@clovek_bp.route("/api/language", methods=["POST"])
@clovek_bp.route("/api/language/", methods=["POST"])
def api_set_language():
    """Set interface language."""
    ensure_session()
    
    data = request.get_json() or {}
    lang = data.get("language")
    
    if lang not in ["slo", "eng"]:
        return jsonify({
            "success": False,
            "error": "Invalid language"
        }), 400
    
    session["language"] = lang
    session.modified = True
    
    return jsonify({
        "success": True,
        "language": lang
    })


@clovek_bp.route("/api/labels/<lang>")
def api_get_labels(lang):
    """Get all labels for specified language."""
    language = set_language(lang)
    labels = get_all_labels(language)
    
    return jsonify(labels)


# =============================================================================
# 🎮 PROFILE ROUTES
# =============================================================================
@clovek_bp.route("/api/player/name", methods=["POST"])
def api_update_player_name():
    """Update player name."""
    ensure_session()
    
    data = request.get_json() or {}
    color = data.get("color")  # "red" or "blue"
    name = data.get("name", "").strip()
    
    if not name or len(name) > 50:
        return jsonify({
            "success": False,
            "error": "Invalid name"
        }), 400
    
    # Update session
    session[f"{color}_player_name"] = name
    session.modified = True
    
    # Update active game if exists
    sid = session["sid"]
    if sid in active_games:
        game = active_games[sid]
        if color == "red":
            game.red_player.name = name
        elif color == "blue":
            game.blue_player.name = name
    
    return jsonify({
        "success": True,
        "color": color,
        "name": name
    })


@clovek_bp.route("/api/player/avatar", methods=["POST"])
def api_update_player_avatar():
    """Update player avatar."""
    ensure_session()
    
    data = request.get_json() or {}
    color = data.get("color")
    avatar = data.get("avatar", "👤")
    
    session[f"{color}_avatar"] = avatar
    session.modified = True
    
    return jsonify({
        "success": True,
        "color": color,
        "avatar": avatar
    })


# =============================================================================
# 🎮 LOBBY & CHATROOM ROUTES
# =============================================================================
@clovek_bp.route("/api/lobby/users")
def api_lobby_users():
    """Get list of online users in lobby."""
    # TODO: Implement with WebSocket or polling
    # For now, return mock data
    return jsonify({
        "users": [
            {"username": "Janez", "status": "online", "ready": False},
            {"username": "Maja", "status": "online", "ready": True}
        ]
    })


@clovek_bp.route("/api/chat/send", methods=["POST"])
def api_chat_send():
    """Send chat message (max 40 characters)."""
    ensure_session()
    
    data = request.get_json() or {}
    message = data.get("message", "").strip()
    
    # Validate message length (max 40 characters)
    if not message:
        return jsonify({
            "success": False,
            "error": "Empty message"
        }), 400
    
    if len(message) > 40:
        message = message[:40]  # Truncate to 40 chars
    
    # TODO: Broadcast to other users in room
    # TODO: Store in chat history (crop at top if too long)
    
    username = session.get("red_player_name", "Anonymous")
    
    return jsonify({
        "success": True,
        "username": username,
        "message": message,
        "timestamp": "now"
    })


@clovek_bp.route("/api/chat/history")
def api_chat_history():
    """Get recent chat messages."""
    # TODO: Load from database or in-memory store
    # Keep only last N messages
    return jsonify({
        "messages": [
            {"username": "System", "message": "Dobrodošli v klepetalnici!", "timestamp": "12:00"}
        ]
    })


# =============================================================================
# 🎮 GAME FLOW - DICE & PAWNS
# =============================================================================
@clovek_bp.route("/api/game/roll-dice", methods=["POST"])
def api_roll_dice():
    """Player rolls the dice."""
    ensure_session()
    sid = session["sid"]
    
    # Check if game exists
    if sid not in active_games:
        return jsonify({
            "success": False,
            "error": "No active game"
        }), 400
    
    game = active_games[sid]
    
    # Check if game is paused
    if session.get("clovek_paused", True):
        return jsonify({
            "success": False,
            "error": "Game is paused"
        }), 400
    
    # Check if game is over
    if game.game_over:
        return jsonify({
            "success": False,
            "error": "Game is over"
        }), 400
    
    # Check if dice already rolled this turn
    if game.dice_value is not None:
        return jsonify({
            "success": False,
            "error": "Dice already rolled this turn"
        }), 400
    
    # Roll dice (1-6)
    dice_value = random.randint(1, 6)
    game.dice_value = dice_value
    
    # TODO: Check for valid moves, AI turn, etc.
    
    return jsonify({
        "success": True,
        "dice_value": dice_value,
        "current_turn": game.current_turn.value
    })


@clovek_bp.route("/api/game/move-pawn", methods=["POST"])
def api_move_pawn():
    """Move a pawn."""
    ensure_session()
    sid = session["sid"]
    
    # Check if game exists
    if sid not in active_games:
        return jsonify({
            "success": False,
            "error": "No active game"
        }), 400
    
    game = active_games[sid]
    
    data = request.get_json() or {}
    pawn_id = data.get("pawn_id")
    
    # Check if game is paused
    if session.get("clovek_paused", True):
        return jsonify({
            "success": False,
            "error": "Game is paused"
        }), 400
    
    # Check if game is over
    if game.game_over:
        return jsonify({
            "success": False,
            "error": "Game is over"
        }), 400
    
    # Check if dice has been rolled
    if game.dice_value is None:
        return jsonify({
            "success": False,
            "error": "Roll dice first"
        }), 400
    
    # TODO: Implement move validation and execution
    # This will use the game engine logic
    
    # For now, basic response
    return jsonify({
        "success": True,
        "pawn_id": pawn_id,
        "message": "Move executed"
    })


@clovek_bp.route("/api/game/state")
def api_get_game_state():
    """Get current game state."""
    ensure_session()
    sid = session["sid"]
    
    if sid not in active_games:
        return jsonify({
            "success": False,
            "error": "No active game"
        }), 400
    
    game = active_games[sid]
    
    return jsonify({
        "success": True,
        "paused": session.get("clovek_paused", True),
        "current_turn": game.current_turn.value,
        "dice_value": game.dice_value,
        "game_over": game.game_over,
        "winner": game.winner.value if game.winner else None,
        "red_player": {
            "name": game.red_player.name,
            "score": game.red_player.score,
            "pawns": [
                {
                    "id": p.id,
                    "position": p.position,
                    "is_home": p.is_home
                }
                for p in game.red_player.pawns
            ]
        },
        "blue_player": {
            "name": game.blue_player.name,
            "score": game.blue_player.score,
            "pawns": [
                {
                    "id": p.id,
                    "position": p.position,
                    "is_home": p.is_home
                }
                for p in game.blue_player.pawns
            ]
        }
    })


@clovek_bp.route("/api/board/tiles")
def api_get_board_tiles():
    """Get board tile positions for animation."""
    from .engine.model import create_board
    
    board = create_board()
    
    # Convert board tiles to simple position dictionary
    tiles = {}
    for tile_id, tile in board.items():
        tiles[tile_id] = {
            "id": tile_id,
            "x": tile.x,
            "y": tile.y,
            "type": tile.tile_type.value
        }
    
    return jsonify({
        "success": True,
        "tiles": tiles,
        "count": len(tiles)
    })


# =============================================================================
# 🎮 HELP
# =============================================================================
@clovek_bp.route("/about")
@clovek_bp.route("/about/")
def about():
    """About page."""
    template = current_app.jinja_env.get_template("clovek_about.html")
    html = template.render()
    return Response(html)


