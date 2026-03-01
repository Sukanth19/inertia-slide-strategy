# ⚡ Inertia – Intelligent Grid Strategy Game

Inertia is a grid-based strategy game built around inertia-style movement mechanics, where the player slides continuously in a chosen direction until an obstacle is hit. The objective is to collect gems efficiently while avoiding mines and competing against an AI opponent that uses advanced algorithmic decision-making.

This project combines game mechanics with algorithm design, featuring three selectable AI modes powered by **Greedy, Divide & Conquer, and Dynamic Programming**.

---

## 🎮 Gameplay Overview

- Control a ball on a 2D grid
- Choose a direction → the ball **slides until it hits a wall, stop, or mine**
- Gems collected along the path increase your score
- Hitting a mine results in immediate elimination
- Player and CPU take **alternate turns**
- Game ends when:
  - All gems are collected, or
  - A mine is triggered

The core challenge is planning optimal sliding paths under constrained movement.

---

## 🖥️ Project Structure

The project is split into two files for clean separation of concerns:

```
inertia-slide-strategy/
│
├── inertia_core.py     # All game logic, board, physics, and AI algorithms
└── inertia_ui.py       # Vesper-themed Tkinter GUI, menus, animations
```

| File | Responsibility |
|------|---------------|
| `inertia_core.py` | Board, tile types, sliding physics, all 3 AI classes, `GameState` API |
| `inertia_ui.py` | Start menu, HUD, board canvas, animations, algo picker popup |

---

## 🧠 AI Algorithms

Three selectable AI modes are available from the **start menu** or **mid-game** via the ⚙ Algo button.

### ⚡ 1. Greedy AI
- Always picks the move that collects the most gems **immediately**
- No lookahead or future planning
- Fastest decision speed
- Weakest long-term strategy

**Time:** `O(8)` per move | **Space:** `O(1)`

---

### 🌳 2. Divide & Conquer AI — Pure D&C

**TRUE Divide & Conquer structure:**

| Phase | What Happens |
|-------|-------------|
| **Divide** | Remaining gem set is split into two spatial halves by median row or column (whichever axis has greater variance) |
| **Conquer** | Each half is solved **independently and recursively** — base case is a single gem, solved by direct slide scoring |
| **Combine** | Both halves' recommended first moves are compared; the higher-scoring one is selected |

This is genuine D&C — the gem set is the input being recursively split, each sub-problem is solved in isolation, and results are merged.

**Time:** `O(8 · log n)` per move | **Space:** `O(n)`

---

### 🧮 3. Dynamic Programming AI — Pure DP

**TRUE Dynamic Programming structure:**

```
State   = (ball_position, frozenset_of_remaining_gems)
dp[s]   = max gems collectable from state s onwards
```

**Recurrence:**
```
dp[(pos, R)] = 0                                        if R is empty
dp[(pos, R)] = max over all moves d of:
                 |gems_collected(d)| + dp[(new_pos, R − collected)]
```

Key properties:
- **Optimal substructure** — best play from state S uses best play from each next state (Bellman principle)
- **Overlapping subproblems** — same `(pos, R)` reachable via multiple move sequences; computed once, reused via hash table
- **Memo lifetime** — table is built once per turn across ALL recursive calls, never cleared mid-expansion
- **No depth cap** — explores all reachable states (bounded by `MAX_GEMS_FOR_DP = 12` for tractability on large maps)

**Time:** `O(8 · 2^n)` | **Space:** `O(pos · 2^n)`

---

### 📊 Algorithm Comparison

| Algorithm | Time Complexity | Space | Speed | Quality |
|-----------|----------------|-------|-------|---------|
| Greedy | O(8) | O(1) | ⚡ Fastest | ★☆☆ Weakest |
| Divide & Conquer | O(8 · log n) | O(n) | 🔥 Fast | ★★☆ Strong |
| Dynamic Programming | O(8 · 2^n) | O(pos · 2^n) | 🐢 Slow | ★★★ Optimal |

---

## 🗺️ Maps & Difficulty Scaling

