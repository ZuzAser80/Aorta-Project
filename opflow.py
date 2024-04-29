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


cap = cv2.VideoCapture('projectoid2.mp4')
vec_mag_dict = {}
vec_dir_dict = {}
flip = False
size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
frameRate = cap.get(cv2.CAP_PROP_FPS)
a, _ = cap.read()


def waitUserInput(_):
    global mn, flip
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
    cntr = []
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
            cntr.append((cX, cY))
            print("u:", cntr)
            cv2.circle(_, (cX, cY), 10, (255, 255, 0), -1)
            #break

    for p in range(len(arr)):
        i = 0
        if len(cntr) > 1 and not cntr[1] == arr[p]:
            i = 1
        vector = vec.Vector2(cntr[i][0] - arr[p][0], (cntr[i][1] - arr[p][1]))
        if not flip and vector.y > 0:
            flip = True
        print(":", vector.magnitude(), " :: ", vector.direction(), ":", vector.y)
        vec_dir_dict[vector.direction()] = vector.magnitude()
        mn = vector.direction()


v = []
last_vector = vec.Vector2(0, 0)


def track():
    global last_vector
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
        for key, value in vec_dir_dict.items():
            y = value * math.cos(math.radians(key))
            x = value * math.sin(math.radians(key))
            if flip:
                y = -y
                x = -x
            #1st vector from the middle(center)
            vector = vec.Vector2(x, y)
            proj = (current_center[0] + int(vector.x), current_center[1] + int(vector.y))
            #display it
            cv2.circle(frame, proj, 5, (0, 127, 0), -1)
            #looking for closest to the original vector's end blue pixel
            distances = np.sqrt((nonzero[:, :, 0] - proj[0]) ** 2 + (nonzero[:, :, 1] - proj[1]) ** 2)
            nearest_index = np.argmin(distances)
            #display it
            cv2.circle(frame, nonzero[nearest_index][0], 5, (0, 127, 127), -1)
            #2nd vector: from the middle through the closest blue pixel(to determine the angle of the thing)
            vector1 = vec.Vector2(current_center[0] - nonzero[nearest_index][0][0],
                                  current_center[1] - nonzero[nearest_index][0][1]).unitvector()
            #display it
            proj1 = (current_center[0] + int(vector1.x * value * (x / abs(x))), current_center[1] + int(vector1.y * value * (x / abs(x))))
            cv2.circle(frame, proj1, 5, (0, 0, 127), -1)
            #looking for the closest to 2nd vector blue pixel(should be final (?))
            distances = np.sqrt((nonzero[:, :, 0] - proj1[0]) ** 2 + (nonzero[:, :, 1] - proj1[1]) ** 2)
            nearest_index_1 = np.argmin(distances)
            # display it
            cv2.circle(frame, nonzero[nearest_index_1][0], 5, (255, 255, 255), -1)
            #f.write(str(proj[0]) + " -- " + str(proj[1]) + " -- " + str(nonzero[nearest_index][0][0]) + " -- " + str(nonzero[nearest_index][0][1]))
        f.write(str(frameId) + "\n")
        cv2.imshow("frame", frame)
        v.append(frame)
        if frameId % 10 == 0:
            cv2.imwrite("frame_" + str(frameId) + ".png", frame)
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
