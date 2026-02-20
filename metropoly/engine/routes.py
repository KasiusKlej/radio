# metropoly/engine/routes.py
import uuid
import traceback
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for

# FIXED: Import the class from the model file in the same directory
from .model import MetropolyGame  

metropoly_bp = Blueprint(
    "metropoly", 
    __name__, 
    template_folder="../templates",
    static_folder="../assets",
    static_url_path="/assets" 
)

# Global in-memory storage: sid -> MetropolyGame instance
active_metropoly_games = {}

# --- HELPERS ---
def get_user_game():
    """Fetches the specific engine instance for the current player's session."""
    sid = session.get("user_sid")
    return active_metropoly_games.get(sid)

def ensure_sid():
    if "user_sid" not in session:
        session["user_sid"] = str(uuid.uuid4())
    if "lang" not in session:
        session["lang"] = "eng"
    return session["user_sid"]


@metropoly_bp.context_processor
def inject_metropoly_context():
    from .parser import metropoly_language_parser
    from pathlib import Path
    import os

    # This gets the absolute path to the 'metropoly' folder
    # metropoly_bp.root_path is .../metropoly/engine
    root = Path(metropoly_bp.root_path).parent 
    lang_dir = root / "assets" / "languages"
    
    lang_code = session.get('lang', 'eng').lower()
    
    # DEBUG: Let's print the actual path to your console to see what's wrong
    print(f"DEBUG: Looking for languages in: {lang_dir}")
    print(f"DEBUG: File exists? {os.path.exists(lang_dir / f'{lang_code}.txt')}")

    try:
        raw_lang = metropoly_language_parser(lang_dir, lang_code)
    except FileNotFoundError:
        # Emergency fallback if the file is missing
        raw_lang = {"menu": {}, "phrases": {}, "turn": {}}

    return dict(
        m=raw_lang.get('menu', {}),
        phrases=raw_lang.get('phrases', {}),
        lang_dict=raw_lang
    )


# --- ROUTES ---
@metropoly_bp.route("/")
def index():
    ensure_sid()
    sid = session["user_sid"]
    if sid not in active_metropoly_games:
        active_metropoly_games[sid] = MetropolyGame() 
    
    # FIXED: Render the specific metropoly template name
    return render_template("metropoly_game.html", game=active_metropoly_games[sid].to_dict())


@metropoly_bp.route("/api/action", methods=["POST"])
def handle_action():
    try:
        engine = get_user_game() 
        if not engine:
            return jsonify({"success": False, "error": "Session expired"}), 401
        
        data = request.get_json()
        event_type = data.get("event")
        
        # Access the state inside the engine
        # In our MetropolyGame class, the attributes are directly on 'engine'
        
        # --- PHASE 2: ROLL DICE ---
        if event_type == "roll" and engine.faza == 2:
            # Here you would call engine.roll_dice() etc.
            return jsonify({"success": True, "msg": "Dice rolled", "game": engine.to_dict()})

        # --- PHASE 4: END TURN ---
        elif event_type == "end_turn":
            # engine.next_player()
            return jsonify({"success": True, "game": engine.to_dict()})

        return jsonify({"success": False, "error": "Invalid phase/action"}), 400

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"success": False, "error": str(e)}), 500
    
#############################################
# THE GAME MENU
#############################################

from flask import Blueprint, jsonify, redirect, url_for, request
from .engine import (
    image_land_info_click,
    image_selected_tool_click
)

# @metropoly_bp.route("/api/new_game", methods=["POST"])
# @metropoly_bp.route("/api/new_game/", methods=["POST"])
# def api_new_game():
#     engine = get_user_game()
#     if not engine:
#         return jsonify({"success": False}), 401
    
#     data = request.get_json()
#     # Data expected from frontend:
#     # {
#     #   "map_choice": "Random", 
#     #   "custom_x": 10, 
#     #   "custom_y": 12,
#     #   "players": [{"active": true, "is_pc": false, "name": "Bugs"}, ...]
#     # }
    
#     from .engine import start_new_game
#     from pathlib import Path
    
#     ini_path = Path(metropoly_bp.root_path) / "metropoly.ini"
    
#     start_new_game(
#         engine.state, 
#         data.get("map_choice"),
#         data.get("custom_x"),
#         data.get("custom_y"),
#         data.get("players"),
#         ini_path
#     )
    
#     return jsonify({"success": True, "game": engine.to_dict()})


@metropoly_bp.route("/api/game/new", methods=["POST"])
@metropoly_bp.route("/api/game/new/", methods=["POST"])
def api_new_game():
    engine = get_user_game()
    data = request.get_json()
    
    # Extract data from the "New Game" form
    map_choice = data.get("map_name", "Random")
    c_x = int(data.get("x")) if data.get("x") else None
    c_y = int(data.get("y")) if data.get("y") else None
    
    # Run the ported logic
    from .engine import start_new_game_logic
    result = start_new_game_logic(engine.state, map_choice, c_x, c_y)
    
    return jsonify({"success": True, "game": result})

