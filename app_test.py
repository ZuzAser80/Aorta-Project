import cv2

import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

import opflow


def open_vid():
    file_path = filedialog.askopenfilename(title="Выберите видео", filetypes=[("Video files", "*.mp4")])
    if file_path:
        display_image(file_path)


def display_image(file_path):
    status_label.config(text=f"Загруженный файл: {file_path}")
    opflow.track_video(file_path, entry_field.get(), True, True, 1)


root = tk.Tk()
root.title("AORTA VALVE TRACKING")
text_widget = tk.Text(root, wrap=tk.WORD, height=15, width=35)
open_button = tk.Button(root, text="Выбрать видео", command=open_vid)
open_button.pack(padx=20, pady=10)
entry_field = tk.Entry()
entry_field.pack(anchor=tk.NW, padx=30, pady= 10)
# enabled = tk.IntVar()
# enabled_checkbutton = tk.Checkbutton(text="Выводить видео", variable=enabled)
# enabled_checkbutton.pack(padx=40, pady=10, anchor=tk.NW)
status_label = tk.Label(root, text="", padx=20, pady=10)
status_label.pack()

root.mainloop()

