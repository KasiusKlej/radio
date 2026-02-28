# metropoly/engine/routes.py
import uuid
import traceback
import random
import os
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from pathlib import Path

# This maps the browser code (fr) to your VB filename (fre.txt)
LANG_MAP = {
    'eng': 'eng', 'spa': 'spa', 'por': 'po', 'it': 'ita',
    'fr': 'fre',  'ger': 'ger', 'chn': 'chn', 'jap': 'jap',
    'kor': 'kor', 'slo': 'slo', 'rus': 'rus', 'yu': 'ser',
    'other': 'eng'
}

# Import only what we need from the consolidated engine
from .new_engine_without_circular_imports import (
    MetropolyGame, 
    metropoly_language_parser,
    start_new_game_logic,
    #update_road_visuals # assuming this is in there   #nothing like that is in there and nothing like that VB original code
)



# # --- 2. BLUEPRINT DEFINITION ---
# # root_path points to .../mywebsite/metropoly/engine
# # static_folder points to .../mywebsite/static/metropoly
# METRO_STATIC = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "static", "metropoly"))
# metropoly_bp = Blueprint(
#     "metropoly", 
#     __name__, 
#     template_folder="../templates",
#     static_folder=METRO_STATIC,
#     static_url_path="/assets" 
# )



# metropoly/engine/routes.py

# Resolve the absolute path to: mywebsite/static/metropoly
BASE_DIR = Path(__file__).resolve().parent.parent.parent
METRO_STATIC = str(BASE_DIR / "static" / "metropoly")
metropoly_bp = Blueprint(
    "metropoly", 
    __name__, 
    template_folder="../templates",
    static_folder=METRO_STATIC,
    # 🩹 CHANGE THIS: Avoid using "assets" as the URL path
    static_url_path="/metro_static" 
)





#### 🔥 What is happening (root cause)
# You have TWO overlapping sources of truth for language and game state:
# Global in-memory objects
# Session-based expectations
# They are not isolated per game, and not isolated per worker.
#### We need two dictionaries: one to hold the unique games, and one to map users to them.
#### active_metropoly_games = {}

# 1. Store the actual game data (The Universal Truth)
# Key: game_instance_id (e.g. "game-123"), Value: MetropolyGame object
METRO_GAMES = {}

# 2. Store which player is looking at which game
# Key: user_sid (from session), Value: game_instance_id
PLAYER_MAP = {}

#new
# 🔗 NAMESPACED KEYS (Isolation from CardGames)
SESSION_LANG_KEY = "metro_lang"  # 👈 This ensures Metropoly language stays in Metropoly
SESSION_GAME_ID = "metro_zap_id"

# -------------------------------------------------
# HELPERS
# -------------------------------------------------

# def get_user_game():
#     sid = session.get("user_sid")
#     game = active_metropoly_games.get(sid)
#     if game:
#         # SYNC: One place to ensure engine matches user preference
#         game.CURRENT_LANGUAGE = session.get("metropoly_lang", "eng")
#     return game

#### rewriten
# def get_user_game():
#     """Fetches the game instance this specific player is attached to."""
#     sid = session.get("user_sid")
#     game_id = PLAYER_MAP.get(sid)
    
#     if not game_id:
#         return None
        
#     return METRO_GAMES.get(game_id)

def get_user_game():
    sid = session.get("user_sid")
    instance_id = PLAYER_MAP.get(sid)
    return METRO_GAMES.get(instance_id)


# def ensure_sid():
#     if "user_sid" not in session:
#         session["user_sid"] = str(uuid.uuid4())
#     if "metro_lang" not in session:
#         session["metro_lang"] = "slo" # ONE place for default lang
#     return session["user_sid"]

def ensure_sid():
    if "user_sid" not in session:
        session["user_sid"] = str(uuid.uuid4())
    # 🩹 FIX: Initialize Metropoly-specific default
    if SESSION_LANG_KEY not in session:
        session[SESSION_LANG_KEY] = "slo"
    return session["user_sid"]

# -------------------------------------------------
# CONTEXT & LANDING
# -------------------------------------------------

# --- 3. THE CONTEXT PROCESSOR ---

#### The context processor is now the only place that cares about the .txt files.
import copy
# @metropoly_bp.context_processor
# def inject_metropoly_context():
#     # 1. Get the language from the session (Personal preference)
#     lang_iso = session.get('metro_lang', 'slo')
#     file_prefix = LANG_MAP.get(lang_iso, 'slo')
    