8 handcrafted maps with progressive difficulty:

| Map | Grid | Difficulty |
|-----|------|------------|
| Map 1 – Introduction | 8×8 | Beginner |
| Map 2 – Corner Maze | 8×8 | Beginner |
| Map 3 – Diamond Challenge | 8×8 | Intermediate |
| Map 4 – Cross Roads | 9×9 | Intermediate |
| Map 5 – Spiral Trap | 9×9 | Advanced |
| Map 6 – Advanced Maze | 10×10 | Advanced |
| Map 7 – Expert Grid | 10×10 | Expert |
| Map 8 – Master Challenge | 12×12 | Expert |

Difficulty increases through grid size, mine density, stop placement, and gem distribution complexity.

---

## ⚙️ Core Game Mechanics

- 8-direction movement (Cardinal + Diagonal)
- Continuous inertia-based sliding physics
- Turn-based Human vs CPU gameplay
- Dynamic board updates after gem collection
- Mine-trigger elimination
- Animated ball movement
- Score, move count, and efficiency tracking per player

---

## 🎨 UI – Vesper Theme

The UI uses the **Vesper colour palette** throughout:

| Role | Colour |
|------|--------|
| Background | `#1e1e2e` deep navy |
| Surface / cards | `#2a2a3e` |
| Accent – purple | `#c792ea` (titles, AI label) |
| Accent – cyan | `#89ddff` (gems, headings) |
| Accent – green | `#c3e88d` (ball, you score) |
| Accent – red | `#f07178` (mines, CPU score) |
| Accent – orange | `#ffcb6b` (stop tiles) |
| Text | `#cdd6f4` |
| Muted | `#6c7086` |

### UI Screens
- **Start Menu** — map selector, algorithm selector, legend, algorithm comparison table
- **Game View** — live HUD with scores/efficiency, animated board, status bar
- **⚙ Algo Picker** — mid-game popup to switch AI without restarting
- **Game Over Overlay** — winner, per-player stats, play again / menu buttons

---

## 🎮 Controls

### ⌨️ Keyboard
| Keys | Direction |
|------|-----------|
| `↑` / `W` | Up |
| `↓` / `S` | Down |
| `←` / `A` | Left |
| `→` / `D` | Right |
| `Q` | Up-Left (diagonal) |
| `E` | Up-Right (diagonal) |
| `Z` | Down-Left (diagonal) |
| `C` | Down-Right (diagonal) |

### 🖱️ Mouse
Click anywhere on the board — direction is inferred from the click position relative to the ball.

---

## 🚀 How to Run

```bash
# Clone the repo
git clone https://github.com/Sukanth19/inertia-slide-strategy.git
cd inertia-slide-strategy

# Run the game (no dependencies needed)
python inertia_ui.py
```

### Requirements
- Python 3.x
- No external libraries — uses only the standard `tkinter` module

---

## 📊 Academic Relevance (DAA)

This project demonstrates applied algorithm design:

| Concept | Implementation |
|---------|---------------|
| Divide & Conquer | Recursive gem-set splitting, independent subproblem solving, result merging |
| Dynamic Programming | Bellman recurrence over `(pos, remaining_gems)` state space, hash-table memoization |
| Greedy Algorithms | Immediate-reward maximisation baseline for comparison |
| Heuristic Search | Manhattan distance proximity scoring for move ordering |
| State-Space Exploration | Constrained 8-direction sliding under obstacle rules |

Suitable for: **Design & Analysis of Algorithms (DAA)**, Game AI, Intelligent Search Systems.

---

## 🏆 Highlights

- Three selectable AI algorithms (Greedy / D&C / DP) — swappable mid-game
- Pure Divide & Conquer: real divide → conquer → combine structure
- Pure Dynamic Programming: Bellman recurrence, overlapping subproblems, no depth cap
- Vesper-themed Tkinter UI with smooth animations
- Clean two-file architecture (core logic vs UI)
- 8 handcrafted maps across 4 difficulty tiers
- Zero external dependencies
