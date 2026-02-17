import re
from pathlib import Path

#from .model import Column, Card
#from .model import menu_items_slo, menu_items_eng, LANG_DIR



from .model import GameState, orig_card_x_size,orig_card_y_size, gap_x, gap_y, LANG_DIR, menu_items_slo, menu_items_eng

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
# -------------------------------------------------
# Main loader with Twip-to-Pixel Conversion
# -------------------------------------------------
def load_gamesVB(state):
    # Constant for the VB coordinate conversion
    TPX = 15 

    lines = GAMES_FILE.read_text(encoding="utf-8").splitlines()
    games = []
    counter = 1
    i = 0

    while i < len(lines):
        line = lines[i].strip()
        i += 1

        if not line or line.startswith("#") or line != "[GAMENAME]":
            continue

        name = lines[i].strip()
        raw_name = name
        game_id = str(counter)
        counter += 1

        # Localization logic preserved
        if "(" in raw_name and ")" in raw_name:
            eng_name = raw_name.split("(")[0].strip()
            slo_name = raw_name.split("(", 1)[1].rstrip(")").strip()
        else:
            eng_name = raw_name; slo_name = raw_name

        menu_items_eng.append(eng_name)
        menu_items_slo.append(slo_name)

        i += 1
        presets = ColumnPresets()
        kup = []
        raw_lines = ["[GAMENAME]", name]

        while i < len(lines) and lines[i].strip() != "[GAMENAME]":
            raw_lines.append(lines[i].rstrip("\n"))
            i += 1

        # ---- PARSE DEFAULTS (Dividing Twips by 15) ----
        j = 0
        while j < len(raw_lines):
            if raw_lines[j].strip() == "[COLUMNS DEFAULTS]":
                j += 1
                while j < len(raw_lines):
                    s = raw_lines[j].strip()
                    j += 1
                    if s == "[END COLUMNS DEFAULTS]": break
                    
                    if s.startswith("overlap_x="):
                        # Convert Twips to Pixels
                        presets.default_overlap_x = int(s.split("=")[1]) // TPX
                    elif s.startswith("overlap_y="):
                        presets.default_overlap_y = int(s.split("=")[1]) // TPX
                    elif s.startswith("zoom="):
                        presets.zoom = float(s.split("=")[1])
                break
            j += 1

        # ---- PARSE COLUMNS ----
        j = 0
        while j < len(raw_lines) and raw_lines[j].strip() != "[COLUMNS]": j += 1
        if j < len(raw_lines):
            j += 1
            c = 0
            while j < len(raw_lines):
                s = raw_lines[j].strip()
                j += 1
                if s == "[END COLUMNS]": break
                parts = [p.strip() for p in s.split(",")]
                # Position (parts[1]) and num_cards (parts[2]) are indices/counts, not twips.
                col = new_column(c, parts[0], parts[1][:2], parts[2], parts[-1])
                kup.append(col)
                c += 1

        # ---- PARSE BEHAVIOUR (Dividing Twips by 15) ----
        j = 0
        current_col = None
        while j < len(raw_lines):
            if raw_lines[j].strip() == "[COLUMNS BEHAVIOUR]":
                j += 1
                while j < len(raw_lines):
                    s = raw_lines[j].strip()
                    j += 1
                    if s == "[END COLUMNS BEHAVIOUR]": break
                    if s.startswith("[") and s.endswith("]"):
                        col_name = s[1:-1]
                        current_col = next((c for c in kup if c.column_name == col_name), None)
                    elif current_col and "=" in s:
                        key, val = s.split("=", 1)
                        val = val.strip()
                        
                        # Apply conversion logic
                        if key == "overlap_x":
                            current_col.overlap_x = presets.default_overlap_x if val == "default" else int(val) // TPX
                        elif key == "overlap_y":
                            current_col.overlap_y = presets.default_overlap_y if val == "default" else int(val) // TPX
                        elif key == "custom_x":
                            # Note: if val is -1, -1 // 15 is still -1 in Python, which is perfect.
                            current_col.custom_x = int(val) // TPX
                        elif key == "custom_y":
                            current_col.custom_y = int(val) // TPX
                        elif key == "cards_face_up":
                            current_col.cards_face_up = val
                break
            j += 1

        games.append({
            "id": game_id,
            "name": name,
            "kup": kup,
            "presets": presets,
            "raw_lines": raw_lines,
        })

    return games