#     # 2. Parse the file
#     mywebsite_root = Path(metropoly_bp.root_path).resolve().parent.parent
#     lang_dir = mywebsite_root / "static" / "metropoly" / "assets" / "languages"
    
#     # 🩹 CRITICAL: Return a deep copy to prevent cross-player contamination
#     raw_data = metropoly_language_parser(lang_dir, f"{file_prefix}.txt")
#     lang_data = copy.deepcopy(raw_data)

#     # 3. Get the game logic
#     game_instance = get_user_game()
    
#     # 4. If the game exists, render its state using this player's language
#     game_json = game_instance.to_dict(lang_data) if game_instance else None

#     return {
#         "m": lang_data.get("menu", {}),
#         "lang_dict": lang_data,
#         "game": game_json, # This is the "Personalized View"
#         "current_lang": lang_iso
#     }

@metropoly_bp.context_processor
def inject_metropoly_context():
    # 1. Get the player's specific Metropoly preference
    lang_iso = session.get(SESSION_LANG_KEY, 'slo')
    lang_data = get_current_lang_data()

    # 2. Get the logical game instance
    game_instance = get_user_game()
    
    # 3. Label the logic with the player's eyes
    game_json = game_instance.to_dict(lang_data) if game_instance else None

    return {
        "m": lang_data.get("menu", {}),
        "turn": lang_data.get("turn", {}),
        "phrases": lang_data.get("phrases", {}),
        "lang_dict": lang_data,
        "game": game_json,
        "current_lang": lang_iso
    }





# @metropoly_bp.route("/exit")
# @metropoly_bp.route("/exit/")
# def exitGame():
#     """
#     Cleans up the player's connection to the game and returns home.
#     Following the 'Universal Games' rule: we only remove the PLAYER'S connection.
#     """
#     sid = session.get("user_sid")
    
#     # 1. Remove this specific player from the map
#     # (The game instance stays in METRO_GAMES in case other players are in the match)
#     PLAYER_MAP.pop(sid, None)
    
#     # 2. Cleanup session markers
#     session.pop("zap_st_igre", None)
    
#     print(f"🚪 Player {sid} exited Metropoly.")
    
#     # 🩹 FIX: Always return a valid redirect response
#     return redirect("/")

@metropoly_bp.route("/exit")
@metropoly_bp.route("/exit/")
def exitGame():
    sid = session.get("user_sid")
    # We remove the player's connection to the match
    PLAYER_MAP.pop(sid, None)
    # Clear Metropoly specific session markers, leave 'lang' (for other games) alone
    session.pop(SESSION_GAME_ID, None)
    return redirect("/")


# @metropoly_bp.route("/")
# def index():
#     """
#     Main entry point. Ensures the user has a game to look at.
#     """
#     ensure_sid()
#     sid = session.get("user_sid")

#     # 1. Check if the player is already assigned to a game
#     instance_id = PLAYER_MAP.get(sid)

#     # 2. If not, create a new match instance and link the player to it
#     if not instance_id:
#         instance_id = f"game-{uuid.uuid4().hex[:8]}" # Unique match ID
#         METRO_GAMES[instance_id] = MetropolyGame()
#         PLAYER_MAP[sid] = instance_id
#         print(f"⚓ NEW MATCH: {instance_id} initialized for Player {sid}")

#     # 3. RENDER
#     # We do NOT pass 'game=' here. 
#     # Because we use the @metropoly_bp.context_processor we built earlier, 
#     # Flask will automatically call get_user_game(), get the language 
#     # from the session, and inject the translated 'game' object into 
#     # 'metropoly_game.html' for us.
#     return render_template("metropoly_game.html")

@metropoly_bp.route("/")
def index():
    ensure_sid()
    sid = session["user_sid"]
    instance_id = PLAYER_MAP.get(sid)

    if not instance_id:
        instance_id = f"game-{uuid.uuid4().hex[:8]}"
        METRO_GAMES[instance_id] = MetropolyGame()
        PLAYER_MAP[sid] = instance_id

    return render_template("metropoly_game.html")


# -------------------------------------------------
# CORE GAME API
# -------------------------------------------------





