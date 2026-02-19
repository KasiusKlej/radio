import uuid
import traceback
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from .engine.model import LANG_DIR
from .engine.game import CardGame
from .engine.parser import load_game_names, load_game_rules

# Import the engine functions explicitly from the engine logic file
from .engine.engine import column_click, card_DblClick, Form_MouseDown, sync_visual_actors

cardgames_bp = Blueprint("cardgames", __name__, template_folder="templates")






# Global in-memory storage: sid -> CardGame instance
active_games = {}

# -------------------------------------------------
# HELPERS
# -------------------------------------------------

def get_user_game():
    """Fetches the specific engine instance for the current player's session."""
    sid = session.get("user_sid")
    return active_games.get(sid)

def ensure_sid():
    """Ensures a unique ID exists for the browser to keep players isolated."""
    if "user_sid" not in session:
        session["user_sid"] = str(uuid.uuid4())
        if "lang" not in session:
            session["lang"] = "eng"
    return session["user_sid"]

# -------------------------------------------------
# CONTEXT & LANDING
# -------------------------------------------------

# ============================================================================
# OPTIMIZED inject_games with Session Caching
# ============================================================================

@cardgames_bp.context_processor
def inject_games():
    """
    Provides translated menu items and game list to all templates.
    
    OPTIMIZATION: Caches language data and game names in session to avoid
    re-parsing files on every page render. Only reloads when language changes.
    """
    lang_code = session.get('lang', 'eng')
    
    # ──────────────────────────────────────────────────────────────────────
    # Check if we have cached data for the current language
    # ──────────────────────────────────────────────────────────────────────
    cached_lang = session.get('_cached_lang_code')
    
    if cached_lang != lang_code or '_cached_lang_dict' not in session:
        # Cache miss or language changed → reload everything
        from .engine.game import get_language_dict 
        from .engine.parser import read_gamenames_from_language_files
        from .engine.model import LANG_DIR
        
        raw_lang = get_language_dict(lang_code)
        games_list = read_gamenames_from_language_files(lang_code, LANG_DIR)
        
        # Store in session for future requests
        session['_cached_lang_code'] = lang_code
        session['_cached_lang_dict'] = raw_lang
        session['_cached_games_list'] = games_list
    else:
        # Cache hit → use stored data
        raw_lang = session['_cached_lang_dict']
        games_list = session['_cached_games_list']
    
    return dict(
        games=games_list,
        lang_dict=raw_lang,
        m=raw_lang.get('menu', {}) 
    )


@cardgames_bp.route("/")
@cardgames_bp.route("")
def index():
    ensure_sid()
    return render_template("allgames.html", game=None)

# -------------------------------------------------
# GAME LIFECYCLE
# -------------------------------------------------

@cardgames_bp.route("/play/<game_id>")
@cardgames_bp.route("/play/<game_id>/")
def play_game(game_id):
    sid = ensure_sid()
    game_engine = CardGame(game_id)
    active_games[sid] = game_engine
    session["zap_st_igre"] = game_id

    return render_template(
        "game.html",
        game=game_engine.state,
        page_title=game_engine.state.name,
        lang=session.get("lang", "eng")
    )

