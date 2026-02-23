# =============================================================================
# 🌍 DATA MODEL
# =============================================================================
from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class Player:
    # Identity
    id: str
    side: str                     # "LEFT" | "RIGHT"

    # Control & Mode
    control_mode: str             # HUMAN | AI | NETWORK
    ai_level: Optional[str] = None
    input_state: Dict[str, bool] = field(default_factory=dict)

    # Paddle
    y: float = 0.0
    dy: float = 0.0
    height: float = 190
    speed_base: float = 12
    speed_multiplier: float = 1.0

    # Effort System
    effort: float = 0.0
    effort_rate: float = 1.0          # points per second
    effort_speed_bonus: float = 0.11  # +11% per effort
    effort_decay: float = 0.5

    # Score
    score: int = 0
    last_score_time: float = 0.0

    # Match Stats
    stats_match: Dict[str, float] = field(default_factory=lambda: {
        "goals": 0,
        "hits": 0,
        "backhands": 0,
        "forehands": 0,
        "misses": 0,
        "avg_goal_received": 0.0,
        "avg_goal": 0.0,
        "avg_effort": 0.0,
        "time_moving": 0.0,
    })

    # Career Stats
    stats_total: Dict[str, float] = field(default_factory=lambda: {
        "games_played": 0,
        "games_won": 0,
        "games_lost": 0,
        "play_time": 0.0,
    })



class Ball:
    value: int      # dice carries random value from 1 to 6
    x: float
    y: float
    dx: float
    dy: float
    speed: float
    radius: float
    
    last_hit_by: str | None
    spin: float
    
    reset_pending: bool

class Match:
    id: str
    
    # --- Players ---
    players: dict[str, Player]   # LEFT / RIGHT
    
    # --- Ball ---
    ball: Ball
    
    # --- State ---
    state: str           # IDLE | RUNNING | PAUSED | FINISHED
    winner: str | None
    
    # --- Rules ---
    score_limit: int     # e.g. 52
    field_width: int
    field_height: int
    
    # --- Timing ---
    start_time: float
    last_tick: float
    
    # --- Meta ---
    is_networked: bool
    seed: int            # deterministic physics


