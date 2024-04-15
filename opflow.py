import math
import cv2
import numpy as np
import os as os
from matplotlib import pyplot as plt

arr = []


#input
def input_point(event, x, y, flags, param):
    global mouseX, mouseY
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(_, (x, y), 10, (255, 0, 0), -1)
        arr.append((x, y))
        mouseX, mouseY = x, y


def dist(point0, point1):
    return np.sqrt(((point1[0] - point0[0]) ** 2 + (point1[1] - point0[1]) ** 2))


cap = cv2.VideoCapture('bend_2.gif.mp4')

a, _ = cap.read()
print("----")
cv2.namedWindow('image')
cv2.setMouseCallback('image', input_point)
cntr = ()
dic = {}
while (1):
    cv2.imshow('image', _)

    k = cv2.waitKey(20) & 0xFF
    if k == 27:
        break
    elif k == ord('a'):
        print(mouseX, mouseY)
img_hsv = cv2.cvtColor(_, cv2.COLOR_BGR2HSV)
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
        cv2.circle(_, (cX, cY), 5, (0, 255, 0), -1)
        cntr = (cX, cY)
for p in arr:
    for i in range(-10, 10):
        dic[dist(cntr, p) + i] = p

lk_params = dict(
    winSize=(15, 15),
    maxLevel=5,
    criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03),
)
print("-----")
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
    for p in nonzero:
        if dist(current_center, p[0]) in dic:
            cv2.circle(frame, p[0], 5, (0, 255, 255), -1)
    cv2.imshow("frame", frame)
    # if frameId % 10 == 0:
    #     cv2.imwrite("frame_" + str(frameId) + ".png", frame)
    k = cv2.waitKey(25) & 0xFF
    if k == 27:
        break

    # Update the previous frame and previous points
    # old_gray = mask_red.copy()
    # p0 = good_new.reshape(-1, 1, 2)
