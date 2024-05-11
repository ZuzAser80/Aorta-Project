import cv2


def mark_valve_on_video(filename: str):
    cap = cv2.VideoCapture(filename)
    while True:
        frameId = cap.get(1)
        ret, frame = cap.read()
        if not ret:
            break


def mark_valve_on_frame(frame):
    print("----")
    

