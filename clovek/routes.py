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
    session.setdefault("clovek_lang", "slo")
    session.setdefault("red_player_name", "Rdeči igralec")
    session.setdefault("blue_player_name", "Modri igralec")
    session.setdefault("options", {
        "fast": False,
        "sound": True,
        "save_result": True
    })


def process_ai_turn(game: GameState) -> dict:
    """
    Process AI turn automatically.
    Returns animation sequence for AI move.
    """
    from .engine.engine import (
        can_player_move_at_all,
        select_ai_move,
        execute_move,
        pass_turn,
        end_turn,
        check_victory
    )
    
    current_player = game.get_current_player()
    
    # Check if current player is AI
    if not current_player.is_ai:
        return {"ai_move": False}
    
    print(f"🤖 AI turn starting for {current_player.name}")
    
    # Roll dice automatically
    dice_value = random.randint(1, 6)
    game.dice_value = dice_value
    
    print(f"🎲 AI rolled: {dice_value}")
    
    # Check if AI can move
    if not can_player_move_at_all(game, dice_value):
        # No valid moves, pass turn
        print(f"⏭️  AI passes (no valid moves)")
        pass_turn(game)
        
        return {
            "ai_move": True,
            "dice_value": dice_value,
            "animations": [],
            "passed": True,
            "current_turn": game.current_turn.value
        }
    
    # AI makes move
    pawn_id = select_ai_move(game, dice_value)
    
    if pawn_id:
        animations = execute_move(game, pawn_id, dice_value)
        
        # Check for victory
        game_over = check_victory(game)
        
        # End turn (gives another turn if rolled 6)
        rolled_six = dice_value == 6
        end_turn(game, rolled_six)
        
        print(f"✅ AI moved pawn {pawn_id}")
        
        return {
            "ai_move": True,
            "dice_value": dice_value,
            "pawn_id": pawn_id,
            "animations": animations,
            "rolled_six": rolled_six,
            "current_turn": game.current_turn.value,
            "game_over": game_over,
            "winner": game.winner.value if game.winner else None
        }
    else:
        # Shouldn't happen, but pass turn as fallback
        pass_turn(game)
        return {
            "ai_move": True,
            "dice_value": dice_value,
            "animations": [],
            "passed": True,
            "current_turn": game.current_turn.value
        }


