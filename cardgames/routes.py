import os
import uuid
import traceback
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from .engine.model import LANG_DIR
from .engine.game import CardGame
from .engine.parser import load_game_rules

cardgames_bp = Blueprint("cardgames", __name__, template_folder="templates")

# ============================================================================
# CRITICAL FIX: Worker-Isolated Storage
# ============================================================================
# PROBLEM: Multiple production workers share the same in-memory dictionary
#   Worker 1: active_games["user123"] = GameA
#   Worker 2: active_games["user123"] = GameB  ← COLLISION!
#   Result: Cards teleport, languages switch, chaos
#
# SOLUTION: Include worker PID in storage key
#   Worker 1: active_games[(PID1, "user123")] = GameA  ✅
#   Worker 2: active_games[(PID2, "user123")] = GameB  ✅
#   Result: Complete isolation, no interference
#
# WHY IT WORKS:
#   - Each worker process has a unique PID
#   - Storage key = (worker_pid, session_id)
#   - Same session_id on different workers → different keys
#   - No cross-contamination possible
# ============================================================================

WORKER_ID = os.getpid()  # Unique per worker process

# Storage: {(worker_id, session_id): CardGame}
active_games = {}

def get_session_key():
    """Generate worker-specific session key to prevent cross-contamination."""
    sid = session.get("user_sid")
    if not sid:
        return None
    return (WORKER_ID, sid)

# -------------------------------------------------
# 1. CORE HELPERS (Now with Complete Isolation)
# -------------------------------------------------

def get_user_game():
    """
    Fetches the engine with complete worker isolation.
    CRITICAL: Each worker maintains its own game instances.
    """
    session_key = get_session_key()
    if not session_key:
        return None

    engine = active_games.get(session_key)
    
    # Self-healing: If engine is gone but session exists, recreate it
    if not engine:
        game_id = session.get("zap_st_igre")
        if game_id:
            engine = CardGame(game_id)
            engine.state.CURRENT_LANGUAGE = session.get("lang", "slo")
            active_games[session_key] = engine
            print(f"🔧 Recreated game for worker {WORKER_ID}, session {session_key[1][:8]}")

    if engine:
        # SYNC: Ensure THIS session's language is active
        current_lang = session.get("lang", "slo")
        if engine.state.CURRENT_LANGUAGE != current_lang:
            engine.state.CURRENT_LANGUAGE = current_lang
            print(f"🔄 Synced language to {current_lang} for session {session_key[1][:8]}")
        
    return engine

def ensure_sid():
    """Ensures a unique ID exists and sets default language."""
    if "user_sid" not in session:
        new_sid = str(uuid.uuid4())
        session["user_sid"] = new_sid
        print(f"✨ New session: {new_sid[:8]} on worker {WORKER_ID}")
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
        m=session.get('_cached_lang_dict', {}).get('menu', {}), 
        #autoplay_enabled=session.get('autoplay_enabled', False)
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
    session_key = get_session_key()
    
    # CRITICAL: Clean up old game for THIS worker/session combo only
    if session_key in active_games:
        del active_games[session_key]
        print(f"🗑️  Cleaned up old game for session {sid[:8]} on worker {WORKER_ID}")
    
    # Start fresh with isolated instance
    engine = CardGame(game_id)
    engine.state.CURRENT_LANGUAGE = session.get("lang", "slo")
    engine.autoplay_enabled = session.get("autoplay_enabled", False)

    # Store with worker-specific key
    active_games[session_key] = engine
    session["zap_st_igre"] = game_id
    
    print(f"🎮 Started game {game_id} for session {sid[:8]} on worker {WORKER_ID}")

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
    """Exit and clean up THIS worker/session only."""
    session_key = get_session_key()
    
    # Clean up THIS worker's game instance only
    if session_key and session_key in active_games:
        del active_games[session_key]
        print(f"🗑️  Session {session_key[1][:8]} exited from worker {WORKER_ID}")
    
    session.clear()
    return redirect("/")

@cardgames_bp.route("/api/options/autoplay", methods=["POST"])
@cardgames_bp.route("/api/options/autoplay/", methods=["POST"])
def toggle_autoplay():
    enabled = bool(request.json.get("enabled", False))
    session["autoplay_enabled"] = enabled
    engine = get_user_game()
    if engine:
        engine.autoplay_enabled = enabled
        print(f"toggled {enabled}")

    return jsonify({
        "ok": True,
        "autoplay_enabled": enabled
    })

# for later
@cardgames_bp.route("/api/register")
@cardgames_bp.route("/api/register/")
def api_about():
    """
    Displays application 'About' information.
    Uses the same popup mechanism as Rules.
    """
    try:
        engine = get_user_game()

        # language fallback
        lang_code = (
            engine.state.CURRENT_LANGUAGE
            if engine and engine.state.CURRENT_LANGUAGE
            else session.get("lang", "slo")
        )

        from .engine.game import get_language_dict
        lang_data = get_language_dict(lang_code)
        lang = lang_data.get("lang", {})

        # Compose About text (VB-style)
        title = lang.get("app", "Card Games for One Player")

        text = (
            f"{lang.get('logo1', 'Card Games for One Player')}\n"
            f"{lang.get('logo2', '')}\n"
            f"{lang.get('logo3', 'made in 1999')}\n"
            f"{lang.get('logo4', '')}"
        ).strip()

        # Last line of defense
        if not text:
            text = "Card Games for One Player\nmade in 1999"

        return jsonify({
            "title": title,
            "text": text
        })

    except Exception:
        return jsonify({
            "title": "Register",
            "text": "Card Games for One Player\nmade in 1999"
        }), 200
