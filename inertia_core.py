# ==================== CONSTANTS ====================

EMPTY = 0
GEM   = 1
MINE  = 2
STOP  = 3

UP         = (-1,  0)
DOWN       = ( 1,  0)
LEFT       = ( 0, -1)
RIGHT      = ( 0,  1)
UP_LEFT    = (-1, -1)
UP_RIGHT   = (-1,  1)
DOWN_LEFT  = ( 1, -1)
DOWN_RIGHT = ( 1,  1)

ALL_DIRECTIONS = [UP, DOWN, LEFT, RIGHT, UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]

DIRECTION_NAMES = {
    UP:         "UP ↑",
    DOWN:       "DOWN ↓",
    LEFT:       "LEFT ←",
    RIGHT:      "RIGHT →",
    UP_LEFT:    "UP-LEFT ↖",
    UP_RIGHT:   "UP-RIGHT ↗",
    DOWN_LEFT:  "DOWN-LEFT ↙",
    DOWN_RIGHT: "DOWN-RIGHT ↘",
}

# ==================== MAPS ====================

MAPS = {
    "Map 1 - Introduction": {
        "rows": 8, "cols": 8,
        "start": (3, 0),
        "gems":  [(3, 3), (3, 5), (5, 3), (1, 3)],
        "mines": [(2, 3), (4, 3), (3, 7)],
        "stops": [(3, 6), (5, 5), (1, 5)],
    },
    "Map 2 - Corner Maze": {
        "rows": 8, "cols": 8,
        "start": (0, 0),
        "gems":  [(0, 7), (7, 0), (7, 7), (3, 3), (4, 4)],
        "mines": [(1, 1), (6, 1), (1, 6), (6, 6)],
        "stops": [(0, 6), (6, 0), (1, 7), (7, 1), (3, 4), (4, 3)],
    },
    "Map 3 - Diamond Challenge": {
        "rows": 8, "cols": 8,
        "start": (4, 0),
        "gems":  [(1, 3), (3, 1), (3, 5), (5, 3), (4, 7), (6, 5)],
        "mines": [(0, 0), (0, 7), (7, 0), (7, 7), (4, 4)],
        "stops": [(4, 1), (4, 6), (2, 3), (6, 3), (3, 3), (5, 5)],
    },
    "Map 4 - Cross Roads": {
        "rows": 9, "cols": 9,
        "start": (0, 4),
        "gems":  [(2, 4), (4, 2), (4, 4), (4, 6), (6, 4), (8, 2), (8, 6)],
        "mines": [(1, 1), (1, 7), (7, 1), (7, 7), (4, 8)],
        "stops": [(3, 4), (5, 4), (4, 3), (4, 5), (6, 2), (6, 6)],
    },
    "Map 5 - Spiral Trap": {
        "rows": 9, "cols": 9,
        "start": (0, 0),
        "gems":  [(0, 8), (8, 8), (8, 0), (4, 4), (2, 2), (6, 6)],
        "mines": [(2, 6), (6, 2), (1, 4), (7, 4), (4, 1), (4, 7)],
        "stops": [(0, 7), (7, 8), (8, 1), (1, 0), (2, 4), (6, 4), (4, 2), (4, 6)],
    },
    "Map 6 - Advanced Maze": {
        "rows": 10, "cols": 10,
        "start": (0, 0),
        "gems":  [(0, 9), (5, 5), (9, 0), (9, 9), (2, 5), (7, 4), (4, 2), (5, 7)],
        "mines": [(2, 2), (2, 7), (7, 2), (7, 7), (4, 4), (5, 6), (3, 0), (6, 9)],
        "stops": [(0, 8), (1, 0), (5, 4), (8, 0), (9, 1), (9, 8), (4, 5), (6, 8), (2, 4), (7, 5)],
    },
    "Map 7 - Expert Grid": {
        "rows": 10, "cols": 10,
        "start": (5, 5),
        "gems":  [(0, 0), (0, 9), (9, 0), (9, 9), (2, 5), (5, 2), (5, 7), (7, 5)],
        "mines": [(1, 1), (1, 8), (8, 1), (8, 8), (3, 3), (3, 6), (6, 3), (6, 6)],
        "stops": [(0, 5), (5, 0), (9, 5), (5, 9), (2, 2), (2, 7), (7, 2), (7, 7), (4, 5), (5, 4)],
    },
    "Map 8 - Master Challenge": {
        "rows": 12, "cols": 12,
        "start": (6, 0),
        "gems":  [(0, 0), (0, 11), (11, 0), (11, 11), (3, 3), (8, 8), (3, 8), (8, 3)],
        "mines": [(1, 1), (1, 10), (10, 1), (10, 10), (5, 5), (6, 6)],
        "stops": [(0, 6), (6, 11), (11, 6), (6, 0), (2, 2), (9, 9), (2, 9), (9, 2), (5, 0), (6, 10)],
    },
}

