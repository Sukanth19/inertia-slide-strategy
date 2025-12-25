import tkinter as tk
from tkinter import messagebox, ttk
from collections import deque
import copy
import random

# Cell types
EMPTY = 0
GEM = 1
MINE = 2
STOP = 3

# Directions - now includes diagonals
UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)
UP_LEFT = (-1, -1)
UP_RIGHT = (-1, 1)
DOWN_LEFT = (1, -1)
DOWN_RIGHT = (1, 1)

ALL_DIRECTIONS = [UP, DOWN, LEFT, RIGHT, UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]
CARDINAL_DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

# Rebalanced maps with better difficulty progression
MAPS = {
    "Map 1 - Introduction": {
        "rows": 8,
        "cols": 8,
        "start": (3, 0),
        "gems": [(3, 3), (3, 5), (5, 3), (1, 3)],
        "mines": [(2, 3), (4, 3), (3, 7)],
        "stops": [(3, 6), (5, 5), (1, 5)]
    },
    "Map 2 - Corner Maze": {
        "rows": 8,
        "cols": 8,
        "start": (0, 0),
        "gems": [(0, 7), (7, 0), (7, 7), (3, 3), (4, 4)],
        "mines": [(1, 1), (6, 1), (1, 6), (6, 6)],
        "stops": [(0, 6), (6, 0), (1, 7), (7, 1), (3, 4), (4, 3)]
    },
    "Map 3 - Diamond Challenge": {
        "rows": 8,
        "cols": 8,
        "start": (4, 0),
        "gems": [(1, 3), (3, 1), (3, 5), (5, 3), (4, 7), (6, 5)],
        "mines": [(0, 0), (0, 7), (7, 0), (7, 7), (4, 4)],
        "stops": [(4, 1), (4, 6), (2, 3), (6, 3), (3, 3), (5, 5)]
    },
    "Map 4 - Cross Roads": {
        "rows": 9,
        "cols": 9,
        "start": (0, 4),
        "gems": [(2, 4), (4, 2), (4, 4), (4, 6), (6, 4), (8, 2), (8, 6)],
        "mines": [(1, 1), (1, 7), (7, 1), (7, 7), (4, 8)],
        "stops": [(3, 4), (5, 4), (4, 3), (4, 5), (6, 2), (6, 6)]
    },
    "Map 5 - Spiral Trap": {
        "rows": 9,
        "cols": 9,
        "start": (0, 0),
        "gems": [(0, 8), (8, 8), (8, 0), (4, 4), (2, 2), (6, 6)],
        "mines": [(2, 6), (6, 2), (1, 4), (7, 4), (4, 1), (4, 7)],
        "stops": [(0, 7), (7, 8), (8, 1), (1, 0), (2, 4), (6, 4), (4, 2), (4, 6)]
    },
    "Map 6 - Advanced Maze": {
        "rows": 10,
        "cols": 10,
        "start": (0, 0),
        "gems": [(0, 9), (5, 5), (9, 0), (9, 9), (2, 5), (7, 4), (4, 2), (5, 7)],
        "mines": [(2, 2), (2, 7), (7, 2), (7, 7), (4, 4), (5, 6), (3, 0), (6, 9)],
        "stops": [(0, 8), (1, 0), (5, 4), (8, 0), (9, 1), (9, 8), (4, 5), (6, 8), (2, 4), (7, 5)]
    },
    "Map 7 - Expert Grid": {
        "rows": 10,
        "cols": 10,
        "start": (5, 5),
        "gems": [(0, 0), (0, 9), (9, 0), (9, 9), (2, 5), (5, 2), (5, 7), (7, 5)],
        "mines": [(1, 1), (1, 8), (8, 1), (8, 8), (3, 3), (3, 6), (6, 3), (6, 6)],
        "stops": [(0, 5), (5, 0), (9, 5), (5, 9), (2, 2), (2, 7), (7, 2), (7, 7), (4, 5), (5, 4)]
    },
    "Map 8 - Master Challenge": {
        "rows": 12,
        "cols": 12,
        "start": (6, 0),
        "gems": [(0, 0), (0, 11), (11, 0), (11, 11), (3, 3), (8, 8), (3, 8), (8, 3)],
        "mines": [(1, 1), (1, 10), (10, 1), (10, 10), (5, 5), (6, 6)],
        "stops": [(0, 6), (6, 11), (11, 6), (6, 0), (2, 2), (9, 9), (2, 9), (9, 2), (5, 0), (6, 10)]
    }
}


