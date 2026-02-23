import uuid
import traceback
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from .engine.model import LANG_DIR
from .engine.game import CardGame
from .engine.parser import load_game_rules

cardgames_bp = Blueprint("cardgames", __name__, template_folder="templates")

# Global in-memory storage: sid -> CardGame instance
active_games = {}

# -------------------------------------------------
# 1. CORE HELPERS (The "Safety Net")
# -------------------------------------------------

def get_user_game():
    """
    Fetches the engine. Ensures the Engine and Session are 
    ALWAYS in the same language.
    """
    sid = session.get("user_sid")
    if not sid:
        return None

    engine = active_games.get(sid)
    
    # Self-healing: If engine is gone but cookie exists, recreate it
    if not engine:
        game_id = session.get("zap_st_igre")
        if game_id:
            engine = CardGame(game_id)
            active_games[sid] = engine
            print(f"🛠️  Auto-repaired engine for {game_id}")

    if engine:
        # SYNC: The "Ace of Spades" must match the current session choice
        current_lang = session.get("lang", "slo")
        engine.state.CURRENT_LANGUAGE = current_lang
        
    return engine

def ensure_sid():
    """Ensures a unique ID exists and sets default language."""
    if "user_sid" not in session:
        session["user_sid"] = str(uuid.uuid4())
    if "lang" not in session:
        session["lang"] = "slo"
    return session["user_sid"]

# -------------------------------------------------
# 2. CONTEXT & MENU
# -------------------------------------------------

@cardgames_bp.context_processor
def inject_games():
    """Provides translated menus. Uses caching to prevent slowdowns."""
    lang_code = session.get('lang', 'slo')
    
    # Use session to cache language dict to prevent heavy file reading
    if session.get('_cached_lang_code') != lang_code:
        from .engine.game import get_language_dict 
        from .engine.parser import read_gamenames_from_language_files
        
        try:
            raw_lang = get_language_dict(lang_code)
            games_list = read_gamenames_from_language_files(lang_code, LANG_DIR)
            session['_cached_lang_code'] = lang_code
            session['_cached_lang_dict'] = raw_lang
            session['_cached_games_list'] = games_list
        except:
            return dict(games=[], lang_dict={}, m={})

    return dict(
        games=session.get('_cached_games_list', []),
        lang_dict=session.get('_cached_lang_dict', {}),
        m=session.get('_cached_lang_dict', {}).get('menu', {}) 
    )

@cardgames_bp.route("/")
def index():
    ensure_sid()
    return render_template("allgames.html", game=None)

# -------------------------------------------------
# 3. GAME LIFECYCLE
# -------------------------------------------------
@cardgames_bp.route("/play/<game_id>")
@cardgames_bp.route("/play/<game_id>/")
def play_game(game_id):
    sid = ensure_sid()
    
    # Start fresh
    engine = CardGame(game_id)
    engine.state.CURRENT_LANGUAGE = session.get("lang", "slo")
    
    active_games[sid] = engine
    session["zap_st_igre"] = game_id

    return render_template(
        "game.html",
        game=engine.state,
        page_title=engine.state.name,
        lang=engine.state.CURRENT_LANGUAGE
    )

# -------------------------------------------------
# 4. MASTER DISPATCHER (Controls the Cards)
# -------------------------------------------------
@cardgames_bp.route("/api/click/", methods=["POST"])
@cardgames_bp.route("/api/click", methods=["POST"])
def handle_click():
    try:
        engine = get_user_game()
        if not engine:
            return jsonify({"success": False, "error": "Expired"}), 401

        from .engine.engine import card_Click, card_DblClick, Form_MouseDown, sync_visual_actors
        
        data = request.get_json()
        event_type = data.get("event_type", "click")
        col_idx = data.get("col_idx")
        card_code = data.get("card_code")

        if event_type == "dblclick" and card_code:
            card_DblClick(engine, card_code)
        elif event_type == "click" and card_code:
            card_Click(engine, card_code)
        elif event_type == "click" and col_idx is not None:
            try:
                Form_MouseDown(engine, int(col_idx))
            except: pass
        elif event_type == "table_click":
            engine.state.usermode = 0
            engine.state.selectedCard = ""
            engine.state.selectedColumn = -1
            if hasattr(engine.state, 'ShapeSelektor'):
                engine.state.ShapeSelektor.visible = False

        sync_visual_actors(engine.state)
        return jsonify({"success": True, "game": engine.to_dict()})
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# -------------------------------------------------
# 5. THE RULES (The "Fragile Match" Killer)
# -------------------------------------------------
@cardgames_bp.route("/api/rules")
@cardgames_bp.route("/api/rules/")
def api_rules():
    """
    Fixes the 'Unsolvable Bug' by using integer IDs and normalized names.
    """
    try:
        engine = get_user_game()
        if not engine:
            return jsonify({"title": "Syncing", "text": "Please restart game."}), 401

        # 1. Anchor: The Integer ID
        game_id = session.get("zap_st_igre")
        
        # 2. Anchor: The Language choice inked on the engine
        lang_code = engine.state.CURRENT_LANGUAGE or "slo"

        from .engine.game import get_language_dict
        lang_data = get_language_dict(lang_code)

        # 3. Robust Name Lookup: Normalize the name to avoid "Golf " vs "Golf"
        gamename = str(engine.state.name).strip()

        # Call the parser using the Index ID (most stable)
        rules_text = load_game_rules(
            game_id=int(game_id) if game_id else 1, 
            language=lang_code,
            lang_dir=LANG_DIR,
            list_game=engine.state.LIST_GAME_LINES,
            lang_vars=lang_data.get('lang', {})
        )

        return jsonify({"title": gamename, "text": rules_text})
    except Exception as e:
        return jsonify({"title": "Error", "text": "Could not load rules."}), 200

# -------------------------------------------------
# 6. SETTINGS & EXIT
# -------------------------------------------------
@cardgames_bp.route("/set-language/<code>")
@cardgames_bp.route("/set-language/<code>/")
def set_language(code):
    session["lang"] = code
    engine = get_user_game()
    if engine:
        engine.state.CURRENT_LANGUAGE = code
    session.pop('_cached_lang_dict', None) # Force menu refresh
    return redirect(request.referrer or url_for("cardgames.index"))

@cardgames_bp.route("/exit")
@cardgames_bp.route("/exit/")
def exit_game():
    sid = session.get("user_sid")
    if sid in active_games:
        del active_games[sid]
    session.clear()
    return redirect("/")

@cardgames_bp.route("/api/options/autoplay", methods=["POST"])
@cardgames_bp.route("/api/options/autoplay/", methods=["POST"])
def toggle_autoplay():
    enabled = request.json.get("enabled", False)

    # bug preprecuje autoplay
    #session["autoplay"] = enabled
    #session["autoplay_enabled"] = enabled

    return jsonify({
        "ok": True,
        "autoplay": enabled
    })