def apply_game_layout_heuristics(game):
    """
    Apply per-game layout intent ONLY for non-slot games.
    Slot-based games must NEVER reach here.
    """
    # gid = game.game_id

    # # 🔒 Absolute guard
    # if any(col.get("has_slot") for col in game.columns.values()):
    #     return

    # if gid == "free_cell":
    #     return

    # if gid == "four_seasons":
    #     # FourSeasons IS slot-based → should never reach here
    #     return
    
    return
