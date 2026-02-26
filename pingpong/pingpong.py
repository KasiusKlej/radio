# pingpong/pingpong.py
import os
import uuid
import random
from pathlib import Path
from flask import Blueprint, render_template, session, redirect, url_for, jsonify, request

# =============================================================================
# 🛠️ UPDATED FACTORY SETTINGS (Admin Scope)
# =============================================================================

FACTORY = {
    "geometry": {"width": 1920, "height": 1280, "background": "#0B6B2A",},
    "racket": {"width": 45, "height": 190, "speed": 12,},
    "ball": {"radius": 32, "speed": 20, "spin": 0.6,},
    "rules": {"max_score": 52,},
    "assets": {"dice_path": "/static/metropoly/assets/graphics/",},
    "modes": {  "HUMAN": {}, 
                "AI": {"levels": {"AI_EASY":   0.04, "AI_MEDIUM":  0.08, "AI_HARD":  0.15,}},
                "NETWORK": {"sync_rate": 30,}
    }
}
# 📂 PATH RESOLUTION
# ASSETS: Points to .../mywebsite/static/pingpong/
# (Assuming your global static folder structure)
BASE = Path(__file__).resolve().parent
STATIC_DIR = BASE.parent / "static" / "pingpong"


# =============================================================================
# 🛰️ BLUEPRINT SETUP
# =============================================================================
pingpong_bp = Blueprint(
    "pingpong", 
    __name__, 
    template_folder="templates",
    static_folder=str(STATIC_DIR),
    static_url_path="/static"
)


# =============================================================================
# 🔧 SHARED HELPERS
# =============================================================================
def ensure_sid():
    """Identical to Metropoly/CardGames to maintain cross-app compatibility."""
    if "user_sid" not in session:
        session["user_sid"] = str(uuid.uuid4())
    if "lang" not in session:
        session["lang"] = "slo"
    return session["user_sid"]

# Global in-memory store for active matches (Player SIDs)
# (Used if you move logic to the server for Network Mode)
active_matches = {}


# =============================================================================
# 🌍 CONTEXT PROCESSOR (Win95 Menu Integration)
# =============================================================================
@pingpong_bp.context_processor
def inject_pingpong_ui():
    pass



