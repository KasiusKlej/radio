import re
from pathlib import Path
from .model import Column, Card
from .model import menu_items_slo, menu_items_eng, LANG_DIR

GAMES_FILE = Path(__file__).parent.parent / "games" / "CardGames-utf8.txt"


# -------------------------------------------------
# Column presets (VB [COLUMNS DEFAULTS])
# -------------------------------------------------
class ColumnPresets:
    def __init__(self):
        self.default_overlap_x = 200
        self.default_overlap_y = 350
        self.zoom = 1


# -------------------------------------------------
# Column factory (VB ReDim Preserve kup(c))
# -------------------------------------------------
def new_column(cId, name, position, num_cards, shuffle_any):
    col = Column()

    col.cId = cId
    col.column_name = name
    col.position = position
    col.num_cards = num_cards
    col.shufle_any_cards = shuffle_any

    # ---- VB defaults ----
    col.max_cards = 0
    col.suit = "-1"
    col.card_value = "-1"
    col.alternate = "-1"
    col.suit_or_card = "-1"
    col.always_allowed_from_columns = "-1"

    col.custom_x = -1
    col.custom_y = -1

    col.overlap_x = 0
    col.overlap_y = 0
    col.overlap = 0

    col.player_can_put_card = "-1"
    col.player_can_put_card_if_empty = "-1"
    col.player_can_take_card = "-1"

    col.contents_at_start = ""
    col.cards_face_up = ""

    col.dblclick_moves_to = "-1"
    col.allways_facedown = "-1"
    col.after_move_action = "-1"
    col.attempted_move_action = "-1"
    col.after_playermove_action = "-1"
    col.attempted_playermove_action = "-1"
    col.use_facedown = "-1"
    col.aces_on_kings = "-1"

    col.backstyle = "-1"
    col.backcolor = "-1"

    col.contents = []
    col.weight = 0

    return col


# -------------------------------------------------
# Main loader
# -------------------------------------------------
# def load_games():
#     lines = GAMES_FILE.read_text(encoding="utf-8").splitlines()

#     games = []
#     i = 0

#     while i < len(lines):
#         line = lines[i].strip()
#         i += 1

#         if not line or line.startswith("#"):
#             continue

#         if line != "[GAMENAME]":
#             continue

#         # -------------------------------
#         # New game
#         # -------------------------------
#         raw_name = lines[i].strip()     # lines[i] example: "FreeCell (Prosta celica)"
#         name = lines[i].strip()

#         if "(" in raw_name and ")" in raw_name:
#             eng_name = raw_name.split("(")[0].strip()
#             slo_name = raw_name.split("(", 1)[1].rstrip(")").strip()
#         else:
#             # fallback if no localization present
#             eng_name = raw_name
#             slo_name = raw_name

#         menu_items_eng.append(eng_name)
#         menu_items_slo.append(slo_name)

#         i += 1


#         game_id = re.sub(r"[^a-z0-9_]", "_", name.lower())

#         presets = ColumnPresets()
#         kup = []

#         # ✅ START RAW CAPTURE
#         raw_lines = ["[GAMENAME]", name]

#         # -------------------------------
#         # Capture until next [GAMENAME] or EOF
#         # -------------------------------
#         start = i
#         while i < len(lines) and lines[i].strip() != "[GAMENAME]":
#             raw_lines.append(lines[i].rstrip("\n"))
#             i += 1

#         # -------------------------------
#         # SECOND PASS: parse from raw_lines
#         # -------------------------------
#         # (this mirrors VB behaviour exactly)

#         # ---- COLUMNS DEFAULTS ----
#         j = 0
#         while j < len(raw_lines):
#             if raw_lines[j].strip() == "[COLUMNS DEFAULTS]":
#                 j += 1
#                 while j < len(raw_lines):
#                     s = raw_lines[j].strip()
#                     j += 1
#                     if s == "[END COLUMNS DEFAULTS]":
#                         break
#                     if s.startswith("overlap_x="):
#                         presets.default_overlap_x = int(s.split("=", 1)[1])
#                     elif s.startswith("overlap_y="):
#                         presets.default_overlap_y = int(s.split("=", 1)[1])
#                     elif s.startswith("zoom="):
#                         presets.zoom = float(s.split("=", 1)[1])
#                 break
#             j += 1

