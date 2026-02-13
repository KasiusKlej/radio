from .engine.model import CURRENT_LANGUAGE, LANG_DIR
from flask import Blueprint, render_template, request, jsonify, session, redirect
from .engine.game import CardGame
from .engine.parser import load_game_names, language_parser, load_game_rules  
import random

cardgames_bp = Blueprint("cardgames", __name__, template_folder="templates")

# Dictionary to hold active games in memory (keyed by game_id)
active_games = {}


# -------------------------------------------------
# Card Games routes
# -------------------------------------------------

@cardgames_bp.route("/")
def index():
    # ---- PHASE 0: load static data ONCE ----
    # Menu only needs game list (no game state)
    games = load_game_names()
    return render_template("menu.html", games=games)


@cardgames_bp.route("/play/<game_id>")
def play_game(game_id):
    # ---- PHASE 1: start particular game ----
    session["zap_st_igre"] = game_id

    game = CardGame(game_id)
    active_games[game_id] = game

    return render_template(
        "game.html",
        game=game,
        page_title=game.name,
        lang=CURRENT_LANGUAGE
    )


# menu change language
@cardgames_bp.route("/set-language/<code>")
def set_language(code):
    global CURRENT_LANGUAGE
    CURRENT_LANGUAGE = language_parser(LANG_DIR, code)
    return redirect(request.referrer or "/")

# menu autoplay toggle option
@cardgames_bp.route("/api/options/autoplay", methods=["POST"])
def set_autoplay():
    data = request.get_json()
    enabled = bool(data.get("enabled", False))

    game_id = session.get("zap_st_igre")
    if not game_id:
        return jsonify({"ok": False, "error": "No active game"}), 400

    game = active_games.get(game_id)
    if not game:
        return jsonify({"ok": False, "error": "Game not found"}), 404

    game.autoplay_enabled = enabled
    return {"ok": True, "autoplay": enabled}

# menu rules
@cardgames_bp.route("/api/rules")
def api_rules():
    game_id = session.get("zap_st_igre")
    if not game_id:
        return jsonify({"title": "", "text": ""})

    game = active_games.get(game_id)
    if not game:
        return jsonify({"title": "", "text": ""})

    rules = load_game_rules(
        gamename=game.gamename,
        language=CURRENT_LANGUAGE,
        lang_dir=LANG_DIR,
        list_game=game.definition_lines,
        lang_vars=game.lang_vars,  # or global LANG_VARS
    )

    return {"title": game.gamename, "text": rules}



# under construction
@cardgames_bp.route("/move", methods=["POST"])
def move():
    data = request.get_json()
    game_id = data.get("game_id")
    from_col = data.get("from_column")
    to_col = data.get("to_column")
    card_code = data.get("card")

    if game_id not in active_games:
        return jsonify({"success": False, "error": "Game not found"}), 400

    game_engine = active_games[game_id]
    success = game_engine.move_card(from_col, to_col, card_code)

    return jsonify({
        "success": success,
        "game": game_engine.to_dict()
    })

