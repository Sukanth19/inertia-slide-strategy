

import tkinter as tk
from tkinter import messagebox
from collections import deque
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

class GridRegion:
    """SUKANTH: Data structure for recursive grid splitting"""
    def __init__(self, board, row_start, row_end, col_start, col_end, parent_gems):
        self.board = board
        self.row_start = row_start
        self.row_end = row_end
        self.col_start = col_start
        self.col_end = col_end
        self.rows = row_end - row_start
        self.cols = col_end - col_start
        self.gems = self._extract_gems(parent_gems)
        
    def _extract_gems(self, parent_gems):
        return {(r, c) for r, c in parent_gems 
                if self.row_start <= r < self.row_end and 
                   self.col_start <= c < self.col_end}
    
    def size(self):
        return self.rows * self.cols


class RegionSolution:
    """NIKHIL: Data structure for storing region solutions"""
    def __init__(self, entry_pos, exit_pos, gems_collected, score, path):
        self.entry_pos = entry_pos
        self.exit_pos = exit_pos
        self.gems_collected = frozenset(gems_collected)
        self.score = score
        self.path = path
    
    def __repr__(self):
        return f"Solution(entry={self.entry_pos}, exit={self.exit_pos}, score={self.score}, gems={len(self.gems_collected)})"


class DivideConquerSolver:
    """SUKANTH + NIKHIL: Pure Divide & Conquer Solver"""
    
    def __init__(self, board, rows, cols, all_gems):
        self.board = board
        self.rows = rows
        self.cols = cols
        self.all_gems = all_gems
        self.split_threshold = 25
        
    # ========== SUKANTH: DIVIDE (from previous commit) ==========
    
    def recursive_split(self, region, depth=0):
        print(f"[SUKANTH-DIVIDE] Depth {depth}: Region {region.rows}x{region.cols}")
        
        if region.size() <= self.split_threshold:
            return [(region, None)]
        
        left_region, right_region, boundary = self._bisect_region(region, depth)
        left_splits = self.recursive_split(left_region, depth + 1)
        right_splits = self.recursive_split(right_region, depth + 1)
        
        return left_splits + right_splits + [(boundary, 'boundary')]
    
    def _bisect_region(self, region, depth):
        split_vertically = (depth % 2 == 0)
        
        if split_vertically:
            mid_col = region.col_start + region.cols // 2
            left_region = GridRegion(self.board, region.row_start, region.row_end,
                                    region.col_start, mid_col, region.gems)
            right_region = GridRegion(self.board, region.row_start, region.row_end,
                                     mid_col, region.col_end, region.gems)
            boundary = [(r, mid_col) for r in range(region.row_start, region.row_end)
                       if self.board[r][mid_col] != MINE]
        else:
            mid_row = region.row_start + region.rows // 2
            left_region = GridRegion(self.board, region.row_start, mid_row,
                                    region.col_start, region.col_end, region.gems)
            right_region = GridRegion(self.board, mid_row, region.row_end,
                                     region.col_start, region.col_end, region.gems)
            boundary = [(mid_row, c) for c in range(region.col_start, region.col_end)
                       if self.board[mid_row][c] != MINE]
        
        return left_region, right_region, boundary
    
    # ========== NIKHIL: CONQUER ==========
    
    def conquer_region(self, region, entry_pos, collected_gems, depth=0):
        """
        NIKHIL - CONQUER: Solve subproblem for a single region.
        
        This is the CONQUER step of D&C:
        - Takes a region (subproblem)
        - Solves it INDEPENDENTLY
        - Returns all possible solutions (different exit points)
        
        Returns: List[RegionSolution]
        """
        print(f"[NIKHIL-CONQUER] Depth {depth}: Solving region {region.rows}x{region.cols} from {entry_pos}")
        
        # BASE CASE: Region is small, solve directly with BFS
        if region.size() <= self.split_threshold:
            return self._solve_small_region_bfs(region, entry_pos, collected_gems)
        
        # RECURSIVE CASE: Split and solve recursively
        left_region, right_region, boundary = self._bisect_region(region, depth)
        
        all_solutions = []
        
        # Try different boundary crossing points
        boundary_sample = self._sample_boundary(boundary, max_points=5)
        
        for boundary_pos in boundary_sample:
            
            # CONQUER LEFT: Recursively solve left subregion
            left_solutions = self.conquer_region(
                left_region, 
                entry_pos, 
                collected_gems,
                depth + 1
            )
            
            # Filter: Only solutions that reach this boundary point
            left_solutions_at_boundary = [
                sol for sol in left_solutions 
                if sol.exit_pos == boundary_pos
            ]
            
            if not left_solutions_at_boundary:
                continue
            
            # Take best left solution
            best_left = max(left_solutions_at_boundary, key=lambda s: s.score)
            
            # CONQUER RIGHT: Recursively solve right subregion
            right_solutions = self.conquer_region(
                right_region,
                boundary_pos,  # Enter right from boundary
                best_left.gems_collected,  # With gems from left
                depth + 1
            )
            
            # COMBINE: Merge left and right solutions
            for right_sol in right_solutions:
                combined_solution = self._merge_solutions(best_left, right_sol)
                all_solutions.append(combined_solution)
        
        print(f"[NIKHIL-CONQUER] Generated {len(all_solutions)} solutions for region")
        return all_solutions
    
    def _solve_small_region_bfs(self, region, entry_pos, collected_gems):
        """
        NIKHIL: BASE CASE - Solve small region with BFS.
        Returns all possible exit points with their solutions.
        """
        solutions = []
        
        # BFS from entry point
        queue = deque([(entry_pos, collected_gems, 0, [entry_pos])])
        visited = {(entry_pos, collected_gems)}
        
        while queue:
            pos, gems, score, path = queue.popleft()
            
            # If at boundary, this is a valid solution
            if self._is_boundary(pos, region):
                solution = RegionSolution(
                    entry_pos=entry_pos,
                    exit_pos=pos,
                    gems_collected=gems,
                    score=len(gems),
                    path=path
                )
                solutions.append(solution)
            
            # Explore neighbors
            for direction in ALL_DIRECTIONS:
                next_pos, new_gems, hit_mine, move_path = self._simulate_move_in_region(
                    pos, direction, region, gems
                )
                
                if hit_mine or next_pos == pos:
                    continue
                
                state = (next_pos, new_gems)
                if state not in visited:
                    visited.add(state)
                    queue.append((
                        next_pos,
                        new_gems,
                        len(new_gems),
                        path + move_path[1:]
                    ))
        
        # If no solutions, return entry as exit (stay in place)
        if not solutions:
            solutions.append(RegionSolution(
                entry_pos=entry_pos,
                exit_pos=entry_pos,
                gems_collected=collected_gems,
                score=len(collected_gems),
                path=[entry_pos]
            ))
        
        return solutions
    
    def _simulate_move_in_region(self, start_pos, direction, region, collected):
        """Simulate move within region boundaries"""
        dr, dc = direction
        r, c = start_pos
        gems_on_path = set()
        path = [(r, c)]
        hit_mine = False
        
        while True:
            next_r, next_c = r + dr, c + dc
            
            # Check region boundaries
            if not (region.row_start <= next_r < region.row_end and 
                    region.col_start <= next_c < region.col_end):
                break
            
            r, c = next_r, next_c
            path.append((r, c))
            
            cell = self.board[r][c]
            if cell == GEM and (r, c) not in collected:
                gems_on_path.add((r, c))
            elif cell == MINE:
                hit_mine = True
                break
            elif cell == STOP:
                break
        
        return (r, c), frozenset(collected | gems_on_path), hit_mine, path
    
    def _is_boundary(self, pos, region):
        """Check if position is on region boundary"""
        r, c = pos
        return (r == region.row_start or r == region.row_end - 1 or
                c == region.col_start or c == region.col_end - 1)
    
    def _sample_boundary(self, boundary, max_points=5):
        """Sample boundary points to limit branching"""
        if len(boundary) <= max_points:
            return boundary
        
        step = len(boundary) // max_points
        return [boundary[i] for i in range(0, len(boundary), step)][:max_points]
    
    # ========== NIKHIL: COMBINE ==========
    
    def _merge_solutions(self, sol1, sol2):
        """
        NIKHIL - COMBINE: Merge two regional solutions.
        
        This is the COMBINE step of D&C:
        - Takes solutions from two adjacent regions
        - Combines them into a single solution
        - Classic merge operation
        """
        combined = RegionSolution(
            entry_pos=sol1.entry_pos,
            exit_pos=sol2.exit_pos,
            gems_collected=sol1.gems_collected | sol2.gems_collected,
            score=sol1.score + sol2.score,
            path=sol1.path + sol2.path[1:]  # Avoid duplicate boundary position
        )
        
        print(f"[NIKHIL-COMBINE] Merged: {sol1.score} + {sol2.score} = {combined.score} gems")
        return combined
    
    def combine_all_solutions(self, solutions):
        """
        NIKHIL: Final combination to select best overall solution.
        """
        if not solutions:
            return None
        
        # Select solution with highest score
        best = max(solutions, key=lambda s: s.score)
        
        print(f"[NIKHIL-COMBINE] Best solution: {best.score} gems, {len(best.path)} moves")
        return best


