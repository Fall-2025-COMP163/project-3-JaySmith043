"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: Jadyn DeWitt-Smith

AI Usage: ChatGPT was used to help design and implement the character
          creation, save/load logic, and character operations. I reviewed
          and understand all functions and exception usage.

This module handles character creation, loading, and saving.
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
# CHARACTER MANAGEMENT FUNCTIONS
# ============================================================================

def create_character(name, character_class):
    """
    Create a new character with stats based on class
    
    Valid classes: Warrior, Mage, Rogue, Cleric
    
    Returns: Dictionary with character data including:
            - name, class, level, health, max_health, strength, magic
            - experience, gold, inventory, active_quests, completed_quests
    
    Raises: InvalidCharacterClassError if class is not valid
    """
    valid_classes = ["Warrior", "Mage", "Rogue", "Cleric"]

    if not isinstance(character_class, str):
        raise InvalidCharacterClassError("Character class must be a string.")

    character_class = character_class.strip().title()
    if character_class not in valid_classes:
        raise InvalidCharacterClassError("Invalid class: " + character_class)

    # Base stats
    if character_class == "Warrior":
        health = 120
        strength = 15
        magic = 5
    elif character_class == "Mage":
        health = 80
        strength = 8
        magic = 20
    elif character_class == "Rogue":
        health = 90
        strength = 12
        magic = 10
    else:  # Cleric
        health = 100
        strength = 10
        magic = 15

    character = {
        "name": name,
        "class": character_class,
        "level": 1,
        "health": health,
        "max_health": health,
        "strength": strength,
        "magic": magic,
        "experience": 0,
        "gold": 100,
        "inventory": [],
        "active_quests": [],
        "completed_quests": []
    }

    return character

def _get_save_path(character_name, save_directory):
    filename = character_name + "_save.txt"
    return os.path.join(save_directory, filename)

def save_character(character, save_directory="data/save_games"):
    """
    Save character to file
    
    Filename format: {character_name}_save.txt
    
    File format:
    NAME: character_name
    CLASS: class_name
    LEVEL: 1
    HEALTH: 120
    MAX_HEALTH: 120
    STRENGTH: 15
    MAGIC: 5
    EXPERIENCE: 0
    GOLD: 100
    INVENTORY: item1,item2,item3
    ACTIVE_QUESTS: quest1,quest2
    COMPLETED_QUESTS: quest1,quest2
    
    Returns: True if successful
    Raises: PermissionError, IOError (let them propagate or handle)
    """
    if not os.path.isdir(save_directory):
        os.makedirs(save_directory, exist_ok=True)

    path = _get_save_path(character["name"], save_directory)

    # Lists -> comma-separated strings
    inventory_str = ",".join(character.get("inventory", []))
    active_str = ",".join(character.get("active_quests", []))
    completed_str = ",".join(character.get("completed_quests", []))

    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write("NAME: " + str(character.get("name", "")) + "\n")
            f.write("CLASS: " + str(character.get("class", "")) + "\n")
            f.write("LEVEL: " + str(character.get("level", 1)) + "\n")
            f.write("HEALTH: " + str(character.get("health", 0)) + "\n")
            f.write("MAX_HEALTH: " + str(character.get("max_health", 0)) + "\n")
            f.write("STRENGTH: " + str(character.get("strength", 0)) + "\n")
            f.write("MAGIC: " + str(character.get("magic", 0)) + "\n")
            f.write("EXPERIENCE: " + str(character.get("experience", 0)) + "\n")
            f.write("GOLD: " + str(character.get("gold", 0)) + "\n")
            f.write("INVENTORY: " + inventory_str + "\n")
            f.write("ACTIVE_QUESTS: " + active_str + "\n")
            f.write("COMPLETED_QUESTS: " + completed_str + "\n")
    except (PermissionError, OSError) as e:
        # Let these bubble up as the docstring says
        raise e

    return True

def load_character(character_name, save_directory="data/save_games"):
    """
    Load character from save file
    
    Args:
        character_name: Name of character to load
        save_directory: Directory containing save files
    
    Returns: Character dictionary
    Raises: 
        CharacterNotFoundError if save file doesn't exist
        SaveFileCorruptedError if file exists but can't be read
        InvalidSaveDataError if data format is wrong
    """
    path = _get_save_path(character_name, save_directory)

    if not os.path.isfile(path):
        raise CharacterNotFoundError("Character not found: " + character_name)

    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except OSError:
        raise SaveFileCorruptedError("Could not read save file for " + character_name)

    data = {}
    for line in lines:
        line = line.strip()
        if line == "":
            continue
        if ": " not in line:
            raise InvalidSaveDataError("Invalid line: " + line)
        key, value = line.split(": ", 1)
        data[key.strip()] = value.strip()

    # Build character dict
    required_keys = [
        "NAME", "CLASS", "LEVEL", "HEALTH", "MAX_HEALTH",
        "STRENGTH", "MAGIC", "EXPERIENCE", "GOLD",
        "INVENTORY", "ACTIVE_QUESTS", "COMPLETED_QUESTS"
    ]
    for k in required_keys:
        if k not in data:
            raise InvalidSaveDataError("Missing field: " + k)

    try:
        character = {
            "name": data["NAME"],
            "class": data["CLASS"],
            "level": int(data["LEVEL"]),
            "health": int(data["HEALTH"]),
            "max_health": int(data["MAX_HEALTH"]),
            "strength": int(data["STRENGTH"]),
            "magic": int(data["MAGIC"]),
            "experience": int(data["EXPERIENCE"]),
            "gold": int(data["GOLD"]),
            "inventory": [],
            "active_quests": [],
            "completed_quests": []
        }
    except ValueError:
        raise InvalidSaveDataError("Numeric fields could not be parsed.")

    # Parse lists
    inv_str = data.get("INVENTORY", "")
    if inv_str.strip() == "":
        character["inventory"] = []
    else:
        character["inventory"] = [x for x in inv_str.split(",") if x != ""]

    active_str = data.get("ACTIVE_QUESTS", "")
    if active_str.strip() == "":
        character["active_quests"] = []
    else:
        character["active_quests"] = [x for x in active_str.split(",") if x != ""]

    completed_str = data.get("COMPLETED_QUESTS", "")
    if completed_str.strip() == "":
        character["completed_quests"] = []
    else:
        character["completed_quests"] = [x for x in completed_str.split(",") if x != ""]

    # Final validation
    validate_character_data(character)

    return character

