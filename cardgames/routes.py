# import uuid
# from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
# from .engine.model import LANG_DIR
# from .engine.game import CardGame
# from .engine.parser import load_game_names, load_game_rules

# # Import the engine functions specifically for the API routes
# from .engine.engine import column_click, card_DblClick

# cardgames_bp = Blueprint("cardgames", __name__, template_folder="templates")

# # Global in-memory storage: sid -> CardGame instance
# active_games = {}

# # -------------------------------------------------
# # HELPERS
# # -------------------------------------------------

# def get_user_game():
#     """Fetches the specific engine instance for the current player's session."""
#     sid = session.get("user_sid")
#     return active_games.get(sid)

# def ensure_sid():
#     """Ensures a unique ID exists for the browser to keep players isolated."""
#     if "user_sid" not in session:
#         session["user_sid"] = str(uuid.uuid4())
#     return session["user_sid"]

# # -------------------------------------------------
# # CONTEXT & LANDING
# # -------------------------------------------------

# @cardgames_bp.context_processor
# def inject_games():
#     from .engine.game import get_language_dict # Import inside to avoid circularity
    
#     lang_code = session.get('lang', 'eng')
#     raw_lang = get_language_dict(lang_code)
    
#     # Safety: If the dictionary is nested, ensure we don't crash on missing keys
#     # We provide a default fallback for the menu structure
#     lang_menu = raw_lang.get('menu', {})
    
#     return dict(
#         games=load_game_names(),
#         lang_dict=raw_lang,
#         m=lang_menu # Short alias for menu translations
#     )

# # @cardgames_bp.context_processor
# # def inject_games():
# #     """Provides the menu list for all templates."""
# #     return dict(games=load_game_names())

# @cardgames_bp.route("/")
# @cardgames_bp.route("")
# def index():
#     """Home page - resets current game selection view."""
#     ensure_sid()
#     return render_template("allgames.html", game=None)

# # -------------------------------------------------
# # GAME LIFECYCLE
# # -------------------------------------------------

# @cardgames_bp.route("/play/<game_id>")
# @cardgames_bp.route("/play/<game_id>/")
# def play_game(game_id):
#     """
#     Initializes a fresh game engine instance.
#     The numeric game_id identifies the game type (Solitaire, etc.)
#     The session sid identifies the specific human player.
#     """
#     sid = ensure_sid()

#     # Create a fresh engine instance for this user
#     # This triggers shuffle and deal internally on the player's private state
#     game_engine = CardGame(game_id)
#     active_games[sid] = game_engine
    
#     session["zap_st_igre"] = game_id

#     return render_template(
#         "game.html",
#         game=game_engine.state,
#         page_title=game_engine.state.name,
#         lang=session.get("lang", "eng")
#     )

# # -------------------------------------------------
# # SETTINGS & INFO
# # -------------------------------------------------

# @cardgames_bp.route("/set-language/<code>")
# @cardgames_bp.route("/set-language/<code>/")
# def set_language(code):
#     """Updates language for this player's session."""
#     session["lang"] = code
#     engine = get_user_game()
#     if engine:
#         engine.state.CURRENT_LANGUAGE = code
#     return redirect(request.referrer or url_for("cardgames.index"))

# @cardgames_bp.route("/api/options/autoplay", methods=["POST"])
# @cardgames_bp.route("/api/options/autoplay/", methods=["POST"])
# def set_autoplay():
#     """Toggles the 'Automatic move' wish for the player."""
#     engine = get_user_game()
#     if not engine:
#         return jsonify({"ok": False, "error": "No active session"}), 401

#     data = request.get_json()
#     enabled = bool(data.get("enabled", False))
#     engine.state.autoplay_enabled = enabled
#     return jsonify({"ok": True, "autoplay": enabled})

# #@cardgames_bp.route("/api/rules", methods=["GET"])
# #@cardgames_bp.route("/api/rules/", methods=["GET"])
# @cardgames_bp.route("/api/rules")
# @cardgames_bp.route("/api/rules/")
# def api_rules():
#     try:
#         engine = get_user_game()
#         if not engine:
#             return jsonify({"title": "Error", "text": "Session expired."}), 401

#         lang_code = session.get("lang", "eng")
        
#         # Jason gets the dictionary from the distant land of game.py
#         from .engine.game import get_language_dict
#         lang_data = get_language_dict(lang_code)
        
#         # Extract the specific 'lang' section for logos
#         lang_vars = lang_data.get('lang', {})

#         from .engine.parser import load_game_rules
#         rules_text = load_game_rules(
#             gamename=engine.state.name,
#             language=lang_code,
#             lang_dir=LANG_DIR,
#             list_game=engine.state.LIST_GAME_LINES,
#             lang_vars=lang_vars # <--- NO LONGER MISSING!
#         )
        
#         return jsonify({
#             "title": engine.state.name, 
#             "text": rules_text
#         })
        
#     except Exception as e:
#         # If Jason trips, we see where in the terminal
#         import traceback
#         print(traceback.format_exc())
#         return jsonify({"title": "Error", "text": "Rules not available."}), 500


# # -------------------------------------------------
# # CORE ENGINE EVENTS (The Brain)
# # -------------------------------------------------


# # THE DISPATCHER
# # @cardgames_bp.route("/api/click", methods=["POST"])
# # @cardgames_bp.route("/api/click/", methods=["POST"])
# # def handle_click():
# #     engine = get_user_game()
# #     data = request.get_json()