# -------------------------------------------------
# MASTER DISPATCHER (One Route to Rule Them All)
# -------------------------------------------------
@cardgames_bp.route("/api/click", methods=["POST"])
@cardgames_bp.route("/api/click/", methods=["POST"])
def handle_click():
    try:
        engine = get_user_game()
        data = request.get_json()
        
        if not engine:
            if data.get("event_type") == "table_click":
                return jsonify({"success": False}), 200
            return jsonify({"success": False, "error": "Session expired"}), 401

        from .engine.engine import (
            card_Click, card_DblClick, Form_MouseDown, 
            sync_visual_actors
        )
        
        event_type = data.get("event_type", "click")
        col_idx = data.get("col_idx")
        card_code = data.get("card_code")
        
        print(f"⚓ EVENT: {event_type.upper()} | Col: {col_idx} | Card: {card_code}")
        
        # ────────────────────────────────────────────────────────────────
        # EVENT ROUTING
        # ────────────────────────────────────────────────────────────────
        
        if event_type == "dblclick" and card_code:
            card_DblClick(engine, card_code)
        
        elif event_type == "click" and card_code:
            card_Click(engine, card_code)
        
        elif event_type == "click" and col_idx is not None and not card_code:
            # ✅ FIX: Validate col_idx before converting to int
            try:
                col_idx_int = int(col_idx)
                # Additional validation: check if column exists
                if 0 <= col_idx_int < len(engine.state.kup):
                    Form_MouseDown(engine, col_idx_int)
                else:
                    print(f"⚠️  Invalid column index: {col_idx_int}")
            except (ValueError, TypeError):
                print(f"⚠️  Cannot convert col_idx to int: {col_idx}")
                # Don't crash - just ignore invalid clicks
        
        elif event_type == "table_click":
            s = engine.state
            s.usermode = 0
            s.selectedCard = ""
            s.selectedColumn = -1
            s.ShapeSelektor.visible = False
        
        # ────────────────────────────────────────────────────────────────
        # POST-EVENT SYNC
        # ────────────────────────────────────────────────────────────────
        sync_visual_actors(engine.state)
        
        return jsonify({"success": True, "game": engine.to_dict()})
    
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({"success": False, "error": str(e)}), 500


# -------------------------------------------------
# INFO & SETTINGS
# -------------------------------------------------

@cardgames_bp.route("/api/rules")
@cardgames_bp.route("/api/rules/")
def api_rules():
    try:
        engine = get_user_game()
        if not engine:
            return jsonify({"title": "Error", "text": "Session expired."}), 401

        # 1. Get the current language code from the session (e.g., 'kor')
        lang_code = session.get("lang", "eng")
        
        # 2. Get the dictionary for logos/messages
        from .engine.game import get_language_dict
        lang_data = get_language_dict(lang_code)
        
        # 3. Calculate the rules FRESH based on the current language
        rules_text = load_game_rules(
            gamename=engine.state.name,
            language=lang_code,
            lang_dir=LANG_DIR,
            list_game=engine.state.LIST_GAME_LINES,
            lang_vars=lang_data.get('lang', {})
        )

        # 4. UPDATE the state so it's synced for next time
        engine.state.rules_of_currently_played_game = rules_text
        engine.state.CURRENT_LANGUAGE = lang_code

        # 5. RETURN THE FRESH RULES (The 'rules_text' variable!)
        return jsonify({
            "title": engine.state.name, 
            "text": rules_text  # <--- FIXED: No longer returning the stale state
        })
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"title": "Error", "text": "Rules unavailable."}), 500
    

@cardgames_bp.route("/set-language/<code>")
@cardgames_bp.route("/set-language/<code>/")
def set_language(code):
    """
    Changes the user's language preference.
    Invalidates cached language data to force reload on next page.
    """
    session["lang"] = code
    
    # Invalidate cache so inject_games reloads on next request
    session.pop('_cached_lang_code', None)
    session.pop('_cached_lang_dict', None)
    session.pop('_cached_games_list', None)
    
    # Update engine state if game is running
    engine = get_user_game()
    if engine:
        engine.state.CURRENT_LANGUAGE = code
    
    return redirect(request.referrer or url_for("cardgames.index"))


@cardgames_bp.route("/api/options/autoplay", methods=["POST"])
@cardgames_bp.route("/api/options/autoplay/", methods=["POST"])
def set_autoplay():
    """Toggles the 'Automatic move' wish for the player."""
    engine = get_user_game()
    if not engine:
        return jsonify({"ok": False, "error": "No active session"}), 401

    data = request.get_json()
    enabled = bool(data.get("enabled", False))
    engine.state.autoplay_enabled = enabled
    return jsonify({"ok": True, "autoplay": enabled})


@cardgames_bp.route("/exit")
@cardgames_bp.route("/exit/")
def exit_game():
    """Cleans up the active game and returns to the site root."""
    sid = session.get("user_sid")
    
    # 1. Remove the engine instance from memory to save RAM
    if sid in active_games:
        del active_games[sid]
    
    # 2. Clear the 'current game' marker from the session
    session.pop("zap_st_igre", None)
    
    # 3. Redirect to the main homepage
    # If your main homepage route is named 'index' in your main app:
    return redirect("/")