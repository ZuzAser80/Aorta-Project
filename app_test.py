import re

import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk

import opflow

video_path = ""


class VideoPlayerApp:
    def __init__(self, rt, row, column):
        self.photo = None
        self.root = rt

        self.video_source = None
        self.cap = None

        # Create a Label to display the video
        self.video_label = tk.Label(rt)
        self.video_label.grid_configure(column=column, row=row)
        self.video_label.grid()

    def open_video(self):
        file_path = filedialog.askopenfilename(title="Выберите видео", filetypes=[("Video files", "*.mp4")])
        if file_path:
            self.video_source = file_path
            display_image(root, file_path)
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
                frame = cv2.resize(frame, (int(frame.shape[1] * k), int(frame.shape[0] * k)),
                                   interpolation=cv2.INTER_AREA)
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
                self.video_label.config(image=self.photo)
                self.video_label.image = self.photo
                self.root.after(int(self.cap.get(cv2.CAP_PROP_FPS)), self.play_video)


def open_vid():
    global video_path
    file_path = filedialog.askopenfilename(title="Выберите видео", filetypes=[("Video files", "*.mp4")])
    print("e", bool(enabled.get()), "::", bool(auto_points.get()), "::")
    if file_path:
        video_path = file_path
        display_image(file_path)


# Function to handle the Entry widget focus events
def set_entry_placeholder(entry, placeholder_text, row, column):
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
    entry.grid_configure(row=row, column=column)
    entry.grid()


def display_image(rt, file_path):
    print("entered")
    s = point_count.get()
    s = re.sub('\\s+', '', s)
    if s.isdigit() or s == '':
        if s == '': s = 0
        status_label.config(text=f"Загруженный файл: {file_path}")
        opflow.track_video(file_path, entry_field.get(), bool(enabled.get()), True, int(int(point_count_e.get())))
        app1.open_video_path(str(entry_field.get() + ".mp4"))
        display_analytix(rt, str(entry_field.get() + ".txt"))
    elif s != '':
        status_label.config(text=f"Пожалуйста, введите количество точек, используя ТОЛЬКО цифры")


def toggle():
    if not bool(auto_points.get()):
        point_count.grid_forget()
    else:
        set_entry_placeholder(point_count, "Введите количество точек...")


def display_analytix(rt, filename):
    configfile = tk.Text(rt, wrap=tk.WORD, width=175, height=20)
    print("entered::1")
    with open(filename, 'r') as f:
        print("::::::1")
        configfile.insert(tk.INSERT, f.read())
    configfile.grid_configure(row=2, column=0, columnspan=2)
    configfile.grid()


root = tk.Tk()

app = VideoPlayerApp(root, 1, 2)
app1 = VideoPlayerApp(root, 2, 2)

root.title("AORTA VALVE TRACKING")
text_widget = tk.Text(root, wrap=tk.WORD, height=15, width=35)

entry_field = tk.Entry(width=50)
set_entry_placeholder(entry_field, "Введите название файла, в который выведутся результаты", 0, 1)

point_count_e = tk.Entry(width=50)
set_entry_placeholder(point_count_e, "Введите кол-во точек", 1, 1)

open_button = tk.Button(root, text="Выбрать видео", command=app.open_video)
open_button.grid_configure(row=0, column=0)
open_button.grid()

enabled = tk.IntVar()
enabled_checkbutton = tk.Checkbutton(text="Выводить видео", variable=enabled)
enabled_checkbutton.grid_configure(row=1, column=0)
enabled_checkbutton.grid()

point_count = tk.Entry(width=50)

auto_points = tk.IntVar()
auto_points_checkbutton = tk.Checkbutton(text="Автоматическая расстановка точек", variable=auto_points, command=toggle)
#auto_points_checkbutton.grid_configure(row=2, column=0)
#auto_points_checkbutton.grid()

status_label = tk.Label(root, text="", padx=20, pady=10)
status_label.grid()

root.mainloop()
