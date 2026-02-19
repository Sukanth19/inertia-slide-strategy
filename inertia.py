
import tkinter as tk
from tkinter import messagebox
import random

EMPTY, GEM, MINE, STOP = 0, 1, 2, 3
UP, DOWN, LEFT, RIGHT = (-1, 0), (1, 0), (0, -1), (0, 1)
UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT = (-1, -1), (-1, 1), (1, -1), (1, 1)
ALL_DIRECTIONS = [UP, DOWN, LEFT, RIGHT, UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]

MAPS = {
    "Map 1": {
        "rows": 10, "cols": 10, "start": (5, 0),
        "gems": [(1, 3), (3, 1), (3, 5), (5, 3), (5, 7), (7, 5), (8, 8), (2, 8), (8, 2)],
        "mines": [(2, 2), (4, 4), (6, 6), (5, 5), (7, 3)],
        "stops": [(1, 2), (2, 5), (5, 2), (5, 8), (8, 5), (3, 7), (7, 1)]
    },
    "Map 2": {
        "rows": 12, "cols": 12, "start": (0, 0),
        "gems": [(0, 11), (11, 0), (11, 11), (5, 5), (3, 3), (8, 8), (3, 8), (8, 3), (6, 2), (2, 9), (9, 6)],
        "mines": [(1, 1), (1, 10), (10, 1), (10, 10), (5, 6), (6, 5), (4, 4), (7, 7), (2, 5), (9, 4)],
        "stops": [(0, 10), (10, 0), (5, 4), (4, 6), (7, 5), (5, 7), (2, 2), (9, 9), (3, 6), (8, 5)]
    },
    "Map 3": {
        "rows": 14, "cols": 14, "start": (7, 7),
        "gems": [(0, 3), (0, 10), (3, 0), (3, 13), (10, 0), (10, 13), (13, 3), (13, 10), (5, 5), (8, 8), (5, 8), (8, 5)],
        "mines": [(1, 1), (1, 12), (12, 1), (12, 12), (4, 7), (9, 7), (7, 4), (7, 9), (6, 6), (7, 8), (8, 7), (5, 9)],
        "stops": [(2, 3), (2, 10), (3, 2), (3, 11), (10, 2), (10, 11), (11, 3), (11, 10), (6, 7), (7, 6), (8, 6), (9, 8)]
    }
}

# ========== SUKANTH 1.1: GRAPH STRUCTURE ==========

class GraphBuilder:
    """SUKANTH 1.1"""
    def __init__(self, board, rows, cols):
        self.board = board
        self.rows = rows
        self.cols = cols
        self.graph = {}
        self.cell_types = {}
    
    def build_adjacency_list(self):
        for r in range(self.rows):
            for c in range(self.cols):
                pos = (r, c)
                self.cell_types[pos] = self.board[r][c]
                if self.board[r][c] == MINE:
                    continue
                neighbors = []
                for dr, dc in ALL_DIRECTIONS:
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < self.rows and 0 <= nc < self.cols and 
                        self.board[nr][nc] != MINE):
                        neighbors.append((nr, nc))
                self.graph[pos] = neighbors
        return self.graph, self.cell_types


# ========== SUKANTH 1.2: GRID REGION STRUCTURE ==========

class GridRegion:
    """SUKANTH 1.2"""
    def __init__(self, board, row_start, row_end, col_start, col_end, all_gems):
        self.board = board
        self.row_start = row_start
        self.row_end = row_end
        self.col_start = col_start
        self.col_end = col_end
        self.rows = row_end - row_start
        self.cols = col_end - col_start
        self.gems = self._extract_gems(all_gems)
        
        # SUKANTH 1.4: Store boundary cells (will be set externally)
        self.boundaries = {'north': [], 'south': [], 'east': [], 'west': []}
    
    def _extract_gems(self, all_gems):
        region_gems = set()
        for r, c in all_gems:
            if self.row_start <= r < self.row_end and self.col_start <= c < self.col_end:
                region_gems.add((r, c))
        return region_gems
    
    def size(self):
        return self.rows * self.cols
    
    def contains(self, pos):
        r, c = pos
        return (self.row_start <= r < self.row_end and 
                self.col_start <= c < self.col_end)
    
    def is_on_boundary(self, pos):
        """SUKANTH 1.4: Check if position is on region boundary"""
        r, c = pos
        return (r == self.row_start or r == self.row_end - 1 or
                c == self.col_start or c == self.col_end - 1)


