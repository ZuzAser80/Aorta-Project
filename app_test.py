import re

import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk

import opflow

video_path = ""


class VideoPlayerApp:
    def __init__(self, rt, side, anchor):
        self.photo = None
        self.root = rt

        self.video_source = None
        self.cap = None

        # Create a Label to display the video
        self.video_label = tk.Label(rt)
        self.video_label.pack_configure(side=side, anchor=anchor)
        self.video_label.pack()

    def open_video(self):
        file_path = filedialog.askopenfilename(title="Выберите видео", filetypes=[("Video files", "*.mp4")])
        if file_path:
            self.video_source = file_path
            display_image(file_path)
            self.cap = cv2.VideoCapture(self.video_source)
            self.play_video()

    def open_video_path(self, path):
        if path:
            self.video_source = path
            self.cap = cv2.VideoCapture(self.video_source)
            self.play_video()

    def play_video(self):
        if self.cap is not None:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                k = frame.shape[0] / root.winfo_screenwidth()
                frame = cv2.resize(frame, (int(frame.shape[1]*k), int(frame.shape[0] * k)), interpolation=cv2.INTER_AREA)
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
                self.video_label.config(image=self.photo)
                self.video_label.image = self.photo
                self.root.after(int(self.cap.get(cv2.CAP_PROP_FPS)), self.play_video)

    def pause_video(self):
        if self.cap is not None:
            self.cap.release()
            self.video_source = None


def open_vid():
    global video_path
    file_path = filedialog.askopenfilename(title="Выберите видео", filetypes=[("Video files", "*.mp4")])
    print("e", bool(enabled.get()), "::", bool(auto_points.get()), "::")
    if file_path:
        video_path = file_path
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
    print("entered")
    s = point_count.get()
    s = re.sub('\\s+', '', s)
    if s.isdigit() or s == '':
        if s == '': s = 0
        status_label.config(text=f"Загруженный файл: {file_path}")
        opflow.track_video(file_path, entry_field.get(), bool(enabled.get()), bool(auto_points.get()), int(s))
        app1.open_video_path(str(entry_field.get() + ".mp4"))
    elif s != '':
        status_label.config(text=f"Пожалуйста, введите количество точек, используя ТОЛЬКО цифры")


def toggle():
    if not bool(auto_points.get()):
        point_count.pack_forget()
    else:
        set_entry_placeholder(point_count, "Введите количество точек...")


root = tk.Tk()

app = VideoPlayerApp(root, tk.TOP, tk.NW)
app1 = VideoPlayerApp(root, tk.TOP, tk.NW)

root.title("AORTA VALVE TRACKING")
text_widget = tk.Text(root, wrap=tk.WORD, height=15, width=35)


entry_field = tk.Entry(width=50)
set_entry_placeholder(entry_field, "Введите название файла, в который выведутся результаты")

open_button = tk.Button(root, text="Выбрать видео", command=app.open_video)
open_button.pack(padx=20, pady=10)

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
