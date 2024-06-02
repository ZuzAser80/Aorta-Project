import cv2
from ultralytics import YOLO


def split_and_save(filename: str, save_path: str):
    cap = cv2.VideoCapture(filename)
    while True:
        frameId = cap.get(1)
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imwrite(str(save_path + "frame" + "_" + str(frameId) + ".png"), frame)


def mark_valve_on_frame(frame):
    print("----")


model = YOLO("yolov8n.pt")

split_and_save(input("name?"), "frames/")
