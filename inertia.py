# ==============================
# Grid & Cell Configuration
# ==============================

# Cell types
EMPTY = 0
GEM = 1
MINE = 2
STOP = 3


# ==============================
# Movement Directions
# ==============================

# Cardinal directions
UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

# Diagonal directions
UP_LEFT = (-1, -1)
UP_RIGHT = (-1, 1)
DOWN_LEFT = (1, -1)
DOWN_RIGHT = (1, 1)

# Direction sets
CARDINAL_DIRECTIONS = [UP, DOWN, LEFT, RIGHT]
ALL_DIRECTIONS = [
    UP, DOWN, LEFT, RIGHT,
    UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT
]


# ==============================
# Map Definitions & Layouts
# ==============================

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
    }
}


# ==============================
# Core Game Engine & State
# ==============================

class InertiaGame:
    def __init__(self, map_name):
        self.map_name = map_name
        self.reset()

    def reset(self):
        map_data = MAPS[self.map_name]

        self.rows = map_data["rows"]
        self.cols = map_data["cols"]
        self.start_pos = map_data["start"]

        self.board = [[EMPTY for _ in range(self.cols)] for _ in range(self.rows)]

        for r, c in map_data["gems"]:
            self.board[r][c] = GEM
        for r, c in map_data["mines"]:
            self.board[r][c] = MINE
        for r, c in map_data["stops"]:
            self.board[r][c] = STOP

        self.ball_pos = self.start_pos
        self.human_score = 0
        self.cpu_score = 0
        self.human_moves = 0
        self.cpu_moves = 0
        self.game_over = False
        self.human_eliminated = False
        self.cpu_eliminated = False
        self.total_gems = len(map_data["gems"])

    def change_map(self, map_name):
        self.map_name = map_name
        self.reset()

    def simulate_move(self, direction):
        dr, dc = direction
        r, c = self.ball_pos

        gems = 0
        hit_mine = False
        path = [(r, c)]

        while True:
            nr, nc = r + dr, c + dc

            if not (0 <= nr < self.rows and 0 <= nc < self.cols):
                break

            r, c = nr, nc
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
        if self.game_over:
            return False, 0, [], False

        end_pos, gems, hit_mine, path = self.simulate_move(direction)

        if hit_mine:
            self.game_over = True
            if is_human:
                self.human_eliminated = True
            else:
                self.cpu_eliminated = True
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

