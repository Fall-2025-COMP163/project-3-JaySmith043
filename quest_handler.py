"""
COMP 163 - Project 3: Quest Chronicles
Quest Handler Module - Completed Implementation

Name: Jadyn Dewitt-Smith

AI Usage:
Quest logic, requirement checks, reward calculations, and display utilities
were generated with ChatGPT assistance and then reviewed and understood by me.
"""

from custom_exceptions import (
    QuestNotFoundError,
    QuestRequirementsNotMetError,
    QuestAlreadyCompletedError,
    QuestNotActiveError,
    InsufficientLevelError
)

import character_manager  # for XP + gold handling

# ============================================================================
# QUEST MANAGEMENT
# ============================================================================

def accept_quest(character, quest_id, quest_data_dict):
    """
    Add quest to active quests if all requirements are met.
    Raises:
        QuestNotFoundError
        InsufficientLevelError
        QuestRequirementsNotMetError
        QuestAlreadyCompletedError
    """

    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest not found: {quest_id}")

    quest = quest_data_dict[quest_id]

    # Already done?
    if quest_id in character["completed_quests"]:
        raise QuestAlreadyCompletedError("Quest already completed.")

    # Already active?
    if quest_id in character["active_quests"]:
        raise QuestRequirementsNotMetError("Quest already active.")

    # Level check
    if character["level"] < quest["required_level"]:
        raise InsufficientLevelError("Character level too low.")

    # Prerequisite check
    prereq = quest["prerequisite"]
    if prereq != "NONE" and prereq not in character["completed_quests"]:
        raise QuestRequirementsNotMetError("Prerequisite quest not completed.")

    # All good → accept quest
    character["active_quests"].append(quest_id)
    return True


# ---------------------------------------------------------------------------

def complete_quest(character, quest_id, quest_data_dict):
    """
    Complete quest → award XP & gold.
    Raises:
        QuestNotFoundError
        QuestNotActiveError
    """

    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest not found: {quest_id}")

    if quest_id not in character["active_quests"]:
        raise QuestNotActiveError("Quest is not active.")

    quest = quest_data_dict[quest_id]

    # Remove from active → move to completed
    character["]()



# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== QUEST HANDLER TEST ===")
    
    # Test data
    # test_char = {
    #     'level': 1,
    #     'active_quests': [],
    #     'completed_quests': [],
    #     'experience': 0,
    #     'gold': 100
    # }
    #
    # test_quests = {
    #     'first_quest': {
    #         'quest_id': 'first_quest',
    #         'title': 'First Steps',
    #         'description': 'Complete your first quest',
    #         'reward_xp': 50,
    #         'reward_gold': 25,
    #         'required_level': 1,
    #         'prerequisite': 'NONE'
    #     }
    # }
    #
    # try:
    #     accept_quest(test_char, 'first_quest', test_quests)
    #     print("Quest accepted!")
    # except QuestRequirementsNotMetError as e:
    #     print(f"Cannot accept: {e}")

