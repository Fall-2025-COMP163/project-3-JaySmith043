"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: Jadyn DeWitt-Smith

AI Usage: ChatGPT was used to help implement file parsing, validation,
          and default data creation. I reviewed and understand how the
          data is loaded, validated, and used.

This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    """
    Load quest data from file
    """
    if not os.path.isfile(filename):
        raise MissingDataFileError("Quest file not found: " + filename)

    quests = {}
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except OSError:
        raise CorruptedDataError("Could not read quest file: " + filename)

    block = []
    for raw_line in lines:
        line = raw_line.strip()
        if line == "":
            if len(block) > 0:
                quest = parse_quest_block(block)
                validate_quest_data(quest)
                quests[quest["quest_id"]] = quest
                block = []
        else:
            block.append(line)

    if len(block) > 0:
        quest = parse_quest_block(block)
        validate_quest_data(quest)
        quests[quest["quest_id"]] = quest

    return quests

def load_items(filename="data/items.txt"):
    """
    Load item data from file
    """
    if not os.path.isfile(filename):
        raise MissingDataFileError("Item file not found: " + filename)

    items = {}
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except OSError:
        raise CorruptedDataError("Could not read item file: " + filename)

    block = []
    for raw_line in lines:
        line = raw_line.strip()
        if line == "":
            if len(block) > 0:
                item = parse_item_block(block)
                validate_item_data(item)
                items[item["item_id"]] = item
                block = []
        else:
            block.append(line)

    if len(block) > 0:
        item = parse_item_block(block)
        validate_item_data(item)
        items[item["item_id"]] = item

    return items

def validate_quest_data(quest_dict):
    """
    Validate that quest dictionary has all required fields
    """
    required = [
        "quest_id", "title", "description",
        "reward_xp", "reward_gold", "required_level",
        "prerequisite"
    ]

    for key in required:
        if key not in quest_dict:
            raise InvalidDataFormatError("Missing quest field: " + key)

    # numeric checks
    for key in ["reward_xp", "reward_gold", "required_level"]:
        if not isinstance(quest_dict[key], int):
            raise InvalidDataFormatError("Quest field must be int: " + key)

    return True

def validate_item_data(item_dict):
    """
    Validate that item dictionary has all required fields
    """
    required = ["item_id", "name", "type", "effect", "cost", "description"]
    for key in required:
        if key not in item_dict:
            raise InvalidDataFormatError("Missing item field: " + key)

    valid_types = ["weapon", "armor", "consumable"]
    if item_dict["type"] not in valid_types:
        raise InvalidDataFormatError("Invalid item type: " + item_dict["type"])

    if not isinstance(item_dict["cost"], int):
        raise InvalidDataFormatError("Item cost must be integer.")

    return True

def create_default_data_files():
    """
    Create default data files if they don't exist
    """
    data_dir = "data"
    if not os.path.isdir(data_dir):
        os.makedirs(data_dir, exist_ok=True)

    quests_path = os.path.join(data_dir, "quests.txt")
    items_path = os.path.join(data_dir, "items.txt")

    if not os.path.isfile(quests_path):
        with open(quests_path, "w", encoding="utf-8") as f:
            f.write(
                "QUEST_ID: first_quest\n"
                "TITLE: First Steps\n"
                "DESCRIPTION: Complete your first quest.\n"
                "REWARD_XP: 50\n"
                "REWARD_GOLD: 25\n"
                "REQUIRED_LEVEL: 1\n"
                "PREREQUISITE: NONE\n\n"
            )

    if not os.path.isfile(items_path):
        with open(items_path, "w", encoding="utf-8") as f:
            f.write(
                "ITEM_ID: health_potion\n"
                "NAME: Health Potion\n"
                "TYPE: consumable\n"
                "EFFECT: health:20\n"
                "COST: 25\n"
                "DESCRIPTION: Restores a small amount of health.\n\n"
                "ITEM_ID: iron_sword\n"
                "NAME: Iron Sword\n"
                "TYPE: weapon\n"
                "EFFECT: strength:5\n"
                "COST: 100\n"
                "DESCRIPTION: A basic iron sword.\n\n"
            )

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    """
    Parse a block of lines into a quest dictionary
    """
    quest = {}

    for line in lines:
        if ": " not in line:
            raise InvalidDataFormatError("Invalid quest line: " + line)
        key, value = line.split(": ", 1)
        key = key.strip().upper()
        value = value.strip()

        if key == "QUEST_ID":
            quest["quest_id"] = value
        elif key == "TITLE":
            quest["title"] = value
        elif key == "DESCRIPTION":
            quest["description"] = value
        elif key == "REWARD_XP":
            try:
                quest["reward_xp"] = int(value)
            except ValueError:
                raise InvalidDataFormatError("Invalid REWARD_XP value.")
        elif key == "REWARD_GOLD":
            try:
                quest["reward_gold"] = int(value)
            except ValueError:
                raise InvalidDataFormatError("Invalid REWARD_GOLD value.")
        elif key == "REQUIRED_LEVEL":
            try:
                quest["required_level"] = int(value)
            except ValueError:
                raise InvalidDataFormatError("Invalid REQUIRED_LEVEL value.")
        elif key == "PREREQUISITE":
            quest["prerequisite"] = value

    # Some fields might be missing; validation will catch that
    return quest

def parse_item_block(lines):
    """
    Parse a block of lines into an item dictionary
    """
    item = {}

    for line in lines:
        if ": " not in line:
            raise InvalidDataFormatError("Invalid item line: " + line)
        key, value = line.split(": ", 1)
        key = key.strip().upper()
        value = value.strip()

        if key == "ITEM_ID":
            item["item_id"] = value
        elif key == "NAME":
            item["name"] = value
        elif key == "TYPE":
            item["type"] = value
        elif key == "EFFECT":
            item["effect"] = value
        elif key == "COST":
            try:
                item["cost"] = int(value)
            except ValueError:
                raise InvalidDataFormatError("Invalid COST value.")
        elif key == "DESCRIPTION":
            item["description"] = value

    return item

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