def load_games2():
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


# returns game's id and name (required for games menu)
# def load_game_names():
#     """
#     Extract game IDs and display names for menu only using numeric IDs.
#     """
#     lines = load_games2()

#     games = []
#     counter = 1
#     i = 0
#     while i < len(lines):
#         if lines[i] == "[GAMENAME]":
#             name = lines[i + 1].strip()
#             # Assign numeric ID as string for URL consistency
#             game_id = str(counter)
            
#             games.append({
#                 "id": game_id,
#                 "name": name
#             })
#             counter += 1
#             i += 2
#         else:
#             i += 1

#     return games
def load_game_names(lang_code="eng"):
    """
    Extracts localized game names. 
    Expects format: "English Name (Localized Name)"
    """
    lines = load_games2() # Assuming this loads your list of lines
    games = []
    counter = 1
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line == "[GAMENAME]":
            # The name is the very next line
            raw_name = lines[i + 1].strip()
            
            display_name = raw_name
            if "(" in raw_name and ")" in raw_name:
                # Split at the first '('
                parts = raw_name.split("(", 1)
                eng_name = parts[0].strip()
                # Get the content between '(' and ')'
                local_name = parts[1].split(")", 1)[0].strip()
                
                # If the current language is NOT english, show the local part
                display_name = local_name if lang_code != "eng" else eng_name
            
            games.append({
                "id": str(counter),
                "name": display_name
            })
            counter += 1
            i += 2
        else:
            i += 1
    return games



