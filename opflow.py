import math
import cv2
import numpy as np
import os as os
from matplotlib import pyplot as plt

arr = []
_ = None


#input
def input_point(event, x, y, flags, param):
    global mouseX, mouseY
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(_, (x, y), 10, (255, 0, 0), -1)
        arr.append((x, y))
        mouseX, mouseY = x, y


def dist(point0, point1):
    return np.sqrt(((point1[0] - point0[0]) ** 2 + (point1[1] - point0[1]) ** 2))


cap = cv2.VideoCapture('projectoid2.mp4')
dic = {}
size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
frameRate = cap.get(cv2.CAP_PROP_FPS)
a, _ = cap.read()


def waitUserInput(_):
    print("----")
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', input_point)
    cntr = ()

    while (1):
        cv2.imshow('image', _)
        cv2.imwrite("circle_picker.png", _)
        k = cv2.waitKey(20) & 0xFF
        if k == 27:
            break
        elif k == ord('a'):
            print(mouseX, mouseY)
    for p in range(1, len(arr)):
        dic[dist(arr[0], arr[p])] = arr[p]


v = []


def track():
    f = open("opflow_res.txt", "w")
    f.write(("xCent -- yCent -- xP -- yP -- xV -- yV -- t" + "\n"))
    while True:
        frameId = cap.get(1)
        ret, frame = cap.read()
        if not ret:
            break
        img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_blue = np.array([100, 50, 50])
        upper_blue = np.array([130, 255, 255])
        mask_red = cv2.inRange(img_hsv, lower_blue, upper_blue)
        current_center = (0, 0)
        contours, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for contour in contours:
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                cv2.circle(frame, (cX, cY), 10, (255, 255, 0), -1)
                current_center = (cX, cY)
        nonzero = cv2.findNonZero(mask_red)
        f.write(str(current_center[0]) + " -- " + str(current_center[1]) + " -- ")
        for p in nonzero:
            if dist(arr[0], p[0]) in dic:
                f.write(str(p[0][0]) + " -- " + str(p[0][1]) + " -- ")
                cv2.circle(frame, p[0], 5, (0, 255, 255), -1)
        f.write(str(frameId) + "\n")
        cv2.imshow("frame", frame)
        v.append(frame)
        k = cv2.waitKey(25) & 0xFF
        if k == 27:
            break


waitUserInput(_)
track()
video = cv2.VideoWriter(
    filename="result1.mp4", fourcc=cv2.VideoWriter_fourcc(*"mp4v"), fps=frameRate, frameSize=size
)
for i in range(len(v)):
    video.write(v[i])
video.release()
