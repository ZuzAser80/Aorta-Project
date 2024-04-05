import math
import cv2
import numpy as np
import os as os
from matplotlib import pyplot as plt

arr = np.empty([1, 1, 2], dtype=np.float32)


#input
def draw_circle(event, x, y, flags, param):
    global mouseX, mouseY
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(_, (x, y), 10, (255, 0, 0), -1)
        arr[0][0] = [x, y]
        mouseX, mouseY = x, y


cap = cv2.VideoCapture('bend_2.gif.mp4')

a, _ = cap.read()
print("----")
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_circle)
while (1):
    cv2.imshow('image', _)
    k = cv2.waitKey(20) & 0xFF
    if k == 27:
        break
    elif k == ord('a'):
        print(mouseX, mouseY)

lk_params = dict(
    winSize=(15, 15),
    maxLevel=5,
    criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03),
)
old_gray = cv2.cvtColor(_, cv2.COLOR_BGR2GRAY)
color = np.array([(0, 0, 255)])
mask = np.zeros_like(_)
p0 = arr
print("-----")
while True:
    ret, frame = cap.read()
    if not ret:
        break
    img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([130, 255, 255])
    mask_red = cv2.inRange(img_hsv, lower_blue, upper_blue)
    # edges = cv2.Canny(gray, 50, 150)
    contours, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.circle(frame, (cX, cY), 40, (255, 0, 0), -1)
    p1, st, err = cv2.calcOpticalFlowPyrLK(
        old_gray, mask_red, p0, None, **lk_params
    )
    print("::", p1)
    # Select good points
    good_new = p1[st == 1]
    good_old = p0[st == 1]

    # Draw the tracks
    for i, (new, old) in enumerate(zip(good_new, good_old)):
        a, b = new.ravel()
        c, d = old.ravel()
        print("::", a, b)
        mask = cv2.line(mask, (int(a), int(b)), (int(c), int(d)), color[i].tolist(), 2)
        frame = cv2.circle(frame, (int(a), int(b)), 5, color[i].tolist(), -1)

    # Display the demo
    img = cv2.add(frame, mask)
    cv2.imshow("frame", img)
    k = cv2.waitKey(25) & 0xFF
    if k == 27:
        break

    # Update the previous frame and previous points
    old_gray = mask_red.copy()
    p0 = good_new.reshape(-1, 1, 2)