#         # ---- COLUMNS ----
#         j = 0
#         while j < len(raw_lines) and raw_lines[j].strip() != "[COLUMNS]":
#             j += 1

#         if j >= len(raw_lines):
#             raise RuntimeError(f"{name}: [COLUMNS] not found")

#         j += 1
#         c = 0

#         while j < len(raw_lines):
#             s = raw_lines[j].strip()
#             j += 1

#             if s == "[END COLUMNS]":
#                 break

#             parts = [p.strip() for p in s.split(",")]
#             col_name = parts[0]
#             position = parts[1][:2]
#             num_cards = parts[2]
#             shuffle_any = parts[-1]

#             col = new_column(c, col_name, position, num_cards, shuffle_any)
#             kup.append(col)
#             c += 1

#         # ---- COLUMNS BEHAVIOUR ----
#         j = 0
#         current_col = None

#         while j < len(raw_lines):
#             s = raw_lines[j].strip()
#             j += 1
#             if s == "[COLUMNS BEHAVIOUR]":
#                 break

#         while j < len(raw_lines):
#             s = raw_lines[j].strip()
#             j += 1

#             if s == "[END COLUMNS BEHAVIOUR]":
#                 break

#             if s.startswith("[") and s.endswith("]"):
#                 col_name = s[1:-1]
#                 current_col = next(
#                     (c for c in kup if c.column_name == col_name),
#                     None
#                 )
#                 continue

#             if not current_col or "=" not in s:
#                 continue

#             key, value = s.split("=", 1)
#             value = value.strip()

#             if key == "overlap_x":
#                 current_col.overlap_x = (
#                     presets.default_overlap_x if value == "default" else int(value)
#                 )
#             elif key == "overlap_y":
#                 current_col.overlap_y = (
#                     presets.default_overlap_y if value == "default" else int(value)
#                 )
#             elif key == "custom_x":
#                 current_col.custom_x = int(value)
#             elif key == "custom_y":
#                 current_col.custom_y = int(value)
#             elif key == "cards_face_up":
#                 current_col.cards_face_up = value

#         # -------------------------------
#         # DONE
#         # -------------------------------
#         games.append({
#             "id": game_id,
#             "name": name,
#             "kup": kup,
#             "presets": presets,
#             "raw_lines": raw_lines,  # ✅ CORRECT
#         })

#     return games

def load_games():
    """
    VB equivalent:
    Open CardGames.txt For Input
    Read all lines into ListGame
    """
    games_file = LANG_DIR / "CardGames-utf8.txt"

    with open(games_file, "r", encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f]



# -------------------------------------------------
# Helper
# -------------------------------------------------
def normalize_game_id(name: str) -> str:
    """
    Convert display game name to canonical id.
    """
    name = name.lower()
    name = re.sub(r"[^\w]+", "_", name)
    name = re.sub(r"_+", "_", name)
    return name.strip("_")

# def load_game_names():
#     games = []

#     with open(LANG_DIR / "CardGames-utf8.txt", encoding="utf-8") as f:
#         for line in f:
#             line = line.strip()
#             if not line or line.startswith("["):
#                 continue

#             display_name = line
#             game_id = normalize_game_id(display_name)

#             games.append({
#                 "id": game_id,
#                 "name": display_name
#             })

#     return games
def load_game_names():
    """
    Extract game IDs and display names for menu only.
    """
    lines = load_games()

    games = []
    i = 0
    while i < len(lines):
        if lines[i] == "[GAMENAME]":
            name = lines[i + 1].strip()
            game_id = name.lower().replace(" ", "_")
            games.append({
                "id": game_id,
                "name": name
            })
            i += 2
        else:
            i += 1

    return games