# ========== SUKANTH 1.3: RECURSIVE BISECTION ==========

class DivideConquerSplitter:
    """SUKANTH 1.3"""
    def __init__(self, board, rows, cols, split_threshold=25):
        self.board = board
        self.rows = rows
        self.cols = cols
        self.split_threshold = split_threshold
    
    def recursive_split(self, region, depth=0):
        if region.size() <= self.split_threshold:
            return [region]
        
        left_region, right_region = self._bisect_region(region, depth)
        left_results = self.recursive_split(left_region, depth + 1)
        right_results = self.recursive_split(right_region, depth + 1)
        
        return left_results + right_results
    
    def _bisect_region(self, region, depth):
        split_vertically = (depth % 2 == 0)
        
        if split_vertically:
            mid_col = region.col_start + region.cols // 2
            left_region = GridRegion(self.board, region.row_start, region.row_end,
                                    region.col_start, mid_col, region.gems)
            right_region = GridRegion(self.board, region.row_start, region.row_end,
                                     mid_col, region.col_end, region.gems)
        else:
            mid_row = region.row_start + region.rows // 2
            left_region = GridRegion(self.board, region.row_start, mid_row,
                                    region.col_start, region.col_end, region.gems)
            right_region = GridRegion(self.board, mid_row, region.row_end,
                                     region.col_start, region.col_end, region.gems)
        
        return left_region, right_region


# ========== SUKANTH 1.4: BOUNDARY DETECTION & STATE TRACKING ==========

class BoundaryDetector:
    """
    SUKANTH 1.4: Identifies boundary cells for region interfaces.
    
    Critical for D&C COMBINE phase:
    - Boundaries are where subproblems connect
    - Need to track which cells form region edges
    - States at boundaries enable solution merging
    """
    
    def __init__(self, board):
        self.board = board
    
    def detect_boundaries(self, region):
        """
        SUKANTH 1.4: Find all boundary cells of a region.
        
        Boundaries are cells on the edge of the region that:
        1. Are not mines
        2. Can serve as entry/exit points
        """
        boundaries = {
            'north': [],   # Top edge
            'south': [],   # Bottom edge
            'east': [],    # Right edge
            'west': []     # Left edge
        }
        
        # North boundary (top row)
        for c in range(region.col_start, region.col_end):
            pos = (region.row_start, c)
            if self.board[pos[0]][pos[1]] != MINE:
                boundaries['north'].append(pos)
        
        # South boundary (bottom row)
        for c in range(region.col_start, region.col_end):
            pos = (region.row_end - 1, c)
            if self.board[pos[0]][pos[1]] != MINE:
                boundaries['south'].append(pos)
        
        # West boundary (left column)
        for r in range(region.row_start, region.row_end):
            pos = (r, region.col_start)
            if self.board[pos[0]][pos[1]] != MINE:
                boundaries['west'].append(pos)
        
        # East boundary (right column)
        for r in range(region.row_start, region.row_end):
            pos = (r, region.col_end - 1)
            if self.board[pos[0]][pos[1]] != MINE:
                boundaries['east'].append(pos)
        
        # Remove duplicates (corners appear in two lists)
        for direction in boundaries:
            boundaries[direction] = list(set(boundaries[direction]))
        
        total = sum(len(v) for v in boundaries.values())
        print(f"[SUKANTH-1.4-BOUNDARY] Region [{region.row_start}:{region.row_end}, "
              f"{region.col_start}:{region.col_end}]: {total} boundary cells")
        
        return boundaries
    
    def get_all_boundary_positions(self, region):
        """
        SUKANTH 1.4: Get flattened list of all boundary positions.
        Used for state tracking.
        """
        boundaries = self.detect_boundaries(region)
        all_positions = []
        for positions in boundaries.values():
            all_positions.extend(positions)
        
        # Remove duplicates
        return list(set(all_positions))