# File / new
@metropoly_bp.route("/api/game/new", methods=["POST"])
@metropoly_bp.route("/api/game/new/", methods=["POST"])
def api_new_game():
    try:
        
        #### When a player clicks "New Game," we create the instance ID and link them to it.
        sid = session.get("user_sid")
        # 1. Create a unique ID for this match
        instance_id = f"game-{uuid.uuid4().hex[:8]}"
        # 2. Create the universal engine
        new_engine = MetropolyGame()
        # 3. Register it
        METRO_GAMES[instance_id] = new_engine
        PLAYER_MAP[sid] = instance_id



        engine = get_user_game()
        if not engine:
            return jsonify({"success": False, "error": "No active session"}), 401
            
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No data received"}), 400

        # Run the ported logic
        # We ensure players is at least an empty list to prevent crashes
        players = data.get("players", [])
        
        result = start_new_game_logic(
            engine, 
            map_choice=data.get("map_name", "Random"), 
            custom_x=data.get("x"), 
            custom_y=data.get("y"),
            player_settings=players
        )
        
        ####return jsonify({"success": True, "game": result})
        return jsonify({"success": True})

    except Exception as e:
        # 🐛 This prints the REAL error to your VS Code console
        print("⚓ CRITICAL ERROR IN NEW GAME:")
        print(traceback.format_exc())
        return jsonify({"success": False, "error": str(e)}), 500

# test ?
@metropoly_bp.route("/api/action", methods=["POST"])
@metropoly_bp.route("/api/action/", methods=["POST"])
def handle_action():
    engine = get_user_game()
    if not engine: return jsonify({"success": False}), 401
    
    data = request.get_json()
    event = data.get("event")

    if event == "roll" and engine.faza == 2:
        # Call engine.roll_dice and engine.calculate_path
        # Return steps for JS animation
        pass

    return jsonify({"success": True, "game": engine.to_dict()})






# -------------------------------------------------
# MENU & SETTINGS
# -------------------------------------------------

# @metropoly_bp.route("/set-language/<code>/")
# @metropoly_bp.route("/set-language/<code>")
# def set_language(code):
#     # Only one thing to change: the session
#     session["metro_lang"] = code
    
#     # Engine will sync on the next get_user_game() call
#     return redirect(url_for("metropoly.index"))

@metropoly_bp.route("/set-language/<code>")
@metropoly_bp.route("/set-language/<code>/")
def set_language(code):
    # 🩹 FIX: Update ONLY the Metropoly preference
    session[SESSION_LANG_KEY] = code
    return redirect(url_for("metropoly.index"))


# toggle buttons
@metropoly_bp.route("/api/toggle/<option_name>", methods=["POST"])
@metropoly_bp.route("/api/toggle/<option_name>/", methods=["POST"])
def toggle_option(option_name):
    game = get_user_game()
    if not game: return jsonify({"success": False}), 401

    # Mapping HTML names to Python Class attributes
    mapping = {
        "fast": "fast_mode",
        "grid": "show_grid",
        "auto": "autoEndTurn",
        "sound": "sound_enabled"
    }
    
    attr = mapping.get(option_name)
    if attr and hasattr(game, attr):
        current_val = getattr(game, attr)
        setattr(game, attr, not current_val) # Flip the boolean
        return jsonify({"success": True, "new_val": not current_val})
    
    return jsonify({"success": False}), 400

# 🩹 ADD THIS: A specific route to stop the favicon 404 noise
@metropoly_bp.route('/favicon.ico')
def favicon():
    return "", 204





import copy
from pathlib import Path
from flask import jsonify, request, session

# =============================================================================
# ROUTE HELPERS
# =============================================================================

# def get_current_lang_data():
#     """
#     Helper to fetch and deep-copy the current player's language dictionary.
#     Ensures the 'Personal Eyes' rule is followed for every response.
#     """
#     from .new_engine_without_circular_imports import metropoly_language_parser
    
#     lang_iso = session.get('lang', 'slo')
#     file_prefix = LANG_MAP.get(lang_iso, 'slo')
    
#     # Path: mywebsite/static/metropoly/assets/languages/
#     root = Path(metropoly_bp.root_path).resolve().parent.parent
#     lang_dir = root / "static" / "metropoly" / "assets" / "languages"
    
#     raw_data = metropoly_language_parser(lang_dir, f"{file_prefix}.txt")
#     return copy.deepcopy(raw_data)