def language_parser(lang_dir: Path, filename: str) -> dict:
    """
    Parse a VB-style language file into structured data.

    lang_dir : Path to directory containing language txt files
    filename : e.g. 'eng.txt', 'kor.txt'
    """

    if not filename.lower().endswith(".txt"):
        filename += ".txt"

    path = lang_dir / filename
    if not path.exists():
        raise FileNotFoundError(f"Language file not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]

    idx = 0

    def next_line():
        nonlocal idx
        val = lines[idx]
        idx += 1
        return val

    lang = {}

    # --- A. core language strings ---
    lang["lang"] = {
        "app": next_line(),
        "msg": next_line(),
        "youwon": next_line(),
        "youlost": next_line(),
        "logo1": next_line(),
        "logo2": next_line(),
        "logo3": next_line(),
        "logo4": next_line(),
        "statWon": next_line(),
        "statLost": next_line(),
        "statPlayed": next_line(),
        "statPct": next_line(),
        "statPctalfa": next_line(),
    }

    next_line()  # separator

    # --- B. menu captions ---
    lang["menu"] = {
        "game": next_line(),
        "zoom": next_line(),
        "options": next_line(),
        "help": next_line(),
        "exit": next_line(),
        "zoomIn": next_line(),
        "zoomOut": next_line(),
        "max": next_line(),
        "min": next_line(),
        "autoplay": next_line(),
        "resizable": next_line(),
        "otherCards": next_line(),
        "statistics": next_line(),
        "overall": next_line(),
        "rules": next_line(),
        "about": next_line(),
    }

    next_line()  # separator

    # --- C. dialog buttons ---
    lang["dialog"] = {
        "ok": next_line(),
        "cancel": next_line(),
    }

    next_line()  # separator

    lang["statistics"] = {
        "ok": next_line(),
        "legend": next_line(),
        "won": next_line(),
        "unfinished": next_line(),
        "lost": next_line(),
    }

    next_line()  # separator

    # --- D. meta menu ---
    lang["meta"] = {
        "language": next_line(),
        "customizing": next_line(),
        "register": next_line(),
    }

    return lang


from pathlib import Path


def load_game_rules(
    gamename: str,
    language: str,
    lang_dir: Path,
    list_game: list[str],
    lang_vars: dict,
) -> str:
    """
    Port of VB mnuRules_Click.

    Returns rules text for the given game and language.
    If nothing is found, returns an empty string or logo text.
    """

    # --- Build logo (used as fallback) ---
    logo = (
        f"{lang_vars.get('lang_logo1', '')}\n"
        f"{lang_vars.get('lang_logo2', '')}\n"
        f"{lang_vars.get('lang_logo3', '')}\n"
        f"{lang_vars.get('lang_logo4', '')}"
    )

    # --- 1) Try language file ---
    lang_file = lang_dir / f"{language}.txt"
    rules = ""

    try:
        if lang_file.exists():
            with lang_file.open("r", encoding="utf-8") as f:
                lines = iter(f)

                for line in lines:
                    line = line.rstrip("\n")
                    if line == "[GAMENAME]":
                        name = next(lines, "").rstrip("\n")
                        if name == gamename:
                            # collect rules
                            for s in lines:
                                s = s.rstrip("\n")
                                if s.startswith("["):
                                    break
                                rules += s + "\n"
                            break
    except Exception:
        # silent fallback (VB used On Error)
        pass

    if rules.strip():
        return rules.strip()

    # --- 2) Fallback: logo only ---
    if not gamename:
        return logo.strip()

    # --- 3) Fallback: read from ListGame ---
    rules = ""
    for s in list_game:
        if s.startswith("["):
            if rules:
                break
            continue
        rules += s + "\n"

    return rules.strip()


def parse_all_games(lang_dir):
    games_by_id = {}
    games_by_name = {}
    game_names = []

    current_name = None
    buffer = []

    with open(lang_dir / "CardGames-utf8.txt", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")

            if line == "[GAMENAME]":
                if current_name:
                    gid = normalize_game_id(current_name)
                    games_by_id[gid] = {
                        "id": gid,
                        "name": current_name,
                        "definition": buffer,
                    }
                    games_by_name[current_name] = games_by_id[gid]
                    game_names.append(games_by_id[gid])
                current_name = next(f).strip()
                buffer = []
            else:
                buffer.append(line)

        if current_name:
            gid = normalize_game_id(current_name)
            games_by_id[gid] = {
                "id": gid,
                "name": current_name,
                "definition": buffer,
            }
            games_by_name[current_name] = games_by_id[gid]
            game_names.append(games_by_id[gid])

    return games_by_id, games_by_name, game_names
