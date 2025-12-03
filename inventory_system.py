"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module - Starter Code

Name: Jadyn DeWitt-Smith

AI Usage: ChatGPT helped implement inventory operations, item usage,
          equipment logic, and shop behavior. I verified all control
          flow and exception cases.

This module handles inventory management, item usage, and equipment.
"""

from custom_exceptions import (
    InventoryFullError,
    ItemNotFoundError,
    InsufficientResourcesError,
    InvalidItemTypeError
)

# Maximum inventory size
MAX_INVENTORY_SIZE = 20

# ============================================================================
# INVENTORY MANAGEMENT
# ============================================================================

def add_item_to_inventory(character, item_id):
    """
    Add an item to character's inventory
    """
    if "inventory" not in character:
        character["inventory"] = []

    if len(character["inventory"]) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full.")

    character["inventory"].append(item_id)
    return True

def remove_item_from_inventory(character, item_id):
    """
    Remove an item from character's inventory
    """
    if "inventory" not in character:
        character["inventory"] = []

    if item_id not in character["inventory"]:
        raise ItemNotFoundError("Item not in inventory: " + str(item_id))

    character["inventory"].remove(item_id)
    return True

def has_item(character, item_id):
    """
    Check if character has a specific item
    """
    if "inventory" not in character:
        character["inventory"] = []
    return item_id in character["inventory"]

def count_item(character, item_id):
    """
    Count how many of a specific item the character has
    """
    if "inventory" not in character:
        character["inventory"] = []
    return character["inventory"].count(item_id)

def get_inventory_space_remaining(character):
    """
    Calculate how many more items can fit in inventory
    """
    if "inventory" not in character:
        character["inventory"] = []
    return MAX_INVENTORY_SIZE - len(character["inventory"])

def clear_inventory(character):
    """
    Remove all items from inventory
    """
    if "inventory" not in character:
        character["inventory"] = []
    removed = character["inventory"][:]
    character["inventory"] = []
    return removed

# ============================================================================
# ITEM USAGE
# ============================================================================

def use_item(character, item_id, item_data):
    """
    Use a consumable item from inventory
    """
    if not has_item(character, item_id):
        raise ItemNotFoundError("Item not in inventory: " + str(item_id))

    if item_data.get("type") != "consumable":
        raise InvalidItemTypeError("Item is not consumable.")

    effect_string = item_data.get("effect", "")
    stat_name, value = parse_item_effect(effect_string)
    apply_stat_effect(character, stat_name, value)

    # Remove one instance
    remove_item_from_inventory(character, item_id)

    return "Used " + item_data.get("name", item_id) + "."

def equip_weapon(character, item_id, item_data):
    """
    Equip a weapon
    """
    if not has_item(character, item_id):
        raise ItemNotFoundError("Weapon not in inventory: " + str(item_id))

    if item_data.get("type") != "weapon":
        raise InvalidItemTypeError("Item is not a weapon.")

    if "equipment_bonuses" not in character:
        character["equipment_bonuses"] = {}

    # Unequip current weapon if exists
    if "equipped_weapon" in character and character["equipped_weapon"] is not None:
        old_id = character["equipped_weapon"]
        # Remove old bonus
        if "weapon" in character["equipment_bonuses"]:
            stat_name, value = character["equipment_bonuses"]["weapon"]
            apply_stat_effect(character, stat_name, -value)
            character["equipment_bonuses"]["weapon"] = None
        # Add old weapon back to inventory (check space)
        if get_inventory_space_remaining(character) <= 0:
            raise InventoryFullError("No space to unequip weapon.")
        character["inventory"].append(old_id)

    # Equip new weapon
    stat_name, value = parse_item_effect(item_data.get("effect", "strength:0"))
    apply_stat_effect(character, stat_name, value)
    character["equipped_weapon"] = item_id
    character["equipment_bonuses"]["weapon"] = (stat_name, value)

    # Remove from inventory
    remove_item_from_inventory(character, item_id)

    return "Equipped weapon: " + item_data.get("name", item_id)

def equip_armor(character, item_id, item_data):
    """
    Equip armor
    """
    if not has_item(character, item_id):
        raise ItemNotFoundError("Armor not in inventory: " + str(item_id))

    if item_data.get("type") != "armor":
        raise InvalidItemTypeError("Item is not armor.")

    if "equipment_bonuses" not in character:
        character["equipment_bonuses"] = {}

    # Unequip current armor if exists
    if "equipped_armor" in character and character["equipped_armor"] is not None:
        old_id = character["equipped_armor"]
        if "armor" in character["equipment_bonuses"]:
            stat_name, value = character["equipment_bonuses"]["armor"]
            apply_stat_effect(character, stat_name, -value)
            character["equipment_bonuses"]["armor"] = None
        if get_inventory_space_remaining(character) <= 0:
            raise InventoryFullError("No space to unequip armor.")
        character["inventory"].append(old_id)

    stat_name, value = parse_item_effect(item_data.get("effect", "max_health:0"))
    apply_stat_effect(character, stat_name, value)
    character["equipped_armor"] = item_id
    character["equipment_bonuses"]["armor"] = (stat_name, value)

    remove_item_from_inventory(character, item_id)

    return "Equipped armor: " + item_data.get("name", item_id)

def unequip_weapon(character):
    """
    Remove equipped weapon and return it to inventory
    """
    if "equipped_weapon" not in character or character["equipped_weapon"] is None:
        return None

    if get_inventory_space_remaining(character) <= 0:
        raise InventoryFullError("No space to unequip weapon.")

    item_id = character["equipped_weapon"]

    if "equipment_bonuses" in character and "weapon" in character["equipment_bonuses"]:
        bonus = character["equipment_bonuses"]["weapon"]
        if bonus is not None:
            stat_name, value = bonus
            apply_stat_effect(character, stat_name, -value)
        character["equipment_bonuses"]["weapon"] = None

    character["equipped_weapon"] = None
    character["inventory"].append(item_id)
    return item_id

def unequip_armor(character):
    """
    Remove equipped armor and return it to inventory
    """
    if "equipped_armor" not in character or character["equipped_armor"] is None:
        return None

    if get_inventory_space_remaining(character) <= 0:
        raise InventoryFullError("No space to unequip armor.")

    item_id = character["equipped_armor"]

    if "equipment_bonuses" in character and "armor" in character["equipment_bonuses"]:
        bonus = character["equipment_bonuses"]["armor"]
        if bonus is not None:
            stat_name, value = bonus
            apply_stat_effect(character, stat_name, -value)
        character["equipment_bonuses"]["armor"] = None

    character["equipped_armor"] = None
    character["inventory"].append(item_id)
    return item_id

# ============================================================================
# SHOP SYSTEM
# ============================================================================

def purchase_item(character, item_id, item_data):
    """
    Purchase an item from a shop
    """
    cost = item_data.get("cost", 0)
    gold = character.get("gold", 0)

    if gold < cost:
        raise InsufficientResourcesError("Not enough gold.")

    if get_inventory_space_remaining(character) <= 0:
        raise InventoryFullError("Inventory is full.")

    character["gold"] = gold - cost
    add_item_to_inventory(character, item_id)
    return True

def sell_item(character, item_id, item_data):
    """
    Sell an item for half its purchase cost
    """
    if not has_item(character, item_id):
        raise ItemNotFoundError("Item not in inventory: " + str(item_id))

    cost = item_data.get("cost", 0)
    sell_price = cost // 2

    remove_item_from_inventory(character, item_id)
    character["gold"] = character.get("gold", 0) + sell_price

    return sell_price

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_item_effect(effect_string):
    """
    Parse item effect string into stat name and value
    """
    if ":" not in effect_string:
        raise ValueError("Invalid effect format.")

    parts = effect_string.split(":", 1)
    stat_name = parts[0].strip()
    try:
        value = int(parts[1].strip())
    except ValueError:
        raise ValueError("Effect value must be integer.")

    return stat_name, value

def apply_stat_effect(character, stat_name, value):
    """
    Apply a stat modification to character
    """
    if stat_name not in ["health", "max_health", "strength", "magic"]:
        # Ignore unknown stats silently
        return

    if stat_name not in character:
        character[stat_name] = 0

    character[stat_name] = character[stat_name] + value

    if stat_name == "health":
        max_hp = character.get("max_health", character["health"])
        if character["health"] > max_hp:
            character["health"] = max_hp

def display_inventory(character, item_data_dict):
    """
    Display character's inventory in formatted way
    """
    if "inventory" not in character:
        character["inventory"] = []

    if len(character["inventory"]) == 0:
        print("Inventory is empty.")
        return

    # Count items
    counts = {}
    for item_id in character["inventory"]:
        if item_id in counts:
            counts[item_id] = counts[item_id] + 1
        else:
            counts[item_id] = 1

    print("\n=== Inventory ===")
    for item_id in counts:
        item_info = item_data_dict.get(item_id, {})
        name = item_info.get("name", item_id)
        item_type = item_info.get("type", "unknown")
        qty = counts[item_id]
        print(f"{name} ({item_type}) x{qty} [{item_id}]")
    print("=================\n")

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== INVENTORY SYSTEM TEST ===")
    
    # Test adding items
    # test_char = {'inventory': [], 'gold': 100, 'health': 80, 'max_health': 80}
    # 
    # try:
    #     add_item_to_inventory(test_char, "health_potion")
    #     print(f"Inventory: {test_char['inventory']}")
    # except InventoryFullError:
    #     print("Inventory is full!")
    
    # Test using items
    # test_item = {
    #     'item_id': 'health_potion',
    #     'type': 'consumable',
    #     'effect': 'health:20'
    # }
    # 
    # try:
    #     result = use_item(test_char, "health_potion", test_item)
    #     print(result)
    # except ItemNotFoundError:
    #     print("Item not found")