def process_ai_turns_until_human(game: GameState) -> list:
    """
    Keep processing AI turns until it's a human player's turn.
    Returns list of all AI moves made.
    """
    ai_moves = []
    max_iterations = 10  # Safety limit
    iterations = 0
    
    while iterations < max_iterations:
        current_player = game.get_current_player()
        
        # Stop if human player's turn or game over
        if not current_player.is_ai or game.game_over:
            break
        
        # Process one AI turn
        ai_result = process_ai_turn(game)
        ai_moves.append(ai_result)
        
        # If AI rolled 6, it gets another turn
        if ai_result.get("rolled_six"):
            print("🎲 AI rolled 6, gets another turn")
            continue
        
        # Check if game is over
        if ai_result.get("game_over"):
            break
        
        iterations += 1
    
    return ai_moves


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
    language = set_language(session.get("clovek_lang", "slo"))

    # Import factory settings
    from .clovek import FACTORY

    return {
        "factory": FACTORY,
        "state": {
            "mode": session["mode"],
            "paused": session["clovek_paused"],
            "clovek_lang": session["clovek_lang"],
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
# from flask import current_app, Response
# @clovek_bp.route("/")
# def index():
#     context = {
#         "CLOVEK": build_clovek_context()
#     }

#     template = current_app.jinja_env.get_template("clovek_game.html")
#     html = template.render(context)

#     return Response(html)

#new - computer opponents
from flask import session, current_app, Response
from .clovek import active_matches # Import your global storage

@clovek_bp.route("/")
def index():
    MODE_MAP = {
        "HUMAN": GameMode.HOTSEAT,
        "AI_EASY": GameMode.AI_EASY,
        "AI_MEDIUM": GameMode.AI_MEDIUM,
        "AI_HARD": GameMode.AI_HARD,
        "NETWORK": GameMode.NETWORK
    }
    ensure_session() # Ensure sid exists
    sid = session["sid"]
    
    # 1. Check if we need to create a new game
    if sid not in active_matches:
        # Get settings from session (set by your /computer1, /human routes)
        raw_mode = session.get("mode", "HUMAN")
        mode_enum = MODE_MAP.get(raw_mode, GameMode.HOTSEAT)
        
        red_name = session.get("red_player_name", "Igralec 1")
        blue_name = session.get("blue_player_name", "Igralec 2")
        
        # 2. Call the factory with session data
        active_games[sid] = initialize_game(mode_enum, red_name, blue_name)
        print(f"🎮 Created new game for {sid} in mode {mode_enum}")

    # 3. Build Context (Pass the game object so the template can see is_ai)
    game_state = active_games[sid]
    context = {
        "CLOVEK": build_clovek_context(), # Your general UI context
        "game": game_state,                # The actual game engine
        "mode": session.get("mode")        # Current mode string
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
    try:
        ensure_session()
        sid = session["sid"]
        
        # Remove old game
        if sid in active_games:
            del active_games[sid]
        
        # Create fresh game
        game = get_or_create_game()
        
        animations = []
        
        # Start game unless in network mode waiting for opponent
        if session["mode"] != "NETWORK":
            # Prepare red pawns (move 1-4 to tiles 1-4)
            from .engine.engine import prepare_pawns
            from .engine.model import PlayerColor
            
            red_animations = prepare_pawns(game, PlayerColor.RED)
            animations.extend(red_animations)
            
            # Prepare blue pawns (move 5-8 to tiles 5-8)
            blue_animations = prepare_pawns(game, PlayerColor.BLUE)
            animations.extend(blue_animations)
            
            # Unpause game after preparation
            session["clovek_paused"] = False
            
            # Set initial turn to red
            game.current_turn = PlayerColor.RED
            
            print(f"✅ Game started in {session['mode']} mode")
        
        return jsonify({
            "success": True,
            "message": "Nova igra začeta",
            "paused": session["clovek_paused"],
            "preparation_animations": animations,
            "current_turn": game.current_turn.value
        })
    
    except Exception as e:
        print(f"❌ Error in api_new_game: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


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
def api_set_language():
    """Set interface language."""
    ensure_session()
    
    data = request.get_json() or {}
    lang = data.get("clovek_lang")
    
    if lang not in ["slo", "eng"]:
        return jsonify({
            "success": False,
            "error": "Invalid language"
        }), 400
    
    session["clovek_lang"] = lang
    session.modified = True
    
    return jsonify({
        "success": True,
        "clovek_lang": lang
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
    
    # Check if player can move
    from .engine.engine import can_player_move_at_all
    
    can_move = can_player_move_at_all(game, dice_value)
    
    result = {
        "success": True,
        "dice_value": dice_value,
        "current_turn": game.current_turn.value,
        "can_move": can_move
    }
    
    # If player can't move, pass turn
    if not can_move:
        from .engine.engine import pass_turn
        pass_turn(game)
        result["passed"] = True
        result["current_turn"] = game.current_turn.value
        
        # Check if next player is AI
        ai_moves = process_ai_turns_until_human(game)
        if ai_moves:
            result["ai_moves"] = ai_moves
    
    return jsonify(result)


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
    
    # Execute move using game engine
    from .engine.engine import execute_move, end_turn, check_victory
    
    animations = execute_move(game, pawn_id, game.dice_value)
    
    if not animations:
        return jsonify({
            "success": False,
            "error": "Invalid move"
        }), 400
    
    # Check for victory
    game_over = check_victory(game)
    
    # End turn (gives another turn if rolled 6)
    rolled_six = game.dice_value == 6
    end_turn(game, rolled_six)
    
    result = {
        "success": True,
        "animation_sequence": animations,
        "rolled_six": rolled_six,
        "current_turn": game.current_turn.value,
        "game_over": game_over,
        "winner": game.winner.value if game.winner else None
    }
    
    # If not rolled 6 and next player is AI, process AI turns
    if not rolled_six and not game_over:
        ai_moves = process_ai_turns_until_human(game)
        if ai_moves:
            result["ai_moves"] = ai_moves
    
    return jsonify(result)


@clovek_bp.route("/api/game/check-moves", methods=["POST"])
def api_check_moves():
    """Check if current player has any valid moves."""
    ensure_session()
    sid = session["sid"]
    
    if sid not in active_games:
        return jsonify({
            "success": False,
            "error": "No active game"
        }), 400
    
    game = active_games[sid]
    
    data = request.get_json() or {}
    dice_value = data.get("dice_value") or game.dice_value
    
    if dice_value is None:
        return jsonify({
            "success": False,
            "error": "No dice value"
        }), 400
    
    # Check if player can move
    from .engine.engine import can_player_move_at_all, get_valid_moves
    
    can_move = can_player_move_at_all(game, dice_value)
    valid_moves = get_valid_moves(game, dice_value) if can_move else []
    
    return jsonify({
        "success": True,
        "can_move": can_move,
        "valid_moves": len(valid_moves),
        "current_player": game.current_turn.value
    })


@clovek_bp.route("/api/game/pass-turn", methods=["POST"])
def api_pass_turn():
    """Pass turn to opponent (no valid moves available)."""
    ensure_session()
    sid = session["sid"]
    
    if sid not in active_games:
        return jsonify({
            "success": False,
            "error": "No active game"
        }), 400
    
    game = active_games[sid]
    
    # Pass turn to opponent
    from .engine.engine import pass_turn
    
    pass_turn(game)
    
    return jsonify({
        "success": True,
        "current_turn": game.current_turn.value,
        "message": "Turn passed"
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





#new
from .engine.engine import select_ai_move, execute_move, end_turn, pass_turn
@clovek_bp.route("/api/ai_move", methods=["POST"])
def ai_move():
    ensure_session()
    game = active_games.get(session["sid"])
    
    player = game.get_current_player()
    if not player.is_ai:
        return jsonify({"error": "Not AI turn"}), 400

    # 1. Roll the dice for the computer
    dice = random.randint(1, 6)
    game.dice_value = dice
    
    # 2. Let the brain pick the pawn
    pawn_id = select_ai_move(game, dice)
    
    if pawn_id:
        # 3. Execute the move
        animations = execute_move(game, pawn_id, dice)
        # Check if they rolled a 6 for extra turn
        rolled_six = (dice == 6)
        end_turn(game, rolled_six)
        
        return jsonify({
            "dice": dice,
            "animations": animations,
            "next_player": game.current_turn.value
        })
    else:
        # No moves possible
        pass_turn(game)
        return jsonify({
            "dice": dice,
            "animations": [],
            "next_player": game.current_turn.value
        })
    