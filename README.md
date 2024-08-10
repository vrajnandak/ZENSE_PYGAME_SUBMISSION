# Rift Rescue

## Game Lore
In a technologically advanced world with evil factions and adventurers, three scientists discover ancient ruins rumored to house a time-travel device. They venture into the ruins but get separated. A retired top adventurer is called to rescue them.

## Gameplay Walkthrough
The ruins are numbered 1, 2, 3 and the protagonist must clear each map to rescue the scientists.

1. **First Ruin**: Enter the correct code (visible in the starting map) to enter Ruin1. Defeat all enemies to rescue Scientist 1.
2. **Second Ruin**: Find the key to rescue the scientist.
3. **Third Ruin**: Defeat all the enemies to reach the third scientist, only to discover he is the true villain. After this revelation, the player must battle all the enemies once more.

## Key Features
- Rich, atmospheric environments with detailed ruins to explore.
- Engaging storyline, efficient algorithms, and basic OOP concepts.
- Enemy-player detection using A* algorithm to navigate around obstacles.
- Mask-collision for a better gaming experience.
- Scrollable settings to control gameplay.
- Multiple game cameras.
- Inventory to store consumables and drops.
- Dialog history to review previous dialogs.
- Smooth map transitions.
- Multiple player weapons and magic.
- Various screens: Start, Pause, Settings.
- Random loot drops based on defeated enemies.
- Arrow indicator for nearest enemy when none are within a specified radius.
- Timer for clearing a map.
- The most important of all, Saving the game.

## Softwares Used
- **GIMP (2.10.30)**: For drawing sprites.
- **Tiled**: For maps and generating CSV files.
- **VScode**: IDE used.
- **pygame**: For game development and handling game logic.
- **pathfinding, json, os etc**: Module used for finding the shortest path, for writing to files, managing files etc.
- **git, github**: Version control and repository hosting.

## To Run the Game
1. Open the 'ZENSE_PROJECT_PYGAME' folder in VScode.
2. Run the `main.py` file.

## Controls
- **Player Movement**: Arrow keys [↑, ↓, ←, →] and [W, A, S, D].
- **Camera Movement**: Hover mouse towards screen edges or use [I (top), J (left), K (down), L (right)]. Hold [B] for Box-camera; [U] to reset the camera.
- **Attack**: [Space]
- **Magic**: [Left Ctrl]
- **Pause Screen**: [Esc]
- **Switching Weapons**: [N] for next weapon, [P] for previous weapon.
- **Switching Magic**: [M] for next magic, [O] for previous magic.
- **Viewing Dialogs**: [G] to view the log of all dialogs. Click a log to display the dialog box.
- **Inventory Box**: [V] to open inventory box. [T], [Y] to move across inventory items. [E] to use the selected item.

## Naming Formats
- **Obstacles**: `<name_of_obstacle>_<elem_id_in_Tiled_map>_<img_width>_<img_height>.png`
- **Invisible Boundaries**: Use ID '1000' in CSV file for invisible boundaries.
- **Portals**: Named `<x>` where 'x' represents the frame number, fixed size 96x96.
(more information in Settings.py file)

## Ruins
1. **Ruin0**: The starting island.
2. **Ruin1**: The 1st ruin to clear.
3. **Ruin2**: The 2nd ruin to clear.
4. **Ruin3**: The 3rd ruin to clear.

## Description of Files

### `src` Directory:
- **Button.py**: Creates buttons with default animations.
- **CollisionHelper.py**: Achieves mask collisions.
- **Enemy.py**: Code for enemy behavior, animations, pathfinding.
- **Game.py**: Core game logic, screens, settings, map transitions.
- **LEVEL_THINGS.py**: Dialogs, scientists, and event handling.
- **Level.py**: Level logic, player actions, UI.
- **main.py**: Runs the game.
- **Obstacle.py**: Static objects for collisions.
- **Particles.py**: Shows particles from attacks and magic.
- **Player.py**: Player controls, collision handling.
- **PlayerMagic.py**: Player magic effects.
- **Portal.py**: Creates and animates portals.
- **RandomLoot.py**: Generates random loot.
- **Settings.py**: Game settings, dialog history, animations.
- **Weapon.py**: Player weapons and damage mechanics.
- **LoadDataManager.py**: Code for saving the data of the curr game into files.

### `graphics` Directory:
Contains images for obstacles, backgrounds, loots, weapons, magic, player, enemies, scientists, and ruins.

### `GIMP_SPRITES` Directory:
Contains .xcf files for sprites created with GIMP.

### `tmp.py`:
Contains code for testing specific pygame features.

## Game Mechanics
- **Camera Offsets**: Adjusted based on player position, mouse movement, or key presses.
- **Pathfinding**: A* algorithm used for enemy movement towards the player.
- **Mask Collision**: Detects and handles collisions with precise mask checks.

## Additional Sources Used
- **Images and Particles Code**: [Clear Code Projects - Zelda](https://github.com/clear-code-projects/Zelda)

---
