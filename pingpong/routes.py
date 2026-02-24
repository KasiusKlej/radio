# pingpong/routes.py

import uuid
from flask import (
    render_template,
    session,
    request,
    jsonify,
    redirect,
    url_for,
)
from flask import current_app, Response

from .pingpong import pingpong_bp, FACTORY


# =============================================================================
# SESSION
# =============================================================================

def ensure_session():
    session.setdefault("sid", str(uuid.uuid4()))
    session.setdefault("pong_mode", "AI_UGLY")
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
            "AI_BAD",
            "AI_UGLY",
            "AI_GOOD",
            "NETWORK",
        ],
    }


# =============================================================================
# MAIN PAGE
# =============================================================================

# @pingpong_bp.route("/")
# def index():
#     context = build_pingpong_context()
#     return render_template(
#         "pong_game.html",
#         PINGPONG=context,
#     )

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
def api_state():
    ensure_session()

    data = request.get_json(silent=True) or {}
    mode = data.get("mode")

    if mode in {
        "HUMAN",
        "AI_BAD",
        "AI_UGLY",
        "AI_GOOD",
        "NETWORK",
    }:
        session["pong_mode"] = mode

    return jsonify(ok=True, mode=session["pong_mode"])


# =============================================================================
# NAVIGATION
# =============================================================================




# =============================================================================
# GAME FLOW
# =============================================================================

@pingpong_bp.route("/start")
def start_game():
    session["pong_paused"] = False
    return redirect(url_for("pingpong.index"))


@pingpong_bp.route("/pause")
def pause_game():
    session["pong_paused"] = True
    return redirect(url_for("pingpong.index"))


@pingpong_bp.route("/play")
def play_game():
    session["pong_paused"] = False
    return redirect(url_for("pingpong.index"))











# # pingpong/routes.py

# import uuid
# from flask import (
#     render_template,
#     session,
#     jsonify,
#     request,
#     redirect,
#     url_for
# )

# from .pingpong import pingpong_bp, FACTORY


# # =============================================================================
# # 🧠 SESSION SETUP
# # =============================================================================

# def ensure_session():
#     """Ensure all required session keys exist."""
#     session.setdefault("sid", str(uuid.uuid4()))
#     session.setdefault("pong_mode", "AI_UGLY")
#     session.setdefault("pong_paused", False)


# # =============================================================================
# # 🌍 TEMPLATE CONTEXT
# # =============================================================================

# @pingpong_bp.context_processor
# def inject_pingpong():
#     ensure_session()

#     return {
#         "PINGPONG": {
#             "factory": FACTORY,
#             "state": {
#                 "mode": session["pong_mode"],
#                 "paused": session["pong_paused"],
#             },
#             "modes": [
#                 "HUMAN",
#                 "AI_BAD",
#                 "AI_UGLY",
#                 "AI_GOOD",
#                 "NETWORK",
#             ],
#         }
#     }


# # =============================================================================
# # 🎮 MAIN VIEW
# # =============================================================================

# @pingpong_bp.route("/")
# def index():
#     ensure_session()
#     return render_template("pong_game.html")


# # =============================================================================
# # 🔌 API (USED BY MENU JS)
# # =============================================================================

# @pingpong_bp.route("/api/state", methods=["POST"])
# def api_state():
#     ensure_session()
#     data = request.get_json(force=True) or {}

#     mode = data.get("mode")
#     if mode in {
#         "HUMAN",
#         "AI_BAD",
#         "AI_UGLY",
#         "AI_GOOD",
#         "NETWORK",
#     }:
#         session["pong_mode"] = mode

#     return jsonify(ok=True, mode=session["pong_mode"])


# # =============================================================================
# # 🧭 NAVIGATION
# # =============================================================================

# @pingpong_bp.route("/exit")
# @pingpong_bp.route("/exit/")
# def exit_game():
#     return redirect(url_for("pingpong.index"))


# @pingpong_bp.route("/about")
# @pingpong_bp.route("/about/")
# def about():
#     return render_template("pong_about.html")


# # =============================================================================
# # ⏯️ GAME FLOW
# # =============================================================================

# @pingpong_bp.route("/start")
# def start_new_game():
#     session["pong_paused"] = False
#     return redirect(url_for("pingpong.index"))


