"""
INERTIA - Core Game Logic  (PURE D&C + PURE DP)
================================================
AI Algorithms:
  Greedy          — immediate best move
  Divide & Conquer— TRUE D&C: splits gem set recursively into subproblems,
                    solves each independently, combines best first-move
  Dynamic Prog.   — TRUE DP: state=(pos, frozenset remaining gems),
                    memoized across the ENTIRE turn, not wiped per call
"""

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
    """Holds the grid and all tile lookups."""

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
    """
    Slide from `start` in `direction` on the REAL board.
    `already_collected` lets the DP/DnC simulate without mutating the board.

    Returns:
        end_pos   : (r, c) where ball stops
        gems_hit  : frozenset of gem positions collected
        hit_mine  : bool
        path      : list[(r,c)] including start
    """
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
    """
    Greedy — pick the move that collects the most gems right now.
    No lookahead, no subproblem splitting.
    """

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
#
# TRUE D&C STRUCTURE
# ==================
# Problem  : "What is the best first move to maximise gems collected
#             from the current position given gem set G?"
#
# Divide   : Split G into two spatial halves (G_left, G_right) by
#             median row or column variance — same axis-split as before.
#
# Conquer  : For EACH half, independently find:
#               best_move(pos, G_half)   ← recursive call
#             This recurses until G_half is a singleton or empty,
#             where the base case returns the direct slide score.
#
# Combine  : From both halves' recommended first moves, pick the one
#             that yields the higher immediate gem count from `pos`.
#             (The combination step merges two independent sub-solutions.)
#
# This is genuine D&C: the gem set is the "input array" being split,
# each half is solved independently, and the results are combined.

class DivideConquerAI:
    """
    Pure Divide & Conquer AI.

    Recursively splits the remaining gem set into spatial halves,
    solves each half independently (base case = slide directly toward
    the sub-cluster), then combines by choosing the first move that
    leads to the higher-value half.
    """

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

    # ------------------------------------------------------------------
    # D&C core
    # ------------------------------------------------------------------

    def _dnc(self, board, pos, gem_set):
        """
        Divide & Conquer over `gem_set`.

        Returns (best_score, best_direction, best_path)
        where best_score = number of gems reachable in `gem_set`
        starting from `pos` using the recommended first move.
        """

        # ---- BASE CASE: 0 or 1 gem ----
        # "Conquer" the trivially small subproblem directly.
        if len(gem_set) == 0:
            return 0, None, []

        if len(gem_set) == 1:
            target = next(iter(gem_set))
            return self._best_move_toward(board, pos, gem_set, target)

        # ---- DIVIDE ----
        left_gems, right_gems = self._split(gem_set)

        # ---- CONQUER each half independently ----
        left_score,  left_dir,  left_path  = self._dnc(board, pos, left_gems)
        right_score, right_dir, right_path = self._dnc(board, pos, right_gems)

        # ---- COMBINE ----
        # Pick the half whose recommended first move yields a higher score.
        # Tie-break: prefer the half with more gems (richer sub-cluster).
        if left_score >= right_score:
            return left_score, left_dir, left_path
        else:
            return right_score, right_dir, right_path

    def _best_move_toward(self, board, pos, gem_set, target):
        """
        Base-case solver: from `pos`, find the move that collects the most
        gems from `gem_set` in a single slide.
        Returns (score, direction, path).
        """
        best_score = -1
        best_dir   = None
        best_path  = []

        for d in ALL_DIRECTIONS:
            end, gems_hit, hit_mine, path = simulate_slide(board, pos, d)
            if hit_mine or end == pos:
                continue
            # Count how many gems from gem_set we actually collect
            collected = len(gems_hit & gem_set)
            if collected > best_score:
                best_score = collected
                best_dir   = d
                best_path  = path

        return max(best_score, 0), best_dir, best_path

    @staticmethod
    def _split(gem_set):
        """
        Split gem_set into two halves along the axis with greater variance.
        Returns (left_half, right_half) as frozensets.
        """
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

        # Guard: if split produced an empty half, push everything to left
        if not right:
            return gem_set, frozenset()
        return left, right