class InertiaGame:
    def __init__(self, map_name):
        self.map_name = map_name
        self.dc_solver = None
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
        
        # Initialize D&C solver (Sukanth + Nikhil)
        all_gems = set(map_data["gems"])
        self.dc_solver = DivideConquerSolver(self.board, self.rows, self.cols, all_gems)
    
    def simulate_move(self, direction, start_pos=None, collected=frozenset()):
        dr, dc = direction
        r, c = start_pos or self.ball_pos
        gems, path, hit_mine = 0 if start_pos is None else set(), [(r, c)], False
        
        while True:
            next_r, next_c = r + dr, c + dc
            if not (0 <= next_r < self.rows and 0 <= next_c < self.cols): break
            
            r, c = next_r, next_c
            path.append((r, c))
            
            cell = self.board[r][c]
            if cell == GEM:
                if start_pos is None: gems += 1
                elif (r, c) not in collected: gems.add((r, c))
            elif cell == MINE: hit_mine = True; break
            elif cell == STOP: break
        
        return (r, c), (gems if start_pos is None else frozenset(gems)), hit_mine, path
    
    def get_cpu_move(self):
        """
        NIKHIL: Use D&C solver for CPU move.
        This demonstrates the full D&C algorithm in action.
        """
        # Create full grid region
        root_region = GridRegion(self.board, 0, self.rows, 0, self.cols, self.dc_solver.all_gems)
        
        # Get current collected gems
        collected = frozenset()
        
        # DIVIDE + CONQUER: Solve recursively
        solutions = self.dc_solver.conquer_region(
            root_region,
            self.ball_pos,
            collected,
            depth=0
        )
        
        # COMBINE: Select best solution
        best_solution = self.dc_solver.combine_all_solutions(solutions)
        
        if best_solution and len(best_solution.path) > 1:
            # Extract next move direction
            current = best_solution.path[0]
            next_pos = best_solution.path[1]
            
            direction = (next_pos[0] - current[0], next_pos[1] - current[1])
            
            # Simulate to get full path for this move
            _, _, _, path = self.simulate_move(direction)
            
            return direction, path
        
        # Fallback: greedy
        return self._greedy_move()
    
    def _greedy_move(self):
        """Fallback greedy strategy"""
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
        self.root.title("INERTIA [C2: Nikhil-D&C-CONQUER+COMBINE]")
        
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
        
        tk.Label(title_inner, text="╺━━━  C2: NIKHIL - PURE D&C (CONQUER+COMBINE)  ━━━╸",
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
            self.animate_move(path, lambda: messagebox.showinfo("MINE!", "You hit a mine!\nAI WINS"))
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
