"""
INERTIA - Vesper UI  (unchanged from previous version)
=======================================================
Run this file:  python inertia_ui.py
Requires:       inertia_core.py in the same folder.

Vesper Colour Palette
  bg        #1e1e2e   surface   #2a2a3e   panel    #313145
  purple    #c792ea   cyan      #89ddff   green    #c3e88d
  red       #f07178   orange    #ffcb6b   text     #cdd6f4
  muted     #6c7086
"""

import tkinter as tk
from inertia_core import (
    EMPTY, GEM, MINE, STOP,
    UP, DOWN, LEFT, RIGHT,
    UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT,
    ALL_DIRECTIONS, MAP_NAMES, AI_NAMES,
    GameState,
)

# ==================== VESPER PALETTE ====================

V = {
    "bg":          "#1e1e2e",
    "surface":     "#2a2a3e",
    "panel":       "#313145",
    "border":      "#44475a",
    "purple":      "#c792ea",
    "cyan":        "#89ddff",
    "green":       "#c3e88d",
    "red":         "#f07178",
    "orange":      "#ffcb6b",
    "yellow":      "#ffe082",
    "text":        "#cdd6f4",
    "muted":       "#6c7086",
    "white":       "#ffffff",
    "gem_fill":    "#89ddff",
    "gem_outline": "#c792ea",
    "mine_fill":   "#f07178",
    "stop_fill":   "#ffcb6b",
    "ball_fill":   "#c3e88d",
    "cell_a":      "#252535",
    "cell_b":      "#2d2d40",
}

CELL_SIZE = 58


# ==================== WIDGET HELPERS ====================

def _btn(parent, text, command, bg=None, fg=None,
         font_size=11, pad_x=18, pad_y=8, **kw):
    bg = bg or V["purple"]
    fg = fg or V["bg"]
    return tk.Button(
        parent, text=text, command=command,
        bg=bg, fg=fg,
        activebackground=V["cyan"], activeforeground=V["bg"],
        font=("Consolas", font_size, "bold"),
        relief=tk.FLAT, bd=0, cursor="hand2",
        padx=pad_x, pady=pad_y, **kw
    )


def _label(parent, text, fg=None, font_size=11,
           bold=False, bg=None, **kw):
    return tk.Label(
        parent, text=text,
        fg=fg or V["text"],
        bg=bg or V["bg"],
        font=("Consolas", font_size, "bold" if bold else "normal"),
        **kw
    )


def _frame(parent, bg=None, **kw):
    return tk.Frame(parent, bg=bg or V["bg"], **kw)


# ==================== START MENU ====================

