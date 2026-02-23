import os
import uuid
import random
from pathlib import Path
from flask import Blueprint, render_template, session, redirect, url_for, jsonify, request

# =============================================================================
# 🛠️ UPDATED FACTORY SETTINGS (Admin Scope)
# =============================================================================

# pingpong/pingpong.py

FACTORY = {
    "geometry": {
        "width": 800,
        "height": 600,
        "fullscreen": True,
    },
    "racket": {
        "width": 14,
        "height": 90,
    },
    "ball": {
        "radius": 8,
        "random_factor": 0.15,
    },
    "rules": {
        "max_score": 52,
    },
    "assets": {
        "dice_path": "/static/metropoly/assets/graphics/",
    },
    "modes": ["HUMAN", "AI", "NETWORK"],
    "ai_levels": [1, 2, 3],
}



# 🧮 GEOMETRY (Full Screen Proportions)
# DEFAULT_X = 1024       # Wider for classic full-screen feel
# DEFAULT_Y = 768        
# DEFAULT_X = 1024       # Wider for classic full-screen feel
# DEFAULT_Y = 768        

# RACKET_SIZE = {"WIDTH": 15, "HEIGHT": 100}
# BALL_SIZE = 10         # Radius

# 🏃 PHYSICAL DYNAMICS
EFFORT_GROWTH_RATE = 0.02  # How fast effort reaches 1.0 (100%)
MAX_SPEED_MULTIPLIER = 2.5 # How much faster racket moves at max effort
SPIN_STRENGTH = 0.6        # How much racket speed alters ball angle
SPEED_STRENGTH = 1.2       # How much racket speed boosts ball speed

# 🎲 VISUALS
BALL_FLIP_FREQ = 800       # ms for ball costume change

# 📂 PATH RESOLUTION
# BASE: Points to .../mywebsite/pingpong/
BASE = Path(__file__).resolve().parent

# ASSETS: Points to .../mywebsite/static/pingpong/
# (Assuming your global static folder structure)
STATIC_DIR = BASE.parent / "static" / "pingpong"
#CSS_PATH   = "css/pong.css"
#JS_PATH    = "js/pong.js"
#DICE_PATH = "metropoly/metro_static/assets/graphics/"
#DICE_PATH = "/static/metropoly/assets/graphics/"

# 🧮 GEOMETRY & PHYSICS
DEFAULT_X = 800       # Canvas Width
DEFAULT_Y = 500       # Canvas Height
RACKET_SIZE = {
    "WIDTH": 10,
    "HEIGHT": 80
}

# 🎲 RANDOMIZATION
# Used for ball angle variation and AI "imperfection"
RANDOM_FACTOR = 0.15 

# 🏆 RULES
MAX_SCORE = 52
PENALTY_MIN = 1
PENALTY_MAX = 6

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

# Global in-memory store for active matches (Player SIDs)
# (Used if you move logic to the server for Network Mode)
active_matches = {}

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

# =============================================================================
# 🌍 CONTEXT PROCESSOR (Win95 Menu Integration)
# =============================================================================

@pingpong_bp.context_processor
def inject_pingpong_ui():
    pass