# @pingpong_bp.route("/pause")
# def pause_game():
#     session["pong_paused"] = True
#     return redirect(url_for("pingpong.index"))


# @pingpong_bp.route("/play")
# def resume_game():
#     session["pong_paused"] = False
#     return redirect(url_for("pingpong.index"))




# # # # pingpong/routes.py
# # # pingpong/routes.py

# # import uuid
# # from flask import render_template, session, jsonify, request, redirect, url_for
# # from .pingpong import pingpong_bp, FACTORY

# # def ensure_session():
# #     session.setdefault("sid", str(uuid.uuid4()))
# #     session.setdefault("pong_mode", "AI")
# #     session.setdefault("pong_ai_level", "UGLY")

# # @pingpong_bp.context_processor
# # def inject_pingpong():
# #     return {
# #         "PINGPONG": {
# #             "factory": FACTORY,
# #             "state": {
# #                 "mode": session.get("pong_mode"),
# #                 "ai_level": session.get("pong_ai_level"),
# #             }
# #         }
# #     }

# # @pingpong_bp.route("/")
# # def index():
# #     ensure_session()
# #     return render_template("pong_game.html")

# # @pingpong_bp.route("/api/state", methods=["POST"])
# # def api_state():
# #     data = request.get_json(force=True)

# #     if "mode" in data:
# #         session["pong_mode"] = data["mode"]

# #     if "ai_level" in data:
# #         session["pong_ai_level"] = data["ai_level"]

# #     return jsonify(ok=True)













# # # =============================================================================
# # # 🎮 ROUTES 1
# # # =============================================================================

# @pingpong_bp.route("/exit")
# def exit_game():
#     return redirect(url_for("pingpong.index"))




@pingpong_bp.route("/about")
def about():
    template = current_app.jinja_env.get_template("pong_about.html")
    html = template.render()
    return Response(html)

@pingpong_bp.route("/exit")
@pingpong_bp.route("/exit/")
def exit_game():
    # Remove only pong-related session keys
    pong_keys = [k for k in session.keys() if k.startswith("pong_") or k == "sid"]
    for k in pong_keys:
        session.pop(k, None)
    # Redirect to homepage instead of pingpong index
    return redirect("/")  # or use url_for("main.index") if your homepage has a blueprint


# # @pingpong_bp.route("/about")
# # @pingpong_bp.route("/about/")
# # def about():
# #     return render_template("pong_about.html")

# # @pingpong_bp.route("/exit")
# # @pingpong_bp.route("/exit/")
# # def exit_pong():
# #     return redirect("/")



# # @pingpong_bp.route("/start")
# # @pingpong_bp.route("/start/")
# # def start_new_game():
# #     # Signal JS to reset variables and scores
# #     return redirect(url_for("pingpong.index", action="reset"))

# # @pingpong_bp.route("/play")
# # def press_play():
# #     session["pong_paused"] = False
# #     return redirect(url_for("pingpong.index"))

# # @pingpong_bp.route("/pause")
# # def press_pause():
# #     session["pong_paused"] = True
# #     return redirect(url_for("pingpong.index"))


# # # --- OPPONENT SETTINGS ---

# # @pingpong_bp.route("/computer")
# # def set_computer():
# #     session["pong_mode"] = "AI"
# #     return redirect(url_for("pingpong.index"))

# # @pingpong_bp.route("/human")
# # def set_human():
# #     session["pong_mode"] = "HUMAN"
# #     return redirect(url_for("pingpong.index"))

# # @pingpong_bp.route("/network")
# # def set_network():
# #     session["pong_mode"] = "NETWORK"
# #     return redirect(url_for("pingpong.index"))

# # # --- AI LEVELS ---

# # @pingpong_bp.route("/computer1")
# # def set_level1():
# #     session["pong_ai_level"] = 1 # Bad
# #     return redirect(url_for("pingpong.index"))

# # @pingpong_bp.route("/computer2")
# # def set_level2():
# #     session["pong_ai_level"] = 2 # Average
# #     return redirect(url_for("pingpong.index"))

# # @pingpong_bp.route("/computer3")
# # def set_level3():
# #     session["pong_ai_level"] = 3 # Good
# #     return redirect(url_for("pingpong.index"))