class StartMenu(tk.Frame):

    def __init__(self, master, on_start):
        super().__init__(master, bg=V["bg"])
        self.on_start      = on_start
        self._sel_map      = tk.StringVar(value=MAP_NAMES[0])
        self._sel_ai       = tk.StringVar(value=AI_NAMES[0])
        self._ai_desc_var  = tk.StringVar()
        self._build()

    def _build(self):
        self.pack(fill=tk.BOTH, expand=True)

        # Title
        top = _frame(self)
        top.pack(fill=tk.X, pady=(50, 10))
        _label(top, "⚡  INERTIA  ⚡",
               fg=V["purple"], font_size=36, bold=True).pack()
        _label(top, "Slide · Collect · Conquer",
               fg=V["muted"], font_size=12).pack(pady=(4, 0))

        # Card
        card = _frame(self, bg=V["surface"])
        card.pack(padx=100, pady=30, ipadx=32, ipady=26)

        self._section(card, "SELECT MAP")
        map_opt = tk.OptionMenu(card, self._sel_map, *MAP_NAMES)
        self._style_menu(map_opt)
        map_opt.pack(fill=tk.X, padx=12, pady=(0, 14))

        self._section(card, "SELECT AI ALGORITHM")
        ai_opt = tk.OptionMenu(card, self._sel_ai, *AI_NAMES)
        self._style_menu(ai_opt)
        ai_opt.pack(fill=tk.X, padx=12, pady=(0, 6))

        self._update_desc()
        self._sel_ai.trace_add("write", lambda *_: self._update_desc())

        desc = _label(card, "", fg=V["muted"], font_size=9,
                      bg=V["surface"], wraplength=360, justify="left")
        desc.config(textvariable=self._ai_desc_var)
        desc.pack(anchor="w", padx=12, pady=(0, 18))

        _btn(card, "▶   START GAME", self._start,
             bg=V["green"], fg=V["bg"],
             font_size=13, pad_x=34, pad_y=13).pack(pady=(4, 12))

        # Legend
        legend = _frame(self)
        legend.pack(pady=12)
        for icon, name, color in [
            ("◆", "Gem",  V["cyan"]),
            ("✕", "Mine", V["red"]),
            ("■", "Stop", V["orange"]),
            ("●", "Ball", V["green"]),
        ]:
            f = _frame(legend)
            f.pack(side=tk.LEFT, padx=20)
            _label(f, icon, fg=color, font_size=15).pack()
            _label(f, name, fg=V["muted"], font_size=9).pack()

        _label(self, "Arrow / WASD / QEZC keys  or  click the board",
               fg=V["muted"], font_size=9).pack(pady=(8, 0))

        # Algorithm comparison table
        self._algo_table()

    def _section(self, parent, text):
        _label(parent, text, fg=V["cyan"], font_size=9,
               bold=True, bg=V["surface"]).pack(anchor="w", padx=12, pady=(10, 3))

    def _style_menu(self, menu):
        menu.config(
            bg=V["panel"], fg=V["text"],
            activebackground=V["purple"], activeforeground=V["bg"],
            highlightthickness=0, font=("Consolas", 10),
            relief=tk.FLAT, bd=0, width=30, anchor="w"
        )
        menu["menu"].config(
            bg=V["panel"], fg=V["text"],
            font=("Consolas", 10),
            activebackground=V["purple"], activeforeground=V["bg"]
        )

    def _update_desc(self):
        from inertia_core import AI_ALGORITHMS
        ai_cls = AI_ALGORITHMS.get(self._sel_ai.get())
        self._ai_desc_var.set(getattr(ai_cls, "description", "") if ai_cls else "")

    def _start(self):
        self.on_start(self._sel_map.get(), self._sel_ai.get())

    def _algo_table(self):
        tbl = _frame(self, bg=V["panel"])
        tbl.pack(padx=60, pady=(10, 0), fill=tk.X, ipadx=10, ipady=8)

        _label(tbl, "ALGORITHM COMPARISON",
               fg=V["yellow"], font_size=9, bold=True, bg=V["panel"]).pack(pady=(6, 4))

        rows = [
            ("Greedy",              "O(8)",        "O(1)",     "Fastest",  "Weakest"),
            ("Divide & Conquer",    "O(8·log n)",  "O(n)",     "Fast",     "Strong"),
            ("Dynamic Programming", "O(8·2^n)",    "O(pos·2^n)","Slow",   "Optimal"),
        ]
        header = _frame(tbl, bg=V["surface"])
        header.pack(fill=tk.X, padx=6, pady=(0, 2))
        for h, w in [("Algorithm", 22), ("Time", 12), ("Space", 14), ("Speed", 8), ("Quality", 8)]:
            _label(header, h, fg=V["cyan"], font_size=8,
                   bold=True, bg=V["surface"], width=w).pack(side=tk.LEFT)

        colors = [V["green"], V["orange"], V["purple"]]
        for i, (algo, time_, space, speed, quality) in enumerate(rows):
            row = _frame(tbl, bg=V["panel"])
            row.pack(fill=tk.X, padx=6, pady=1)
            for val, w in [(algo, 22), (time_, 12), (space, 14), (speed, 8), (quality, 8)]:
                _label(row, val, fg=colors[i], font_size=8,
                       bg=V["panel"], width=w).pack(side=tk.LEFT)


# ==================== HUD ====================