def list_saved_characters(save_directory="data/save_games"):
    """
    Get list of all saved character names
    
    Returns: List of character names (without _save.txt extension)
    """
    names = []

    if not os.path.isdir(save_directory):
        return names

    for filename in os.listdir(save_directory):
        if filename.endswith("_save.txt"):
            base = filename[:-9]  # strip "_save.txt"
            names.append(base)

    return names

def delete_character(character_name, save_directory="data/save_games"):
    """
    Delete a character's save file
    
    Returns: True if deleted successfully
    Raises: CharacterNotFoundError if character doesn't exist
    """
    path = _get_save_path(character_name, save_directory)

    if not os.path.isfile(path):
        raise CharacterNotFoundError("Character not found: " + character_name)

    os.remove(path)
    return True

# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    """
    Add experience to character and handle level ups
    
    Level up formula: level_up_xp = current_level * 100
    Example when leveling up:
    - Increase level by 1
    - Increase max_health by 10
    - Increase strength by 2
    - Increase magic by 2
    - Restore health to max_health
    
    Raises: CharacterDeadError if character health is 0
    """
    if is_character_dead(character):
        raise CharacterDeadError("Cannot gain experience when dead.")

    if xp_amount < 0:
        xp_amount = 0

    character["experience"] = character["experience"] + xp_amount

    # Level up loop
    leveled_up = True
    while leveled_up:
        leveled_up = False
        current_level = character["level"]
        required_xp = current_level * 100
        if character["experience"] >= required_xp:
            character["level"] = character["level"] + 1
            character["max_health"] = character["max_health"] + 10
            character["strength"] = character["strength"] + 2
            character["magic"] = character["magic"] + 2
            character["health"] = character["max_health"]
            leveled_up = True

def add_gold(character, amount):
    """
    Add gold to character's inventory
    
    Args:
        character: Character dictionary
        amount: Amount of gold to add (can be negative for spending)
    
    Returns: New gold total
    Raises: ValueError if result would be negative
    """
    current = character.get("gold", 0)
    new_total = current + amount
    if new_total < 0:
        raise ValueError("Gold cannot be negative.")
    character["gold"] = new_total
    return new_total

def heal_character(character, amount):
    """
    Heal character by specified amount
    
    Health cannot exceed max_health
    
    Returns: Actual amount healed
    """
    if amount < 0:
        amount = 0

    max_hp = character["max_health"]
    current_hp = character["health"]

    heal_amount = max_hp - current_hp
    if heal_amount <= 0:
        return 0

    if amount < heal_amount:
        heal_amount = amount

    character["health"] = current_hp + heal_amount
    return heal_amount

def is_character_dead(character):
    """
    Check if character's health is 0 or below
    
    Returns: True if dead, False if alive
    """
    return character.get("health", 0) <= 0

def revive_character(character):
    """
    Revive a dead character with 50% health
    
    Returns: True if revived
    """
    if not is_character_dead(character):
        return False

    max_hp = character.get("max_health", 0)
    half_hp = max_hp // 2
    if half_hp <= 0 and max_hp > 0:
        half_hp = 1
    character["health"] = half_hp
    return True

# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):
    """
    Validate that character dictionary has all required fields
    
    Required fields: name, class, level, health, max_health, 
                    strength, magic, experience, gold, inventory,
                    active_quests, completed_quests
    
    Returns: True if valid
    Raises: InvalidSaveDataError if missing fields or invalid types
    """
    required = [
        "name", "class", "level", "health", "max_health",
        "strength", "magic", "experience", "gold",
        "inventory", "active_quests", "completed_quests"
    ]

    for key in required:
        if key not in character:
            raise InvalidSaveDataError("Missing field: " + key)

    # Type checks
    numeric_keys = ["level", "health", "max_health",
                    "strength", "magic", "experience", "gold"]
    for key in numeric_keys:
        value = character[key]
        if not isinstance(value, int):
            raise InvalidSaveDataError("Field must be int: " + key)

    list_keys = ["inventory", "active_quests", "completed_quests"]
    for key in list_keys:
        if not isinstance(character[key], list):
            raise InvalidSaveDataError("Field must be list: " + key)

    return True
    
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

