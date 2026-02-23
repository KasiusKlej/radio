# # pingpong/routes.py
# pingpong/routes.py

import uuid
from flask import Blueprint, render_template, session, redirect, url_for, jsonify, request
from .pingpong import FACTORY

pingpong_bp = Blueprint(
    "pingpong",
    __name__,
    template_folder="templates",
)

# ---------------------------------------------------------------------
# Session bootstrap
# ---------------------------------------------------------------------

def ensure_sid():
    session.setdefault("user_sid", str(uuid.uuid4()))
    session.setdefault("lang", "slo")
    session.setdefault("pong_mode", "AI")
    session.setdefault("pong_ai_level", 2)

# ---------------------------------------------------------------------
# Context processor (NEVER crashes)
# ---------------------------------------------------------------------

@pingpong_bp.context_processor
def inject_pingpong():
    return {
        "FACTORY": FACTORY,
        "PONG_STATE": {
            "mode": session.get("pong_mode", "AI"),
            "ai_level": session.get("pong_ai_level", 2),
            "dice_path": ""
        },
    }

# ---------------------------------------------------------------------
# API (JS → server, multiplayer-ready)
# ---------------------------------------------------------------------

@pingpong_bp.route("/api/state", methods=["POST"])
def set_state():
    data = request.get_json(silent=True) or {}
    if data.get("mode") in FACTORY["modes"]:
        session["pong_mode"] = data["mode"]
    if data.get("ai_level") in FACTORY["ai_levels"]:
        session["pong_ai_level"] = data["ai_level"]
    
    return jsonify(ok=True)













# # =============================================================================
# # 🛠️ FACTORY SETTINGS (AUTHORITATIVE)
# # =============================================================================

# FACTORY = {
#     "geometry": {
#         "width": 1920,
#         "height": 1280,
#         "fullscreen": True,
#     },
#     "racket": {
#         "width": 14,
#         "height": 90,
#     },
#     "ball": {
#         "radius": 8,
#         "random_factor": 0.15,
#     },
#     "rules": {
#         "max_score": 52,
#     },
#     "modes": ["HUMAN", "AI", "NETWORK"],
#     "ai_levels": [1, 2, 3],
# }


# import uuid
# from flask import Blueprint, render_template, session, redirect, url_for, jsonify, request
# from .pingpong import FACTORY

# pingpong_bp = Blueprint(
#     "pingpong",
#     __name__,
#     template_folder="templates",
# )

# # =============================================================================
# # 🔧 SESSION BOOTSTRAP
# # =============================================================================

# def ensure_sid():
#     if "user_sid" not in session:
#         session["user_sid"] = str(uuid.uuid4())
#     if "lang" not in session:
#         session["lang"] = "slo"
#     if "pong_mode" not in session:
#         session["pong_mode"] = "AI"
#     if "pong_ai_level" not in session:
#         session["pong_ai_level"] = 2

# # =============================================================================
# # 🌍 CONTEXT PROCESSOR (THIS FIXES ERROR #1)
# # =============================================================================

# @pingpong_bp.context_processor
# def inject_pingpong():
#     return {
#         "PONG_CONFIG": FACTORY,
#         "PONG_STATE": {
#             "mode": session.get("pong_mode", "AI"),
#             "ai_level": session.get("pong_ai_level", 2),
#         }
#     }

# # @pingpong_bp.context_processor
# # def inject_pingpong_ui():
# #     return {
# #         "pong_config": {
# #             "width": 800,
# #             "height": 500,
# #             "max_score": 52,
# #             "dice_path": "/static/metropoly/assets/graphics/"
# #         }
# #     }



# # =============================================================================
# # ⚙️ API (FOR JS)
# # =============================================================================

# @pingpong_bp.route("/api/state", methods=["POST"])
# def set_state():
#     data = request.get_json(force=True)
#     if "mode" in data:
#         session["pong_mode"] = data["mode"]
#     if "ai_level" in data:
#         session["pong_ai_level"] = data["ai_level"]
#     return jsonify(ok=True)



# =============================================================================
# 🎮 ROUTES 1
# =============================================================================

@pingpong_bp.route("/")
def index():
    ensure_sid()
    return render_template("pong_game.html")

@pingpong_bp.route("/exit")
@pingpong_bp.route("/exit/")
def exit_game():
    return redirect("/")

@pingpong_bp.route("/about")
@pingpong_bp.route("/about/")
def about():
    return render_template("pong_about.html")

@pingpong_bp.route("/exit")
@pingpong_bp.route("/exit/")
def exit_pong():
    return redirect("/")

@pingpong_bp.route("/start")
@pingpong_bp.route("/start/")
def start_new_game():
    # Signal JS to reset variables and scores
    return redirect(url_for("pingpong.index", action="reset"))

@pingpong_bp.route("/play")
def press_play():
    session["pong_paused"] = False
    return redirect(url_for("pingpong.index"))

@pingpong_bp.route("/pause")
def press_pause():
    session["pong_paused"] = True
    return redirect(url_for("pingpong.index"))


# --- OPPONENT SETTINGS ---

@pingpong_bp.route("/computer")
def set_computer():
    session["pong_mode"] = "AI"
    return redirect(url_for("pingpong.index"))

@pingpong_bp.route("/human")
def set_human():
    session["pong_mode"] = "HUMAN"
    return redirect(url_for("pingpong.index"))

@pingpong_bp.route("/network")
def set_network():
    session["pong_mode"] = "NETWORK"
    return redirect(url_for("pingpong.index"))

# --- AI LEVELS ---

@pingpong_bp.route("/computer1")
def set_level1():
    session["pong_ai_level"] = 1 # Bad
    return redirect(url_for("pingpong.index"))

@pingpong_bp.route("/computer2")
def set_level2():
    session["pong_ai_level"] = 2 # Average
    return redirect(url_for("pingpong.index"))

@pingpong_bp.route("/computer3")
def set_level3():
    session["pong_ai_level"] = 3 # Good
    return redirect(url_for("pingpong.index"))