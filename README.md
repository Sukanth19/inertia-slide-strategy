# ⚡ Inertia – Intelligent Grid Strategy Game

Inertia is a grid-based strategy game built around inertia-style movement mechanics, where the player slides continuously in a chosen direction until an obstacle is hit. The objective is to collect gems efficiently while avoiding mines and competing against an AI opponent that uses advanced algorithmic decision-making.

This project combines game mechanics with algorithm design, featuring a hybrid AI powered by **Divide & Conquer, Dynamic Programming, and Recursive Search**.

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

## 🧠 AI System (Final Architecture)

The CPU uses a hybrid intelligent solver that integrates Divide & Conquer, Dynamic Programming, and recursive decision search instead of simple greedy or BFS logic.

### 🔷 1. Divide & Conquer – Gem Clustering
- Remaining gems are recursively divided into spatial clusters
- Clustering is based on row and column variance
- Reduces search complexity and improves decision focus
- Helps the AI prioritize strategic gem regions instead of brute-force exploration

---

### 🔷 2. Dynamic Programming – Memoized State Search

The AI uses **Top-Down Dynamic Programming (Memoization)** where each state is defined as:

```
(state) = (ball_position, collected_gems_set)
```

Why this is important:
- Avoids recomputing previously explored states
- Handles overlapping subproblems efficiently
- Optimizes long-term decision making

Key DP Features:
- Hash-based memoization table
- State validation and caching
- Goal state detection (all gems collected)
- Efficient state transitions

---

### 🔷 3. Recursive Depth-Limited Solver (Conquer Phase)

The solver performs bounded recursive search:
- Simulates all 8-direction sliding moves
- Evaluates future outcomes recursively
- Uses depth-limited planning for performance
- Selects the move that maximizes long-term gem collection

This makes the AI **strategic**, not greedy.

---

### 🔷 4. Heuristic Move Prioritization

Move ordering is optimized using:
- Immediate gem collection value
- Distance to nearest gem cluster (Manhattan distance)
- Mine avoidance checks
- Valid path simulation

This significantly reduces unnecessary branching while maintaining strong decision quality.

---

## 🗺️ Maps & Difficulty Scaling

The game includes multiple handcrafted maps with progressive difficulty:

| Level Type | Characteristics |
|------------|-----------------|
| Beginner | Small grids and simple layouts |
| Intermediate | Strategic stops and traps |
| Advanced | Dense hazards and complex paths |
| Expert | Large grids with multi-cluster gem distribution |

Difficulty increases through:
- Grid size
- Mine placement density
- Stop cell positioning
- Strategic gem layouts
- Larger decision search space for the AI

---

## ⚙️ Core Game Mechanics

- 8-direction movement (Cardinal + Diagonal)
- Continuous inertia-based sliding system
- Turn-based Human vs CPU gameplay
- Dynamic board updates after gem collection
- Mine-trigger elimination system
- Animated movement rendering
- Score and efficiency tracking

---

## 🎮 Controls

### ⌨️ Keyboard
- Arrow Keys / WASD → Cardinal Movement  
- Q / E / Z / C → Diagonal Movement (8 directions)

### 🖱️ Mouse
- Click relative to the ball’s position to slide in that direction

---

## 🧩 Algorithmic Design Summary

| Module | Responsibility | Algorithm Concept |
|--------|---------------|-------------------|
| GemDivider | Spatial gem clustering | Divide & Conquer |
| ClusterConqueror | Move simulation & evaluation | Heuristic + Simulation |
| DPStateManager | State memoization | Dynamic Programming |
| RecursiveSolver | Decision engine | DP + Recursive Search |
| InertiaGame | Core game logic | State Management |
| InertiaGUI | Rendering & animations | Tkinter GUI |

---

## 💻 Technologies Used

- Python 3
- Tkinter (GUI & Animations)
- Object-Oriented Programming (OOP)
- Recursive Algorithms
- Memoization (Dynamic Programming)
- Heuristic Search Optimization

No external libraries are required.

---

## 🏗️ Project Structure

```
inertia.py
│
├── GemDivider          # Divide & Conquer clustering
├── ClusterConqueror    # Move simulation engine
├── DPStateManager      # Memoization & DP state handling
├── RecursiveSolver     # Hybrid AI solver (D&C + DP)
├── InertiaGame         # Core game mechanics
└── InertiaGUI          # GUI, animation, and controls
```

---

## 🚀 How to Run

```bash
python inertia.py
```

### Requirements
- Python 3.x
- No external dependencies

---

## 📊 Academic Relevance (DAA)

This project demonstrates applied algorithm design using:
- Divide & Conquer (problem decomposition via clustering)
- Dynamic Programming (memoized state-space optimization)
- Recursive search with heuristic pruning
- State-space exploration under constrained movement

The hybrid approach reduces exponential branching while maintaining strong strategic decision quality, making it suitable for:
- Design and Analysis of Algorithms (DAA)
- Game AI
- Intelligent Search Systems

---

## 🏆 Highlights

- Hybrid Divide & Conquer + Dynamic Programming AI
- Modular algorithmic architecture
- Fully animated Tkinter GUI
- Multi-map difficulty scaling
- Efficient memoized decision engine
- Zero external libraries
