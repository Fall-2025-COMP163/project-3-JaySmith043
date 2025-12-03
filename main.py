"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Completed Implementation

Name: Jadyn Dewitt-Smith

AI Usage:
Game loop design, menu structures, and integration logic were generated with
ChatGPT assistance. All code was reviewed, understood, and finalized by me.
"""

import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data
from custom_exceptions import *

# ============================================================================
# GAME STATE
# ============================================================================

current_character = None
all_quests = {}
all_items = {}
game_running = False

# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu():
    """
    Display main menu and validate choice.
    """
    print("\n=== MAIN MENU ===")
    print("1. New Game")
    print("2. Load Game")
    print("3. Exit")

    choice = input("Choose an option: ").strip()

    if choice in ["1", "2", "3"]:
        return int(choice)
    else:
        print("Invalid choice. Try again.")
        return main_menu()

# ============================================================================
# NEW GAME
# ============================================================================

def new_game():
    global current_character

    print("\n=== NEW GAME ===")
    name = input("Enter character name: ").strip()

    print("\nChoose a class:")
    print("1. Warrior")
    print("2. Mage")
    print("3. Rogue")
    print("4. Cleric")

    class_choice = input("Choose class (1-4): ").strip()
    class_map = {"1": "Warrior", "2": "Mage", "3": "Rogue", "4": "Cleric"}

    if class_choice not in class_map:
        print("Invalid class choice. Returning to main menu...")
        return

    char_class = class_map[class_choice]

    try:
        current_character = character_manager.create_character(name, char_class)
        character_manager.save_character(current_character)
        print(f"\nCreated {name} the {char_class}!")
        game_loop()
    except InvalidCharacterClassError:
        print("Invalid class name. Try again.")
        new_game()

# ============================================================================
# LOAD GAME
# ============================================================================

def load_game():
    global current_character

    print("\n=== LOAD GAME ===")
    saved = character_manager.list_saved_characters()

    if not saved:
        print("No saved characters found.")
        return

    print("Saved Characters:")
    for i, name in enumerate(saved, 1):
        print(f"{i}. {name}")

    choice = input("Select a character by number: ").strip()

    if not choice.isdigit() or int(choice) not in range(1, len(saved) + 1):
        print("Invalid selection.")
        return

    selected = saved[int(choice) - 1]

    try:
        current_character = character_manager.load_character(selected)
        print(f"Loaded character: {selected}")
        game_loop()
    except CharacterNotFoundError:
        print("Character not found.")
    except SaveFileCorruptedError:
        print("Save file corrupted.")
    except InvalidSaveDataError:
        print("Invalid save data.")

# ============================================================================
# GAME LOOP
# ============================================================================

def game_loop():
    global game_running, current_character

    print("\n=== ENTERING GAME WORLD ===")
    game_running = True

    while game_running:
        choice = game_menu()

        if choice == 1:
            view_character_stats()
        elif choice == 2:
            view_inventory()
        elif choice == 3:
            quest_menu()
        elif choice == 4:
            explore()
        elif choice == 5:
            shop()
        elif choice == 6:
            save_game()
            print("Game saved. Goodbye!")
            game_running = False

# ============================================================================
# GAME MENU
# ============================================================================

def game_menu():
    print("\n=== GAME MENU ===")
    print("1. View Character Stats")
    print("2. Inventory")
    print("3. Quest Menu")
    print("4. Explore (Battle)")
    print("5. Shop")
    print("6. Save & Quit")

    choice = input("Choose an option: ").strip()

    if choice in ["1", "2", "3", "4", "5", "6"]:
        return int(choice)
    else:
        print("Invalid choice. Try again.")
        return game_menu()

# ============================================================================
# ACTIONS
# ============================================================================

def view_character_stats():
    print("\n=== CHARACTER STATS ===")
    for key in ["name", "class", "level", "health", "max_health", "strength", "magic", "experience", "gold"]:
        print(f"{key.capitalize()}: {current_character[key]}")

    quest_handler.display_character_quest_progress(current_character, all_quests)


def view_inventory():
    global current_character, all_items

    print("\n=== INVENTORY MENU ===")
    inventory_system.display_inventory(current_character, all_items)

    if not current_character["inventory"]:
        return

    print("\nOptions:")
    print("1. Use Item")
    print("2. Equip Weapon")
    print("3. Equip Armor")
    print("4. Drop Item")
    print("5. Back")

    choice = input("Choose an option: ").strip()
    if choice == "5":
        return

    item_id = input("Enter item ID: ").strip()
    if item_id not in all_items:
        print("Invalid item ID.")
        return

    try:
        if choice == "1":
            print(inventory_system.use_item(current_character, item_id, all_items[item_id]))
        elif choice == "2":
            print(inventory_system.equip_weapon(current_character, item_id, all_items[item_id]))
        elif choice == "3":
            print(inventory_system.equip_armor(current_character, item_id, all_items[item_id]))
        elif choice == "4":
            inventory_system.remove_item_from_inventory(current_character, item_id)
            print("Item removed.")
    except Exception as e:
        print("Error:", e)

# ============================================================================
# QUEST MENU
# ============================================================================

def quest_menu():
    global current_character, all_quests

    print("\n=== QUEST MENU ===")
    print("1. View Active Quests")
    print("2. View Available Quests")
    print("3. View Completed Quests")
    print("4. Accept Quest")
    print("5. Abandon Quest")
    print("6. Complete Quest (Testing)")
    print("7. Back")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        active = quest_handler.get_active_quests(current_character, all_quests)
        quest_handler.display_quest_list(active)

    elif choice == "2":
        available = quest_handler.get_available_quests(current_character, all_quests)
        quest_handler.display_quest_list(available)

    elif choice == "3":
        completed = quest_handler.get_completed_quests(current_character, all_quests)
        quest_handler.display_quest_list(completed)

    elif choice == "4":
        qid = input("Enter quest ID to accept: ").strip()
        try:
            quest_handler.accept_quest(current_character, qid, all_quests)
            print("Quest accepted!")
        except QuestError as e:
            print("Error:", e)

    elif choice == "5":
        qid = input("Enter quest ID to abandon: ").strip()
        try:
            quest_handler.abandon_quest(current_character, qid)
            print("Quest abandoned.")
        except QuestError as e:
            print("Error:", e)

    elif choice == "6":
        qid = input("Enter quest ID to complete: ").strip()
        try:
            rewards = quest_handler.complete_quest(current_character, qid, all_quests)
            print(f"Quest completed! Rewards: {rewards}")
        except QuestError as e:
            print("Error:", e)

    elif choice == "7":
        return

# ============================================================================
# EXPLORATION (FIND BATTLES)
# ============================================================================

def explore():
    global current_character

    print("\n=== EXPLORING ===")

    try:
        enemy = combat_system.get_random_enemy_for_level(current_character["level"])
        print(f"You encounter a {enemy['name']}!")

        battle = combat_system.SimpleBattle(current_character, enemy)
        result = battle.start_battle()

        if result["winner"] == "player":
            print(f"You won! +{result['xp_gained']} XP, +{result['gold_gained']} gold")
            character_manager.gain_experience(current_character, result["xp_gained"])
            character_manager.add_gold(current_character, result["gold_gained"])

        else:
            print("You were defeated...")
            handle_character_death()

    except CharacterDeadError:
        print("You cannot fight while dead.")
        handle_character_death()

# ============================================================================
# SHOP
# ============================================================================

def shop():
    global current_character, all_items

    print("\n=== SHOP ===")
    print(f"Your gold: {current_character['gold']}")

    print("\nItems for sale:")
    for item_id, data in all_items.items():
        print(f"{item_id}: {data['name']} (Cost: {data['cost']})")

    print("\nOptions:")
    print("1. Buy Item")
    print("2. Sell Item")
    print("3. Back")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        item_id = input("Enter item ID to buy: ").strip()
        if item_id in all_items:
            try:
                inventory_system.purchase_item(current_character, item_id, all_items[item_id])
                print("Purchase successful!")
            except Exception as e:
                print("Error:", e)
        else:
            print("Invalid item.")

    elif choice == "2":
        item_id = input("Enter item ID to sell: ").strip()
        if item_id in all_items:
            try:
                gold = inventory_system.sell_item(current_character, item_id, all_items[item_id])
                print(f"Item sold for {gold} gold.")
            except Exception as e:
                print("Error:", e)
        else:
            print("Invalid item.")

# ============================================================================
# SAVE & LOAD HELPERS
# ============================================================================

def save_game():
    global current_character
    try:
        character_manager.save_character(current_character)
        print("Game saved successfully.")
    except Exception as e:
        print("Save error:", e)

def load_game_data():
    global all_quests, all_items

    try:
        all_quests = game_data.load_quests()
        all_items = game_data.load_items()
    except MissingDataFileError:
        print("Missing data files. Creating defaults...")
        game_data.create_default_data_files()
        load_game_data()
    except InvalidDataFormatError as e:
        print("Invalid data file format:", e)
        return

# ============================================================================
# CHARACTER DEATH
# ============================================================================

def handle_character_death():
    global current_character, game_running

    print("\n=== YOU DIED ===")
    print("1. Revive (Costs 20 gold)")
    print("2. Quit Game")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        if current_character["gold"] < 20:
            print("Not enough gold. You cannot revive.")
            game_running = False
        else:
            current_character["gold"] -= 20
            character_manager.revive_character(current_character)
            print("You have been revived!")
    else:
        game_running = False

# ============================================================================
# WELCOME SCREEN
# ============================================================================

def display_welcome():
    print("=" * 50)
    print("       QUEST CHRONICLES - RPG ADVENTURE")
    print("=" * 50)
    print("Welcome, hero. Your journey begins now.\n")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    display_welcome()
    load_game_data()

    while True:
        choice = main_menu()

        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("Goodbye, adventurer!")
            break


if __name__ == "__main__":
    main()


