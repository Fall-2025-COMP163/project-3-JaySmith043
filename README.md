# Quest Chronicles  
### COMP 163 – Project 3  
### Modular RPG Adventure Game  
**Author:** Jadyn DeWitt-Smith
**AI Usage:** Documented below  

---

## 📌 Project Overview
Quest Chronicles is a modular, text-based RPG designed to demonstrate mastery of **Python modules**, **custom exceptions**, and **game state management**.  
The system includes:

- Character classes (Warrior, Mage, Rogue, Cleric)  
- Inventory and equipment  
- Quest progression system  
- Turn-based combat  
- Random enemy encounters  
- Save/load system  
- Shop for buying and selling items  

All features follow the constraints of COMP 163: **only concepts up to Modules + Exceptions.**

---

## 📁 Project Structure

quest_chronicles/
│
├── main.py
├── character_manager.py
├── inventory_system.py
├── quest_handler.py
├── combat_system.py
├── game_data.py
├── custom_exceptions.py
│
├── data/
│ ├── quests.txt
│ ├── items.txt
│ └── save_games/
│
└── tests/

yaml
Copy code

---

## 🧩 Module Architecture

### **main.py**
Handles:
- Main menu  
- Game loop  
- Navigation to other modules  
- Saving after major actions  

### **character_manager.py**
Handles:
- Character creation  
- Save/load  
- Leveling  
- Validation  
- Health + gold management  

### **inventory_system.py**
Handles:
- Inventory storage  
- Item usage  
- Weapon/armor equipping  
- Stat effects  
- Shop interactions  

### **quest_handler.py**
Handles:
- Accepting quests  
- Completing quests  
- Checking prerequisites  
- Reward calculation  
- Quest progress tracking  

### **combat_system.py**
Handles:
- Enemy creation (goblin, orc, dragon)  
- Turn-based combat  
- Special abilities  
- Escaping  

### **game_data.py**
Handles:
- Loading and validating `.txt` data  
- Creating default files if missing  

---

## ⚠️ Exception Strategy

Quest Chronicles uses structured exceptions for clean error handling.

### Character Exceptions
- InvalidCharacterClassError  
- CharacterNotFoundError  
- InvalidSaveDataError  
- CharacterDeadError  

### Combat Exceptions
- InvalidTargetError  
- CombatNotActiveError  
- AbilityOnCooldownError  

### Quest Exceptions
- QuestNotFoundError  
- QuestRequirementsNotMetError  
- QuestAlreadyCompletedError  
- QuestNotActiveError  

### Inventory Exceptions
- InventoryFullError  
- ItemNotFoundError  
- InsufficientResourcesError  
- InvalidItemTypeError  

### Data Exceptions
- MissingDataFileError  
- InvalidDataFormatError  
- CorruptedDataError  

This ensures each module reports errors cleanly to `main.py`.

---

## 🎮 How to Play

### Run the Game
python main.py

yaml
Copy code

### Main Menu Options
1. New Game  
2. Load Game  
3. Exit  

### In-Game Menu Options
1. View Character Stats  
2. View Inventory  
3. Quest Menu  
4. Explore (Fight Enemies)  
5. Shop  
6. Save & Quit  

---

## 🧪 Running Automated Tests

Run all tests:
python -m pytest tests/ -v

sql
Copy code

Run specific tests:
python -m pytest tests/test_exception_handling.py -v
python -m pytest tests/test_module_structure.py -v
python -m pytest tests/test_game_integration.py -v

yaml
Copy code

---

## 🎨 Design Choices

### ✔ Characters as Dictionaries  
Chosen to avoid circular imports across modules and comply with COMP 163’s limitation (no advanced OOP). Dictionaries also serialize easily.

### ✔ Data-Driven Items & Quests  
Editable through `quests.txt` and `items.txt` without touching code.

### ✔ Strict Module Separation  
Each module handles exactly one type of functionality, making debugging and testing easier.

### ✔ Clear, Test-Friendly Logic  
All code uses only loops, branches, simple functions, exceptions, and modules — the concepts allowed in COMP 163.

### ✔ Safe Error Handling  
Every invalid action produces a meaningful custom exception.

---

## 🤖 AI Usage Disclosure
AI assistance (ChatGPT) was used for:

- Structuring module interactions  
- Template logic for combat, inventory, and quest systems  
- Debugging exception flow  
- README formatting  
- Ensuring clarity and modularity  

All code was reviewed, understood, tested, and modified by me. 


---

## 🚀 Future Improvements

- More enemy types (trolls, vampires, ghosts)  
- Add elemental damage  
- Critical hit and dodge mechanics  
- Crafting or refining system  
- Class skill trees  

---

## 🎉 Thank You for Reviewing Quest Chronicles!
A modular Python RPG adventure designed to meet COMP 163 requirements.
