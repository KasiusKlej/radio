# ============================================================================
# CLOVEK (LUDO) - Language Labels
# ============================================================================
# Hardcoded translations for Slovenian and English
# ============================================================================

from enum import Enum
from typing import Dict

class Language(Enum):
    SLOVENIAN = "slo"
    ENGLISH = "eng"

# ============================================================================
# MENU LABELS
# ============================================================================

LABELS = {
    # Game title
    "game_title": {
        Language.SLOVENIAN: "Človek ne jezi se",
        Language.ENGLISH: "Game of Ludo"
    },
    
    # Main menu items
    "game": {
        Language.SLOVENIAN: "Igra",
        Language.ENGLISH: "Game"
    },
    "new": {
        Language.SLOVENIAN: "Nova",
        Language.ENGLISH: "New"
    },
    "end": {
        Language.SLOVENIAN: "Konec",
        Language.ENGLISH: "End"
    },
    "options": {
        Language.SLOVENIAN: "Opcije",
        Language.ENGLISH: "Options"
    },
    "fast": {
        Language.SLOVENIAN: "Hitro",
        Language.ENGLISH: "Fast"
    },
    "sound": {
        Language.SLOVENIAN: "Zvok",
        Language.ENGLISH: "Sound"
    },
    "save_result": {
        Language.SLOVENIAN: "Shrani rezultat",
        Language.ENGLISH: "Save the Result"
    },
    "statistics": {
        Language.SLOVENIAN: "Statistika",
        Language.ENGLISH: "Statistics"
    },
    
    # Opponent settings
    "opponent": {
        Language.SLOVENIAN: "Nasprotnik",
        Language.ENGLISH: "Opponent"
    },
    "computer": {
        Language.SLOVENIAN: "Računalnik",
        Language.ENGLISH: "Computer"
    },
    "bad": {
        Language.SLOVENIAN: "Slab",
        Language.ENGLISH: "Bad"
    },
    "good": {
        Language.SLOVENIAN: "Dober",
        Language.ENGLISH: "Good"
    },
    "very_good": {
        Language.SLOVENIAN: "Zelo dober",
        Language.ENGLISH: "Very Good"
    },
    "human": {
        Language.SLOVENIAN: "Človek",
        Language.ENGLISH: "Human"
    },
    "network": {
        Language.SLOVENIAN: "Omrežje",
        Language.ENGLISH: "Network"
    },
    
    # Language settings
    "language": {
        Language.SLOVENIAN: "Jezik",
        Language.ENGLISH: "Language"
    },
    "slovene": {
        Language.SLOVENIAN: "Slovensko",
        Language.ENGLISH: "Slovene"
    },
    "english": {
        Language.SLOVENIAN: "Angleško",
        Language.ENGLISH: "English"
    },
    
    # Board
    "board": {
        Language.SLOVENIAN: "Tabla",
        Language.ENGLISH: "Board"
    }
}

# ============================================================================
# STATISTICS LABELS (9 items for player stats)
# ============================================================================