MAP_NAMES = list(MAPS.keys())


# ==================== BOARD ====================

class Board:
    def __init__(self, map_name):
        self.map_name = map_name
        data          = MAPS[map_name]
        self.rows     = data["rows"]
        self.cols     = data["cols"]
        self.start    = data["start"]
        self.grid     = [[EMPTY] * self.cols for _ in range(self.rows)]
        for r, c in data["gems"]:
            self.grid[r][c] = GEM
        for r, c in data["mines"]:
            self.grid[r][c] = MINE
        for r, c in data["stops"]:
            self.grid[r][c] = STOP

    def in_bounds(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols

    def cell(self, r, c):
        return self.grid[r][c]

    def remove_gem(self, r, c):
        if self.grid[r][c] == GEM:
            self.grid[r][c] = EMPTY

    def remaining_gems(self):
        gems = set()
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == GEM:
                    gems.add((r, c))
        return frozenset(gems)

    def total_gems(self):
        return len(MAPS[self.map_name]["gems"])


# ==================== PHYSICS ====================

def simulate_slide(board, start, direction, already_collected=None):
    if already_collected is None:
        already_collected = frozenset()
    dr, dc   = direction
    r, c     = start
    path     = [(r, c)]
    gems     = set()
    hit_mine = False
    while True:
        nr, nc = r + dr, c + dc
        if not board.in_bounds(nr, nc):
            break
        r, c = nr, nc
        path.append((r, c))
        cell = board.cell(r, c)
        if cell == GEM:
            if (r, c) not in already_collected:
                gems.add((r, c))
        elif cell == MINE:
            hit_mine = True
            break
        elif cell == STOP:
            break
    return (r, c), frozenset(gems), hit_mine, path


# ==================== GREEDY AI ====================

class GreedyAI:
    name        = "Greedy"
    description = "Always picks the single move collecting the most gems immediately."

    def choose_move(self, board, ball_pos):
        best_dir  = None
        best_gems = -1
        best_path = []
        for d in ALL_DIRECTIONS:
            end, gems, hit_mine, path = simulate_slide(board, ball_pos, d)
            if hit_mine or end == ball_pos:
                continue
            if len(gems) > best_gems:
                best_gems = len(gems)
                best_dir  = d
                best_path = path
        return best_dir, best_path


# ==================== DIVIDE & CONQUER AI ====================

class DivideConquerAI:
    name        = "Divide & Conquer"
    description = (
        "TRUE D&C: recursively splits the gem set into halves, "
        "solves each independently, combines by best first move."
    )

    def choose_move(self, board, ball_pos):
        remaining = board.remaining_gems()
        if not remaining:
            return None, []
        _, best_dir, best_path = self._dnc(board, ball_pos, remaining)
        if best_dir is None:
            return GreedyAI().choose_move(board, ball_pos)
        return best_dir, best_path

    def _dnc(self, board, pos, gem_set):
        if len(gem_set) == 0:
            return 0, None, []
        if len(gem_set) == 1:
            target = next(iter(gem_set))
            return self._best_move_toward(board, pos, gem_set, target)
        left_gems, right_gems = self._split(gem_set)
        left_score,  left_dir,  left_path  = self._dnc(board, pos, left_gems)
        right_score, right_dir, right_path = self._dnc(board, pos, right_gems)
        if left_score >= right_score:
            return left_score, left_dir, left_path
        return right_score, right_dir, right_path

    def _best_move_toward(self, board, pos, gem_set, target):
        best_score = -1
        best_dir   = None
        best_path  = []
        for d in ALL_DIRECTIONS:
            end, gems_hit, hit_mine, path = simulate_slide(board, pos, d)
            if hit_mine or end == pos:
                continue
            collected = len(gems_hit & gem_set)
            if collected > best_score:
                best_score = collected
                best_dir   = d
                best_path  = path
        return max(best_score, 0), best_dir, best_path

    @staticmethod
    def _split(gem_set):
        lst  = list(gem_set)
        rows = [g[0] for g in lst]
        cols = [g[1] for g in lst]
        rv   = max(rows) - min(rows)
        cv   = max(cols) - min(cols)
        if rv >= cv:
            med   = sorted(rows)[len(rows) // 2]
            left  = frozenset(g for g in lst if g[0] <= med)
            right = frozenset(g for g in lst if g[0] >  med)
        else:
            med   = sorted(cols)[len(cols) // 2]
            left  = frozenset(g for g in lst if g[1] <= med)
            right = frozenset(g for g in lst if g[1] >  med)
        if not right:
            return gem_set, frozenset()
        return left, right


# ==================== DYNAMIC PROGRAMMING AI ====================

class DPAI:
    name        = "Dynamic Programming"
    description = (
        "TRUE DP: memoizes dp[state]=max_gems over ALL reachable states, "
        "no depth cap, overlapping subproblems reused."
    )
    MAX_GEMS_FOR_DP = 12

    def __init__(self):
        self._memo = {}

    def choose_move(self, board, ball_pos):
        remaining = board.remaining_gems()
        if len(remaining) > self.MAX_GEMS_FOR_DP:
            remaining = self._reachable_gems(board, ball_pos, remaining)
        self._memo = {}
        best_score = -1
        best_dir   = None
        best_path  = []
        for d in ALL_DIRECTIONS:
            end, gems_hit, hit_mine, path = simulate_slide(board, ball_pos, d)
            if hit_mine or end == ball_pos:
                continue
            collected     = gems_hit & remaining
            new_remaining = remaining - collected
            future = self._dp(board, end, new_remaining)
            total  = len(collected) + future
            if total > best_score:
                best_score = total
                best_dir   = d
                best_path  = path
        if best_dir is None:
            return GreedyAI().choose_move(board, ball_pos)
        return best_dir, best_path

    def _dp(self, board, pos, remaining):
        if not remaining:
            return 0
        state = (pos, remaining)
        if state in self._memo:
            return self._memo[state]
        best = 0
        for d in ALL_DIRECTIONS:
            end, gems_hit, hit_mine, _ = simulate_slide(board, pos, d)
            if hit_mine or end == pos:
                continue
            collected     = gems_hit & remaining
            new_remaining = remaining - collected
            future = self._dp(board, end, new_remaining)
            total  = len(collected) + future
            if total > best:
                best = total
        self._memo[state] = best
        return best

    def _reachable_gems(self, board, pos, all_gems):
        ranked = sorted(all_gems,
                        key=lambda g: abs(g[0] - pos[0]) + abs(g[1] - pos[1]))
        return frozenset(ranked[:self.MAX_GEMS_FOR_DP])


# ==================================================================
# BACKTRACKING AI — Contribution 1 of 4
# Author  : Badri Nath — State Space & Decision Tree
# ==================================================================

class BacktrackState:
    """S = (position, remaining_gems) — one node in the search tree."""

    MAX_DEPTH = 6

    def __init__(self, position, remaining, depth=0):
        self.position  = position
        self.remaining = remaining
        self.depth     = depth

    def is_terminal(self):
        return (not self.remaining) or (self.depth >= self.MAX_DEPTH)

    def child(self, new_position, gems_collected):
        return BacktrackState(
            position  = new_position,
            remaining = self.remaining - gems_collected,
            depth     = self.depth + 1,
        )

    def __repr__(self):
        return (f"BacktrackState(pos={self.position}, "
                f"gems_left={len(self.remaining)}, depth={self.depth})")


# ==================================================================
# BACKTRACKING AI — Contribution 2 of 4
# Author  : Dhiraj — Move Generation
# ==================================================================

class BacktrackMoveGen:
    """Dhiraj — expands a state into all valid (direction, end, collected, path) tuples."""

    @staticmethod
    def generate_moves(board, state):
        moves = []
        for direction in ALL_DIRECTIONS:
            end, gems_hit, hit_mine, path = simulate_slide(
                board, state.position, direction
            )
            if hit_mine or end == state.position:
                continue
            collected = gems_hit & state.remaining
            moves.append((direction, end, collected, path))
        return moves

    @staticmethod
    def score_move(end_pos, collected, remaining_after):
        immediate = len(collected) * 10
        if remaining_after:
            min_dist = min(
                abs(end_pos[0] - g[0]) + abs(end_pos[1] - g[1])
                for g in remaining_after
            )
        else:
            min_dist = 0
        return immediate - min_dist


# ==================================================================
# BACKTRACKING AI — Contribution 3 of 4
# Author  : Nikhil
# Topic   : Recursive Exploration — Depth-Limited Search Engine
# ==================================================================
#
# THE RECURSIVE STRUCTURE
# ------------------------
# solve(state, depth)  is the heart of the algorithm.
#
#   solve(state, depth):
#       if terminal:
#           return 0
#       for each move in generate_moves(state):
#           child_state = state.child(move)     ← go deeper
#           future = solve(child_state, depth-1) ← RECURSIVE CALL
#           score  = gems_now + future
#           track best score
#       return best score
#
# SEARCH TREE EXAMPLE
# --------------------
#   State S  (depth 0)
#    ├─ Move A  → State SA  (depth 1)
#    │    ├─ Move A1 → State SA1  (depth 2) → base case returns 0
#    │    └─ Move A2 → State SA2  (depth 2) → base case returns 1
#    │         score(A) = gems(A) + max(0, 1) = gems(A) + 1
#    └─ Move B  → State SB  (depth 1)
#         ├─ Move B1 → State SB1  (depth 2) → returns 2
#         └─ Move B2 → State SB2  (depth 2) → returns 0
#              score(B) = gems(B) + max(2, 0) = gems(B) + 2
#
#   best at root = max(score(A), score(B))
#
# DEPTH-LIMITED SEARCH
# ---------------------
# Without a depth cap the recursion could run forever in cyclic grids.
# BacktrackState.MAX_DEPTH = 6 caps it.  Adaptive depth (Sukanth's
# contribution) relaxes this cap to MAX_DEPTH=∞ when ≤4 gems remain.
#
# WHY EVALUATE FUTURE OUTCOMES?
# --------------------------------
# A greedy algorithm only asks: "which move scores most NOW?"
# The recursive engine asks:    "which move leads to the most gems
#                                across ALL future moves within depth?"
# This is the key difference that makes backtracking strategic.

class BacktrackSearchEngine:
    """
    Nikhil — Recursive Search Engine
    ==================================
    Explores the search tree depth-first, evaluating future outcomes
    at each node by recursing into child states.

    Uses BacktrackState (Badri Nath) to represent nodes and
    BacktrackMoveGen (Dhiraj) to expand them.

    Returns the best total gem score reachable from a given state,
    plus the first move and path leading to that score.
    """

    def recurse(self, board, state):
        """
        Depth-limited recursive search from `state`.

        Pattern:
            explore move
            ↓
            recurse deeper          (go down the tree)
            ↓
            score = now + future    (evaluate on the way back UP)
            ↓
            track best              (compare branches)

        Returns
        -------
        (best_score, best_direction, best_path)
        """

        # ---- Base case: terminal state --------------------------------
        # No gems left OR depth cap reached — nothing more to collect.
        if state.is_terminal():
            return 0, None, []

        # ---- Generate and order moves (Dhiraj's layer) ----------------
        raw_moves = BacktrackMoveGen.generate_moves(board, state)

        if not raw_moves:
            return 0, None, []   # no legal moves from this position

        # Order moves best-first using the heuristic score
        # so good branches are found early (enables better pruning later)
        ordered = sorted(
            raw_moves,
            key=lambda m: BacktrackMoveGen.score_move(
                m[1], m[2], state.remaining - m[2]
            ),
            reverse=True,
        )

        # ---- Recursive exploration ------------------------------------
        best_score = -1
        best_dir   = None
        best_path  = []

        for direction, end, collected, path in ordered:

            # Build the child state (Badri Nath's BacktrackState.child)
            # This is the "explore deeper" step — descend one level
            child_state = state.child(end, collected)

            # Recursive call — evaluate all moves from the child state
            future_score, _, _ = self.recurse(board, child_state)

            # Calculate total gems reachable via this branch
            total = len(collected) + future_score

            # Track the best branch seen so far
            if total > best_score:
                best_score = total
                best_dir   = direction
                best_path  = path

            # Early exit: perfect solution found — stop searching
            if best_score == len(state.remaining):
                break

        return best_score, best_dir, best_path


# ==================== AI REGISTRY ====================

AI_ALGORITHMS = {
    "Greedy":              GreedyAI,
    "Divide & Conquer":    DivideConquerAI,
    "Dynamic Programming": DPAI,
}

AI_NAMES = list(AI_ALGORITHMS.keys())


# ==================== GAME STATE ====================

class GameState:
    def __init__(self, map_name, ai_name="Greedy"):
        self.map_name = map_name
        self.ai_name  = ai_name
        self._build()

    def _build(self):
        self.board     = Board(self.map_name)
        self.ball_pos  = self.board.start
        self.human_score = 0
        self.cpu_score   = 0
        self.human_moves = 0
        self.cpu_moves   = 0
        self.game_over        = False
        self.human_eliminated = False
        self.cpu_eliminated   = False
        ai_cls  = AI_ALGORITHMS.get(self.ai_name, GreedyAI)
        self.ai = ai_cls()

    def reset(self):
        self._build()

    def change_map(self, map_name):
        self.map_name = map_name
        self._build()

    def change_ai(self, ai_name):
        self.ai_name = ai_name
        ai_cls  = AI_ALGORITHMS.get(ai_name, GreedyAI)
        self.ai = ai_cls()

    def human_move(self, direction):
        if self.game_over:
            return False, [], False
        end, gems, hit_mine, path = simulate_slide(self.board, self.ball_pos, direction)
        if hit_mine:
            self.ball_pos         = end
            self.human_eliminated = True
            self.game_over        = True
            return False, path, True
        if end == self.ball_pos:
            return False, [], False
        self.ball_pos = end
        self.human_moves += 1
        for r, c in path[1:]:
            if self.board.cell(r, c) == GEM:
                self.board.remove_gem(r, c)
                self.human_score += 1
        self._check_done()
        return True, path, False

    def cpu_move(self):
        if self.game_over:
            return False, [], False
        direction, _ = self.ai.choose_move(self.board, self.ball_pos)
        if direction is None:
            self.game_over = True
            return False, [], False
        end, gems, hit_mine, path = simulate_slide(self.board, self.ball_pos, direction)
        if hit_mine:
            self.ball_pos       = end
            self.cpu_eliminated = True
            self.game_over      = True
            return False, path, True
        if end == self.ball_pos:
            self.game_over = True
            return False, [], False
        self.ball_pos = end
        self.cpu_moves += 1
        for r, c in path[1:]:
            if self.board.cell(r, c) == GEM:
                self.board.remove_gem(r, c)
                self.cpu_score += 1
        self._check_done()
        return True, path, False

    def _check_done(self):
        if self.human_score + self.cpu_score >= self.board.total_gems():
            self.game_over = True

    def winner_text(self):
        if self.human_eliminated:
            return "💥 You hit a mine! CPU wins!"
        if self.cpu_eliminated:
            return "💥 CPU hit a mine! You win!"
        if self.human_score > self.cpu_score:
            return "🎉 You win!"
        if self.cpu_score > self.human_score:
            return "🤖 CPU wins!"
        return "🤝 It's a tie!"

    def human_efficiency(self):
        return self.human_score / max(self.human_moves, 1)

    def cpu_efficiency(self):
        return self.cpu_score / max(self.cpu_moves, 1)

    def remaining_gems(self):
        return len(self.board.remaining_gems())