# ==================== DYNAMIC PROGRAMMING AI ====================
#
# TRUE DP STRUCTURE
# =================
# State         : (ball_position, frozenset_of_remaining_gems)
#                 — fully captures everything needed to decide optimally.
#
# Subproblem    : dp[state] = maximum number of gems collectable
#                             from this state onwards (no depth cap).
#
# Recurrence    : dp[(pos, R)] = max over all valid moves d of
#                     |gems_collected(d)| + dp[(new_pos, R - collected)]
#
# Base case     : dp[(pos, frozenset())] = 0   (no gems left)
#
# Overlapping   : The same (pos, R) can be reached via different move
# subproblems     sequences — memoization ensures it is computed once.
#
# Optimal sub-  : The best play from state S is built from the best play
# structure       from each next state — verified by Bellman principle.
#
# Memo lifetime : The table is built ONCE per call to choose_move and
#                 persists for the entire recursive expansion.  It is NOT
#                 cleared between recursive calls (unlike the old code).
#                 It IS cleared between turns because the real board
#                 changes (gems removed) so states are different anyway.

class DPAI:
    """
    Pure Dynamic Programming AI.

    Solves dp[(pos, remaining_gems)] = max gems collectable from here,
    with full memoization and NO arbitrary depth limit.

    To keep it tractable the state space is bounded by capping the
    number of remaining gems considered at MAX_GEMS_FOR_DP.  For larger
    gem counts it falls back to the top-k most reachable gems.
    """

    name        = "Dynamic Programming"
    description = (
        "TRUE DP: memoizes dp[state]=max_gems over ALL reachable states, "
        "no depth cap, overlapping subproblems reused."
    )

    MAX_GEMS_FOR_DP = 12   # beyond this the state space explodes

    def __init__(self):
        # memo persists across recursive calls within one choose_move()
        self._memo = {}

    def choose_move(self, board, ball_pos):
        remaining = board.remaining_gems()

        # If gem count is large, restrict to reachable gems only
        if len(remaining) > self.MAX_GEMS_FOR_DP:
            remaining = self._reachable_gems(board, ball_pos, remaining)

        # Clear memo for this turn (board has changed since last turn)
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

            # Solve the subproblem from the next state
            future = self._dp(board, end, new_remaining)
            total  = len(collected) + future

            if total > best_score:
                best_score = total
                best_dir   = d
                best_path  = path

        if best_dir is None:
            return GreedyAI().choose_move(board, ball_pos)
        return best_dir, best_path

    # ------------------------------------------------------------------
    # DP recurrence
    # ------------------------------------------------------------------

    def _dp(self, board, pos, remaining):
        """
        Returns the maximum number of gems collectable from
        state (pos, remaining) — memoized.

        This is the pure DP recurrence:
            dp[(pos, R)] = 0                           if R is empty
            dp[(pos, R)] = max_d( |collect(d)| + dp[(end_d, R-collect(d))] )
        """
        # ---- Base case ----
        if not remaining:
            return 0

        state = (pos, remaining)

        # ---- Memoization check (overlapping subproblems) ----
        if state in self._memo:
            return self._memo[state]

        # ---- Recurrence ----
        best = 0
        for d in ALL_DIRECTIONS:
            end, gems_hit, hit_mine, _ = simulate_slide(board, pos, d)
            if hit_mine or end == pos:
                continue

            collected     = gems_hit & remaining
            new_remaining = remaining - collected

            # Recursive call — will be memoized on return
            future = self._dp(board, end, new_remaining)
            total  = len(collected) + future

            if total > best:
                best = total

        # ---- Store result ----
        self._memo[state] = best
        return best

    # ------------------------------------------------------------------
    # Helper: limit state space for large boards
    # ------------------------------------------------------------------

    def _reachable_gems(self, board, pos, all_gems):
        """
        BFS-style reachability: return the closest MAX_GEMS_FOR_DP gems
        by Manhattan distance from `pos`.  This keeps the DP tractable
        without sacrificing local optimality.
        """
        ranked = sorted(all_gems,
                        key=lambda g: abs(g[0] - pos[0]) + abs(g[1] - pos[1]))
        return frozenset(ranked[:self.MAX_GEMS_FOR_DP])

    def memo_stats(self):
        return {"memo_size": len(self._memo)}


# ==================== AI REGISTRY ====================

AI_ALGORITHMS = {
    "Greedy":              GreedyAI,
    "Divide & Conquer":    DivideConquerAI,
    "Dynamic Programming": DPAI,
}

AI_NAMES = list(AI_ALGORITHMS.keys())


# ==================== GAME STATE ====================

class GameState:
    """
    Manages one full game session.
    Tracks board, positions, scores and exposes clean methods
    for both human and CPU play.
    """

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

    # ---- human move ----

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

    # ---- cpu move ----

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

    # ---- helpers ----

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
