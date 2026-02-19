# COMMIT 1.2 - SUKANTH
# Added: GridRegion class for spatial decomposition

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

# ========== SUKANTH 1.1: GRAPH STRUCTURE (from previous) ==========

class GraphBuilder:
    """SUKANTH 1.1: Adjacency list graph construction"""
    
    def __init__(self, board, rows, cols):
        self.board = board
        self.rows = rows
        self.cols = cols
        self.graph = {}
        self.cell_types = {}
    
    def build_adjacency_list(self):
        """Build adjacency list for grid"""
        print(f"[SUKANTH-1.1] Building graph for {self.rows}x{self.cols} grid")
        
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
        
        print(f"[SUKANTH-1.1] Graph built: {len(self.graph)} nodes")
        return self.graph, self.cell_types


# ========== SUKANTH 1.2: GRID REGION STRUCTURE ==========

class GridRegion:
    """
    SUKANTH 1.2: Represents a rectangular region of the grid.
    This is the fundamental unit for divide-and-conquer spatial decomposition.
    
    Stores:
    - Boundary coordinates (row_start, row_end, col_start, col_end)
    - Gems within this region
    - Size information
    """
    
    def __init__(self, board, row_start, row_end, col_start, col_end, all_gems):
        self.board = board
        self.row_start = row_start
        self.row_end = row_end
        self.col_start = col_start
        self.col_end = col_end
        self.rows = row_end - row_start
        self.cols = col_end - col_start
        
        # SUKANTH 1.2: Extract gems that fall within this region
        self.gems = self._extract_gems(all_gems)
        
        print(f"[SUKANTH-1.2] Region created: [{row_start}:{row_end}, {col_start}:{col_end}] "
              f"size={self.rows}x{self.cols}, gems={len(self.gems)}")
    
    def _extract_gems(self, all_gems):
        """
        SUKANTH 1.2: Filter gems that belong to this region.
        Critical for divide-and-conquer: each subproblem only sees its gems.
        """
        region_gems = set()
        for r, c in all_gems:
            if self.row_start <= r < self.row_end and self.col_start <= c < self.col_end:
                region_gems.add((r, c))
        return region_gems
    
    def size(self):
        """SUKANTH 1.2: Total cells in region"""
        return self.rows * self.cols
    
    def contains(self, pos):
        """SUKANTH 1.2: Check if position is inside region"""
        r, c = pos
        return (self.row_start <= r < self.row_end and 
                self.col_start <= c < self.col_end)
    
    def __repr__(self):
        return f"GridRegion({self.rows}x{self.cols}, {len(self.gems)} gems)"


class InertiaGame:
    def __init__(self, map_name):
        self.map_name = map_name
        self.graph_builder = None
        self.graph = {}
        self.cell_types = {}
        self.root_region = None  # NEW: Will hold the full grid region
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
        
        # SUKANTH 1.2: Create root region (entire grid)
        all_gems = set(map_data["gems"])
        self.root_region = GridRegion(self.board, 0, self.rows, 0, self.cols, all_gems)
    
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
        """Simple greedy AI"""
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
        self.root.title("INERTIA [C1.2: Sukanth-GridRegion]")
        
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
        
        tk.Label(title_inner, text="C1.2: SUKANTH - Grid Region Structure",
                font=("Courier", 11, "bold"), fg=self.colors['accent_purple'], bg=self.colors['bg_dark']).pack(pady=(8, 0))
        
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
