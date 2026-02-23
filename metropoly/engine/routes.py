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




active_metropoly_games = {}

# -------------------------------------------------
# HELPERS
# -------------------------------------------------

def get_user_game():
    sid = session.get("user_sid")
    game = active_metropoly_games.get(sid)
    if game:
        # SYNC: One place to ensure engine matches user preference
        game.CURRENT_LANGUAGE = session.get("metropoly_lang", "eng")
    return game

def ensure_sid():
    if "user_sid" not in session:
        session["user_sid"] = str(uuid.uuid4())
    if "lang" not in session:
        session["lang"] = "slo" # ONE place for default lang
    return session["user_sid"]

# -------------------------------------------------
# CONTEXT & LANDING
# -------------------------------------------------

# --- 3. THE CONTEXT PROCESSOR ---
@metropoly_bp.context_processor
def inject_metropoly_context():
    # Import the parser inside to avoid circular issues with logic.py
    from .new_engine_without_circular_imports import metropoly_language_parser
    
    lang_iso = session.get('lang', 'slo')
    
    # Use the map defined at the top of the file
    file_prefix = LANG_MAP.get(lang_iso, 'eng') 
    
    # Robust Path Resolution:
    # We go up from 'engine' (root_path) to 'metropoly', then to 'mywebsite'
    mywebsite_root = Path(metropoly_bp.root_path).resolve().parent.parent
    
    # Path: mywebsite/static/metropoly/assets/languages/
    lang_dir = mywebsite_root / "static" / "metropoly" / "assets" / "languages"
    
    target_filename = f"{file_prefix}.txt"

    try:
        # Pass the Path object and the filename
        raw_lang = metropoly_language_parser(lang_dir, target_filename)
    except Exception as e:
        # Helpful console output if it fails again
        raw_lang = {"menu": {}, "phrases": {}, "turn": {}}

    return {
        "m": raw_lang.get("menu", {}),
        "phrases": raw_lang.get("phrases", {}),
        "turn": raw_lang.get("turn", {}), # 👈 ADD THIS: Fixes the crash
        "lang_dict": raw_lang,
        "game": get_user_game()
    }








@metropoly_bp.route("/")
def index():
    ensure_sid()
    sid = session["user_sid"]
    if sid not in active_metropoly_games:
        active_metropoly_games[sid] = MetropolyGame() 
    return render_template("metropoly_game.html", game=active_metropoly_games[sid].to_dict())

# -------------------------------------------------
# CORE GAME API
# -------------------------------------------------

# click on board
@metropoly_bp.route("/api/map_click", methods=["POST"])
@metropoly_bp.route("/api/map_click", methods=["POST"])
def api_map_click():
    game = get_user_game()
    data = request.get_json()
    
    # x, y come from JS based on which tile was clicked
    handle_map_click(game, data['x'], data['y'])
    
    return jsonify({"success": True, "game": game.to_dict()})

# keyboard shortcuts
@metropoly_bp.route("/api/set_mode/<int:mode_id>", methods=["POST"])
@metropoly_bp.route("/api/set_mode/<int:mode_id>", methods=["POST"])
def set_clk_mode(mode_id):
    """
    VB: Logic inside mnuRoad_Click, mnuSell_Click, etc.
    Sets the mouse behavior and updates the status label from lngg.
    """
    game = get_user_game()
    if not game: return jsonify({"success": False}), 401
    
    p = game.players[game.curpl]
    
    if not p.is_pc:
        game.clkMode = mode_id
        # Map mode to lngg index
        if mode_id == 1: # SELL
            game.status_label = game.lngg[100]
        elif mode_id == 2: # ROAD
            game.status_label = game.lngg[113]
        elif mode_id == 3: # CREATE SEMAPHORE
            game.status_label = game.lngg[83]
            
    return jsonify({"success": True, "game": game.to_dict()})

# File / new
@metropoly_bp.route("/api/game/new", methods=["POST"])
@metropoly_bp.route("/api/game/new/", methods=["POST"])
@metropoly_bp.route("/api/game/new", methods=["POST"])
@metropoly_bp.route("/api/game/new/", methods=["POST"])
def api_new_game():
    try:
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
        
        return jsonify({"success": True, "game": result})

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


@metropoly_bp.route("/api/roll", methods=["POST"])
@metropoly_bp.route("/api/roll/", methods=["POST"])
def roll():
    game = get_user_game()
    if not game: return jsonify({"success": False}), 401
    
    # 1. Roll (sets engine.kocka)
    dice_results = game.roll_dice() 
    
    # 2. Process (Calculates path AND runs landing logic)
    # This now uses the function you just verified
    steps = game.process_move_sequence() 
    
    return jsonify({
        "success": True,
        "dice": dice_results,
        "steps": steps, # The list of x, y, smer for JS animation
        "game": game.to_dict() # Includes the results of pristanek()
    })

@metropoly_bp.route("/api/end_turn", methods=["POST"])
@metropoly_bp.route("/api/end_turn/", methods=["POST"])
def api_end_turn():
    game = get_user_game()
    if not game:
        return jsonify({"success": False}), 401
    
    # Call the ported VB logic
    # We use engine.state if it's external, or engine if it's the class method
    mnu_end_turn_click(game)
    
    return jsonify({
        "success": True, 
        "game": game.to_dict()
    })

# -------------------------------------------------
# MENU & SETTINGS
# -------------------------------------------------

@metropoly_bp.route("/set-language/<code>/")
@metropoly_bp.route("/set-language/<code>")
def set_language(code):
    # Only one thing to change: the session
    session["lang"] = code
    
    # Engine will sync on the next get_user_game() call
    return redirect(url_for("metropoly.index"))

# File / exit
@metropoly_bp.route("/exit")
@metropoly_bp.route("/exit/")
def exitGame():
    sid = session.get("user_sid")
    active_metropoly_games.pop(sid, None)
    session.pop("zap_st_igre", None)
    # 🩹 FIX: Explicitly return the redirect so Flask doesn't get 'None'
    return redirect("/")

@metropoly_bp.route("/api/editor/begin", methods=["POST"])
@metropoly_bp.route("/api/editor/begin/", methods=["POST"])
def editor_begin():
    """Triggers the begin_map_editor logic in the engine."""
    game = get_user_game()
    if not game: return jsonify({"success": False}), 401
    
    # Use the function we ported to your big engine file
    from .new_engine_without_circular_imports import begin_map_editor
    begin_map_editor(game) 
    
    return jsonify({"success": True, "game": game.to_dict()})

@metropoly_bp.route("/api/editor/end", methods=["POST"])
@metropoly_bp.route("/api/editor/end/", methods=["POST"])
def editor_end():
    """Triggers the end_map_editor logic and returns to game mode."""
    game = get_user_game()
    if not game: return jsonify({"success": False}), 401
    
    from .new_engine_without_circular_imports import end_map_editor
    end_map_editor(game)
    
    return jsonify({"success": True, "game": game.to_dict()})



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

@metropoly_bp.route("/api/save_map", methods=["POST"])
@metropoly_bp.route("/api/save_map/", methods=["POST"])
def api_save_map():
    game = get_user_game()
    data = request.get_json()
    filename = data.get("filename", "my.map")

    from .new_engine_without_circular_imports import save_map_to_disk, fill_combo_logic
    
    success = save_map_to_disk(game, filename)
    
    if success:
        # VB: NewGame.fill_combo (Refresh the list of available maps)
        fill_combo_logic(game)
        
    return jsonify({
        "success": success, 
        "game": game.to_dict() # Returns updated map_list
    })