class HUD(tk.Frame):

    def __init__(self, master, on_menu, on_restart, on_change_algo):
        super().__init__(master, bg=V["surface"])
        self._on_menu    = on_menu
        self._on_restart = on_restart
        self._on_change  = on_change_algo
        self._build()

    def _build(self):
        self.pack(fill=tk.X)
        self.configure(pady=6)

        left = _frame(self, bg=V["surface"])
        left.pack(side=tk.LEFT, padx=10)
        _btn(left, "← Menu", self._on_menu,
             bg=V["panel"], fg=V["muted"],
             font_size=9, pad_x=8, pad_y=4).pack(side=tk.LEFT)
        _label(left, "  ⚡ INERTIA",
               fg=V["purple"], font_size=14, bold=True,
               bg=V["surface"]).pack(side=tk.LEFT)

        centre = _frame(self, bg=V["surface"])
        centre.pack(side=tk.LEFT, expand=True)

        self._human_var = tk.StringVar()
        self._cpu_var   = tk.StringVar()
        self._rem_var   = tk.StringVar()
        self._ai_var    = tk.StringVar()

        for var, fg in [
            (self._human_var, V["green"]),
            (self._rem_var,   V["cyan"]),
            (self._cpu_var,   V["red"]),
            (self._ai_var,    V["purple"]),
        ]:
            lbl = _label(centre, "", fg=fg, font_size=10,
                         bold=True, bg=V["surface"])
            lbl.config(textvariable=var)
            lbl.pack(side=tk.LEFT, padx=14)

        right = _frame(self, bg=V["surface"])
        right.pack(side=tk.RIGHT, padx=10)
        _btn(right, "⚙ Algo", self._on_change,
             bg=V["orange"], fg=V["bg"],
             font_size=9, pad_x=10, pad_y=4).pack(side=tk.LEFT, padx=4)
        _btn(right, "↺ Restart", self._on_restart,
             bg=V["panel"], fg=V["text"],
             font_size=9, pad_x=10, pad_y=4).pack(side=tk.LEFT)

    def update(self, gs: GameState):
        self._human_var.set(
            f"👤  {gs.human_score} gems  "
            f"({gs.human_moves} moves, {gs.human_efficiency():.2f} eff)"
        )
        self._cpu_var.set(
            f"🤖  {gs.cpu_score} gems  "
            f"({gs.cpu_moves} moves, {gs.cpu_efficiency():.2f} eff)"
        )
        self._rem_var.set(f"💎  {gs.remaining_gems()} left")
        self._ai_var.set( f"AI: {gs.ai_name}")


# ==================== ALGO PICKER POPUP ====================

class AlgoPicker(tk.Toplevel):

    def __init__(self, master, current_ai, on_pick):
        super().__init__(master)
        self.title("Switch Algorithm")
        self.configure(bg=V["bg"])
        self.resizable(False, False)
        self.grab_set()

        _label(self, "SWITCH AI ALGORITHM",
               fg=V["cyan"], font_size=12, bold=True).pack(pady=(20, 10))

        from inertia_core import AI_ALGORITHMS
        for name in AI_NAMES:
            ai_cls = AI_ALGORITHMS[name]
            desc   = getattr(ai_cls, "description", "")
            row    = _frame(self, bg=V["surface"])
            row.pack(fill=tk.X, padx=20, pady=5, ipadx=10, ipady=8)
            col = V["green"] if name == current_ai else V["purple"]
            _btn(row, name,
                 lambda n=name: self._pick(n, on_pick),
                 bg=col, fg=V["bg"],
                 font_size=10, pad_x=10, pad_y=6).pack(side=tk.LEFT)
            _label(row, f"  {desc}",
                   fg=V["muted"], font_size=9,
                   bg=V["surface"]).pack(side=tk.LEFT, padx=8)

        _btn(self, "Cancel", self.destroy,
             bg=V["panel"], fg=V["muted"], font_size=9).pack(pady=(8, 20))

    def _pick(self, name, callback):
        callback(name)
        self.destroy()


# ==================== BOARD CANVAS ====================

