import tkinter as tk
from PIL import ImageTk
import sqlite3
from numpy import random


bg_color = "#3d6466"


def clear_widgets(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def fetch_db():
    connection = sqlite3.connect("data/recipes.db")
    cursor = connection.cursor()
    # fetch all the table names
    cursor.execute("SELECT * FROM sqlite_master WHERE type='table';")
    all_tables = cursor.fetchall()
    # chose random recipe idx
    idx = random.randint(0, len(all_tables)-1)
    print(all_tables[idx])

    # fetch ingredients
    table_name = all_tables[idx][1]
    cursor.execute("SELECT * FROM " + table_name + ";")
    table_records = cursor.fetchall()

    connection.close()
    return table_name, table_records


def pre_process(table_name, table_records):
    title = table_name[:-6]
    title = [char if char.islower() else " " + char for char in title]

    ingredients = []

    # ingredients
    for i in table_records:
        name = i[1]
        qty = i[2]
        unit = i[3]
        ingredients.append(qty + " " + unit + " of " + name)

    return title, ingredients


def load_frame1():
    clear_widgets(frame2)
    frame1.tkraise()
    frame1.pack_propagate(False)
    # logo widgets
    logo_img = ImageTk.PhotoImage(file="assets/RRecipe_logo.png")
    logo_widget = tk.Label(frame1, image=logo_img, bg=bg_color)
    logo_widget.image_name = logo_img
    logo_widget.pack()
    
    # insturctions widget
    tk.Label(
        frame1,
        text="ready for your random recipe?",
        bg=bg_color,
        fg="white",
        font=("TkMenuFont", 14)
    ).pack()

    # button widget
    tk.Button(
        frame1,
        text="SHUFFLE",
        font=("TkHeadingFont", 20),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="black",
        command=lambda: load_frame2()
    ).pack(pady=20)


def load_frame2():
    clear_widgets(frame1)
    frame2.tkraise()

    table_name, table_records = fetch_db()
    title, ingredients = pre_process(table_name, table_records)
    
    # logo widgets
    logo_img = ImageTk.PhotoImage(file="assets/RRecipe_logo_bottom.png")
    logo_widget = tk.Label(frame2, image=logo_img, bg=bg_color)
    logo_widget.image_name = logo_img
    logo_widget.pack(pady=20)

    # insturctions widget
    tk.Label(
        frame2,
        text=title,
        bg=bg_color,
        fg="white",
        font=("TkHeadingFont", 20)
    ).pack(pady=25)

    for i in ingredients:
        # insturctions widget
        tk.Label(
            frame2,
            text=i,
            bg="#28393a",
            fg="white",
            font=("TkMenuFont", 12)
        ).pack(fill="both")

    tk.Button(
            frame2,
            text="BACK",
            font=("TkHeadingFont", 18),
            bg="#28393a",
            fg="white",
            cursor="hand2",
            activebackground="#badee2",
            activeforeground="black",
            command=lambda: load_frame1()
        ).pack(pady=20)


# initiallize app
root = tk.Tk()
root.title("Recipe Picker")
root.eval("tk::PlaceWindow   . center")

# create a frame widget
frame1 = tk.Frame(root, width=500, height=600, bg=bg_color)
frame2 = tk.Frame(root, bg=bg_color)

for frame in (frame1, frame2):
    frame.grid(row=0, column=0, sticky="nesw")

load_frame1()

# run app
root.mainloop()
