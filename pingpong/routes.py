# pingpong/routes.py
import uuid
from flask import render_template, session, request, jsonify, redirect, url_for, current_app, Response
from .pingpong import pingpong_bp, FACTORY

# =============================================================================
# 🧠 SESSION SETUP
# =============================================================================
def ensure_session():
    session.setdefault("sid", str(uuid.uuid4()))
    session.setdefault("pong_mode", "HUMAN")
    session.setdefault("pong_paused", False)

def build_pingpong_context():
    """Explicit context – never merged globally."""
    ensure_session()

    return {
        "factory": FACTORY,
        "state": {
            "mode": session["pong_mode"],
            "paused": session["pong_paused"],
        },
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
@pingpong_bp.route("/")
def index():
    context = {
        "PINGPONG": build_pingpong_context()
    }

    template = current_app.jinja_env.get_template("pong_game.html")
    html = template.render(context)

    return Response(html)

# =============================================================================
# API
# =============================================================================
@pingpong_bp.route("/api/state", methods=["POST"])
@pingpong_bp.route("/api/state/", methods=["POST"])
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
        session["pong_mode"] = mode

    return jsonify(ok=True, mode=session["pong_mode"])









# =============================================================================
# 🎮 MENU ROUTES 
# =============================================================================
# MENU GAME
@pingpong_bp.route("/start")
@pingpong_bp.route("/start/")
def start_game():
    session["pong_paused"] = False
    return redirect(url_for("pingpong.index"))

@pingpong_bp.route("/exit")
@pingpong_bp.route("/exit/")
def exit_game():
    # Remove only pong-related session keys
    pong_keys = [k for k in session.keys() if k.startswith("pong_") or k == "sid"]
    for k in pong_keys:
        session.pop(k, None)
    # Redirect to homepage instead of pingpong index
    return redirect("/")  # or use url_for("main.index") if your homepage has a blueprint

# GAME FLOW
@pingpong_bp.route("/pause")
def pause_game():
    session["pong_paused"] = True
    return redirect(url_for("pingpong.index"))

@pingpong_bp.route("/play")
def play_game():
    session["pong_paused"] = False
    return redirect(url_for("pingpong.index"))

# MENU HELP
@pingpong_bp.route("/about")
@pingpong_bp.route("/about/")
def about():
    template = current_app.jinja_env.get_template("pong_about.html")
    html = template.render()
    return Response(html)

# MENU OPPONENT SETTINGS
@pingpong_bp.route("/human")
def set_human():
    session["pong_mode"] = "HUMAN"
    return redirect(url_for("pingpong.index"))

# --- AI LEVELS ---
@pingpong_bp.route("/computer1")
@pingpong_bp.route("/computer1/")
def set_level1():
    session["pong_ai_level"] = 1 # Bad
    session["pong_mode"] = "AI_EASY"
    return redirect(url_for("pingpong.index"))

@pingpong_bp.route("/computer2")
@pingpong_bp.route("/computer2/")
def set_level2():
    session["pong_ai_level"] = 2 # Average
    session["pong_mode"] = "AI_MEDIUM"
    return redirect(url_for("pingpong.index"))

@pingpong_bp.route("/computer3")
@pingpong_bp.route("/computer3/")
def set_level3():
    session["pong_ai_level"] = 3 # Good
    session["pong_mode"] = "AI_HARD"
    return redirect(url_for("pingpong.index"))

# # @pingpong_bp.route("/network")
# # def set_network():
# #     session["pong_mode"] = "NETWORK"
# #     return redirect(url_for("pingpong.index"))
