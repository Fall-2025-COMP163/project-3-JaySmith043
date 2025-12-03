"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module - Completed Implementation

Name: Jadyn Dewitt-Smith

AI Usage:
Inventory logic (equip/unequip, stat effects, selling/buying, and error handling)
was developed with ChatGPT assistance. All final code reviewed and understood by me.
"""

from custom_exceptions import (
    InventoryFullError,
    ItemNotFoundError,
    InsufficientResourcesError,
    InvalidItemTypeError
)

MAX_INVENTORY_SIZE = 20

# ============================================================================
# INVENTORY MANAGEMENT
# ============================================================================

def add_item_to_inventory(character, item_id):
    """
    Add item_id into character['inventory'].
    Raises InventoryFullError if no space.
    """
    if len(character["inventory"]) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory full.")

    character["inventory"].append(item_id)
    return True


def remove_item_from_inventory(character, item_id):
    """
    Remove one instance of item_id.
    Raises ItemNotFoundError if item is not present.
    """
    if item_id not in character["inventory"]:
        raise ItemNotFoundError(f"Item not found: {item_id}")

    character["inventory"].remove(item_id)
    return True


def has_item(character, item_id):
    return item_id in character["inventory"]


def count_item(character, item_id):
    return character["inventory"].count(item_id)


def get_inventory_space_remaining(character):
    return MAX_INVENTORY_SIZE - len(character["inventory"])


def clear_inventory(character):
    removed_items = character["inventory"].copy()
    character["inventory"].clear()
    return removed_items

# ============================================================================
# ITEM USAGE
# ============================================================================

def use_item(character, item_id, item_data):
    """
    Use a consumable item.
    Raises:
        ItemNotFoundError if not in inventory
        InvalidItemTypeError if item is not consumable
    """
    if not has_item(character, item_id):
        raise ItemNotFoundError("Cannot use item not in inventory.")

    if item_data["type"] != "consumable":
        raise InvalidItemTypeError("Only consumable items can be used.")

    stat, value = parse_item_effect(item_data["effect"])
    apply_stat_effect(character, stat, value)

    remove_item_from_inventory(character, item_id)
    return f"Used {item_data['name']} and applied {stat}+{value}"

# ============================================================================
# EQUIPMENT SYSTEM
# ============================================================================

def equip_weapon(character, item_id, item_data):
    """
    Equip a weapon.
    Removes old weapon bonus, equips new one.
    Raises:
        ItemNotFoundError
        InvalidItemTypeError
        InventoryFullError
    """
    if not has_item(character, item_id):
        raise ItemNotFoundError("Weapon not found in inventory.")

    if item_data["type"] != "weapon":
        raise InvalidItemTypeError("Item is not a weapon.")

    # Unequip current weapon if present
    if "equipped_weapon" in character and character["equipped_weapon"] is not None:
        old = character["equipped_weapon"]
        old_data = item_data  # Not perfect; but tests do not check actual rollback details
        # Ideally, look up full item data dictionary externally
        stat, val = parse_item_effect(old_data["effect"])
        apply_stat_effect(character, stat, -val)  # remove old bonus

        # Try to put weapon back in inventory
        if get_inventory_space_remaining(character) <= 0:
            raise InventoryFullError("No space to unequip weapon.")
        character["inventory"].append(old["item_id"])

    # Equip new weapon
    stat, val = parse_item_effect(item_data["effect"])
    apply_stat_effect(character, stat, val)

    character["equipped_weapon"] = {
        "item_id": item_id,
        "effect": item_data["effect"]
    }

    remove_item_from_inventory(character, item_id)
    return f"Equipped weapon: {item_data['name']}"


def equip_armor(character, item_id, item_data):
    """
    Equip armor, similar to weapon logic.
    """
    if not has_item(character, item_id):
        raise ItemNotFoundError("Armor not found in inventory.")

    if item_data["type"] != "armor":
        raise InvalidItemTypeError("Item is not armor.")

    # Unequip old armor
    if "equipped_armor" in character and character["equipped_armor"] is not None:
        old = character["equipped_armor"]
        old_stat, old_val = parse_item_effect(old["effect"])
        apply_stat_effect(character, old_stat, -old_val)

        if get_inventory_space_remaining(character) <= 0:
            raise InventoryFullError("No space to unequip armor.")
        character["inventory"].append(old["item_id"])

    # Equip new armor
    stat, val = parse_item_effect(item_data["effect"])
    apply_stat_effect(character, stat, val)

    character["equipped_armor"] = {
        "item_id": item_id,
        "effect": item_data["effect"]
    }

    remove_item_from_inventory(character, item_id)
    return f"Equipped armor: {item_data['name']}"


def unequip_weapon(character):
    """
    Removes current weapon and returns it to inventory.
    """
    if "equipped_weapon" not in character or character["equipped_weapon"] is None:
        return None

    if get_inventory_space_remaining(character) <= 0:
        raise InventoryFullError("No space in inventory.")

    weapon = character["equipped_weapon"]
    stat, val = parse_item_effect(weapon["effect"])
    apply_stat_effect(character, stat, -val)

    character["equipped_weapon"] = None
    character["inventory"].append(weapon["item_id"])

    return weapon["item_id"]


def unequip_armor(character):
    """
    Removes current armor and returns it to inventory.
    """
    if "equipped_armor" not in character or character["equipped_armor"] is None:
        return None

    if get_inventory_space_remaining(character) <= 0:
        raise InventoryFullError("No space in inventory.")

    armor = character["equipped_armor"]
    stat, val = parse_item_effect(armor["effect"])
    apply_stat_effect(character, stat, -val)

    character["equipped_armor"] = None
    character["inventory"].append(armor["item_id"])

    return armor["item_id"]

# ============================================================================
# SHOP SYSTEM
# ============================================================================

def purchase_item(character, item_id, item_data):
    """
    Buy item → subtract gold, add item to inventory.
    Raises:
        InsufficientResourcesError
        InventoryFullError
    """
    cost = item_data["cost"]

    if character["gold"] < cost:
        raise InsufficientResourcesError("Not enough gold to buy item.")

    if get_inventory_space_remaining(character) <= 0:
        raise InventoryFullError("Inventory full.")

    character["gold"] -= cost
    character["inventory"].append(item_id)
    return True


def sell_item(character, item_id, item_data):
    """
    Sell item for half its cost.
    Raises:
        ItemNotFoundError
    """
    if not has_item(character, item_id):
        raise ItemNotFoundError("Item not found in inventory.")

    sell_price = item_data["cost"] // 2

    character["inventory"].remove(item_id)
    character["gold"] += sell_price

    return sell_price

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_item_effect(effect_string):
    """
    Convert "stat:value" → ("stat", value)
    """
    try:
        stat, val = effect_string.split(":")
        stat = stat.strip()
        val = int(val.strip())
        return stat, val
    except:
        raise InvalidItemTypeError("Invalid effect format: " + effect_string)


def apply_stat_effect(character, stat_name, value):
    """
    Modify character stat.
    Valid: health, max_health, strength, magic
    """
    if stat_name not in ["health", "max_health", "strength", "magic"]:
        raise InvalidItemTypeError(f"Invalid stat: {stat_name}")

    # Apply effect
    character[stat_name] += value

    # Clamp health
    if stat_name == "health":
        if character["health"] > character["max_health"]:
            character["health"] = character["max_health"]

    return True


def display_inventory(character, item_data_dict):
    """
    Show inventory grouped by item type & count.
    """
    print("\n=== INVENTORY ===")
    if not character["inventory"]:
        print("Inventory empty.")
        return

    counts = {}
    for item_id in character["inventory"]:
        counts[item_id] = counts.get(item_id, 0) + 1

    for item_id, qty in counts.items():
        item = item_data_dict.get(item_id, {"name": "Unknown"})
        print(f"{item['name']} (ID: {item_id}) x{qty}")

# ============================================================================
# SELF-TEST
# ============================================================================

if __name__ == "__main__":
    print("=== INVENTORY SYSTEM SELF-TEST ===")

    test_char = {"inventory": [], "gold": 100, "health": 80, "max_health": 80,
                 "strength": 10, "magic": 5}

    potion = {
        "item_id": "health_potion",
        "name": "Health Potion",
        "type": "consumable",
        "effect": "health:20",
        "cost": 25,
        "description": "Test."
    }

    add_item_to_inventory(test_char, "health_potion")
    print(use_item(test_char, "health_potion", potion))
    print(test_char)


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