class BoardCanvas(tk.Canvas):

    def __init__(self, master, gs: GameState):
        self.gs = gs
        brd     = gs.board
        w = brd.cols * CELL_SIZE
        h = brd.rows * CELL_SIZE
        super().__init__(
            master, width=w, height=h,
            bg=V["bg"], highlightthickness=2,
            highlightbackground=V["border"]
        )
        self.pack(padx=16, pady=10)
        self._draw()

    def refresh(self, gs: GameState):
        self.gs = gs
        self._draw()

    def _draw(self):
        self.delete("all")
        gs  = self.gs
        brd = gs.board

        for r in range(brd.rows):
            for c in range(brd.cols):
                x = c * CELL_SIZE
                y = r * CELL_SIZE
                fill = V["cell_a"] if (r + c) % 2 == 0 else V["cell_b"]
                self.create_rectangle(
                    x, y, x + CELL_SIZE, y + CELL_SIZE,
                    fill=fill, outline=""
                )

        for r in range(brd.rows):
            for c in range(brd.cols):
                cx = c * CELL_SIZE + CELL_SIZE // 2
                cy = r * CELL_SIZE + CELL_SIZE // 2
                cell = brd.cell(r, c)
                if cell == GEM:
                    self._gem(cx, cy)
                elif cell == MINE:
                    self._mine(cx, cy)
                elif cell == STOP:
                    self._stop(cx, cy)

        self._ball(*gs.ball_pos)

    def _gem(self, cx, cy):
        s = CELL_SIZE // 3
        self.create_polygon(
            cx, cy - s, cx + s, cy, cx, cy + s, cx - s, cy,
            fill=V["gem_fill"], outline=V["gem_outline"], width=2
        )

    def _mine(self, cx, cy):
        r = CELL_SIZE // 3 - 2
        self.create_oval(
            cx - r, cy - r, cx + r, cy + r,
            fill=V["mine_fill"], outline=V["red"], width=2
        )
        m = r - 4
        self.create_line(cx - m, cy - m, cx + m, cy + m, fill=V["white"], width=3)
        self.create_line(cx + m, cy - m, cx - m, cy + m, fill=V["white"], width=3)

    def _stop(self, cx, cy):
        r = CELL_SIZE // 3 - 2
        self.create_oval(
            cx - r, cy - r, cx + r, cy + r,
            fill=V["stop_fill"], outline=V["orange"], width=2
        )
        bh = max(3, r // 2)
        self.create_rectangle(
            cx - r + 4, cy - bh, cx + r - 4, cy + bh,
            fill=V["bg"], outline=""
        )

    def _ball(self, row, col, tag="ball"):
        self.delete(tag)
        cx = col * CELL_SIZE + CELL_SIZE // 2
        cy = row * CELL_SIZE + CELL_SIZE // 2
        r  = CELL_SIZE // 3 - 1
        self.create_oval(
            cx - r, cy - r, cx + r, cy + r,
            fill=V["ball_fill"], outline=V["green"], width=2, tags=tag
        )
        gr = max(3, r // 3)
        self.create_oval(
            cx - r + 4, cy - r + 4,
            cx - r + 4 + gr, cy - r + 4 + gr,
            fill=V["white"], outline="", tags=tag
        )

    def animate_path(self, path, done_cb, delay=70):
        self._ap       = path
        self._ai       = 0
        self._acb      = done_cb
        self._adelay   = delay
        self._astep()

    def _astep(self):
        if self._ai >= len(self._ap):
            self._acb()
            return
        r, c = self._ap[self._ai]
        self._ball(r, c)
        self._ai += 1
        self.after(self._adelay, self._astep)


# ==================== GAME VIEW ====================

class GameView(tk.Frame):

    def __init__(self, master, map_name, ai_name, on_menu):
        super().__init__(master, bg=V["bg"])
        self.on_menu    = on_menu
        self._animating = False
        self._waiting   = False
        self.gs         = GameState(map_name, ai_name)
        self._build()
        self.pack(fill=tk.BOTH, expand=True)

    def _build(self):
        self.hud = HUD(
            self,
            on_menu        = self._go_menu,
            on_restart     = self._restart,
            on_change_algo = self._change_algo,
        )
        self.hud.update(self.gs)

        self._map_var = tk.StringVar(value=self.gs.map_name)
        ml = _label(self, "", fg=V["muted"], font_size=9)
        ml.config(textvariable=self._map_var)
        ml.pack()

        host = _frame(self)
        host.pack()
        self.bc = BoardCanvas(host, self.gs)
        self.bc.bind("<Button-1>", self._click)

        self._status = tk.StringVar(
            value="Your move  ·  arrow / WASD / QEZC  or  click"
        )
        sl = _label(self, "", fg=V["muted"], font_size=9)
        sl.config(textvariable=self._status)
        sl.pack(pady=(0, 8))

        self._bind_keys()

    def _bind_keys(self):
        root = self.winfo_toplevel()
        for key, d in [
            ("<Up>", UP), ("<Down>", DOWN),
            ("<Left>", LEFT), ("<Right>", RIGHT),
            ("w", UP), ("s", DOWN), ("a", LEFT), ("d", RIGHT),
            ("q", UP_LEFT), ("e", UP_RIGHT),
            ("z", DOWN_LEFT), ("c", DOWN_RIGHT),
        ]:
            root.bind(key, lambda ev, d=d: self._human_move(d))

    def _click(self, event):
        if self._animating or self._waiting or self.gs.game_over:
            return
        col = event.x // CELL_SIZE
        row = event.y // CELL_SIZE
        br, bc = self.gs.ball_pos
        dr, dc = row - br, col - bc
        if dr == 0 and dc == 0:
            return
        if abs(dr) > 0 and abs(dc) > 0:
            d = (1 if dr > 0 else -1, 1 if dc > 0 else -1)
        elif abs(dr) > abs(dc):
            d = (1 if dr > 0 else -1, 0)
        else:
            d = (0, 1 if dc > 0 else -1)
        self._human_move(d)

    def _human_move(self, direction):
        if self._animating or self._waiting or self.gs.game_over:
            return
        success, path, hit_mine = self.gs.human_move(direction)
        if not success and not hit_mine:
            return
        self._animating = True
        self._status.set("Sliding…")

        def after():
            self._animating = False
            self.bc.refresh(self.gs)
            self.hud.update(self.gs)
            if hit_mine or self.gs.game_over:
                self._end_game()
                return
            self._cpu_turn()

        self.bc.animate_path(path, after)

    def _cpu_turn(self):
        self._waiting = True
        self._status.set("CPU thinking…")
        self.after(350, self._run_cpu)

    def _run_cpu(self):
        success, path, hit_mine = self.gs.cpu_move()
        if not success and not hit_mine:
            self._waiting = False
            self._end_game()
            return
        self._animating = True

        def after():
            self._animating = False
            self._waiting   = False
            self.bc.refresh(self.gs)
            self.hud.update(self.gs)
            if hit_mine or self.gs.game_over:
                self._end_game()
                return
            self._status.set("Your move  ·  arrow / WASD / QEZC  or  click")

        self.bc.animate_path(path, after)

    def _end_game(self):
        self.bc.refresh(self.gs)
        self.hud.update(self.gs)
        self._status.set(self.gs.winner_text())
        self._overlay()

    def _overlay(self):
        gs = self.gs
        ov = tk.Toplevel(self.winfo_toplevel())
        ov.title("Game Over")
        ov.configure(bg=V["bg"])
        ov.resizable(False, False)
        ov.grab_set()

        _label(ov, gs.winner_text(),
               fg=V["yellow"], font_size=18, bold=True).pack(pady=(24, 8))

        for name, score, moves, eff, color in [
            ("👤 You", gs.human_score, gs.human_moves, gs.human_efficiency(), V["green"]),
            ("🤖 CPU", gs.cpu_score,   gs.cpu_moves,   gs.cpu_efficiency(),   V["red"]),
        ]:
            _label(ov,
                   f"{name}:  {score} gems  ·  {moves} moves  ·  eff {eff:.2f}",
                   fg=color, font_size=11).pack(pady=2)

        _label(ov, f"Algorithm: {gs.ai_name}", fg=V["purple"], font_size=10).pack(pady=(8, 2))
        _label(ov, f"Map: {gs.map_name}",      fg=V["muted"],  font_size=9).pack(pady=(0, 16))

        row = _frame(ov)
        row.pack(pady=(0, 20))

        def _restart():
            ov.destroy()
            self._restart()

        def _menu():
            ov.destroy()
            self._go_menu()

        _btn(row, "↺  Play Again", _restart,
             bg=V["green"],  fg=V["bg"],   font_size=11).pack(side=tk.LEFT, padx=8)
        _btn(row, "← Main Menu",  _menu,
             bg=V["surface"], fg=V["text"], font_size=11).pack(side=tk.LEFT, padx=8)

    def _restart(self):
        self._animating = False
        self._waiting   = False
        self.gs.reset()
        self.bc.refresh(self.gs)
        self.hud.update(self.gs)
        self._status.set("Your move  ·  arrow / WASD / QEZC  or  click")

    def _change_algo(self):
        AlgoPicker(self.winfo_toplevel(), self.gs.ai_name, self._apply_algo)

    def _apply_algo(self, ai_name):
        self.gs.change_ai(ai_name)
        self.hud.update(self.gs)

    def _go_menu(self):
        root = self.winfo_toplevel()
        for key in ("<Up>","<Down>","<Left>","<Right>",
                    "w","s","a","d","q","e","z","c"):
            try:
                root.unbind(key)
            except Exception:
                pass
        self.destroy()
        self.on_menu()


# ==================== APP ====================

class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("⚡ INERTIA")
        self.configure(bg=V["bg"])
        self.resizable(True, True)
        self._show_menu()

    def _show_menu(self):
        StartMenu(self, on_start=self._start_game)

    def _start_game(self, map_name, ai_name):
        for w in self.winfo_children():
            w.destroy()
        GameView(self, map_name, ai_name, on_menu=self._back_to_menu)

    def _back_to_menu(self):
        for w in self.winfo_children():
            w.destroy()
        self._show_menu()


if __name__ == "__main__":
    App().mainloop()
