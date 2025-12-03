"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Completed Implementation

Name: Jadyn Dewitt-Smith

AI Usage:
Parsing logic, format validation, and error-handling structure generated with
assistance from ChatGPT. All data-handling logic reviewed and integrated by me.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

# ============================================================================
# LOAD QUESTS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    """
    Loads quest definitions from file.

    Expected block format:

    QUEST_ID: quest_id_here
    TITLE: Title Here
    DESCRIPTION: Description text...
    REWARD_XP: #
    REWARD_GOLD: #
    REQUIRED_LEVEL: #
    PREREQUISITE: some_quest_id or NONE

    Blank line separates entries.
    Returns dict {quest_id: quest_data}
    """
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Quest file not found: {filename}")

    try:
        with open(filename, "r") as f:
            lines = f.read().strip().split("\n")
    except Exception:
        raise CorruptedDataError("Unable to read quest file.")

    # Break into blocks
    quests = {}
    block = []

    def process_block(block_lines):
        quest = parse_quest_block(block_lines)
        validate_quest_data(quest)
        quests[quest["quest_id"]] = quest

    for line in lines + [""]:
        if line.strip() == "":
            if block:
                process_block(block)
                block = []
        else:
            block.append(line)

    return quests

# ============================================================================
# LOAD ITEMS
# ============================================================================

def load_items(filename="data/items.txt"):
    """
    Loads items from datafile.

    Expected block format:

    ITEM_ID: id_here
    NAME: Display Name
    TYPE: weapon|armor|consumable
    EFFECT: stat:value
    COST: #
    DESCRIPTION: text...

    Returns dict {item_id: item_data}
    """
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Item file not found: {filename}")

    try:
        with open(filename, "r") as f:
            lines = f.read().strip().split("\n")
    except Exception:
        raise CorruptedDataError("Unable to read item file.")

    items = {}
    block = []

    def process_block(block_lines):
        item = parse_item_block(block_lines)
        validate_item_data(item)
        items[item["item_id"]] = item

    for line in lines + [""]:
        if line.strip() == "":
            if block:
                process_block(block)
                block = []
        else:
            block.append(line)

    return items

# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def validate_quest_data(q):
    required = [
        "quest_id", "title", "description", "reward_xp",
        "reward_gold", "required_level", "prerequisite"
    ]

    for key in required:
        if key not in q:
            raise InvalidDataFormatError(f"Missing quest field: {key}")

    # Type checking
    if not isinstance(q["reward_xp"], int):
        raise InvalidDataFormatError("reward_xp must be an integer")
    if not isinstance(q["reward_gold"], int):
        raise InvalidDataFormatError("reward_gold must be an integer")
    if not isinstance(q["required_level"], int):
        raise InvalidDataFormatError("required_level must be an integer")

    return True


def validate_item_data(i):
    required = [
        "item_id", "name", "type", "effect", "cost", "description"
    ]

    for key in required:
        if key not in i:
            raise InvalidDataFormatError(f"Missing item field: {key}")

    if i["type"] not in ["weapon", "armor", "consumable"]:
        raise InvalidDataFormatError("Invalid item type: " + i["type"])

    try:
        int(i["cost"])
    except:
        raise InvalidDataFormatError("Item cost must be integer")

    # EFFECT FORMAT stat:value
    if ":" not in i["effect"]:
        raise InvalidDataFormatError("Invalid item effect format")

    return True

# ============================================================================
# DEFAULT FILE GENERATION
# ============================================================================

def create_default_data_files():
    """
    Creates data directory and generates simple default quests/items
    so game can run even if files are missing.
    """

    if not os.path.exists("data"):
        os.makedirs("data")

    # Default quests
    if not os.path.exists("data/quests.txt"):
        with open("data/quests.txt", "w") as f:
            f.write("""QUEST_ID: first_quest
TITLE: First Steps
DESCRIPTION: Complete your first quest.
REWARD_XP: 50
REWARD_GOLD: 25
REQUIRED_LEVEL: 1
PREREQUISITE: NONE

QUEST_ID: slay_goblin
TITLE: Slay a Goblin
DESCRIPTION: Defeat a goblin in battle.
REWARD_XP: 75
REWARD_GOLD: 40
REQUIRED_LEVEL: 1
PREREQUISITE: first_quest

""")

    # Default items
    if not os.path.exists("data/items.txt"):
        with open("data/items.txt", "w") as f:
            f.write("""ITEM_ID: health_potion
NAME: Health Potion
TYPE: consumable
EFFECT: health:20
COST: 25
DESCRIPTION: Restores 20 HP.

ITEM_ID: iron_sword
NAME: Iron Sword
TYPE: weapon
EFFECT: strength:5
COST: 50
DESCRIPTION: A basic iron sword.

ITEM_ID: leather_armor
NAME: Leather Armor
TYPE: armor
EFFECT: max_health:10
COST: 40
DESCRIPTION: Light armor offering modest protection.

""")

# ============================================================================
# PARSING BLOCKS
# ============================================================================

def parse_quest_block(lines):
    """
    Parse quest block into dictionary.
    Raises InvalidDataFormatError on formatting issues.
    """
    quest = {}

    try:
        for line in lines:
            if ":" not in line:
                raise InvalidDataFormatError("Invalid quest line: " + line)

            key, value = line.split(":", 1)
            key = key.strip().lower()
            value = value.strip()

            if key == "quest_id":
                quest["quest_id"] = value
            elif key == "title":
                quest["title"] = value
            elif key == "description":
                quest["description"] = value
            elif key == "reward_xp":
                quest["reward_xp"] = int(value)
            elif key == "reward_gold":
                quest["reward_gold"] = int(value)
            elif key == "required_level":
                quest["required_level"] = int(value)
            elif key == "prerequisite":
                quest["prerequisite"] = value
            else:
                raise InvalidDataFormatError("Unknown quest key: " + key)

        return quest
    except Exception as e:
        raise InvalidDataFormatError(f"Quest parsing failed: {e}")


def parse_item_block(lines):
    """
    Parse item block into dictionary.
    Raises InvalidDataFormatError on formatting issues.
    """
    item = {}

    try:
        for line in lines:
            if ":" not in line:
                raise InvalidDataFormatError("Invalid item line: " + line)

            key, value = line.split(":", 1)
            key = key.strip().lower()
            value = value.strip()

            if key == "item_id":
                item["item_id"] = value
            elif key == "name":
                item["name"] = value
            elif key == "type":
                item["type"] = value
            elif key == "effect":
                item["effect"] = value
            elif key == "cost":
                item["cost"] = int(value)
            elif key == "description":
                item["description"] = value
            else:
                raise InvalidDataFormatError("Unknown item key: " + key)

        return item
    except Exception as e:
        raise InvalidDataFormatError(f"Item parsing failed: {e}")

# ============================================================================
# SELF-TEST
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA SELF TEST ===")
    create_default_data_files()

    quests = load_quests()
    print("Loaded quests:", quests)

    items = load_items()
    print("Loaded items:", items)

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")
    
    # Test creating default files
    # create_default_data_files()
    
    # Test loading quests
    # try:
    #     quests = load_quests()
    #     print(f"Loaded {len(quests)} quests")
    # except MissingDataFileError:
    #     print("Quest file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid quest format: {e}")
    
    # Test loading items
    # try:
    #     items = load_items()
    #     print(f"Loaded {len(items)} items")
    # except MissingDataFileError:
    #     print("Item file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid item format: {e}")

