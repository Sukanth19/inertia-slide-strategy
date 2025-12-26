# Inertia

Inertia is a grid-based strategy game inspired by inertia-style movement mechanics.  
Players slide across the board in fixed directions, collecting gems while avoiding mines and competing against an AI opponent.

The game emphasizes planning, spatial awareness, and decision-making under constraints, with different maps introducing increasing levels of difficulty.

---

## 🎮 Gameplay Overview

- The player controls a ball on a grid.
- Once a direction is chosen, the ball **slides until it hits a stop, wall, or mine**.
- Gems collected along the path increase the score.
- Hitting a mine immediately ends the game.
- The player and CPU take **alternate turns**.
- The game ends when all gems are collected or a mine is triggered.

---

## 🧠 AI Design

The CPU opponent uses **map-specific strategies**, ranging from simple greedy behavior to bounded graph search.

Implemented AI approaches include:
- Greedy gem collection
- Distance-based heuristics
- Risk-aware movement
- Pattern-based strategies (corners, center-out, spiral)
- Limited Breadth-First Search for optimal short-term planning

Each map selects an AI strategy tailored to its layout and difficulty.

---

## 🗺️ Maps & Difficulty

The game includes multiple handcrafted maps:
- Small introductory grids for learning mechanics
- Medium maps emphasizing positional control
- Large expert maps with dense hazards and strategic traps

Difficulty increases through:
- Grid size
- Mine placement
- Stop positioning
- AI aggressiveness

---

## 🖥️ Controls

**Keyboard**
- Arrow Keys / WASD – Cardinal movement
- Q / E / Z / C – Diagonal movement

**Mouse**
- Click in any direction relative to the ball to slide

---

## ⚙️ Technologies Used

- Python 3
- Tkinter (GUI)
- Deque-based BFS for AI planning
- Heuristic-based decision making

No external libraries required.

---

## 👥 Team Contributions

- **Core game logic & mechanics:** Core movement, scoring, and rules  
- **Map design & constants:** Grid layouts, obstacles, difficulty tuning  
- **AI strategies:** Heuristic design, greedy algorithms, and BFS planning  
- **GUI & animations:** Tkinter interface, rendering, and animations  

---

## ▶️ How to Run

``` bash
python inertia.py