def language_parser(lang_dir: Path, filename: str) -> dict:
    """
    Parse a VB-style language file into structured data and strip '&' mnemonics.
    """

    if not filename.lower().endswith(".txt"):
        filename += ".txt"

    path = lang_dir / filename
    if not path.exists():
        raise FileNotFoundError(f"Language file not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        # Read all lines and strip trailing whitespace/newlines
        lines = [line.rstrip("\n") for line in f]

    idx = 0

    def next_line():
        """Helper to get next line, remove VB '&' shortcuts, and handle EOF."""
        nonlocal idx
        if idx >= len(lines):
            return "" # Return empty string if we reach end of file unexpectedly
        
        val = lines[idx]
        idx += 1
        
        # ---------------------------------------------------------
        # THE FIX: Strip the '&' artefact.
        # We replace "&&" with a temporary marker if we wanted to preserve 
        # literal ampersands, but for a standard port, simply removing 
        # single '&' is the best approach for clean web menus.
        # ---------------------------------------------------------
        return val.replace("&", "")

    lang = {}

    # --- A. Core language strings ---
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

    next_line()  # skip separator

    # --- B. Menu captions (The ones that showed &Help) ---
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

    next_line()  # skip separator

    # --- C. Dialog buttons ---
    lang["dialog"] = {
        "ok": next_line(),
        "cancel": next_line(),
    }

    next_line()  # skip separator

    lang["statistics"] = {
        "ok": next_line(),
        "legend": next_line(),
        "won": next_line(),
        "unfinished": next_line(),
        "lost": next_line(),
    }

    next_line()  # skip separator

    # --- D. Meta menu (Language, Register, etc.) ---
    lang["meta"] = {
        "language": next_line(),
        "customizing": next_line(),
        "register": next_line(),
    }

    return lang





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
    counter = 1

    current_name = None
    buffer = []

    with open(lang_dir / "CardGames-utf8.txt", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")

            if line == "[GAMENAME]":
                if current_name:
                    gid = str(counter)
                    games_by_id[gid] = {
                        "id": gid,
                        "name": current_name,
                        "definition": buffer,
                    }
                    games_by_name[current_name] = games_by_id[gid]
                    game_names.append(games_by_id[gid])
                    counter += 1
                
                current_name = next(f).strip()
                buffer = []
            else:
                buffer.append(line)

        # Handle the last game in the file
        if current_name:
            gid = str(counter)
            games_by_id[gid] = {
                "id": gid,
                "name": current_name,
                "definition": buffer,
            }
            games_by_name[current_name] = games_by_id[gid]
            game_names.append(games_by_id[gid])

    return games_by_id, games_by_name, game_names



def read_gamenames_from_language_files(language: str, lang_dir: Path) -> list[dict]:
    """
    Returns a list of game dictionaries with localized names.
    
    Args:
        language: Language code (e.g., "eng", "slo", "ger")
        lang_dir: Path to the directory containing language files
    
    Returns:
        List of dicts: [{"id": "1", "name": "Klondike"}, ...]
        The order matches the game order in CardGames-utf8.txt.
    
    Implementation notes:
        1. Try to read from {language}.txt first (e.g., eng.txt)
        2. If not found, fall back to reading from CardGames-utf8.txt
        3. Always preserve game order and IDs (1, 2, 3... matching file order)
    """
    
    # --- STEP 1: Try language-specific file ---
    lang_file = lang_dir / f"{language}.txt"
    
    if lang_file.exists():
        try:
            games = _extract_names_from_language_file(lang_file)
            if games:  # If we got names, return them
                return games
        except Exception as e:
            print(f"Warning: Failed to parse {lang_file}: {e}")
            # Fall through to fallback
    
    # --- STEP 2: Fallback to CardGames-utf8.txt ---
    default_file = lang_dir / "CardGames-utf8.txt"
    if default_file.exists():
        try:
            return _extract_names_from_game_definitions(default_file, language)
        except Exception as e:
            print(f"Error: Failed to parse {default_file}: {e}")
            return []
    
    return []


def _extract_names_from_language_file(filepath: Path) -> list[dict]:
    """
    Extract game names from a language file (eng.txt, slo.txt, etc.).
    
    Format:
        [GAMENAME]
        Game Name Here
        rules text...
        
        [GAMENAME]
        Next Game Name
        more rules...
    """
    games = []
    game_id = 1
    
    with filepath.open("r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if line == "[GAMENAME]":
            # Next line is the game name
            if i + 1 < len(lines):
                name = lines[i + 1].strip()
                games.append({
                    "id": str(game_id),
                    "name": name
                })
                game_id += 1
            i += 2  # Skip [GAMENAME] and the name line
        else:
            i += 1
    
    return games


def _extract_names_from_game_definitions(filepath: Path, language: str) -> list[dict]:
    """
    Extract game names from CardGames-utf8.txt.
    
    Format in CardGames-utf8.txt:
        [GAMENAME]
        English Name (Localized Name)
        ...
        
        [GAMENAME]
        Next Game (Naslednja Igra)
        ...
    
    The names follow the pattern: "English Name (Local Name)"
    We extract the appropriate part based on the language.
    """
    games = []
    game_id = 1
    
    with filepath.open("r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if line == "[GAMENAME]":
            if i + 1 < len(lines):
                raw_name = lines[i + 1].strip()
                
                # Parse "English (Local)" format
                display_name = raw_name
                if "(" in raw_name and ")" in raw_name:
                    parts = raw_name.split("(", 1)
                    eng_name = parts[0].strip()
                    local_name = parts[1].split(")", 1)[0].strip()
                    
                    # Choose which part to show based on language
                    display_name = eng_name if language == "eng" else local_name
                
                games.append({
                    "id": str(game_id),
                    "name": display_name
                })
                game_id += 1
            
            i += 2
        else:
            i += 1
    
    return games