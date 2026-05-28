import tkinter as tk
import math

drawing = False
radius = 12
path = []
progress_index = 0

mint = "#3EB489"
turquoise = "#7FFFD4"
easy_color = "#6BFFB0"
medium_color = "#FFD166"
hard_color = "#FF6B6B"
level_color = "#4FC3F7"
back_color = "#AAAAAA"

current_difficulty = None
current_level = 1

def dist(px, py, x1, y1, x2, y2):
    A = px - x1
    B = py - y1
    C = x2 - x1
    D = y2 - y1

    dot = A * C + B * D
    len_sq = C * C + D * D

    param = dot / len_sq if len_sq != 0 else -1

    if param < 0:
        xx, yy = x1, y1
    elif param > 1:
        xx, yy = x2, y2
    else:
        xx = x1 + param * C
        yy = y1 + param * D

    dx = px - xx
    dy = py - yy

    return math.sqrt(dx * dx + dy * dy)


def center_path(path):
    xs = [p[0] for p in path]
    ys = [p[1] for p in path]

    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    path_center_x = (min_x + max_x) / 2
    path_center_y = (min_y + max_y) / 2

    canvas.update_idletasks()
    w = canvas.winfo_width()
    h = canvas.winfo_height()

    dx = w / 2 - path_center_x
    dy = h / 2 - path_center_y

    return [(x + dx, y + dy) for x, y in path]

easy_levels = [
    [(100, 300), (700, 300)],
    [(400, 100), (400, 500)],
    [(100, 250), (700, 350)]
]

medium_levels = [
    [(100, 400), (200, 350), (300, 300), (400, 270), (500, 300), (600, 350), (700, 400)],
    [(100, 400), (300, 200), (500, 400), (700, 300)],
    [(400, 200), (500, 250), (550, 350), (500, 450), (400, 500), (300, 450), (250, 350), (300, 250), (400, 100)]
]

hard_levels = [
    [(100, 400), (200, 400), (200, 300), (300, 300), (300, 200), (400, 200), (400, 100)],
    [(400, 300), (500, 300), (500, 400), (300, 400), (300, 200), (600, 200), (600, 500), (200, 500)],
    [(150, 250), (220, 450), (290, 200), (360, 450), (430, 200), (500, 450), (570, 200), (640, 450), (710, 250)]
]

def show_end_screen(text):
    canvas.pack_forget()
    hide_game_menu_button()
    prev_btn.place_forget()
    next_btn.place_forget()
    difficulty_btn.place_forget()
    end_label.config(text=text)
    end_frame.place(relx=0.5, rely=0.5, anchor="center")

def start_game():
    menu_frame.place_forget()
    level_frame.place(relx=0.5, rely=0.5, anchor="center")

def show_rules():
    menu_frame.place_forget()
    rules_frame.place(relx=0.5, rely=0.5, anchor="center")

def back_to_menu(frame):
    frame.place_forget()
    canvas.pack_forget()
    canvas.delete("all")
    levels_select_frame.place_forget()
    level_frame.place_forget()
    end_frame.place_forget()

    prev_btn.place_forget()
    next_btn.place_forget()
    difficulty_btn.place_forget()

    menu_frame.place(relx=0.5, rely=0.5, anchor="center")
    hide_game_menu_button()


def back_to_difficulty():
    levels_select_frame.place_forget()
    level_frame.place(relx=0.5, rely=0.5, anchor="center")


def back_to_difficulty_from_game():
    canvas.pack_forget()
    hide_game_menu_button()
    prev_btn.place_forget()
    next_btn.place_forget()
    difficulty_btn.place_forget()
    level_frame.place(relx=0.5, rely=0.5, anchor="center")


def update_level_buttons():
    if current_level == 1:
        prev_btn.place_forget()
    else:
        prev_btn.place(x=10, y=60)

    if current_level == 3:
        next_btn.place_forget()
    else:
        next_btn.place(x=160, y=60)


def next_level():
    if current_level < 3:
        load_level(current_difficulty, current_level + 1)


def prev_level():
    if current_level > 1:
        load_level(current_difficulty, current_level - 1)


def load_level(diff, lvl):
    global path, current_difficulty, current_level

    current_difficulty = diff
    current_level = lvl

    levels_select_frame.place_forget()
    canvas.pack(fill="both", expand=True)
    canvas.delete("all")

    show_game_menu_button()

    if diff == "easy":
        path = center_path(easy_levels[lvl - 1])
    elif diff == "medium":
        path = center_path(medium_levels[lvl - 1])
    elif diff == "hard":
        path = center_path(hard_levels[lvl - 1])

    draw_level()
    update_level_buttons()
    difficulty_btn.place(x=320, y=10)