# #     # --- HARBOR LOG: What is the Argonauts' mission? ---
# #     print("\n" + "~"*50)
# #     print(f"⚓ WISH ARRIVED | Session: {session.get('user_sid')[:8]}...")
# #     print(f"🌍 Language: {session.get('lang')} | Autoplay: {engine.state.autoplay_enabled if engine else 'N/A'}")
# #     print(f"🎭 Action: {data.get('event_type').upper()}")
# #     if data.get('col_idx') is not None: print(f"📍 Column: {data.get('col_idx')}")
# #     if data.get('card_code'): print(f"🃏 Card: {data.get('card_code')}")
# #     print("~"*50)

    
# #     event_type = data.get("event_type")
# #     col_idx = data.get("col_idx") # Can be string/int or None
# #     card_code = data.get("card_code") # Can be string or None

# #     # --- THE "SESSION EXPIRED" GUARD ---
# #     if not engine:
# #         # If it was a table click, be quiet. If it was a gameplay move, alert.
# #         if event_type == "table_click":
# #             return jsonify({"success": False}), 200 
# #         return jsonify({"success": False, "error": "Session expired"}), 401

# #     # --- THE DISPATCHER (Jason's Commands) ---
# #     from .engine import column_click, card_DblClick, Form_MouseDown, sync_visual_actors

# #     s = engine.state

# #     if event_type == "dblclick":
# #         # VB: card_DblClick or imageFaceDown_DblClick
# #         card_DblClick(s, card_code)

# #     elif event_type == "mousedown":
# #         # VB: Form_MouseDown handles the initial press
# #         if col_idx is not None:
# #             Form_MouseDown(s, int(col_idx))

# #     elif event_type == "click":
# #         # The main logic for Select/Move
# #         if col_idx is not None:
# #             # col_idx is provided whether we clicked a card or a placeholder
# #             column_click(s, int(col_idx), card_code)

# #     elif event_type == "table_click":
# #         # User clicked the green felt. 
# #         # VB Logic: Deselect current card if one is selected.
# #         s.usermode = 0
# #         s.selectedCard = ""
# #         s.selectedColumn = -1
# #         s.ShapeSelektor.visible = False

# #     # --- THE UNIVERSAL SYNC (Argonauts docking at port) ---
# #     # This ensures that no matter what happened above, the masks 
# #     # (imageFaceDown) and actor positions are perfectly aligned.
# #     sync_visual_actors(s)

# #     return jsonify({
# #         "success": True,
# #         "game": engine.to_dict()
# #     })

# @cardgames_bp.route("/api/click", methods=["POST"])
# @cardgames_bp.route("/api/click/", methods=["POST"])
# def handle_click():
#     try:
#         engine = get_user_game()
#         data = request.get_json()
        
#         if not engine:
#             return jsonify({"success": False, "error": "Session expired"}), 401

#         from .engine.engine import column_click, card_DblClick, Form_MouseDown, sync_visual_actors
        
#         event_type = data.get("event_type")
#         col_idx = data.get("col_idx")
#         card_code = data.get("card_code")

#         # Logic Dispatcher
#         if event_type == "dblclick":
#             card_DblClick(engine.state, card_code)
#         elif event_type == "mousedown" and col_idx is not None:
#             Form_MouseDown(engine.state, int(col_idx))
#         elif col_idx is not None:
#             column_click(engine.state, int(col_idx), card_code)

#         # The Argonauts Sync
#         sync_visual_actors(engine.state)

#         return jsonify({"success": True, "game": engine.to_dict()})

#     except Exception as e:
#         import traceback
#         print(traceback.format_exc()) # Prints the full VB-style error to your terminal
#         return jsonify({"success": False, "error": str(e)}), 500


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

@cardgames_bp.context_processor
def inject_games():
    """Provides translated menu items and game list to all templates."""
    from .engine.game import get_language_dict 
    
    lang_code = session.get('lang', 'eng')
    raw_lang = get_language_dict(lang_code)
    
    # FIX: If your load_game_names doesn't take arguments yet, 
    # we call it without them to prevent the TypeError.
    # To get localized names, you must update the function in parser.py
    try:
        games_list = load_game_names(lang_code)
    except TypeError:
        games_list = load_game_names()
    
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

        s = engine.state
        event_type = data.get("event_type", "click")
        col_idx = data.get("col_idx")
        card_code = data.get("card_code")

        # Harbor Log
        print(f"⚓ DISPATCHER: {event_type.upper()} | Col: {col_idx} | Card: {card_code}")

        if event_type == "dblclick":
            card_DblClick(s, card_code)
            
        elif event_type == "mousedown" and col_idx is not None:
            Form_MouseDown(s, int(col_idx))
            
        elif event_type == "table_click":
            s.usermode = 0
            s.selectedCard = ""
            s.selectedColumn = -1
            s.ShapeSelektor.visible = False
            
        elif col_idx is not None:
            # The heart of the engine: column_click
            # Pass 'engine' so it can call engine.do_whole_action()
            column_click(engine, int(col_idx), card_code)

        # The Argonauts Sync (Universal Visual Alignment)
        sync_visual_actors(s)

        return jsonify({"success": True, "game": engine.to_dict()})

    except Exception as e:
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
    session["lang"] = code
    engine = get_user_game()
    if engine:
        # Tell the engine immediately that the language has changed
        engine.state.CURRENT_LANGUAGE = code
        # Optional: Re-trigger the rules loading so the suitcase is updated
        # engine._load_rules_to_state() 
    return redirect(request.referrer or url_for("cardgames.index"))