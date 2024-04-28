import math

import VectorsPY as vec
import cv2
import numpy as np

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


def compare_delta(points0, points1, l):
    d00 = points0[0][0][0] - points0[1][0][0]
    d01 = points0[0][0][1] - points0[1][0][1]
    d10 = points1[0][0][0] - points1[1][0][0]
    d11 = points1[0][0][1] - points1[1][0][1]
    return abs(d00 - d10) <= l and abs(d01 - d11) <= l


cap = cv2.VideoCapture('projectoid2.mp4')
dic = {}
vec_mag_dict = {}
vec_dir_dict = {}
size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
frameRate = cap.get(cv2.CAP_PROP_FPS)
a, _ = cap.read()


def waitUserInput(_):
    print("----")
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', input_point)

    while (1):
        cv2.imshow('image', _)
        cv2.imwrite("circle_picker.png", _)
        k = cv2.waitKey(20) & 0xFF
        if k == 27:
            break
        elif k == ord('a'):
            print(mouseX, mouseY)
    cntr = ()
    img_hsv = cv2.cvtColor(_, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([110, 150, 150])
    upper_blue = np.array([130, 255, 255])
    mask_red = cv2.inRange(img_hsv, lower_blue, upper_blue)
    contours, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.circle(_, (cX, cY), 10, (255, 255, 0), -1)
            cntr = (cX, cY)

    for p in range(len(arr)):
        vector = vec.Vector2(cntr[0] - arr[p][0], cntr[1] - arr[p][1])
        vec_mag_dict[vector.magnitude()] = vector.direction()
        print(":", vector.magnitude(), " :: ", vector.direction())
        vec_dir_dict[vector.direction()] = vector.magnitude()
        for i in range(-10, 10):
            dic[dist(arr[0], arr[p]) + i] = arr[p]
            dic[dist(cntr, arr[p]) + i] = arr[p]


v = []
last_point = ()
written = False
written1 = False


def track():
    global written, last_point, written1
    f = open("opflow_res.txt", "w")
    f.write(("xCent -- yCent -- xP -- yP -- xV -- yV -- t" + "\n"))
    while True:
        frameId = cap.get(1)
        ret, frame = cap.read()
        if not ret:
            break
        img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_blue = np.array([110, 150, 150])
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
                break
        nonzero = cv2.findNonZero(mask_red)
        f.write(str(current_center[0]) + " -- " + str(current_center[1]) + " -- ")
        for p in nonzero:
            vector = vec.Vector2(current_center[0] - p[0][0], current_center[1] - p[0][1])
            #print("curdir:", vector.direction(), "fr:", frameId)
            if any(abs(key - vector.direction()) < 1 and abs(vector.magnitude() - value) < 10 for key, value in vec_dir_dict.items()):
                cv2.circle(frame, p[0], 5, (255, 0, 255), -1)
                #break
        f.write(str(frameId) + "\n")
        cv2.imshow("frame", frame)
        v.append(frame)
        # if frameId % 10 == 0:
        #     cv2.imwrite("frame_" + str(frameId) + ".png", frame)
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
