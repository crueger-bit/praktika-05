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


def open_levels(diff):
    for w in levels_select_frame.winfo_children():
        w.destroy()

    level_frame.place_forget()
    levels_select_frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(levels_select_frame, text=f"Уровни ({diff})",
             font=("Segoe UI", 30, "bold"), fg=mint, bg="black").pack(pady=20)

    for i in range(1, 4):
        tk.Button(levels_select_frame, text=f"Уровень {i}",
                  command=lambda n=i: load_level(diff, n),
                  width=25, height=2,
                  font=("Segoe UI", 16, "bold"),
                  bg=level_color, fg="black", bd=0).pack(pady=10)

    tk.Button(levels_select_frame, text="Назад",
              command=back_to_difficulty,
              width=25, height=2,
              font=("Segoe UI", 16, "bold"),
              bg=back_color, fg="black", bd=0).pack(pady=20)


def draw_level():
    canvas.delete("all")

    for i in range(len(path) - 1):
        canvas.create_line(path[i], path[i + 1], width=24, fill=mint, capstyle="round")

    canvas.create_oval(path[0][0] - 15, path[0][1] - 15,
                       path[0][0] + 15, path[0][1] + 15,
                       fill="green", outline="")

    canvas.create_oval(path[-1][0] - 15, path[-1][1] - 15,
                       path[-1][0] + 15, path[-1][1] + 15,
                       fill="red", outline="")

    canvas.create_text(canvas.winfo_width() // 2, 40,
                       text=f"Уровень {current_level} / 3",
                       fill="white",
                       font=("Segoe UI", 22, "bold"))


def mouse_down(event):
    global drawing, progress_index
    if math.dist((event.x, event.y), path[0]) < 25:
        drawing = True
        progress_index = 0
        canvas.old_x = event.x
        canvas.old_y = event.y


def mouse_move(event):
    global drawing, progress_index, current_level

    if not drawing:
        return

    inside = False
    for i in range(len(path) - 1):
        if dist(event.x, event.y, *path[i], *path[i + 1]) < radius:
            inside = True
            progress_index = max(progress_index, i)

    if not inside:
        drawing = False
        show_end_screen("Поражение\nВы вышли за дорожку")
        return

    canvas.create_line(canvas.old_x, canvas.old_y,
                       event.x, event.y,
                       width=12, fill=turquoise, capstyle="round")

    canvas.old_x = event.x
    canvas.old_y = event.y

    if progress_index >= len(path) - 2 and math.dist((event.x, event.y), path[-1]) < 25:
        drawing = False
        if current_level < 3:
            load_level(current_difficulty, current_level + 1)
        else:
            show_end_screen("Победа\nВы прошли все уровни!")


def mouse_up(event):
    global drawing
    if drawing:
        drawing = False
        show_end_screen("Поражение\nВы оторвали перо")


root = tk.Tk()
root.title("Обведи, не отрывая пера")
root.attributes("-fullscreen", True)
root.configure(bg="black")

canvas = tk.Canvas(root, bg="black", highlightthickness=0)
canvas.bind("<ButtonPress-1>", mouse_down)
canvas.bind("<B1-Motion>", mouse_move)
canvas.bind("<ButtonRelease-1>", mouse_up)


def show_game_menu_button():
    game_menu_button.place(x=10, y=10)


def hide_game_menu_button():
    game_menu_button.place_forget()


menu_frame = tk.Frame(root, bg="black")
menu_frame.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(menu_frame, text="Обведи, не отрывая пера",
         font=("Segoe UI", 36, "bold"),
         fg=mint, bg="black").pack(pady=40)

def btn(parent, text, cmd):
    b = tk.Button(parent, text=text, command=cmd,
                  width=25, height=2,
                  font=("Segoe UI", 16, "bold"),
                  bg=mint, fg="black", bd=0)
    b.pack(pady=10)
    return b


btn(menu_frame, "Играть", start_game)
btn(menu_frame, "Правила", show_rules)
btn(menu_frame, "Выход", root.destroy)

level_frame = tk.Frame(root, bg="black")
tk.Label(level_frame, text="Сложность",
         font=("Segoe UI", 30, "bold"),
         fg=mint, bg="black").pack(pady=30)

tk.Button(level_frame, text="Легкий",
          command=lambda: open_levels("easy"),
          bg=easy_color, width=25, height=2,
          font=("Segoe UI", 16, "bold")).pack(pady=10)

tk.Button(level_frame, text="Средний",
          command=lambda: open_levels("medium"),
          bg=medium_color, width=25, height=2,
          font=("Segoe UI", 16, "bold")).pack(pady=10)

tk.Button(level_frame, text="Сложный",
          command=lambda: open_levels("hard"),
          bg=hard_color, width=25, height=2,
          font=("Segoe UI", 16, "bold")).pack(pady=10)

tk.Button(level_frame, text="Назад",
          command=lambda: back_to_menu(level_frame),
          bg=back_color, width=25, height=2,
          font=("Segoe UI", 16, "bold")).pack(pady=10)

levels_select_frame = tk.Frame(root, bg="black")

game_menu_button = tk.Button(root, text="Меню",
                             command=lambda: back_to_menu(canvas),
                             bg=mint, fg="red",
                             font=("Segoe UI", 14, "bold"))

prev_btn = tk.Button(root, text="Назад", command=prev_level,
                     bg=back_color, font=("Segoe UI", 12, "bold"))

next_btn = tk.Button(root, text="Вперёд", command=next_level,
                     bg=back_color, font=("Segoe UI", 12, "bold"))

difficulty_btn = tk.Button(root, text="Сложность",
                           command=back_to_difficulty_from_game,
                           bg=level_color, font=("Segoe UI", 12, "bold"))

rules_frame = tk.Frame(root, bg="black")
tk.Label(rules_frame,
         text="Начни с зелёной точки\nДойди до красной\nНе выходи за линию\nНе отрывай перо",
         font=("Segoe UI", 24),
         fg="white", bg="black").pack(pady=40)

btn(rules_frame, "Назад", lambda: back_to_menu(rules_frame))

end_frame = tk.Frame(root, bg="black")

end_label = tk.Label(end_frame,
                     text="",
                     font=("Segoe UI", 40, "bold"),
                     fg="white",
                     bg="black")
end_label.pack(pady=50)

tk.Button(end_frame,
          text="В меню",
          command=lambda: back_to_menu(end_frame),
          width=25, height=2,
          font=("Segoe UI", 16, "bold"),
          bg=mint, fg="black").pack(pady=20)

root.mainloop()