STATISTICS_LABELS = {
    "statistics": {
        Language.SLOVENIAN: "Statistika",
        Language.ENGLISH: "Statistics"
    },
    "points": {
        Language.SLOVENIAN: "Točke",
        Language.ENGLISH: "Points"
    },
    "dice_average": {
        Language.SLOVENIAN: "Povprečen met",
        Language.ENGLISH: "Dice Average"
    },
    "number_of_rolls": {
        Language.SLOVENIAN: "Število metov",
        Language.ENGLISH: "Number of Rolls"
    },
    "number_of_steps": {
        Language.SLOVENIAN: "Število korakov",
        Language.ENGLISH: "Number of Steps"
    },
    "pit_starts": {
        Language.SLOVENIAN: "Ven iz hiške",
        Language.ENGLISH: "Pit Starts"
    },
    "kills": {
        Language.SLOVENIAN: "Zbitki",
        Language.ENGLISH: "Kills"
    },
    "deaths": {
        Language.SLOVENIAN: "Smrti",
        Language.ENGLISH: "Deaths"
    },
    "time": {
        Language.SLOVENIAN: "Čas",
        Language.ENGLISH: "Time"
    }
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_label(key: str, language: Language = Language.SLOVENIAN) -> str:
    """
    Get a menu label in the specified language.
    
    Args:
        key: Label key (e.g., "game_title", "new", "opponent")
        language: Target language (default: Slovenian)
    
    Returns:
        Translated label string
    """
    if key in LABELS:
        return LABELS[key].get(language, LABELS[key][Language.ENGLISH])
    return key  # Return key itself if not found


def get_stat_label(key: str, language: Language = Language.SLOVENIAN) -> str:
    """
    Get a statistics label in the specified language.
    
    Args:
        key: Statistics label key (e.g., "points", "kills")
        language: Target language (default: Slovenian)
    
    Returns:
        Translated statistics label string
    """
    if key in STATISTICS_LABELS:
        return STATISTICS_LABELS[key].get(language, STATISTICS_LABELS[key][Language.ENGLISH])
    return key


def get_all_labels(language: Language = Language.SLOVENIAN) -> Dict[str, str]:
    """
    Get all labels (menu + statistics) in specified language.
    
    Args:
        language: Target language (default: Slovenian)
    
    Returns:
        Dictionary of all labels
    """
    result = {}
    
    # Add menu labels
    for key, translations in LABELS.items():
        result[key] = translations.get(language, translations[Language.ENGLISH])
    
    # Add statistics labels
    for key, translations in STATISTICS_LABELS.items():
        if key not in result:  # Avoid duplicate "statistics" key
            result[key] = translations.get(language, translations[Language.ENGLISH])
    
    return result


def set_language(lang_code: str) -> Language:
    """
    Convert language code string to Language enum.
    
    Args:
        lang_code: "slo" or "eng"
    
    Returns:
        Language enum
    """
    if lang_code.lower() in ["slo", "slovenian", "slovene"]:
        return Language.SLOVENIAN
    return Language.ENGLISH


# ============================================================================
# COMPLETE LABELS DICTIONARY (for easy access)
# ============================================================================

ALL_LABELS = {
    Language.SLOVENIAN: {
        # Menu
        "game_title": "Človek ne jezi se",
        "game": "Igra",
        "new": "Nova",
        "end": "Konec",
        "options": "Opcije",
        "fast": "Hitro",
        "sound": "Zvok",
        "save_result": "Shrani rezultat",
        "statistics": "Statistika",
        "opponent": "Nasprotnik",
        "bad": "Slab",
        "good": "Dober",
        "very_good": "Zelo dober",
        "human": "Človek",
        "network": "Omrežje",
        "language": "Jezik",
        "slovene": "Slovensko",
        "english": "Angleško",
        "board": "Tabla",
        
        # Statistics
        "points": "Točke",
        "dice_average": "Povprečen met",
        "number_of_rolls": "Število metov",
        "number_of_steps": "Število korakov",
        "pit_starts": "Ven iz hiške",
        "kills": "Zbitki",
        "deaths": "Smrti",
        "time": "Čas"
    },
    
    Language.ENGLISH: {
        # Menu
        "game_title": "Game of Ludo",
        "game": "Game",
        "new": "New",
        "end": "End",
        "options": "Options",
        "fast": "Fast",
        "sound": "Sound",
        "save_result": "Save the Result",
        "statistics": "Statistics",
        "opponent": "Opponent",
        "bad": "Bad",
        "good": "Good",
        "very_good": "Very Good",
        "human": "Human",
        "network": "Network",
        "language": "Language",
        "slovene": "Slovene",
        "english": "English",
        "board": "Board",
        
        # Statistics
        "points": "Points",
        "dice_average": "Dice Average",
        "number_of_rolls": "Number of Rolls",
        "number_of_steps": "Number of Steps",
        "pit_starts": "Pit Starts",
        "kills": "Kills",
        "deaths": "Deaths",
        "time": "Time"
    }
}


# # ============================================================================
# # EXAMPLE USAGE
# # ============================================================================

# if __name__ == "__main__":
#     # Example 1: Get individual labels
#     print("=== Individual Labels ===")
#     print(f"Game Title (SLO): {get_label('game_title', Language.SLOVENIAN)}")
#     print(f"Game Title (ENG): {get_label('game_title', Language.ENGLISH)}")
#     print(f"Opponent (SLO): {get_label('opponent', Language.SLOVENIAN)}")
#     print(f"Opponent (ENG): {get_label('opponent', Language.ENGLISH)}")
    
#     # Example 2: Get statistics labels
#     print("\n=== Statistics Labels ===")
#     print(f"Points (SLO): {get_stat_label('points', Language.SLOVENIAN)}")
#     print(f"Points (ENG): {get_stat_label('points', Language.ENGLISH)}")
#     print(f"Kills (SLO): {get_stat_label('kills', Language.SLOVENIAN)}")
#     print(f"Kills (ENG): {get_stat_label('kills', Language.ENGLISH)}")
    
#     # Example 3: Get all labels at once
#     print("\n=== All Slovenian Labels ===")
#     slo_labels = get_all_labels(Language.SLOVENIAN)
#     for key in ["game_title", "new", "opponent", "points", "kills"]:
#         print(f"{key}: {slo_labels[key]}")
    
#     print("\n=== All English Labels ===")
#     eng_labels = get_all_labels(Language.ENGLISH)
#     for key in ["game_title", "new", "opponent", "points", "kills"]:
#         print(f"{key}: {eng_labels[key]}")
    
#     # Example 4: Language code conversion
#     print("\n=== Language Code Conversion ===")
#     lang1 = set_language("slo")
#     lang2 = set_language("eng")
#     print(f"'slo' → {lang1.value}")
#     print(f"'eng' → {lang2.value}")
    
#     # Example 5: Using ALL_LABELS dictionary directly
#     print("\n=== Direct Dictionary Access ===")
#     print(f"Slovenian 'very_good': {ALL_LABELS[Language.SLOVENIAN]['very_good']}")
#     print(f"English 'very_good': {ALL_LABELS[Language.ENGLISH]['very_good']}")
    
#     # Example 6: Menu categories
#     print("\n=== Menu Categories ===")
#     menu_items = ["game", "new", "end", "options", "statistics"]
#     opponent_items = ["opponent", "bad", "good", "very_good", "human", "network"]
    
#     print("Menu (Slovenian):")
#     for item in menu_items:
#         print(f"  - {get_label(item, Language.SLOVENIAN)}")
    
#     print("\nOpponent Options (English):")
#     for item in opponent_items:
#         print(f"  - {get_label(item, Language.ENGLISH)}")
    
#     # Example 7: Statistics display
#     print("\n=== Statistics Display ===")
#     stats_keys = ["points", "dice_average", "number_of_rolls", "kills", "deaths", "time"]
    
#     print("Player Statistics (Slovenian):")
#     for key in stats_keys:
#         print(f"  {get_stat_label(key, Language.SLOVENIAN)}: 0")
    
#     print("\nPlayer Statistics (English):")
#     for key in stats_keys:
#         print(f"  {get_stat_label(key, Language.ENGLISH)}: 0")
        