class InertiaGame:
    def __init__(self, map_name="Map 1 - Introduction"):
        self.map_name = map_name
        # Map-specific AI strategies
        self.ai_strategies = {
            "Map 1 - Introduction": self._ai_strategy_cautious,
            "Map 2 - Corner Maze": self._ai_strategy_corners,
            "Map 3 - Diamond Challenge": self._ai_strategy_center_out,
            "Map 4 - Cross Roads": self._ai_strategy_cross,
            "Map 5 - Spiral Trap": self._ai_strategy_spiral,
            "Map 6 - Advanced Maze": self._ai_strategy_greedy,
            "Map 7 - Expert Grid": self._ai_strategy_optimal,
            "Map 8 - Master Challenge": self._ai_strategy_aggressive
        }
        self.reset()
    
    def reset(self):
        """Reset game to initial state"""
        map_data = MAPS[self.map_name]
        self.rows = map_data["rows"]
        self.cols = map_data["cols"]
        self.initial_pos = map_data["start"]
        
        self.board = [[EMPTY for _ in range(self.cols)] for _ in range(self.rows)]
        
        # Place gems
        for r, c in map_data["gems"]:
            self.board[r][c] = GEM
        
        # Place mines
        for r, c in map_data["mines"]:
            self.board[r][c] = MINE
        
        # Place stops
        for r, c in map_data["stops"]:
            self.board[r][c] = STOP
        
        self.ball_pos = self.initial_pos
        self.human_score = 0
        self.cpu_score = 0
        self.human_moves = 0
        self.cpu_moves = 0
        self.game_over = False
        self.human_eliminated = False
        self.cpu_eliminated = False
        self.total_gems = len(map_data["gems"])
    
    def change_map(self, map_name):
        """Change to different map"""
        self.map_name = map_name
        self.reset()
    
    def _ai_strategy_cautious(self):
        """Cautious AI - prioritizes safety, avoids risky moves"""
        best_direction = None
        best_score = -1
        best_path = []
        
        for direction in CARDINAL_DIRECTIONS:  # Only cardinal for safety
            end_pos, gems, hit_mine, path = self.simulate_move(direction)
            if not hit_mine and end_pos != self.ball_pos:
                # Score: gems collected - risk factor
                risk = len([p for p in path if self._is_near_mine(p)])
                score = gems * 10 - risk * 2
                if score > best_score:
                    best_direction = direction
                    best_score = score
                    best_path = path
        
        return best_direction, best_path
    
    def _ai_strategy_corners(self):
        """Corner-focused AI - heads to corners first"""
        corners = [(0, 0), (0, self.cols-1), (self.rows-1, 0), (self.rows-1, self.cols-1)]
        uncollected_corners = [c for c in corners if self.board[c[0]][c[1]] == GEM]
        
        if uncollected_corners:
            # Try to reach nearest corner
            target = min(uncollected_corners, key=lambda c: abs(c[0]-self.ball_pos[0]) + abs(c[1]-self.ball_pos[1]))
            return self._move_towards_target(target)
        
        return self._ai_strategy_greedy()
    
    def _ai_strategy_center_out(self):
        """Center-out AI - collects from center, then expands"""
        center = (self.rows // 2, self.cols // 2)
        
        # Find gems sorted by distance from center
        gems = [(r, c) for r in range(self.rows) for c in range(self.cols) if self.board[r][c] == GEM]
        gems_by_distance = sorted(gems, key=lambda g: abs(g[0]-center[0]) + abs(g[1]-center[1]))
        
        if gems_by_distance:
            return self._move_towards_target(gems_by_distance[0])
        
        return None, []
    
    def _ai_strategy_cross(self):
        """Cross pattern AI - follows cross lines"""
        mid_row = self.rows // 2
        mid_col = self.cols // 2
        
        # Prefer moves along cross lines
        best_direction = None
        best_score = -1
        best_path = []
        
        for direction in ALL_DIRECTIONS:
            end_pos, gems, hit_mine, path = self.simulate_move(direction)
            if not hit_mine and end_pos != self.ball_pos:
                score = gems * 10
                # Bonus for staying on cross lines
                if end_pos[0] == mid_row or end_pos[1] == mid_col:
                    score += 5
                if score > best_score:
                    best_direction = direction
                    best_score = score
                    best_path = path
        
        return best_direction, best_path
    
    def _ai_strategy_spiral(self):
        """Spiral AI - moves in spiral pattern from outside to inside"""
        # Prioritize outer gems first
        gems = [(r, c) for r in range(self.rows) for c in range(self.cols) if self.board[r][c] == GEM]
        center = (self.rows / 2, self.cols / 2)
        
        # Sort by distance from center (descending)
        outer_gems = sorted(gems, key=lambda g: abs(g[0]-center[0]) + abs(g[1]-center[1]), reverse=True)
        
        if outer_gems:
            return self._move_towards_target(outer_gems[0])
        
        return None, []
    
    def _ai_strategy_greedy(self):
        """Greedy AI - always takes move with most gems"""
        best_direction = None
        best_gems = 0
        best_path = []
        
        for direction in ALL_DIRECTIONS:
            end_pos, gems, hit_mine, path = self.simulate_move(direction)
            if not hit_mine and end_pos != self.ball_pos:
                if gems > best_gems or (gems == best_gems and best_direction is None):
                    best_direction = direction
                    best_gems = gems
                    best_path = path
        
        return best_direction, best_path
    
    def _ai_strategy_optimal(self):
        """Optimal AI - uses BFS to find best path"""
        start_state = (self.ball_pos, frozenset(), [])
        queue = deque([start_state])
        visited = {(self.ball_pos, frozenset())}
        
        target_gems = frozenset(
            (r, c) for r in range(self.rows) for c in range(self.cols)
            if self.board[r][c] == GEM
        )
        
        # Limited BFS for next few moves
        for _ in range(500):  # Limit iterations
            if not queue:
                break
                
            pos, collected, moves = queue.popleft()
            
            if len(moves) >= 3:  # Look ahead 3 moves
                continue
            
            for direction in ALL_DIRECTIONS:
                end_pos, gems_on_path, hit_mine, path = self._simulate_move_from(pos, direction, collected)
                
                if hit_mine or end_pos == pos:
                    continue
                
                new_collected = collected | gems_on_path
                
                if len(moves) == 0 and len(gems_on_path) > 0:
                    # Return first move that collects gems
                    return direction, path
                
                state = (end_pos, new_collected)
                if state not in visited:
                    visited.add(state)
                    queue.append((end_pos, new_collected, moves + [direction]))
        
        # Fallback to greedy
        return self._ai_strategy_greedy()
    
    def _ai_strategy_aggressive(self):
        """Aggressive AI - uses diagonals and takes risks"""
        best_direction = None
        best_score = -1
        best_path = []
        
        for direction in ALL_DIRECTIONS:  # All 8 directions
            end_pos, gems, hit_mine, path = self.simulate_move(direction)
            if not hit_mine and end_pos != self.ball_pos:
                # Aggressive scoring - prioritize gems heavily
                score = gems * 15 + len(path)  # Bonus for longer moves
                if score > best_score:
                    best_direction = direction
                    best_score = score
                    best_path = path
        
        return best_direction, best_path
    
    def _is_near_mine(self, pos):
        """Check if position is adjacent to a mine"""
        r, c = pos
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    if self.board[nr][nc] == MINE:
                        return True
        return False
    
    def _move_towards_target(self, target):
        """Find best move towards a target position"""
        best_direction = None
        best_distance = float('inf')
        best_path = []
        
        for direction in ALL_DIRECTIONS:
            end_pos, gems, hit_mine, path = self.simulate_move(direction)
            if not hit_mine and end_pos != self.ball_pos:
                distance = abs(end_pos[0] - target[0]) + abs(end_pos[1] - target[1])
                score = distance - gems * 100  # Heavily prioritize gems
                if score < best_distance:
                    best_direction = direction
                    best_distance = score
                    best_path = path
        
        return best_direction, best_path
    
    def _simulate_move_from(self, start_pos, direction, already_collected):
        """
        Simulate a move from given position, considering already collected gems.
        Returns: (end_pos, new_gems_set, hit_mine, path)
        """
        dr, dc = direction
        r, c = start_pos
        gems_on_path = set()
        path = [(r, c)]
        hit_mine = False
        
        while True:
            next_r, next_c = r + dr, c + dc
            
            if next_r < 0 or next_r >= self.rows or next_c < 0 or next_c >= self.cols:
                break
            
            r, c = next_r, next_c
            path.append((r, c))
            
            if self.board[r][c] == GEM and (r, c) not in already_collected:
                gems_on_path.add((r, c))
            elif self.board[r][c] == MINE:
                hit_mine = True
                break
            elif self.board[r][c] == STOP:
                break
        
        return (r, c), frozenset(gems_on_path), hit_mine, path
    
    def simulate_move(self, direction):
        """
        Simulate a slide in given direction from current position.
        Returns: (end_pos, gems_collected, hit_mine, path)
        """
        dr, dc = direction
        r, c = self.ball_pos
        gems = 0
        path = [(r, c)]
        hit_mine = False
        
        while True:
            next_r, next_c = r + dr, c + dc
            
            if next_r < 0 or next_r >= self.rows or next_c < 0 or next_c >= self.cols:
                break
            
            r, c = next_r, next_c
            path.append((r, c))
            
            if self.board[r][c] == GEM:
                gems += 1
            elif self.board[r][c] == MINE:
                hit_mine = True
                break
            elif self.board[r][c] == STOP:
                break
        
        return (r, c), gems, hit_mine, path
    
    def make_move(self, direction, is_human=True):
        """
        Execute a move for human or CPU.
        Returns: (success, gems_collected, path, hit_mine)
        """
        if self.game_over:
            return False, 0, [], False
        
        end_pos, gems, hit_mine, path = self.simulate_move(direction)
        
        # If hit mine, player is eliminated
        if hit_mine:
            if is_human:
                self.human_eliminated = True
            else:
                self.cpu_eliminated = True
            self.game_over = True
            return False, 0, path, True
        
        if end_pos == self.ball_pos:
            return False, 0, [], False
        
        self.ball_pos = end_pos
        
        if is_human:
            self.human_moves += 1
        else:
            self.cpu_moves += 1
        
        # Collect gems along path
        for r, c in path[1:]:
            if self.board[r][c] == GEM:
                self.board[r][c] = EMPTY
                if is_human:
                    self.human_score += 1
                else:
                    self.cpu_score += 1
        
        # Check win condition
        if self.human_score + self.cpu_score >= self.total_gems:
            self.game_over = True
        
        return True, gems, path, False
    
    def get_cpu_move(self):
        """
        Get CPU move using map-specific strategy.
        """
        # Use the AI strategy specific to this map
        strategy_func = self.ai_strategies.get(self.map_name, self._ai_strategy_greedy)
        return strategy_func()


class InertiaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Inertia - Slide & Collect")
        self.root.configure(bg="#1a1a2e")
        
        # Start with random map
        random_map = random.choice(list(MAPS.keys()))
        self.game = InertiaGame(random_map)
        self.cell_size = 60
        self.animating = False
        self.waiting_for_cpu = False
        
        self._create_widgets()
        self._bind_keys()
        self.draw_board()
    
    def _create_widgets(self):
        """Create UI widgets with modern styling"""
        # Title bar
        title_frame = tk.Frame(self.root, bg="#16213e", pady=15)
        title_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            title_frame, 
            text="⚡ INERTIA ⚡", 
            font=("Arial", 28, "bold"),
            fg="#00d4ff",
            bg="#16213e"
        )
        title_label.pack()
        
        subtitle = tk.Label(
            title_frame,
            text="Slide across the grid and collect all gems before the CPU!",
            font=("Arial", 10),
            fg="#a8dadc",
            bg="#16213e"
        )
        subtitle.pack()
        
        # Control panel
        control_frame = tk.Frame(self.root, bg="#1a1a2e", pady=10)
        control_frame.pack()
        
        # Current map display
        map_frame = tk.Frame(control_frame, bg="#1a1a2e")
        map_frame.pack(side=tk.LEFT, padx=10)
        
        tk.Label(
            map_frame, 
            text="Current Map:", 
            font=("Arial", 11, "bold"),
            fg="#ffffff",
            bg="#1a1a2e"
        ).pack(side=tk.LEFT, padx=5)
        
        self.map_label = tk.Label(
            map_frame,
            text=self.game.map_name,
            font=("Arial", 11),
            fg="#00d4ff",
            bg="#1a1a2e"
        )
        self.map_label.pack(side=tk.LEFT, padx=5)
        
        # New Game button (random map)
        new_game_btn = tk.Button(
            control_frame,
            text="🎲 New Game",
            command=self.new_random_game,
            font=("Arial", 11, "bold"),
            bg="#4CAF50",
            fg="white",
            activebackground="#45a049",
            activeforeground="white",
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor="hand2"
        )
        new_game_btn.pack(side=tk.LEFT, padx=10)
        
        # Restart button with modern styling
        restart_btn = tk.Button(
            control_frame,
            text="🔄 Restart",
            command=self.restart_game,
            font=("Arial", 11, "bold"),
            bg="#e94560",
            fg="white",
            activebackground="#c23550",
            activeforeground="white",
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor="hand2"
        )
        restart_btn.pack(side=tk.LEFT, padx=10)
        
        # Score panel with gradient-like effect
        score_frame = tk.Frame(self.root, bg="#16213e", pady=15)
        score_frame.pack(fill=tk.X, padx=20)
        
        self.info_label = tk.Label(
            score_frame,
            text="",
            font=("Arial", 12, "bold"),
            fg="#00d4ff",
            bg="#16213e",
            pady=10
        )
        self.info_label.pack()
        
        # Canvas frame with border
        canvas_container = tk.Frame(self.root, bg="#0f3460", padx=3, pady=3)
        canvas_container.pack(pady=10)
        
        self.canvas = tk.Canvas(
            canvas_container,
            bg="#e8f4f8",
            highlightthickness=0
        )
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.mouse_click)
        
        # Instructions with better styling
        inst_frame = tk.Frame(self.root, bg="#1a1a2e", pady=10)
        inst_frame.pack()
        
        instructions = [
            ("🎮 Controls:", "#00d4ff", "bold"),
            ("Arrow Keys / WASD", "#ffffff", "normal"),
            ("or", "#a8dadc", "normal"),
            ("Click/Drag Mouse", "#ffffff", "normal"),
            ("(8 Directions!)", "#00d4ff", "normal")
        ]
        
        for text, color, weight in instructions:
            tk.Label(
                inst_frame,
                text=text,
                font=("Arial", 9, weight),
                fg=color,
                bg="#1a1a2e"
            ).pack(side=tk.LEFT, padx=3)
        
        # Legend
        legend_frame = tk.Frame(self.root, bg="#16213e", pady=10)
        legend_frame.pack(fill=tk.X, padx=20)
        
        legend_items = [
            ("💎 Gem", "#00aaff"),
            ("❌ Mine", "#ff0000"),
            ("🛑 Stop", "#666666"),
            ("⚫ Ball", "#4a4a4a")
        ]
        
        for text, color in legend_items:
            item_frame = tk.Frame(legend_frame, bg="#16213e")
            item_frame.pack(side=tk.LEFT, padx=15)
            tk.Label(
                item_frame,
                text=text,
                font=("Arial", 9),
                fg=color,
                bg="#16213e"
            ).pack()
    
    def _bind_keys(self):
        """Bind keyboard controls including diagonals"""
        # Arrow keys
        self.root.bind("<Up>", lambda e: self.human_move(UP))
        self.root.bind("<Down>", lambda e: self.human_move(DOWN))
        self.root.bind("<Left>", lambda e: self.human_move(LEFT))
        self.root.bind("<Right>", lambda e: self.human_move(RIGHT))
        
        # WASD
        self.root.bind("w", lambda e: self.human_move(UP))
        self.root.bind("s", lambda e: self.human_move(DOWN))
        self.root.bind("a", lambda e: self.human_move(LEFT))
        self.root.bind("d", lambda e: self.human_move(RIGHT))
        
        # Diagonals with QE ZC
        self.root.bind("q", lambda e: self.human_move(UP_LEFT))
        self.root.bind("e", lambda e: self.human_move(UP_RIGHT))
        self.root.bind("z", lambda e: self.human_move(DOWN_LEFT))
        self.root.bind("c", lambda e: self.human_move(DOWN_RIGHT))
        
        # Numpad diagonals
        self.root.bind("<Home>", lambda e: self.human_move(UP_LEFT))     # 7
        self.root.bind("<Prior>", lambda e: self.human_move(UP_RIGHT))   # 9
        self.root.bind("<End>", lambda e: self.human_move(DOWN_LEFT))    # 1
        self.root.bind("<Next>", lambda e: self.human_move(DOWN_RIGHT))  # 3
    
    def mouse_click(self, event):
        """Handle mouse click with 8-directional movement"""
        if self.animating or self.waiting_for_cpu or self.game.game_over:
            return
        
        # Convert click to grid coordinates
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        
        if row < 0 or row >= self.game.rows or col < 0 or col >= self.game.cols:
            return
        
        ball_r, ball_c = self.game.ball_pos
        
        # Determine direction (including diagonals)
        dr = row - ball_r
        dc = col - ball_c
        
        direction = None
        
        # Determine the best direction based on click position
        if dr == 0 and dc == 0:
            return  # Clicked on ball
        
        # Check for diagonal movement
        if abs(dr) > 0 and abs(dc) > 0:
            # Diagonal movement
            dir_r = DOWN if dr > 0 else UP
            dir_c = RIGHT if dc > 0 else LEFT
            direction = (dir_r[0] + dir_c[0], dir_r[1] + dir_c[1])
        elif abs(dr) > abs(dc):
            # Vertical movement
            direction = DOWN if dr > 0 else UP
        elif abs(dc) > abs(dr):
            # Horizontal movement
            direction = RIGHT if dc > 0 else LEFT
        else:
            # Equal distance, prefer horizontal
            if dc != 0:
                direction = RIGHT if dc > 0 else LEFT
            elif dr != 0:
                direction = DOWN if dr > 0 else UP
        
        if direction:
            self.human_move(direction)
    
    def draw_board(self):
        """Draw the game board with enhanced visuals"""
        self.canvas.delete("all")
        
        # Adjust canvas size
        canvas_width = self.game.cols * self.cell_size
        canvas_height = self.game.rows * self.cell_size
        self.canvas.config(width=canvas_width, height=canvas_height)
        
        # Draw checkered background
        for r in range(self.game.rows):
            for c in range(self.game.cols):
                x = c * self.cell_size
                y = r * self.cell_size
                color = "#f0f8ff" if (r + c) % 2 == 0 else "#e1f0fa"
                self.canvas.create_rectangle(
                    x, y, x + self.cell_size, y + self.cell_size,
                    fill=color, outline=""
                )
        
        # Draw grid lines
        for i in range(self.game.rows + 1):
            y = i * self.cell_size
            self.canvas.create_line(0, y, canvas_width, y, fill="#c0d8e8", width=1)
        
        for j in range(self.game.cols + 1):
            x = j * self.cell_size
            self.canvas.create_line(x, 0, x, canvas_height, fill="#c0d8e8", width=1)
        
        # Draw cells with enhanced graphics
        for r in range(self.game.rows):
            for c in range(self.game.cols):
                x = c * self.cell_size
                y = r * self.cell_size
                cx, cy = x + self.cell_size // 2, y + self.cell_size // 2
                
                if self.game.board[r][c] == GEM:
                    # Enhanced gem with glow effect
                    size = self.cell_size // 3
                    # Glow
                    self.canvas.create_oval(
                        cx - size - 3, cy - size - 3,
                        cx + size + 3, cy + size + 3,
                        fill="#80d4ff", outline=""
                    )
                    # Diamond shape
                    self.canvas.create_polygon(
                        cx, cy - size,
                        cx + size, cy,
                        cx, cy + size,
                        cx - size, cy,
                        fill="#00aaff", outline="#0088cc", width=2
                    )
                    # Highlight
                    self.canvas.create_polygon(
                        cx, cy - size,
                        cx + size//2, cy - size//2,
                        cx, cy,
                        cx - size//2, cy - size//2,
                        fill="#66ccff", outline=""
                    )
                    
                elif self.game.board[r][c] == MINE:
                    # Enhanced mine with danger symbol
                    margin = self.cell_size // 5
                    # Red circle background
                    self.canvas.create_oval(
                        cx - margin * 1.5, cy - margin * 1.5,
                        cx + margin * 1.5, cy + margin * 1.5,
                        fill="#ff3333", outline="#cc0000", width=2
                    )
                    # X mark
                    m = margin
                    self.canvas.create_line(
                        cx - m, cy - m, cx + m, cy + m,
                        fill="white", width=3
                    )
                    self.canvas.create_line(
                        cx + m, cy - m, cx - m, cy + m,
                        fill="white", width=3
                    )
                    
                elif self.game.board[r][c] == STOP:
                    # Enhanced stop sign
                    radius = self.cell_size // 3
                    # Octagon shape
                    points = []
                    for i in range(8):
                        angle = i * 3.14159 * 2 / 8
                        px = cx + radius * 0.9 * (1 if i % 2 == 0 else 0.7) * (1 if i < 4 else -1) * abs(((i + 1) % 4 - 1.5))
                        py = cy + radius * 0.9 * (1 if i % 2 == 0 else 0.7) * (1 if 1 <= i < 5 else -1) * abs(((i - 0.5) % 4 - 1.5))
                    
                    self.canvas.create_oval(
                        cx - radius, cy - radius,
                        cx + radius, cy + radius,
                        fill="#ff6b6b", outline="#cc0000", width=3
                    )
                    self.canvas.create_rectangle(
                        cx - radius * 0.6, cy - radius * 0.15,
                        cx + radius * 0.6, cy + radius * 0.15,
                        fill="white", outline=""
                    )
        
        # Draw ball with 3D effect
        if self.game.ball_pos:
            r, c = self.game.ball_pos
            x = c * self.cell_size
            y = r * self.cell_size
            cx, cy = x + self.cell_size // 2, y + self.cell_size // 2
            radius = self.cell_size // 3
            
            # Shadow
            self.canvas.create_oval(
                cx - radius + 2, cy - radius + 2,
                cx + radius + 2, cy + radius + 2,
                fill="#b0b0b0", outline="", tags="ball"
            )
            # Main ball
            self.canvas.create_oval(
                cx - radius, cy - radius,
                cx + radius, cy + radius,
                fill="#2a2a2a", outline="#000000", width=2, tags="ball"
            )
            # Highlight for 3D effect
            self.canvas.create_oval(
                cx - radius * 0.6, cy - radius * 0.6,
                cx - radius * 0.2, cy - radius * 0.2,
                fill="#5a5a5a", outline="", tags="ball"
            )
        
        self.update_info()
    
    def update_info(self):
        """Update information display with better formatting"""
        remaining = self.game.total_gems - self.game.human_score - self.game.cpu_score
        info = (f"👤 You: {self.game.human_score} gems ({self.game.human_moves} moves)  |  "
                f"🤖 CPU: {self.game.cpu_score} gems ({self.game.cpu_moves} moves)  |  "
                f"💎 Remaining: {remaining}")
        self.info_label.config(text=info)
    
    def animate_move(self, path, callback):
        """Animate ball sliding along path with smoother animation"""
        if len(path) <= 1:
            callback()
            return
        
        self.animating = True
        self._animate_step(path, 0, callback)
    
    def _animate_step(self, path, index, callback):
        """Single animation step with improved visuals"""
        if index >= len(path):
            self.animating = False
            callback()
            return
        
        r, c = path[index]
        x = c * self.cell_size
        y = r * self.cell_size
        cx, cy = x + self.cell_size // 2, y + self.cell_size // 2
        
        self.canvas.delete("ball")
        
        radius = self.cell_size // 3
        
        # Shadow
        self.canvas.create_oval(
            cx - radius + 2, cy - radius + 2,
            cx + radius + 2, cy + radius + 2,
            fill="#b0b0b0", outline="", tags="ball"
        )
        # Main ball
        self.canvas.create_oval(
            cx - radius, cy - radius,
            cx + radius, cy + radius,
            fill="#2a2a2a", outline="#000000", width=2, tags="ball"
        )
        # Highlight
        self.canvas.create_oval(
            cx - radius * 0.6, cy - radius * 0.6,
            cx - radius * 0.2, cy - radius * 0.2,
            fill="#5a5a5a", outline="", tags="ball"
        )
        
        self.root.after(80, lambda: self._animate_step(path, index + 1, callback))
    
    def human_move(self, direction):
        """Handle human move"""
        if self.animating or self.waiting_for_cpu or self.game.game_over:
            return
        
        success, gems, path, hit_mine = self.game.make_move(direction, is_human=True)
        
        if hit_mine:
            # Player hit a mine - show explosion and end game
            self.animate_move(path, lambda: self.show_mine_hit("human"))
            return
        
        if not success:
            return
        
        self.animate_move(path, self.cpu_move)
    
    def cpu_move(self):
        """Handle CPU move"""
        self.draw_board()
        
        if self.game.game_over:
            self.show_game_over()
            return
        
        self.waiting_for_cpu = True
        
        direction, path = self.game.get_cpu_move()
        
        if direction is None:
            self.waiting_for_cpu = False
            if self.game.human_score + self.game.cpu_score < self.game.total_gems:
                messagebox.showinfo("CPU Stuck", "CPU has no valid moves! You win!")
            self.show_game_over()
            return
        
        success, gems, path, hit_mine = self.game.make_move(direction, is_human=False)
        
        if hit_mine:
            # CPU hit a mine - you win!
            def after_cpu_mine():
                self.draw_board()
                self.waiting_for_cpu = False
                self.show_mine_hit("cpu")
            
            self.root.after(400, lambda: self.animate_move(path, after_cpu_mine))
            return
        
        def after_cpu_move():
            self.draw_board()
            self.waiting_for_cpu = False
            if self.game.game_over:
                self.show_game_over()
        
        self.root.after(400, lambda: self.animate_move(path, after_cpu_move))
    
    def show_game_over(self):
        """Show game over message with better formatting"""
        if not self.game.game_over and self.game.human_score + self.game.cpu_score < self.game.total_gems:
            return
        
        # Check for mine elimination
        if self.game.human_eliminated:
            winner = "💥 You Hit a Mine! CPU Wins! 💥"
            color = "red"
        elif self.game.cpu_eliminated:
            winner = "💥 CPU Hit a Mine! You Win! 💥"
            color = "green"
        elif self.game.human_score > self.game.cpu_score:
            winner = "🎉 You Win! 🎉"
            color = "green"
        elif self.game.cpu_score > self.game.human_score:
            winner = "🤖 CPU Wins!"
            color = "red"
        else:
            winner = "🤝 It's a Tie!"
            color = "blue"
        
        efficiency_human = self.game.human_score / max(self.game.human_moves, 1)
        efficiency_cpu = self.game.cpu_score / max(self.game.cpu_moves, 1)
        
        msg = (f"{winner}\n\n"
               f"👤 You: {self.game.human_score} gems in {self.game.human_moves} moves "
               f"(Efficiency: {efficiency_human:.2f})\n"
               f"🤖 CPU: {self.game.cpu_score} gems in {self.game.cpu_moves} moves "
               f"(Efficiency: {efficiency_cpu:.2f})\n\n"
               f"Click 'New Game' for a random map!")
        
        messagebox.showinfo("Game Over", msg)
    
    def show_mine_hit(self, who):
        """Show mine hit explosion"""
        if who == "human":
            msg = "💥 BOOM! You hit a mine!\n\nCPU wins this round!"
        else:
            msg = "💥 BOOM! CPU hit a mine!\n\nYou win this round!"
        
        messagebox.showinfo("Mine Hit!", msg)
        self.show_game_over()
    
    def new_random_game(self):
        """Start a new game with a random map"""
        random_map = random.choice(list(MAPS.keys()))
        self.game.change_map(random_map)
        self.animating = False
        self.waiting_for_cpu = False
        self.map_label.config(text=random_map)
        self.draw_board()
    
    def restart_game(self):
        """Restart current map"""
        self.game.reset()
        self.animating = False
        self.waiting_for_cpu = False
        self.draw_board()


def main():
    root = tk.Tk()
    app = InertiaGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