class BoundaryStateTracker:
    """
    SUKANTH 1.4: Tracks states at region boundaries.
    
    For D&C COMBINE:
    - Each boundary position can have multiple states
    - State = (position, gems_collected, score)
    - Used to match exit states from one region with entry states to next
    """
    
    def __init__(self):
        self.boundary_states = {}  # boundary_pos → list of states
    
    def add_state(self, boundary_pos, gems_collected, score, path):
        """
        SUKANTH 1.4: Add a state at a boundary position.
        Multiple states possible at same position (different gem collections).
        """
        if boundary_pos not in self.boundary_states:
            self.boundary_states[boundary_pos] = []
        
        state = {
            'position': boundary_pos,
            'gems': frozenset(gems_collected),
            'score': score,
            'path': path
        }
        
        self.boundary_states[boundary_pos].append(state)
    
    def get_states_at(self, boundary_pos):
        """SUKANTH 1.4: Get all states at a boundary position"""
        return self.boundary_states.get(boundary_pos, [])
    
    def get_all_boundary_positions(self):
        """SUKANTH 1.4: Get all boundary positions that have states"""
        return list(self.boundary_states.keys())
    
    def count_states(self):
        """SUKANTH 1.4: Total number of states tracked"""
        return sum(len(states) for states in self.boundary_states.values())


class InertiaGame:
    def __init__(self, map_name):
        self.map_name = map_name
        self.graph_builder = None
        self.graph = {}
        self.cell_types = {}
        self.root_region = None
        self.dc_splitter = None
        self.leaf_regions = []
        self.boundary_detector = None  # NEW: SUKANTH 1.4
        self.region_boundaries = {}     # NEW: region_id → boundaries
        self.reset()
    
    def reset(self):
        map_data = MAPS[self.map_name]
        self.rows, self.cols = map_data["rows"], map_data["cols"]
        self.initial_pos = map_data["start"]
        self.board = [[EMPTY] * self.cols for _ in range(self.rows)]
        
        for r, c in map_data["gems"]: self.board[r][c] = GEM
        for r, c in map_data["mines"]: self.board[r][c] = MINE
        for r, c in map_data["stops"]: self.board[r][c] = STOP
        
        self.ball_pos = self.initial_pos
        self.human_score = self.cpu_score = self.human_moves = self.cpu_moves = 0
        self.game_over = self.human_eliminated = self.cpu_eliminated = False
        self.total_gems = len(map_data["gems"])
        self.cpu_history = []
        
        # SUKANTH 1.1: Build graph
        self.graph_builder = GraphBuilder(self.board, self.rows, self.cols)
        self.graph, self.cell_types = self.graph_builder.build_adjacency_list()
        
        # SUKANTH 1.2: Create root region
        all_gems = set(map_data["gems"])
        self.root_region = GridRegion(self.board, 0, self.rows, 0, self.cols, all_gems)
        
        # SUKANTH 1.3: Recursively split grid
        self.dc_splitter = DivideConquerSplitter(self.board, self.rows, self.cols)
        self.leaf_regions = self.dc_splitter.recursive_split(self.root_region, depth=0)
        
        # SUKANTH 1.4: Detect boundaries for each region
        self.boundary_detector = BoundaryDetector(self.board)
        self.region_boundaries = {}
        
        for i, region in enumerate(self.leaf_regions):
            boundaries = self.boundary_detector.detect_boundaries(region)
            self.region_boundaries[i] = boundaries
            
            # Store in region object
            region.boundaries = boundaries
        
        print(f"[SUKANTH-1.4-COMPLETE] D&C DIVIDE phase complete:")
        print(f"  - {len(self.leaf_regions)} regions")
        print(f"  - Boundaries detected for all regions")
        print(f"  - Ready for CONQUER phase (Nikhil)")
    
    def simulate_move(self, direction):
        dr, dc = direction
        r, c = self.ball_pos
        gems, path, hit_mine = 0, [(r, c)], False
        
        while True:
            next_r, next_c = r + dr, c + dc
            if not (0 <= next_r < self.rows and 0 <= next_c < self.cols): break
            
            r, c = next_r, next_c
            path.append((r, c))
            
            cell = self.board[r][c]
            if cell == GEM: gems += 1
            elif cell == MINE: hit_mine = True; break
            elif cell == STOP: break
        
        return (r, c), gems, hit_mine, path
    
    def get_cpu_move(self):
        """Simple greedy AI - will be replaced by D&C+DP"""
        best_dir, best_score, best_path = None, -999999, []
        
        for direction in ALL_DIRECTIONS:
            end_pos, gems, hit_mine, path = self.simulate_move(direction)
            if hit_mine or end_pos == self.ball_pos: continue
            if end_pos in self.cpu_history[-3:]: continue
            
            score = gems * 10000
            remaining = [(r, c) for r in range(self.rows) for c in range(self.cols) 
                        if self.board[r][c] == GEM]
            if remaining:
                min_dist = min(abs(end_pos[0]-g[0]) + abs(end_pos[1]-g[1]) for g in remaining)
                score -= min_dist * 50
            
            if score > best_score:
                best_dir, best_score, best_path = direction, score, path
        
        return best_dir, best_path
    
    def make_move(self, direction, is_human=True):
        if self.game_over: return False, 0, [], False
        
        end_pos, gems, hit_mine, path = self.simulate_move(direction)
        
        if hit_mine:
            if is_human: self.human_eliminated = True
            else: self.cpu_eliminated = True
            self.game_over = True
            return False, 0, path, True
        
        if end_pos == self.ball_pos: return False, 0, [], False
        
        self.ball_pos = end_pos
        
        if is_human: self.human_moves += 1
        else:
            self.cpu_moves += 1
            self.cpu_history.append(end_pos)
            if len(self.cpu_history) > 6: self.cpu_history.pop(0)
        
        for r, c in path[1:]:
            if self.board[r][c] == GEM:
                self.board[r][c] = EMPTY
                if is_human: self.human_score += 1
                else: self.cpu_score += 1
        
        if self.human_score + self.cpu_score >= self.total_gems: self.game_over = True
        
        return True, gems, path, False
    
    def change_map(self, map_name):
        self.map_name = map_name
        self.reset()


class InertiaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("INERTIA [C1.4: Sukanth-COMPLETE]")
        
        self.colors = {
            'bg_darkest': '#0d0221', 'bg_dark': '#1a0b2e', 'bg_medium': '#2d1b4e',
            'accent_cyan': '#00f5ff', 'accent_magenta': '#e148d4', 'accent_purple': '#a663cc',
            'gem': '#00d9ff', 'mine': '#ff006e', 'stop': '#c77dff', 'ball': '#ffffff',
            'text_bright': '#ffffff', 'text_dim': '#b8b8ff'
        }
        
        self.root.configure(bg=self.colors['bg_darkest'])
        
        self.map_rotation = list(MAPS.keys())
        random.shuffle(self.map_rotation)
        self.current_map_index = 0
        
        self.game = InertiaGame(self.map_rotation[0])
        self.cell_size = 55
        self.animating = self.waiting_for_cpu = False
        
        self._create_widgets()
        self._bind_keys()
        self.draw_board()
    
    def _create_widgets(self):
        main = tk.Frame(self.root, bg=self.colors['bg_darkest'])
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        title_border = tk.Frame(main, bg=self.colors['accent_magenta'], padx=3, pady=3)
        title_border.pack()
        
        title_inner = tk.Frame(title_border, bg=self.colors['bg_dark'], padx=30, pady=20)
        title_inner.pack()
        
        tk.Label(title_inner, text="⬢  I N E R T I A  ⬢", font=("Helvetica", 42, "bold"),
                fg=self.colors['accent_cyan'], bg=self.colors['bg_dark']).pack()
        
        tk.Label(title_inner, text="C1.4: SUKANTH - Boundary Detection (D&C COMPLETE)",
                font=("Courier", 10, "bold"), fg=self.colors['accent_purple'], bg=self.colors['bg_dark']).pack(pady=(8, 0))
        
        map_outer = tk.Frame(main, bg=self.colors['accent_cyan'], padx=2, pady=2)
        map_outer.pack(fill=tk.X, pady=(20, 15))
        
        map_frame = tk.Frame(map_outer, bg=self.colors['bg_medium'], padx=20, pady=15)
        map_frame.pack(fill=tk.X)
        
        self.map_label = tk.Label(map_frame, text=self.game.map_name, font=("Helvetica", 14, "bold"),
                                  fg=self.colors['text_bright'], bg=self.colors['bg_medium'])
        self.map_label.pack()
        
        controls = tk.Frame(main, bg=self.colors['bg_darkest'])
        controls.pack(pady=(0, 15))
        
        for text, cmd in [("▶ NEXT", self.next_map), ("↻ RESTART", self.restart_game)]:
            border = tk.Frame(controls, bg=self.colors['accent_magenta'], padx=2, pady=2)
            border.pack(side=tk.LEFT, padx=8)
            tk.Button(border, text=text, font=("Helvetica", 12, "bold"),
                     fg=self.colors['text_bright'], bg=self.colors['bg_medium'],
                     relief=tk.FLAT, padx=30, pady=12, cursor="hand2", command=cmd).pack()
        
        score_outer = tk.Frame(main, bg=self.colors['accent_purple'], padx=2, pady=2)
        score_outer.pack(fill=tk.X, pady=(0, 15))
        
        score_frame = tk.Frame(score_outer, bg=self.colors['bg_medium'], padx=25, pady=18)
        score_frame.pack(fill=tk.X)
        
        self.info_label = tk.Label(score_frame, text="", font=("Courier", 13, "bold"),
                                   fg=self.colors['accent_cyan'], bg=self.colors['bg_medium'])
        self.info_label.pack()
        
        canvas_outer = tk.Frame(main, bg=self.colors['accent_cyan'], padx=5, pady=5)
        canvas_outer.pack(pady=(0, 15))
        
        canvas_inner = tk.Frame(canvas_outer, bg=self.colors['bg_dark'], padx=3, pady=3)
        canvas_inner.pack()
        
        self.canvas = tk.Canvas(canvas_inner, bg=self.colors['bg_darkest'], highlightthickness=0)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.mouse_click)
    
    def _bind_keys(self):
        for key, direction in [("<Up>", UP), ("<Down>", DOWN), ("<Left>", LEFT), ("<Right>", RIGHT),
                               ("w", UP), ("s", DOWN), ("a", LEFT), ("d", RIGHT),
                               ("q", UP_LEFT), ("e", UP_RIGHT), ("z", DOWN_LEFT), ("c", DOWN_RIGHT)]:
            self.root.bind(key, lambda e, d=direction: self.human_move(d))
    
    def mouse_click(self, event):
        if self.animating or self.waiting_for_cpu or self.game.game_over: return
        col, row = event.x // self.cell_size, event.y // self.cell_size
        if not (0 <= row < self.game.rows and 0 <= col < self.game.cols): return
        
        ball_r, ball_c = self.game.ball_pos
        dr, dc = row - ball_r, col - ball_c
        if dr == 0 and dc == 0: return
        
        if dr != 0 and dc != 0:
            direction = ((1 if dr > 0 else -1), (1 if dc > 0 else -1))
        elif abs(dr) > abs(dc):
            direction = DOWN if dr > 0 else UP
        else:
            direction = RIGHT if dc > 0 else LEFT
        
        self.human_move(direction)
    
    def draw_board(self):
        self.canvas.delete("all")
        width, height = self.game.cols * self.cell_size, self.game.rows * self.cell_size
        self.canvas.config(width=width, height=height)
        
        for r in range(self.game.rows):
            for c in range(self.game.cols):
                x, y = c * self.cell_size, r * self.cell_size
                cx, cy = x + self.cell_size // 2, y + self.cell_size // 2
                
                color = self.colors['bg_darkest'] if (r + c) % 2 == 0 else self.colors['bg_dark']
                self.canvas.create_rectangle(x, y, x + self.cell_size, y + self.cell_size,
                                            fill=color, outline=self.colors['bg_medium'], width=1)
                
                cell = self.game.board[r][c]
                
                if cell == GEM:
                    s = self.cell_size // 3
                    self.canvas.create_polygon(cx, cy-s, cx+s, cy, cx, cy+s, cx-s, cy,
                                             fill=self.colors['gem'], outline=self.colors['accent_cyan'], width=3)
                elif cell == MINE:
                    m = self.cell_size // 3.5
                    self.canvas.create_oval(cx-m, cy-m, cx+m, cy+m,
                                          fill=self.colors['mine'], outline=self.colors['accent_magenta'], width=3)
                    self.canvas.create_line(cx-m+6, cy-m+6, cx+m-6, cy+m-6, fill='white', width=4)
                    self.canvas.create_line(cx+m-6, cy-m+6, cx-m+6, cy+m-6, fill='white', width=4)
                elif cell == STOP:
                    rad = self.cell_size // 3.2
                    self.canvas.create_oval(cx-rad, cy-rad, cx+rad, cy+rad,
                                          fill=self.colors['stop'], outline=self.colors['accent_magenta'], width=3)
        
        if self.game.ball_pos:
            r, c = self.game.ball_pos
            cx, cy = c * self.cell_size + self.cell_size // 2, r * self.cell_size + self.cell_size // 2
            rad = self.cell_size // 3
            self.canvas.create_oval(cx-rad, cy-rad, cx+rad, cy+rad,
                                  fill=self.colors['ball'], outline=self.colors['accent_cyan'], width=4, tags="ball")
        
        self.update_info()
    
    def update_info(self):
        remaining = self.game.total_gems - self.game.human_score - self.game.cpu_score
        self.info_label.config(text=f"YOU: {self.game.human_score}  |  AI: {self.game.cpu_score}  |  LEFT: {remaining}")
    
    def animate_move(self, path, callback):
        if len(path) <= 1: callback(); return
        self.animating = True
        self._animate_step(path, 0, callback)
    
    def _animate_step(self, path, index, callback):
        if index >= len(path):
            self.animating = False
            callback()
            return
        r, c = path[index]
        cx, cy = c * self.cell_size + self.cell_size // 2, r * self.cell_size + self.cell_size // 2
        rad = self.cell_size // 3
        self.canvas.delete("ball")
        self.canvas.create_oval(cx-rad, cy-rad, cx+rad, cy+rad,
                              fill=self.colors['ball'], outline=self.colors['accent_cyan'], width=4, tags="ball")
        self.root.after(50, lambda: self._animate_step(path, index + 1, callback))
    
    def human_move(self, direction):
        if self.animating or self.waiting_for_cpu or self.game.game_over: return
        success, gems, path, hit_mine = self.game.make_move(direction, is_human=True)
        if hit_mine:
            self.animate_move(path, lambda: messagebox.showinfo("MINE!", "You hit a mine!"))
            return
        if not success: return
        self.animate_move(path, self.cpu_move)
    
    def cpu_move(self):
        self.draw_board()
        if self.game.game_over: return
        
        self.waiting_for_cpu = True
        direction, path = self.game.get_cpu_move()
        if direction is None:
            self.waiting_for_cpu = False
            return
        
        success, gems, path, hit_mine = self.game.make_move(direction, is_human=False)
        
        def after_move():
            self.draw_board()
            self.waiting_for_cpu = False
        
        self.root.after(400, lambda: self.animate_move(path, after_move))
    
    def next_map(self):
        self.current_map_index = (self.current_map_index + 1) % len(self.map_rotation)
        self.game.change_map(self.map_rotation[self.current_map_index])
        self.animating = self.waiting_for_cpu = False
        self.map_label.config(text=self.game.map_name)
        self.draw_board()
    
    def restart_game(self):
        self.game.reset()
        self.animating = self.waiting_for_cpu = False
        self.draw_board()


def main():
    root = tk.Tk()
    InertiaGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
