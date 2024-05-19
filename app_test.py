import re

import cv2

import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

import opflow


def open_vid():
    file_path = filedialog.askopenfilename(title="Выберите видео", filetypes=[("Video files", "*.mp4")])
    print("e", bool(enabled.get()), "::", bool(auto_points.get()), "::")
    if file_path:
        display_image(file_path)


# Function to handle the Entry widget focus events
def set_entry_placeholder(entry, placeholder_text):
    def on_entry_focus_in(event):
        if entry.get() == placeholder_text:
            entry.delete(0, tk.END)
            entry.configure(show="")

    def on_entry_focus_out(event):
        if entry.get() == "":
            entry.insert(0, placeholder_text)
            entry.configure(show="*")

    entry.insert(0, placeholder_text)
    entry.bind("<FocusIn>", on_entry_focus_in)
    entry.bind("<FocusOut>", on_entry_focus_out)
    entry.pack(anchor=tk.NW, padx=20, pady=5)


def display_image(file_path):
    s = point_count.get()
    s = re.sub('\\s+', '', s)
    if s.isdigit():
        status_label.config(text=f"Загруженный файл: {file_path}")
        opflow.track_video(file_path, entry_field.get(), bool(enabled.get()), bool(auto_points.get()), int(s))
    else:
        status_label.config(text=f"Пожалуйста, введите количество точек, используя ТОЛЬКО цифры")


def toggle():
    if not bool(auto_points.get()):
        point_count.pack_forget()
    else:
        set_entry_placeholder(point_count, "Введите количество точек...")


root = tk.Tk()

root.title("AORTA VALVE TRACKING")
text_widget = tk.Text(root, wrap=tk.WORD, height=15, width=35)

open_button = tk.Button(root, text="Выбрать видео", command=open_vid)
open_button.pack(padx=20, pady=10)

entry_field = tk.Entry(width=50)
set_entry_placeholder(entry_field, "Введите название файла, в который выведутся результаты")

enabled = tk.IntVar()
enabled_checkbutton = tk.Checkbutton(text="Выводить видео", variable=enabled)
enabled_checkbutton.pack(padx=20, pady=10, anchor=tk.NW)

point_count = tk.Entry(width=50)

auto_points = tk.IntVar()
auto_points_checkbutton = tk.Checkbutton(text="Автоматическая расстановка точек", variable=auto_points, command=toggle)
auto_points_checkbutton.pack(padx=20, pady=10, anchor=tk.NW)

status_label = tk.Label(root, text="", padx=20, pady=10)
status_label.pack()

root.mainloop()
