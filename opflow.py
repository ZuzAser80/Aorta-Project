import math

import VectorsPY as vec
import cv2
import numpy as np

arr = []
_ = None


def dist(point0, point1):
    return np.sqrt(((point1[0] - point0[0]) ** 2 + (point1[1] - point0[1]) ** 2))


def track_video(filename: str, output_name: str, show_video: bool, place_points_auto: bool = True,
                points_count: int = 1) -> bool:
    cap = cv2.VideoCapture(filename)
    vec_dir_dict = {}
    flips = {}
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    frameRate = cap.get(cv2.CAP_PROP_FPS)
    a, _ = cap.read()

    def input_point(event, x, y, flags, param):
        global mouseX, mouseY
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.circle(_, (x, y), 10, (255, 0, 0), -1)
            arr.append((x, y))
            mouseX, mouseY = x, y

    def get_current_center(img, color=(255, 255, 0)):
        cntr = []
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_blue = np.array([110, 150, 150])
        upper_blue = np.array([130, 255, 255])
        mask_red = cv2.inRange(img_hsv, lower_blue, upper_blue)
        contours, img = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for contour in contours:
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                cntr.append((cX, cY))
                cv2.circle(img, (cX, cY), 10, color, -1)
        return cntr

    def waitUserInput(_):
        print("----")

        if place_points_auto:
            #prelude
            r = cv2.selectROI(_)
            imCrop = _[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]

            img_hsv = cv2.cvtColor(imCrop, cv2.COLOR_BGR2HSV)
            lower_blue = np.array([110, 150, 150])
            upper_blue = np.array([130, 255, 255])
            mask_red = cv2.inRange(img_hsv, lower_blue, upper_blue)

            old_center = get_current_center(_)[0]
            current_center = get_current_center(imCrop)[0]
            k = vec.Vector2(old_center[0] - current_center[0], old_center[1] - current_center[1])

            # display it
            cv2.circle(imCrop, current_center, 10, (255, 255, 255), -1)

            cnts = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if len(cnts) == 2 else cnts[1]
            c = max(cnts, key=cv2.contourArea)

            #Самые дельние синие точки на выделенном участке
            #left, right, top, bottom
            extremes = [tuple(c[c[:, :, 0].argmin()][0]), tuple(c[c[:, :, 0].argmax()][0]),
                        tuple(c[c[:, :, 1].argmin()][0]), tuple(c[c[:, :, 1].argmax()][0])]

            print("extremes:", extremes)

            dists = {}
            for ex in extremes:
                dists[dist(current_center, ex)] = ex

            #Находим 2 самых дальных точки
            l = list(dists.keys())
            pivot_0 = max(l)
            l.remove(pivot_0)
            pivot_1 = max(l)

            pivots = [dists[pivot_0], dists[pivot_1]]

            #перебираем сначала точки, потом промежуточные точки
            for p in pivots:
                for l in range(points_count):
                    vector = vec.Vector2(current_center[0] - p[0], (current_center[1] - p[1]))
                    y = vector.magnitude() * math.cos(math.radians(vector.direction()))
                    x = vector.magnitude() * math.sin(math.radians(vector.direction()))
                    if vector.y > 0:
                        x = -x
                        y = -y
                    point = (int(current_center[0] + ((x * (l + 1)) / points_count)),
                             int(current_center[1] + ((y * (l + 1)) / points_count)))
                    cv2.circle(imCrop, point, 2, (255, 0, 255), -1)
                    arr.append(
                        (point[0] + old_center[0] - current_center[0], point[1] + old_center[1] - current_center[1]))

            cv2.imshow("Image", imCrop)
            cv2.imwrite("auto_picker.png", imCrop)
            cv2.waitKey(0)

        else:
            cv2.namedWindow("windowName")
            cv2.setMouseCallback("windowName", input_point)
            while 1:
                cv2.imshow("windowName", _)
                cv2.imwrite("circle_picker.png", _)
                k = cv2.waitKey(20) & 0xFF
                if k == 27:
                    break
                elif k == ord('a'):
                    print(mouseX, mouseY)
        cntr = get_current_center(_)
        for p in range(len(arr)):
            i = 0
            if len(cntr) > 1 and not cntr[1] == arr[p]:
                i = 1
            vector = vec.Vector2(cntr[i][0] - arr[p][0], (cntr[i][1] - arr[p][1]))
            if vector.y > 0:
                flips[p] = True
            print(":", vector.magnitude(), " :: ", vector.direction(), ":", vector.y)
            vec_dir_dict[vector.direction()] = vector.magnitude()

    v = []

    def track():
        f = open(output_name + ".txt", "w")
        f.write("CentDist -- xCent -- yCent -- ")
        for el in range(len(arr)):
            f.write("P#" + str(el) + "X -- P#" + str(el) + "Y -- ")
        f.write("t" + "\n")
        while True:
            frameId = cap.get(1)
            ret, __ = cap.read()
            if not ret:
                break
            frame = __.copy()
            img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            lower_blue = np.array([110, 150, 150])
            upper_blue = np.array([130, 255, 255])
            mask_red = cv2.inRange(img_hsv, lower_blue, upper_blue)
            current_center = (0, 0)
            centers = []
            contours, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            for contour in contours:
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    cv2.circle(frame, (cX, cY), 10, (255, 255, 0), -1)
                    if len(centers) == 0:
                        current_center = (cX, cY)
                    centers.append((cX, cY))
            nonzero = cv2.findNonZero(mask_red)

            # looking for closest to the original vector's end blue pixel
            if len(centers) == 0:
                continue
            if len(centers) >= 2:
                f.write((str(int(dist(centers[0], centers[1]))) + " -- "))
            else:
                f.write("0 -- ")

            f.write(str(current_center[0]) + " -- " + str(current_center[1]) + " -- ")
            for key, value in vec_dir_dict.items():

                y = value * math.cos(math.radians(key))
                x = value * math.sin(math.radians(key))

                if list(vec_dir_dict.keys()).index(key) in list(flips.keys()) and flips[
                    list(vec_dir_dict.keys()).index(key)]:
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
                x1 = abs(current_center[0] - nonzero[nearest_index][0][0])
                y1 = abs(current_center[1] - nonzero[nearest_index][0][1])

                vector1 = vec.Vector2(x1, y1).unitvector()
                #setting the magnitude
                vector1.x *= abs(value)
                vector1.y *= abs(value)

                #display it
                #print("shoebill:", vector1.x, x, (x / abs(x)))
                proj1 = (
                    current_center[0] + int(vector1.x * (x / abs(x))),
                    current_center[1] + int(vector1.y * (y / abs(y))))
                cv2.circle(frame, proj1, 5, (0, 0, 255), -1)

                #looking for the closest to 2nd vector blue pixel(should be final (?))
                distances = np.sqrt((nonzero[:, :, 0] - proj1[0]) ** 2 + (nonzero[:, :, 1] - proj1[1]) ** 2)
                nearest_index_1 = np.argmin(distances)

                # display it
                true_point = nonzero[nearest_index_1][0]
                if dist(nonzero[nearest_index_1][0], proj1) <= 10:
                    true_point = proj1
                cv2.circle(frame, true_point, 5, (255, 255, 255), -1)

                #write to file
                f.write(str(true_point[0]) + " -- " + str(true_point[1]) + " -- ")
            f.write(str(frameId) + "\n")
            if show_video:
                cv2.imshow("frame", frame)
            v.append(frame)
            if frameId % 10 == 0:
                cv2.imwrite("frame_" + str(frameId) + ".png", frame)
            k = cv2.waitKey(25) & 0xFF
            if k == 27:
                break

    waitUserInput(_)
    cv2.destroyAllWindows()
    track()
    cv2.destroyAllWindows()
    #wrapping into video
    video = cv2.VideoWriter(
        filename=(output_name + ".mp4"), fourcc=cv2.VideoWriter_fourcc(*"mp4v"), fps=frameRate,
        frameSize=size
    )
    for i in range(len(v)):
        video.write(v[i])
    video.release()
    return True

#track_video("projectoid2.mp4", "projectoid2_res", True, True, 4)
