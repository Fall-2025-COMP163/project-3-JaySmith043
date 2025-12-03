"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Completed Implementation

Name: Jadyn Dewitt-Smith

AI Usage:
Portions of logic, structure, and error-handling design were generated
with assistance from ChatGPT. All code was reviewed, tested,
and integrated by me.
"""

import os
from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InvalidSaveDataError,
    CharacterDeadError
)

# ============================================================================
# CHARACTER CREATION
# ============================================================================

VALID_CLASSES = {
    "Warrior": {"health": 120, "strength": 15, "magic": 5},
    "Mage": {"health": 80, "strength": 8, "magic": 20},
    "Rogue": {"health": 90, "strength": 12, "magic": 10},
    "Cleric": {"health": 100, "strength": 10, "magic": 15}
}

REQUIRED_FIELDS = [
    "name", "class", "level", "health", "max_health",
    "strength", "magic", "experience", "gold",
    "inventory", "active_quests", "completed_quests"
]


def create_character(name, character_class):
    """
    Create a new dictionary-based character with stats based on class.
    Raises InvalidCharacterClassError for invalid class.
    """
    character_class = character_class.title().strip()

    if character_class not in VALID_CLASSES:
        raise InvalidCharacterClassError(f"Invalid class: {character_class}")

    base = VALID_CLASSES[character_class]

    character = {
        "name": name.strip(),
        "class": character_class,
        "level": 1,
        "health": base["health"],
        "max_health": base["health"],
        "strength": base["strength"],
        "magic": base["magic"],
        "experience": 0,
        "gold": 100,
        "inventory": [],
        "active_quests": [],
        "completed_quests": []
    }
    return character

# ============================================================================
# SAVE & LOAD SYSTEM
# ============================================================================

def save_character(character, save_directory="data/save_games"):
    """
    Save character data into a structured file.
    Raises PermissionError or IOError naturally.
    """

    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    filename = os.path.join(save_directory, f"{character['name']}_save.txt")

    try:
        with open(filename, "w") as f:
            for key in REQUIRED_FIELDS:
                value = character[key]
                if isinstance(value, list):
                    value = ",".join(value)
                f.write(f"{key.upper()}: {value}\n")
        return True
    except Exception as e:
        raise e


def load_character(character_name, save_directory="data/save_games"):
    """
    Load character file and return character dictionary.
    Raises:
        CharacterNotFoundError
        SaveFileCorruptedError
        InvalidSaveDataError
    """
    filename = os.path.join(save_directory, f"{character_name}_save.txt")

    if not os.path.isfile(filename):
        raise CharacterNotFoundError(f"No save file found for: {character_name}")

    try:
        with open(filename, "r") as f:
            lines = f.readlines()
    except Exception:
        raise SaveFileCorruptedError("Could not read save file")

    character = {}
    try:
        for line in lines:
            if ":" not in line:
                continue
            key, value = line.strip().split(":", 1)
            key = key.lower().strip()
            value = value.strip()

            if key in ["inventory", "active_quests", "completed_quests"]:
                character[key] = value.split(",") if value else []
            elif key in ["level", "health", "max_health", "strength", "magic", "experience", "gold"]:
                character[key] = int(value)
            else:
                character[key] = value
    except Exception:
        raise InvalidSaveDataError("Invalid formatting in save file")

    validate_character_data(character)
    return character


def list_saved_characters(save_directory="data/save_games"):
    """
    Return list of character names (based on filename patterns).
    """
    if not os.path.exists(save_directory):
        return []

    names = []
    for file in os.listdir(save_directory):
        if file.endswith("_save.txt"):
            names.append(file.replace("_save.txt", ""))
    return names


def delete_character(character_name, save_directory="data/save_games"):
    """
    Delete associated save file.
    Raises CharacterNotFoundError if file doesn't exist.
    """
    filename = os.path.join(save_directory, f"{character_name}_save.txt")

    if not os.path.isfile(filename):
        raise CharacterNotFoundError(f"No save file for: {character_name}")

    os.remove(filename)
    return True

# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    """
    Add XP and handle leveling.
    Raises CharacterDeadError if character health is 0.
    """

    if character["health"] <= 0:
        raise CharacterDeadError("Cannot gain XP while dead.")

    character["experience"] += xp_amount

    # Leveling formula
    while character["experience"] >= character["level"] * 100:
        character["experience"] -= character["level"] * 100
        character["level"] += 1

        # Stat increases
        character["max_health"] += 10
        character["strength"] += 2
        character["magic"] += 2
        character["health"] = character["max_health"]



def add_gold(character, amount):
    """
    Modify gold total. Negative = spending.
    Raises ValueError if gold would go below zero.
    """
    new_total = character["gold"] + amount
    if new_total < 0:
        raise ValueError("Not enough gold.")
    character["gold"] = new_total
    return new_total


def heal_character(character, amount):
    """
    Heal but not above max_health.
    Returns actual healed value.
    """
    before = character["health"]
    character["health"] = min(character["max_health"], character["health"] + amount)
    return character["health"] - before


def is_character_dead(character):
    return character["health"] <= 0


def revive_character(character):
    """
    Revive to 50% max health.
    """
    if character["health"] > 0:
        return False

    character["health"] = character["max_health"] // 2
    return True

# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):
    """
    Ensure required fields and correct types exist.
    Raises InvalidSaveDataError if invalid or missing.
    """
    for field in REQUIRED_FIELDS:
        if field not in character:
            raise InvalidSaveDataError(f"Missing field: {field}")

    # Type checking
    ints = ["level", "health", "max_health", "strength", "magic", "experience", "gold"]
    lists = ["inventory", "active_quests", "completed_quests"]

    for key in ints:
        if not isinstance(character[key], int):
            raise InvalidSaveDataError(f"Invalid numeric field: {key}")

    for key in lists:
        if not isinstance(character[key], list):
            raise InvalidSaveDataError(f"Invalid list field: {key}")

    return True


# ============================================================================
# TEST HARNESS
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER SELF-TEST ===")
    hero = create_character("Aiden", "Warrior")
    print(hero)
    save_character(hero)
    loaded = load_character("Aiden")
    print("Loaded:", loaded)
    
# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")
    
    # Test character creation
    # try:
    #     char = create_character("TestHero", "Warrior")
    #     print(f"Created: {char['name']} the {char['class']}")
    #     print(f"Stats: HP={char['health']}, STR={char['strength']}, MAG={char['magic']}")
    # except InvalidCharacterClassError as e:
    #     print(f"Invalid class: {e}")
    
    # Test saving
    # try:
    #     save_character(char)
    #     print("Character saved successfully")
    # except Exception as e:
    #     print(f"Save error: {e}")
    
    # Test loading
    # try:
    #     loaded = load_character("TestHero")
    #     print(f"Loaded: {loaded['name']}")
    # except CharacterNotFoundError:
    #     print("Character not found")
    # except SaveFileCorruptedError:
    #     print("Save file corrupted")

