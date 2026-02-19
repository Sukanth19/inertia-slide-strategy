import tkinter as tk
from tkinter import messagebox
import random

# Cell types
EMPTY = 0
GEM = 1
MINE = 2
STOP = 3

# Directions - includes all 8 directions
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

# Maps - 8 balanced maps with increasing difficulty
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


# ==================== SUKANT'S MODULE ✅ COMPLETE ====================

class GemDivider:
    
    def __init__(self, game, min_cluster_size=2):
        self.game = game
        self.min_cluster_size = min_cluster_size
        self.clusters_created = 0
    
    def get_remaining_gems(self):
        """Extract all gems currently on the board."""
        gems = set()
        for r in range(self.game.rows):
            for c in range(self.game.cols):
                if self.game.board[r][c] == GEM:
                    gems.add((r, c))
        return frozenset(gems)
    
    def divide_gems_into_clusters(self, gems):
        """Recursively divide gems into optimal clusters using variance."""
        self.clusters_created = 0
        clusters = self._recursive_divide(gems, depth=0)
        return clusters
    
    def _recursive_divide(self, gems, depth):
        """Recursively divide gems based on spatial variance."""
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
        """Calculate variance (spread) of values."""
        if not values:
            return 0
        return max(values) - min(values)
    
    def _split_by_rows(self, gems_list, rows):
        """Split gems by median row (horizontal line)."""
        median_r = sorted(rows)[len(rows) // 2]
        cluster1 = frozenset(g for g in gems_list if g[0] <= median_r)
        cluster2 = frozenset(g for g in gems_list if g[0] > median_r)
        return cluster1, cluster2
    
    def _split_by_cols(self, gems_list, cols):
        """Split gems by median column (vertical line)."""
        median_c = sorted(cols)[len(cols) // 2]
        cluster1 = frozenset(g for g in gems_list if g[1] <= median_c)
        cluster2 = frozenset(g for g in gems_list if g[1] > median_c)
        return cluster1, cluster2
    
    def get_cluster_count(self):
        """Return number of clusters created in last division."""
        return self.clusters_created


# ==================== NIKHIL'S MODULE ✅ COMPLETE ====================

class ClusterConqueror:
    
    def __init__(self, game):
        self.game = game
        
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
        
        self.DIRECTION_NAMES = {
            self.UP: "UP ↑",
            self.DOWN: "DOWN ↓",
            self.LEFT: "LEFT ←",
            self.RIGHT: "RIGHT →",
            self.UP_LEFT: "UP_LEFT ↖",
            self.UP_RIGHT: "UP_RIGHT ↗",
            self.DOWN_LEFT: "DOWN_LEFT ↙",
            self.DOWN_RIGHT: "DOWN_RIGHT ↘"
        }
    
    def simulate_move(self, start_pos, direction, already_collected):
        """Simulate a complete sliding move with gem collection."""
        if not self.is_valid_direction(direction):
            return start_pos, frozenset(), False, [start_pos]
        
        dr, dc = direction
        r, c = start_pos
        gems_on_path = set()
        path = [(r, c)]
        hit_mine = False
        
        while True:
            next_r, next_c = r + dr, c + dc
            
            if not self._is_in_bounds(next_r, next_c):
                break
            
            r, c = next_r, next_c
            path.append((r, c))
            
            cell_type = self.game.board[r][c]
            
            if cell_type == GEM:
                if (r, c) not in already_collected:
                    gems_on_path.add((r, c))
            elif cell_type == MINE:
                hit_mine = True
                break
            elif cell_type == STOP:
                break
        
        end_pos = (r, c)
        gems_collected = frozenset(gems_on_path)
        
        return end_pos, gems_collected, hit_mine, path
    
    def find_fallback_move(self):
        """Find a fallback move using multi-level strategy."""
        current_pos = self.game.ball_pos
        
        gem_move = self._find_best_gem_collecting_move(current_pos)
        if gem_move[0] is not None:
            return gem_move
        
        valid_move = self._find_any_valid_move(current_pos)
        if valid_move[0] is not None:
            return valid_move
        
        return None, []
    
    def _find_best_gem_collecting_move(self, start_pos):
        """Find move that collects most gems."""
        best_direction = None
        best_path = []
        best_gem_count = 0
        
        for direction in self.ALL_DIRECTIONS:
            end_pos, gems, hit_mine, path = self.simulate_move(
                start_pos, direction, frozenset()
            )
            
            if not hit_mine and end_pos != start_pos and len(gems) > 0:
                if len(gems) > best_gem_count:
                    best_direction = direction
                    best_path = path
                    best_gem_count = len(gems)
        
        return best_direction, best_path
    
    def _find_any_valid_move(self, start_pos):
        """Find any valid move that doesn't hit a mine."""
        for direction in self.ALL_DIRECTIONS:
            end_pos, gems, hit_mine, path = self.simulate_move(
                start_pos, direction, frozenset()
            )
            
            if not hit_mine and end_pos != start_pos:
                return direction, path
        
        return None, []
    
    def calculate_distance_to_cluster(self, pos, cluster):
        """Calculate minimum Manhattan distance to cluster."""
        if not cluster:
            return float('inf')
        
        min_distance = min(
            abs(pos[0] - g[0]) + abs(pos[1] - g[1])
            for g in cluster
        )
        
        return min_distance
    
    def is_valid_direction(self, direction):
        """Validate if direction is one of the 8 valid directions."""
        if not isinstance(direction, tuple) or len(direction) != 2:
            return False
        return direction in self.ALL_DIRECTIONS
    
    def get_direction_name(self, direction):
        """Get human-readable name for direction."""
        return self.DIRECTION_NAMES.get(direction, f"UNKNOWN {direction}")
    
    def _is_in_bounds(self, r, c):
        """Check if position is within grid boundaries."""
        return 0 <= r < self.game.rows and 0 <= c < self.game.cols
    
    def get_all_directions(self):
        """Get all 8 possible directions."""
        return self.ALL_DIRECTIONS


# ==================== DHIRJA'S MODULE ✅ COMPLETE ====================

class DPStateManager:
    
    def __init__(self):
        self.memo = {}
        self.memo_hits = 0
        self.memo_misses = 0
    
    def create_state(self, position, collected_gems):
        """Create a DP state for memoization."""
        if not isinstance(position, tuple) or len(position) != 2:
            return None
        
        if not isinstance(collected_gems, frozenset):
            collected_gems = frozenset(collected_gems)
        
        state = (position, collected_gems)
        return state
    
    def validate_state(self, state):
        """Validate if a state is properly formatted."""
        if not isinstance(state, tuple) or len(state) != 2:
            return False
        
        position, collected_gems = state
        
        if not isinstance(position, tuple) or len(position) != 2:
            return False
        
        if not isinstance(collected_gems, frozenset):
            return False
        
        return True
    
    def clear_memo(self):
        """Clear the memoization table and reset statistics."""
        self.memo.clear()
        self.memo_hits = 0
        self.memo_misses = 0
    
    def has_state(self, state):
        """Check if a state exists in the memoization table."""
        if not self.validate_state(state):
            return False
        return state in self.memo
    
    def get_memo(self, state):
        """Retrieve memoized result for a state."""
        if not self.validate_state(state):
            return None
        
        if state in self.memo:
            self.memo_hits += 1
            return self.memo[state]
        else:
            self.memo_misses += 1
            return None
    
    def set_memo(self, state, score, direction, path):
        """Store a computed result in the memoization table."""
        if not self.validate_state(state):
            return
        
        result = (score, direction, path)
        self.memo[state] = result
    
    def get_memo_size(self):
        """Get the current size of the memoization table."""
        return len(self.memo)
    
    def get_memo_stats(self):
        """Get comprehensive statistics about memoization performance."""
        total_lookups = self.memo_hits + self.memo_misses
        hit_rate = (self.memo_hits / total_lookups * 100) if total_lookups > 0 else 0
        
        stats = {
            'memo_hits': self.memo_hits,
            'memo_misses': self.memo_misses,
            'memo_size': len(self.memo),
            'hit_rate': hit_rate,
            'total_lookups': total_lookups
        }
        
        return stats
    
    def merge_collected_gems(self, gems_set1, gems_set2):
        """Merge two sets of collected gems."""
        merged = frozenset(gems_set1) | frozenset(gems_set2)
        return merged
    
    def create_next_state(self, current_state, new_position, newly_collected_gems):
        """Create a next state from current state and move results."""
        if not self.validate_state(current_state):
            return None
        
        _, current_collected = current_state
        all_collected = self.merge_collected_gems(current_collected, newly_collected_gems)
        next_state = self.create_state(new_position, all_collected)
        
        return next_state
    
    def is_goal_state(self, state, total_gems):
        """Check if a state represents a goal (all gems collected)."""
        if not self.validate_state(state):
            return False
        
        _, collected_gems = state
        is_goal = len(collected_gems) >= total_gems
        
        return is_goal
    
    def get_uncollected_gems(self, state, all_gems):
        """Get gems that haven't been collected yet in this state."""
        if not self.validate_state(state):
            return all_gems
        
        _, collected_gems = state
        uncollected = all_gems - collected_gems
        
        return uncollected
    
    def state_to_string(self, state):
        """Convert state to human-readable string for debugging."""
        if not self.validate_state(state):
            return "INVALID STATE"
        
        pos, collected = state
        return f"State(pos={pos}, collected={len(collected)} gems)"
    
    def get_state_position(self, state):
        """Extract position from a state."""
        if not self.validate_state(state):
            return None
        return state[0]
    
    def get_state_collected(self, state):
        """Extract collected gems from a state."""
        if not self.validate_state(state):
            return frozenset()
        return state[1]


# ==================== BADRI'S MODULE ✅ COMPLETE ====================

class RecursiveSolver:

    
    def __init__(self, game, gem_divider, cluster_conqueror, dp_state_manager, max_depth=3):
        """
        Initialize the Recursive Solver with all dependencies.
        
        This is where the magic happens - all 4 modules work together!
        """
        self.game = game
        
        # FINAL INTEGRATION: All modules connected
        self.gem_divider = gem_divider              # Sukant's Divide
        self.cluster_conqueror = cluster_conqueror  # Nikhil's Conquer
        self.dp_state_manager = dp_state_manager    # Dhirja's DP
        
        self.max_depth = max_depth
    
    def solve(self, start_position):
        """
        Main entry point for solving the game.
        
        This orchestrates the entire Divide-and-Conquer + DP algorithm!
        """
        # Clear memo for fresh start
        self.dp_state_manager.clear_memo()
        
        # Create initial state using Dhirja's module
        initial_state = self.dp_state_manager.create_state(start_position, frozenset())
        
        # Start recursive solving
        result = self._solve_recursive(initial_state, depth=0)
        
        return result
    
    def _solve_recursive(self, state, depth):
        """
        Complete recursive DP solver with cluster optimization.
        
        This is the heart of the AI - combining:
        - Sukant's clustering (Divide)
        - Nikhil's move simulation (Conquer)
        - Dhirja's memoization (DP)
        """
        # Check memoization (Dhirja's module)
        cached_result = self.dp_state_manager.get_memo(state)
        if cached_result is not None:
            return cached_result
        
        # Base case 1: Goal state (Dhirja's module)
        all_gems = self.gem_divider.get_remaining_gems()
        if self.dp_state_manager.is_goal_state(state, len(all_gems)):
            result = (len(all_gems), None, [])
            self.dp_state_manager.set_memo(state, *result)
            return result
        
        # Base case 2: Depth limit reached
        if depth >= self.max_depth:
            current_score = len(self.dp_state_manager.get_state_collected(state))
            result = (current_score, None, [])
            self.dp_state_manager.set_memo(state, *result)
            return result
        
        # Extract current info (Dhirja's module)
        current_pos = self.dp_state_manager.get_state_position(state)
        already_collected = self.dp_state_manager.get_state_collected(state)
        
        # Get uncollected gems and cluster them (Sukant's module)
        uncollected = self.dp_state_manager.get_uncollected_gems(state, all_gems)
        
        if len(uncollected) > 0:
            clusters = self.gem_divider.divide_gems_into_clusters(uncollected)
        else:
            clusters = []
        
        # Initialize best result
        best_score = len(already_collected)
        best_direction = None
        best_path = []
        
        # Prioritize moves using cluster proximity
        move_candidates = []
        
        for direction in self.cluster_conqueror.get_all_directions():
            # Simulate move (Nikhil's module)
            end_pos, new_gems, hit_mine, path = self.cluster_conqueror.simulate_move(
                current_pos, direction, already_collected
            )
            
            # Skip invalid moves
            if hit_mine or end_pos == current_pos:
                continue
            
            # Calculate priority based on immediate gems and cluster proximity
            immediate_value = len(new_gems) * 100
            
            min_cluster_dist = float('inf')
            if clusters:
                for cluster in clusters:
                    dist = self.cluster_conqueror.calculate_distance_to_cluster(end_pos, cluster)
                    min_cluster_dist = min(min_cluster_dist, dist)
            
            proximity_value = 1000 / (min_cluster_dist + 1) if min_cluster_dist != float('inf') else 0
            priority = immediate_value + proximity_value
            
            move_candidates.append((priority, direction, end_pos, new_gems, path))
        
        # Sort moves by priority
        move_candidates.sort(reverse=True, key=lambda x: x[0])
        
        # Try moves in priority order
        for priority, direction, end_pos, new_gems, path in move_candidates:
            # Create next state (Dhirja's module)
            next_state = self.dp_state_manager.create_next_state(state, end_pos, new_gems)
            
            if next_state is None:
                continue
            
            # RECURSIVE CALL - The DP magic!
            future_score, _, future_path = self._solve_recursive(next_state, depth + 1)
            
            # Update best if better
            if future_score > best_score:
                best_score = future_score
                best_direction = direction
                best_path = path
        
        # Memoize result (Dhirja's module)
        result = (best_score, best_direction, best_path)
        self.dp_state_manager.set_memo(state, *result)
        
        return result


# ==================== GAME ENGINE ====================

class InertiaGame:
    """Main game engine - coordinates all modules."""
    
    def __init__(self, map_name="Map 1 - Introduction"):
        self.map_name = map_name
        self.reset()
        
        # Initialize all 4 modules
        self.gem_divider = GemDivider(self, min_cluster_size=2)
        self.cluster_conqueror = ClusterConqueror(self)
        self.dp_state_manager = DPStateManager()
        self.recursive_solver = RecursiveSolver(
            self,
            self.gem_divider,
            self.cluster_conqueror,
            self.dp_state_manager,
            max_depth=3
        )
    
    def reset(self):
        """Reset game to initial state."""
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
        
        # Reinitialize modules
        self.gem_divider = GemDivider(self, min_cluster_size=2)
        self.cluster_conqueror = ClusterConqueror(self)
        self.dp_state_manager = DPStateManager()
        self.recursive_solver = RecursiveSolver(
            self,
            self.gem_divider,
            self.cluster_conqueror,
            self.dp_state_manager,
            max_depth=3
        )
    
    def change_map(self, map_name):
        """Change to different map."""
        self.map_name = map_name
        self.reset()
    
    def simulate_move(self, direction):
        """Simulate a move (for game mechanics)."""
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
        🎯 FINAL CPU AI - Using complete recursive DP solver!
        
        This is where all 4 modules work together in perfect harmony:
        - Sukant's clustering divides the problem
        - Nikhil's simulation conquers each subproblem
        - Dhirja's memoization prevents redundant work
        - Badri's recursion ties it all together
        """
        # Solve from current position using the complete algorithm
        score, direction, path = self.recursive_solver.solve(self.ball_pos)
        
        # Return the best move found
        if direction:
            return direction, path
        else:
            # Fallback if no good move found
            return self.cluster_conqueror.find_fallback_move()


# ==================== GUI ====================

class InertiaGUI:
    """Beautiful GUI for the complete game."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🎉 INERTIA - FINAL VERSION 🏆")
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
        """Create beautiful UI widgets."""
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
            font=("Arial", 10, "bold"),
            fg="#FFD700",
            bg="#16213e"
        )
        subtitle.pack()
        
        subtitle2 = tk.Label(
            title_frame,
            font=("Arial", 9),
            fg="#a8dadc",
            bg="#16213e"
        )
        subtitle2.pack()
        
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
            ("Arrow Keys / WASD / QEZC", "#ffffff", "normal"),
            ("or", "#a8dadc", "normal"),
            ("Click Mouse", "#ffffff", "normal"),
            ("(All 8 Directions!)", "#00d4ff", "normal")
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
        """Bind keyboard controls."""
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
        """Handle mouse click."""
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
        """Draw the game board."""
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
        """Update information display."""
        remaining = self.game.total_gems - self.game.human_score - self.game.cpu_score
        info = (f"👤 You: {self.game.human_score} gems ({self.game.human_moves} moves)  |  "
                f"🤖 CPU: {self.game.cpu_score} gems ({self.game.cpu_moves} moves)  |  "
                f"💎 Remaining: {remaining}")
        self.info_label.config(text=info)
    
    def animate_move(self, path, callback):
        """Animate ball sliding."""
        if len(path) <= 1:
            callback()
            return
        
        self.animating = True
        self._animate_step(path, 0, callback)
    
    def _animate_step(self, path, index, callback):
        """Single animation step."""
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
        """Handle human move."""
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
        """Handle CPU move."""
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
        """Show game over message."""
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
               f"Thank you for playing!")
        
        messagebox.showinfo("Game Over", msg)
    
    def show_mine_hit(self, who):
        """Show mine hit explosion."""
        msg = "💥 BOOM! You hit a mine!\n\nCPU wins!" if who == "human" else "💥 BOOM! CPU hit a mine!\n\nYou win!"
        messagebox.showinfo("Mine Hit!", msg)
        self.show_game_over()
    
    def new_random_game(self):
        """Start a new game with a random map."""
        random_map = random.choice(list(MAPS.keys()))
        self.game.change_map(random_map)
        self.animating = False
        self.waiting_for_cpu = False
        self.map_label.config(text=random_map)
        self.draw_board()
    
    def restart_game(self):
        """Restart current map."""
        self.game.reset()
        self.animating = False
        self.waiting_for_cpu = False
        self.draw_board()


# ==================== MAIN ====================

def main():
    root = tk.Tk()
    app = InertiaGUI(root)
    root.mainloop()
    
    print()
    print("=" * 70)
    print("🎉 Thank you for playing INERTIA! 🎉")
    print("=" * 70)


if __name__ == "__main__":
    main()