# game menu routes
@metropoly_bp.route("/new-game", methods=["POST"])
@metropoly_bp.route("/new-game/", methods=["POST"])
def new_game():
    state = get_user_game()
    
    # Setup players from POST data or default
    # For now, assume some data is sent as JSON: {'players':[...]}
    data = request.json or {}
    num_players = len(data.get("players", []))
    if num_players == 0:
        return jsonify({"status":"error","message":"No players"}), 400
    
    # Reset state
    state.numpl = num_players
    state.curpl = random.randint(1, num_players)
    state.clkMode = 0
    state.dayOfWeek = 1
    
    # draw map (engine function)
    draw_map(state)
    draw_players(state)
    
    # Prepare first player turn
    next_player(state)
    
    return jsonify(state.to_dict())


@metropoly_bp.route("/exit")
@metropoly_bp.route("/exit/")
def exit_metropoly():
    return redirect(url_for("index"))  # your homepage

@metropoly_bp.route("/ui/hide-land-info/", methods=["POST"])
@metropoly_bp.route("/ui/hide-land-info", methods=["POST"])
def hide_land_info():
    state = get_user_game()
    image_land_info_click(state)
    return jsonify(state.to_dict())

@metropoly_bp.route("/ui/select-tool/<int:index>/", methods=["POST"])
@metropoly_bp.route("/ui/select-tool/<int:index>", methods=["POST"])
def select_tool(index):
    state = get_user_game()
    image_selected_tool_click(state, index)
    return jsonify(state.to_dict())

@metropoly_bp.route("/about")
@metropoly_bp.route("/about/")
def about():
    return render_template("frmAbout.html")

@metropoly_bp.route("/help")
@metropoly_bp.route("/help/")
def help_contents():
    return render_template("help.html")

@metropoly_bp.route("/toggle-auto-end-turn", methods=["POST"])
@metropoly_bp.route("/toggle-auto-end-turn/", methods=["POST"])
def toggle_auto_end_turn():
    state = get_user_game()
    mnu_auto_end_turn_click(state)
    return jsonify(state.to_dict())

@metropoly_bp.route("/toggle-fast", methods=["POST"])
@metropoly_bp.route("/toggle-fast/", methods=["POST"])
def toggle_fast():
    state = get_user_game()
    mnu_fast_click(state)
    return jsonify(state.to_dict())


@metropoly_bp.route("/map-editor")
@metropoly_bp.route("/map-editor/")
def map_editor():
    # Initial form data
    initial_data = {
        "Text1": ["", ""],
        "Combo1": ""
    }
    return render_template("frmMapEditor.html", data=initial_data)


@metropoly_bp.route("/set-language/<code>")
@metropoly_bp.route("/set-language/<code>/")
def set_language(code):
    session["lang"] = code

    session.pop('_cached_lang_code', None)
    session.pop('_cached_lang_dict', None)

    game = get_user_game()
    if game:
        game.state.CURRENT_LANGUAGE = code

    return redirect(request.referrer or url_for("metropoly_game.index"))

# logic
@metropoly_bp.route("/create-semafors", methods=["POST"])
@metropoly_bp.route("/create-semafors/", methods=["POST"])
def create_semafors():
    state = get_user_game()
    mnu_create_semafors_click(state)
    return jsonify(state.to_dict())

# open/save
# open/save
from .model import OpenSaveMode

@metropoly_bp.route("/game/save")
@metropoly_bp.route("/game/save/")
def menu_save():
    ensure_sid()
    state = get_user_game()

    if not state:
        return redirect(url_for("metropoly.index"))

    state.open_save_mode = OpenSaveMode.SAVE
    state.open_save_filename = "game.sav"

    return render_template(
        "game_open_save.html",
        caption=lngg(57),      # "Save"
        filename="game.sav",
        mode="save",
        files=list_save_files()
    )


@metropoly_bp.route("/game/open")
@metropoly_bp.route("/game/open/")
def menu_open():
    ensure_sid()
    state = get_user_game()

    if not state:
        return redirect(url_for("metropoly.index"))

    state.open_save_mode = OpenSaveMode.OPEN
    state.open_save_filename = ""

    return render_template(
        "game_open_save.html",
        caption=lngg(56),      # "Open"
        filename="",
        mode="open",
        files=list_save_files()
    )

@metropoly_bp.route("/api/load", methods=["POST"])
@metropoly_bp.route("/api/load/", methods=["POST"])
def load_game():
    data = request.json
    engine = get_user_game()

    engine.load_from_dict(data["state"])
    return jsonify(engine.to_dict())

@metropoly_bp.route("/api/save", methods=["GET"])
@metropoly_bp.route("/api/save/", methods=["GET"])
def save_game():
    engine = get_user_game()
    return jsonify(engine.to_dict())

# map editor
@metropoly_bp.route("/api/editor/click", methods=["POST"])
@metropoly_bp.route("/api/editor/click/", methods=["POST"])
def editor_click():
    engine = get_user_game()
    data = request.get_json()
    # tool_index comes from the UI (which button is highlighted)
    edit_map_tile(engine.state, data['x'], data['y'], data['tool_index'])
    return jsonify(engine.state.to_dict())