def get_current_lang_data():
    """
    Fetches and deep-copies language data strictly for Metropoly.
    """
    from .new_engine_without_circular_imports import metropoly_language_parser
    
    # 🩹 FIX: Look strictly at the Metropoly-specific session key
    lang_iso = session.get(SESSION_LANG_KEY, 'slo')
    file_prefix = LANG_MAP.get(lang_iso, 'slo')
    
    mywebsite_root = Path(metropoly_bp.root_path).resolve().parent.parent
    lang_dir = mywebsite_root / "static" / "metropoly" / "assets" / "languages"
    
    raw_data = metropoly_language_parser(lang_dir, f"{file_prefix}.txt")
    return copy.deepcopy(raw_data)


# =============================================================================
# CORE API ROUTES
# =============================================================================

@metropoly_bp.route("/api/save_map", methods=["POST"])
def api_save_map():
    game = get_user_game()
    if not game: return jsonify({"success": False}), 401
    
    data = request.get_json()
    filename = data.get("filename", "my.map")
    lang_data = get_current_lang_data()

    from .new_engine_without_circular_imports import save_map_to_disk, fill_combo_logic
    
    success = save_map_to_disk(game, filename)
    if success:
        fill_combo_logic(game)
        
    return jsonify({
        "success": success, 
        "game": game.to_dict(lang_data) 
    })

@metropoly_bp.route("/api/end_turn", methods=["POST"])
def api_end_turn():
    game = get_user_game()
    if not game: return jsonify({"success": False}), 401
    
    lang_data = get_current_lang_data()

    from .new_engine_without_circular_imports import mnu_end_turn_click
    mnu_end_turn_click(game)
    
    return jsonify({
        "success": True, 
        "game": game.to_dict(lang_data)
    })

@metropoly_bp.route("/api/map_click", methods=["POST"])
def api_map_click():
    game = get_user_game()
    if not game: return jsonify({"success": False}), 401

    data = request.get_json()
    lang_data = get_current_lang_data()

    from .new_engine_without_circular_imports import handle_map_click
    handle_map_click(game, data['x'], data['y'])
    
    return jsonify({
        "success": True, 
        "game": game.to_dict(lang_data)
    })

@metropoly_bp.route("/api/set_mode/<int:mode_id>", methods=["POST"])
def set_clk_mode(mode_id):
    game = get_user_game()
    if not game: return jsonify({"success": False}), 401
    
    lang_data = get_current_lang_data()
    p = game.players.get(game.curpl)
    
    if p and not p.is_pc:
        game.clkMode = mode_id
        # We pull the correct translated label from the lang_data we just loaded
        # Replicating VB: LabelStatus.Caption = lngg(100/113/83)
        l = lang_data.get("raw", [""] * 151)
        if mode_id == 1: game.status_label = l[100]
        elif mode_id == 2: game.status_label = l[113]
        elif mode_id == 3: game.status_label = l[83]
            
    return jsonify({
        "success": True, 
        "game": game.to_dict(lang_data)
    })

@metropoly_bp.route("/api/roll", methods=["POST"])
def roll():
    game = get_user_game()
    if not game: return jsonify({"success": False}), 401
    
    lang_data = get_current_lang_data()
    
    # 1. Roll (sets engine.kocka)
    # 2. Process Sequence (Calculates path AND runs landing logic)
    dice_results = game.roll_dice() 
    steps = game.process_move_sequence() 
    
    return jsonify({
        "success": True,
        "dice": dice_results,
        "steps": steps, 
        "game": game.to_dict(lang_data)
    })

@metropoly_bp.route("/api/editor/begin", methods=["POST"])
def editor_begin():
    game = get_user_game()
    if not game: return jsonify({"success": False}), 401
    
    lang_data = get_current_lang_data()

    from .new_engine_without_circular_imports import begin_map_editor
    begin_map_editor(game) 
    
    return jsonify({
        "success": True, 
        "game": game.to_dict(lang_data)
    })


@metropoly_bp.route("/api/editor/end", methods=["POST"])
@metropoly_bp.route("/api/editor/end/", methods=["POST"])
def editor_end():
    """Triggers the end_map_editor logic and returns to game mode."""
    game = get_user_game()
    if not game: return jsonify({"success": False}), 401

    lang_data = get_current_lang_data()
    
    from .new_engine_without_circular_imports import end_map_editor
    end_map_editor(game)
        
    return jsonify({"success": True, "game": game.to_dict(lang_data)})



