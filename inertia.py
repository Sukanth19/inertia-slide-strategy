
import tkinter as tk
from tkinter import messagebox
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

# Maps
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


# ==================== SUKANT'S MODULE - COMPLETE ✅ ====================

class GemDivider:
    """SUKANT - Divide Phase ✅ COMPLETE"""
    
    def __init__(self, game, min_cluster_size=2):
        self.game = game
        self.min_cluster_size = min_cluster_size
        self.clusters_created = 0
    
    def get_remaining_gems(self):
        gems = set()
        for r in range(self.game.rows):
            for c in range(self.game.cols):
                if self.game.board[r][c] == GEM:
                    gems.add((r, c))
        return frozenset(gems)
    
    def divide_gems_into_clusters(self, gems):
        self.clusters_created = 0
        clusters = self._recursive_divide(gems, depth=0)
        return clusters
    
    def _recursive_divide(self, gems, depth):
        if len(gems) <= self.min_cluster_size or depth > 3:
            if len(gems) > 0:
                self.clusters_created += 1
            return [gems] if len(gems) > 0 else []
        
        gems_list = list(gems)
        rows = [g[0] for g in gems_list]
        cols = [g[1] for g in gems_list]
        
        r_variance = self._calculate_variance(rows)
        c_variance = self._calculate_variance(cols)
        
        if r_variance >= c_variance:
            cluster1, cluster2 = self._split_by_rows(gems_list, rows)
        else:
            cluster1, cluster2 = self._split_by_cols(gems_list, cols)
        
        result_clusters = []
        if cluster1:
            result_clusters.extend(self._recursive_divide(cluster1, depth + 1))
        if cluster2:
            result_clusters.extend(self._recursive_divide(cluster2, depth + 1))
        
        return result_clusters if result_clusters else [gems]
    
    def _calculate_variance(self, values):
        if not values:
            return 0
        return max(values) - min(values)
    
    def _split_by_rows(self, gems_list, rows):
        median_r = sorted(rows)[len(rows) // 2]
        cluster1 = frozenset(g for g in gems_list if g[0] <= median_r)
        cluster2 = frozenset(g for g in gems_list if g[0] > median_r)
        return cluster1, cluster2
    
    def _split_by_cols(self, gems_list, cols):
        median_c = sorted(cols)[len(cols) // 2]
        cluster1 = frozenset(g for g in gems_list if g[1] <= median_c)
        cluster2 = frozenset(g for g in gems_list if g[1] > median_c)
        return cluster1, cluster2
    
    def get_cluster_count(self):
        return self.clusters_created


# ==================== NIKHIL'S MODULE - COMMIT 1/5 ====================

class ClusterConqueror:
    """
    NIKHIL - Conquer Phase (Commit 1/5)
    Basic move simulation structure
    
    Responsibility:
    - Simulate moves from any position (C1) ✅ NEW
    - Handle continuous sliding mechanics
    - Track path traversal
    
    TODO (next commits):
    - Boundary detection (C2)
    - Gem collection (C3)
    - 8-direction support (C4)
    - Fallback strategies (C5)
    """
    
    def __init__(self, game):
        """
        Initialize the Cluster Conqueror.
        
        Args:
            game: InertiaGame instance
        """
        self.game = game
        
        # Direction constants
        self.UP = (-1, 0)
        self.DOWN = (1, 0)
        self.LEFT = (0, -1)
        self.RIGHT = (0, 1)
        self.UP_LEFT = (-1, -1)
        self.UP_RIGHT = (-1, 1)
        self.DOWN_LEFT = (1, -1)
        self.DOWN_RIGHT = (1, 1)
        
        self.ALL_DIRECTIONS = [
            self.UP, self.DOWN, self.LEFT, self.RIGHT,
            self.UP_LEFT, self.UP_RIGHT, self.DOWN_LEFT, self.DOWN_RIGHT
        ]
        
        print("[NIKHIL C1] ✅ ClusterConqueror initialized - Basic simulation ready")
    
    def simulate_move(self, start_pos, direction, already_collected):
        """
        NEW (C1): Basic move simulation structure.
        
        Simulates a slide movement from start_pos in given direction.
        The ball slides continuously until it hits an obstacle.
        
        Args:
            start_pos: Starting position (r, c)
            direction: Direction tuple (dr, dc)
            already_collected: Frozenset of gem positions already collected
        
        Returns:
            Tuple of (end_pos, gems_collected_set, hit_mine, path)
        """
        print(f"[NIKHIL C1] 🎯 Simulating move from {start_pos} in direction {direction}")
        
        dr, dc = direction
        r, c = start_pos
        gems_on_path = set()
        path = [(r, c)]
        hit_mine = False
        
        # TODO (C2): Add boundary detection
        # TODO (C3): Add gem collection logic
        # TODO (C4): Ensure all 8 directions work properly
        
        # Basic sliding loop (placeholder - will be enhanced in C2)
        steps = 0
        while steps < 1:  # Temporary: only one step for now
            next_r, next_c = r + dr, c + dc
            
            # Simple boundary check (will be enhanced in C2)
            if next_r < 0 or next_r >= self.game.rows or next_c < 0 or next_c >= self.game.cols:
                print(f"[NIKHIL C1] 🛑 Would hit boundary at ({next_r}, {next_c})")
                break
            
            r, c = next_r, next_c
            path.append((r, c))
            steps += 1
            
            # Placeholder for obstacle detection (will be added in C2)
            break
        
        end_pos = (r, c)
        print(f"[NIKHIL C1] ✅ Move complete: {start_pos} → {end_pos}, path length: {len(path)}")
        
        return end_pos, frozenset(gems_on_path), hit_mine, path
    
    def get_all_directions(self):
        """
        Get all 8 possible directions.
        
        Returns:
            List of direction tuples
        """
        return self.ALL_DIRECTIONS


# ==================== GAME CODE ====================

class InertiaGame:
    def __init__(self, map_name="Map 1 - Introduction"):
        self.map_name = map_name
        self.reset()
        
        # Sukant's module
        self.gem_divider = GemDivider(self, min_cluster_size=2)
        
        # NIKHIL'S ADDITION: Initialize cluster conqueror
        self.cluster_conqueror = ClusterConqueror(self)
    
    def reset(self):
        """Reset game to initial state"""
        map_data = MAPS[self.map_name]
        self.rows = map_data["rows"]
        self.cols = map_data["cols"]
        self.initial_pos = map_data["start"]
        
        self.board = [[EMPTY for _ in range(self.cols)] for _ in range(self.rows)]
        
        for r, c in map_data["gems"]:
            self.board[r][c] = GEM
        
        for r, c in map_data["mines"]:
            self.board[r][c] = MINE
        
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
        
        self.gem_divider = GemDivider(self, min_cluster_size=2)
        self.cluster_conqueror = ClusterConqueror(self)
    
    def change_map(self, map_name):
        """Change to different map"""
        self.map_name = map_name
        self.reset()
    
    def simulate_move(self, direction):
        """Original simulate_move (for game mechanics)"""
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
        """Execute a move for human or CPU."""
        if self.game_over:
            return False, 0, [], False
        
        end_pos, gems, hit_mine, path = self.simulate_move(direction)
        
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
        
        for r, c in path[1:]:
            if self.board[r][c] == GEM:
                self.board[r][c] = EMPTY
                if is_human:
                    self.human_score += 1
                else:
                    self.cpu_score += 1
        
        if self.human_score + self.cpu_score >= self.total_gems:
            self.game_over = True
        
        return True, gems, path, False
    
    def get_cpu_move(self):
        """
        Get CPU move - TEMPORARY: Uses simple greedy strategy
        
        NIKHIL'S TEST (C1): Test basic simulation structure
        TODO: Full integration in later commits
        """
        # Test Nikhil's basic simulation
        print(f"\n{'='*70}")
        print("[CPU AI] Testing Nikhil's ClusterConqueror (C1)")
        
        test_direction = RIGHT
        end_pos, gems, hit_mine, path = self.cluster_conqueror.simulate_move(
            self.ball_pos, test_direction, frozenset()
        )
        print(f"[CPU AI] Test result: Moved from {self.ball_pos} to {end_pos}")
        print(f"{'='*70}\n")
        
        # Temporary greedy AI (will be replaced)
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


class InertiaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Inertia [Commit 5/16: Nikhil - Basic Simulation]")
        self.root.configure(bg="#1a1a2e")
        
        random_map = random.choice(list(MAPS.keys()))
        self.game = InertiaGame(random_map)
        self.cell_size = 60
        self.animating = False
        self.waiting_for_cpu = False
        
        self._create_widgets()
        self._bind_keys()
        self.draw_board()
    
    def _create_widgets(self):
        """Create UI widgets"""
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
            text="Commit 5/16: Nikhil - Basic Move Simulation (1/5) ✅",
            font=("Arial", 10),
            fg="#a8dadc",
            bg="#16213e"
        )
        subtitle.pack()
        
        control_frame = tk.Frame(self.root, bg="#1a1a2e", pady=10)
        control_frame.pack()
        
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
        
        new_game_btn = tk.Button(
            control_frame,
            text="🎲 New Game",
            command=self.new_random_game,
            font=("Arial", 11, "bold"),
            bg="#4CAF50",
            fg="white",
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor="hand2"
        )
        new_game_btn.pack(side=tk.LEFT, padx=10)
        
        restart_btn = tk.Button(
            control_frame,
            text="🔄 Restart",
            command=self.restart_game,
            font=("Arial", 11, "bold"),
            bg="#e94560",
            fg="white",
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor="hand2"
        )
        restart_btn.pack(side=tk.LEFT, padx=10)
        
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
        
        canvas_container = tk.Frame(self.root, bg="#0f3460", padx=3, pady=3)
        canvas_container.pack(pady=10)
        
        self.canvas = tk.Canvas(
            canvas_container,
            bg="#e8f4f8",
            highlightthickness=0
        )
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.mouse_click)
        
        inst_frame = tk.Frame(self.root, bg="#1a1a2e", pady=10)
        inst_frame.pack()
        
        instructions = [
            ("🎮 Controls:", "#00d4ff", "bold"),
            ("Arrow Keys / WASD", "#ffffff", "normal"),
            ("or", "#a8dadc", "normal"),
            ("Click Mouse", "#ffffff", "normal")
        ]
        
        for text, color, weight in instructions:
            tk.Label(
                inst_frame,
                text=text,
                font=("Arial", 9, weight),
                fg=color,
                bg="#1a1a2e"
            ).pack(side=tk.LEFT, padx=3)
        
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
        """Bind keyboard controls"""
        self.root.bind("<Up>", lambda e: self.human_move(UP))
        self.root.bind("<Down>", lambda e: self.human_move(DOWN))
        self.root.bind("<Left>", lambda e: self.human_move(LEFT))
        self.root.bind("<Right>", lambda e: self.human_move(RIGHT))
        self.root.bind("w", lambda e: self.human_move(UP))
        self.root.bind("s", lambda e: self.human_move(DOWN))
        self.root.bind("a", lambda e: self.human_move(LEFT))
        self.root.bind("d", lambda e: self.human_move(RIGHT))
        self.root.bind("q", lambda e: self.human_move(UP_LEFT))
        self.root.bind("e", lambda e: self.human_move(UP_RIGHT))
        self.root.bind("z", lambda e: self.human_move(DOWN_LEFT))
        self.root.bind("c", lambda e: self.human_move(DOWN_RIGHT))
    
    def mouse_click(self, event):
        """Handle mouse click"""
        if self.animating or self.waiting_for_cpu or self.game.game_over:
            return
        
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        
        if row < 0 or row >= self.game.rows or col < 0 or col >= self.game.cols:
            return
        
        ball_r, ball_c = self.game.ball_pos
        dr = row - ball_r
        dc = col - ball_c
        
        if dr == 0 and dc == 0:
            return
        
        if abs(dr) > 0 and abs(dc) > 0:
            dir_r = DOWN if dr > 0 else UP
            dir_c = RIGHT if dc > 0 else LEFT
            direction = (dir_r[0] + dir_c[0], dir_r[1] + dir_c[1])
        elif abs(dr) > abs(dc):
            direction = DOWN if dr > 0 else UP
        else:
            direction = RIGHT if dc > 0 else LEFT
        
        if direction:
            self.human_move(direction)
    
    def draw_board(self):
        """Draw the game board"""
        self.canvas.delete("all")
        
        canvas_width = self.game.cols * self.cell_size
        canvas_height = self.game.rows * self.cell_size
        self.canvas.config(width=canvas_width, height=canvas_height)
        
        for r in range(self.game.rows):
            for c in range(self.game.cols):
                x = c * self.cell_size
                y = r * self.cell_size
                color = "#f0f8ff" if (r + c) % 2 == 0 else "#e1f0fa"
                self.canvas.create_rectangle(
                    x, y, x + self.cell_size, y + self.cell_size,
                    fill=color, outline=""
                )
        
        for r in range(self.game.rows):
            for c in range(self.game.cols):
                x = c * self.cell_size
                y = r * self.cell_size
                cx, cy = x + self.cell_size // 2, y + self.cell_size // 2
                
                if self.game.board[r][c] == GEM:
                    size = self.cell_size // 3
                    self.canvas.create_polygon(
                        cx, cy - size,
                        cx + size, cy,
                        cx, cy + size,
                        cx - size, cy,
                        fill="#00aaff", outline="#0088cc", width=2
                    )
                    
                elif self.game.board[r][c] == MINE:
                    margin = self.cell_size // 5
                    self.canvas.create_oval(
                        cx - margin * 1.5, cy - margin * 1.5,
                        cx + margin * 1.5, cy + margin * 1.5,
                        fill="#ff3333", outline="#cc0000", width=2
                    )
                    m = margin
                    self.canvas.create_line(cx - m, cy - m, cx + m, cy + m, fill="white", width=3)
                    self.canvas.create_line(cx + m, cy - m, cx - m, cy + m, fill="white", width=3)
                    
                elif self.game.board[r][c] == STOP:
                    radius = self.cell_size // 3
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
        
        if self.game.ball_pos:
            r, c = self.game.ball_pos
            x = c * self.cell_size
            y = r * self.cell_size
            cx, cy = x + self.cell_size // 2, y + self.cell_size // 2
            radius = self.cell_size // 3
            
            self.canvas.create_oval(
                cx - radius, cy - radius,
                cx + radius, cy + radius,
                fill="#2a2a2a", outline="#000000", width=2, tags="ball"
            )
        
        self.update_info()
    
    def update_info(self):
        """Update information display"""
        remaining = self.game.total_gems - self.game.human_score - self.game.cpu_score
        info = (f"👤 You: {self.game.human_score} gems ({self.game.human_moves} moves)  |  "
                f"🤖 CPU: {self.game.cpu_score} gems ({self.game.cpu_moves} moves)  |  "
                f"💎 Remaining: {remaining}")
        self.info_label.config(text=info)
    
    def animate_move(self, path, callback):
        """Animate ball sliding"""
        if len(path) <= 1:
            callback()
            return
        
        self.animating = True
        self._animate_step(path, 0, callback)
    
    def _animate_step(self, path, index, callback):
        """Single animation step"""
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
        self.canvas.create_oval(
            cx - radius, cy - radius,
            cx + radius, cy + radius,
            fill="#2a2a2a", outline="#000000", width=2, tags="ball"
        )
        
        self.root.after(80, lambda: self._animate_step(path, index + 1, callback))
    
    def human_move(self, direction):
        """Handle human move"""
        if self.animating or self.waiting_for_cpu or self.game.game_over:
            return
        
        success, gems, path, hit_mine = self.game.make_move(direction, is_human=True)
        
        if hit_mine:
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
            self.show_game_over()
            return
        
        success, gems, path, hit_mine = self.game.make_move(direction, is_human=False)
        
        if hit_mine:
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
        """Show game over message"""
        if not self.game.game_over and self.game.human_score + self.game.cpu_score < self.game.total_gems:
            return
        
        if self.game.human_eliminated:
            winner = "💥 You Hit a Mine! CPU Wins! 💥"
        elif self.game.cpu_eliminated:
            winner = "💥 CPU Hit a Mine! You Win! 💥"
        elif self.game.human_score > self.game.cpu_score:
            winner = "🎉 You Win! 🎉"
        elif self.game.cpu_score > self.game.human_score:
            winner = "🤖 CPU Wins!"
        else:
            winner = "🤝 It's a Tie!"
        
        efficiency_human = self.game.human_score / max(self.game.human_moves, 1)
        efficiency_cpu = self.game.cpu_score / max(self.game.cpu_moves, 1)
        
        msg = (f"{winner}\n\n"
               f"👤 You: {self.game.human_score} gems in {self.game.human_moves} moves "
               f"(Efficiency: {efficiency_human:.2f})\n"
               f"🤖 CPU: {self.game.cpu_score} gems in {self.game.cpu_moves} moves "
               f"(Efficiency: {efficiency_cpu:.2f})\n\n"
               f"Nikhil's Module: 1/5 commits ✅")
        
        messagebox.showinfo("Game Over", msg)
    
    def show_mine_hit(self, who):
        """Show mine hit explosion"""
        msg = "💥 BOOM! You hit a mine!\n\nCPU wins!" if who == "human" else "💥 BOOM! CPU hit a mine!\n\nYou win!"
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
    print("=" * 70)
    print("COMMIT 5/16 - NIKHIL: Basic Move Simulation Structure")
    print("=" * 70)
    print("✅ ClusterConqueror class created")
    print("✅ simulate_move() skeleton implemented")
    print("✅ Basic path tracking added")
    print("✅ ALL_DIRECTIONS defined")
    print("📊 Progress: Nikhil 1/5 commits")
    print("📊 Total Progress: 5/16 commits")
    print("⏭️  Next: Boundary & obstacle detection (C2)")
    print("=" * 70)
    
    root = tk.Tk()
    app = InertiaGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
