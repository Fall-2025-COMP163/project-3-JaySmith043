"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Completed Implementation

Name: Jadyn Dewitt-Smith

AI Usage:
Combat structure, ability logic, and flow-control were developed with
ChatGPT assistance. All logic was reviewed and integrated by the me.
"""

import random
from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)

# ============================================================================
# ENEMY DEFINITIONS
# ============================================================================

def create_enemy(enemy_type):
    """
    Create predefined enemy types.
    Raises InvalidTargetError for unknown enemy types.
    """
    enemy_type = enemy_type.lower().strip()

    if enemy_type == "goblin":
        return {
            "name": "Goblin",
            "type": "goblin",
            "health": 50,
            "max_health": 50,
            "strength": 8,
            "magic": 2,
            "xp_reward": 25,
            "gold_reward": 10
        }
    elif enemy_type == "orc":
        return {
            "name": "Orc",
            "type": "orc",
            "health": 80,
            "max_health": 80,
            "strength": 12,
            "magic": 5,
            "xp_reward": 50,
            "gold_reward": 25
        }
    elif enemy_type == "dragon":
        return {
            "name": "Dragon",
            "type": "dragon",
            "health": 200,
            "max_health": 200,
            "strength": 25,
            "magic": 15,
            "xp_reward": 200,
            "gold_reward": 100
        }
    else:
        raise InvalidTargetError(f"Unknown enemy type: {enemy_type}")


def get_random_enemy_for_level(character_level):
    """
    Levels 1-2 → Goblins
    Levels 3-5 → Orcs
    Levels 6+ → Dragons
    """
    if character_level <= 2:
        return create_enemy("goblin")
    elif character_level <= 5:
        return create_enemy("orc")
    else:
        return create_enemy("dragon")

# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:
    """
    Manages turn-based combat between a character dictionary
    and an enemy dictionary.
    """

    def __init__(self, character, enemy):
        if character["health"] <= 0:
            raise CharacterDeadError("Character is already dead before battle!")

        self.character = character
        self.enemy = enemy
        self.combat_active = True
        self.turn_number = 1

    def start_battle(self):
        """
        Main combat loop.
        Returns winner + reward dict.
        """
        if self.character["health"] <= 0:
            raise CharacterDeadError("Cannot start battle with a dead character.")

        while self.combat_active:
            display_combat_stats(self.character, self.enemy)

            # PLAYER TURN
            self.player_turn()
            result = self.check_battle_end()
            if result:
                return result

            # ENEMY TURN
            self.enemy_turn()
            result = self.check_battle_end()
            if result:
                return result

            self.turn_number += 1

        # If combat was ended another way
        return {"winner": "none", "xp_gained": 0, "gold_gained": 0}

    # ----------------------------------------------------------------------

    def player_turn(self):
        """
        Player chooses:
        1. Basic Attack
        2. Special Ability
        3. Run away
        """
        if not self.combat_active:
            raise CombatNotActiveError("No battle in progress.")

        print("\n--- PLAYER TURN ---")
        print("1. Basic Attack")
        print("2. Special Ability")
        print("3. Attempt Escape")

        choice = input("Choose an action: ").strip()

        if choice == "1":
            damage = self.calculate_damage(self.character, self.enemy)
            self.apply_damage(self.enemy, damage)
            display_battle_log(f"You hit the enemy for {damage} damage!")

        elif choice == "2":
            try:
                message = use_special_ability(self.character, self.enemy)
                display_battle_log(message)
            except AbilityOnCooldownError:
                display_battle_log("Your ability is on cooldown!")
            except Exception as e:
                display_battle_log(str(e))

        elif choice == "3":
            escaped = self.attempt_escape()
            if escaped:
                display_battle_log("You successfully escaped!")
                self.combat_active = False
            else:
                display_battle_log("Escape failed!")

        else:
            print("Invalid choice — you lose your turn.")

    # ----------------------------------------------------------------------

    def enemy_turn(self):
        """
        Enemy always performs a basic attack.
        """
        if not self.combat_active:
            raise CombatNotActiveError("No battle in progress.")

        print("\n--- ENEMY TURN ---")
        damage = self.calculate_damage(self.enemy, self.character)
        self.apply_damage(self.character, damage)
        display_battle_log(f"{self.enemy['name']} hits you for {damage} damage!")

    # ----------------------------------------------------------------------

    def calculate_damage(self, attacker, defender):
        """
        strength - (defender_strength / 4)
        min damage = 1
        """
        base = attacker["strength"]
        reduction = defender["strength"] // 4
        damage = base - reduction
        return max(damage, 1)

    # ----------------------------------------------------------------------

    def apply_damage(self, target, damage):
        """
        Reduces HP but not below 0.
        """
        target["health"] = max(target["health"] - damage, 0)

    # ----------------------------------------------------------------------

    def check_battle_end(self):
        """
        Returns results dict if someone dies.
        """
        if self.enemy["health"] <= 0:
            display_battle_log("Enemy defeated!")

            return {
                "winner": "player",
                "xp_gained": self.enemy.get("xp_reward", 0),
                "gold_gained": self.enemy.get("gold_reward", 0)
            }

        if self.character["health"] <= 0:
            display_battle_log("You have been defeated!")
            return {
                "winner": "enemy",
                "xp_gained": 0,
                "gold_gained": 0
            }

        return None

    # ----------------------------------------------------------------------

    def attempt_escape(self):
        """
        50% chance escape.
        """
        success = random.random() < 0.5
        if success:
            self.combat_active = False
        return success


# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy):
    """
    Routes to correct special ability.
    """
    char_class = character["class"]

    if char_class == "Warrior":
        dmg = warrior_power_strike(character, enemy)
        return f"Power Strike hits for {dmg} damage!"

    elif char_class == "Mage":
        dmg = mage_fireball(character, enemy)
        return f"Fireball deals {dmg} magic damage!"

    elif char_class == "Rogue":
        dmg = rogue_critical_strike(character, enemy)
        return f"Critical Strike hits for {dmg} damage!"

    elif char_class == "Cleric":
        healed = cleric_heal(character)
        return f"Cleric heals for {healed} health!"

    else:
        raise InvalidTargetError("Unknown class for ability")

# ----------------------------------------------------------------------

def warrior_power_strike(character, enemy):
    """
    Deals 2× Strength.
    """
    damage = character["strength"] * 2
    enemy["health"] = max(enemy["health"] - damage, 0)
    return damage

def mage_fireball(character, enemy):
    """
    Deals 2× Magic.
    """
    damage = character["magic"] * 2
    enemy["health"] = max(enemy["health"] - damage, 0)
    return damage

def rogue_critical_strike(character, enemy):
    """
    50% chance triple damage.
    Otherwise normal strength damage.
    """
    if random.random() < 0.5:
        damage = character["strength"] * 3
    else:
        damage = character["strength"]

    enemy["health"] = max(enemy["health"] - damage, 0)
    return damage

def cleric_heal(character):
    """
    Heals 30 HP but not above max.
    """
    before = character["health"]
    character["health"] = min(character["max_health"], character["health"] + 30)
    return character["health"] - before


# ============================================================================
# UTILITIES
# ============================================================================

def can_character_fight(character):
    """
    Character can fight if HP > 0.
    """
    return character["health"] > 0

def get_victory_rewards(enemy):
    """
    Return XP + gold rewards from defeated enemy.
    """
    return {
        "xp": enemy.get("xp_reward", 0),
        "gold": enemy.get("gold_reward", 0)
    }

def display_combat_stats(character, enemy):
    """
    Displays HP information.
    """
    print("\n=== COMBAT STATUS ===")
    print(f"{character['name']} HP: {character['health']} / {character['max_health']}")
    print(f"{enemy['name']} HP: {enemy['health']} / {enemy['max_health']}")

def display_battle_log(message):
    print(f">>> {message}")


# ============================================================================
# TESTING HARNESS
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM SELF-TEST ===")
    hero = {"name": "Hero", "class": "Warrior", "health": 120,
            "max_health": 120, "strength": 15, "magic": 5}

    goblin = create_enemy("goblin")
    battle = SimpleBattle(hero, goblin)
    result = battle.start_battle()
    print(result)
# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")
    
    # Test enemy creation
    # try:
    #     goblin = create_enemy("goblin")
    #     print(f"Created {goblin['name']}")
    # except InvalidTargetError as e:
    #     print(f"Invalid enemy: {e}")
    
    # Test battle
    # test_char = {
    #     'name': 'Hero',
    #     'class': 'Warrior',
    #     'health': 120,
    #     'max_health': 120,
    #     'strength': 15,
    #     'magic': 5
    # }
    #
    # battle = SimpleBattle(test_char, goblin)
    # try:
    #     result = battle.start_battle()
    #     print(f"Battle result: {result}")
    # except CharacterDeadError:
    #     print("Character is dead!")

