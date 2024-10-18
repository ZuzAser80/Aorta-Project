import math
import random

import VectorsPY as vec
import cv2
import numpy as np

#DONE BY ZUZ8 IN 2023-2024
arr = []
_ = None


#Дистанция между 2 точками
def dist(point0, point1):
    return np.sqrt(((point1[0] - point0[0]) ** 2 + (point1[1] - point0[1]) ** 2))


#Главная функция отслеживания
def track_video(filename: str, output_name: str, show_video: bool, place_points_auto: bool = True,
                points_count: int = 1) -> bool:
    cap = cv2.VideoCapture(filename)
    vec_dir_dict = {}
    flips = {}
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    frameRate = cap.get(cv2.CAP_PROP_FPS)
    a, _ = cap.read()

    #Считываем ввод точек (deprecated)
    def input_point(event, x, y, flags, param):
        global mouseX, mouseY
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.circle(_, (x, y), 10, (255, 0, 0), -1)
            arr.append((x, y))
            mouseX, mouseY = x, y

    #Находим центр синего силуэта на фото img
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

    #Ждем ввод от пользователя
    def waitUserInput(_):
        print("----")

        #Если расставляем точки автоматически
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

            # Выводим изображение
            cv2.circle(imCrop, current_center, 10, (255, 255, 255), -1)

            cnts = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if len(cnts) == 2 else cnts[1]
            c = max(cnts, key=cv2.contourArea)

            #Самые дельние синие точки на выделенном участке
            #left, right, top, bottom
            extremes = [tuple(c[c[:, :, 0].argmin()][0]), tuple(c[c[:, :, 0].argmax()][0]),
                        tuple(c[c[:, :, 1].argmin()][0]), tuple(c[c[:, :, 1].argmax()][0])]
            #Самые дальние синие точки
            #print("extremes:", extremes)

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
                        (point[0] - current_center[0], point[1] - current_center[1]))
                    # (point[0] + old_center[0] - current_center[0], point[1] + old_center[1] - current_center[1]
                    print("====", (point[0] - current_center[0], point[1] - current_center[1]))
            #Показываем и запоминаем точки
            cv2.imshow("Image", imCrop)
            cv2.imwrite("auto_picker.png", imCrop)
            cv2.waitKey(0)

        else:
            #Если пользователь сам расставляет точки (КРАЙНЕ НЕ РЕКОМЕНДУЕТСЯ)
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
        # cntr = get_current_center(_)
        for p in range(len(arr)):
            # i = 0
            # if len(cntr) > 1 and not cntr[1] == arr[p]:
            #     i = 1
            vector = vec.Vector2(arr[p][0], arr[p][1])
            if vector.x > 0:
                flips[p] = True
            print(":", vector.direction(), " :: ", vector.magnitude(), ":")
            if vector.direction() not in vec_dir_dict.keys():
                vec_dir_dict[vector.direction()] = vector.magnitude()
            else:
                vec_dir_dict[vector.direction() + random.uniform(-0.1, 0.1)] = vector.magnitude()

    v = []

    #Главная функция отслеживания
    def track():
        #Создаем файл для вывода результатов
        f = open(output_name + ".csv", "w")
        f.write("Центр X,Центр Y,")
        for el in range(len(arr)):
            f.write("Точка № " + str(el) + " X,Точка № " + str(el) + " Y,")
        f.write("t" + "\n")
        #Обрабатываем видео покадрово
        while True:
            frameId = cap.get(1)
            ret, __ = cap.read()
            if not ret:
                break
            frame = __.copy()
            #Маска по цвету
            img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            lower_blue = np.array([110, 150, 150])
            upper_blue = np.array([130, 255, 255])
            mask_red = cv2.inRange(img_hsv, lower_blue, upper_blue)
            current_center = (0, 0)
            centers = []
            contours, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            #Находим центры синих силуэтов
            for contour in contours:
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    cv2.circle(frame, (cX, cY), 5, (255, 255, 0), -1)
                    if len(centers) == 0:
                        current_center = (cX, cY)
                    centers.append((cX, cY))
            # Находим все синие пиксели
            nonzero = cv2.findNonZero(mask_red)

            # Если нету центров - пропускаем итерацию
            # if len(centers) == 0:
            #     continue
            # Cent distance / Дистанция между центрами если надо
            # if len(centers) >= 2:
            #     f.write((str(int(dist(centers[0], centers[1]))) + ","))
            # else:
            #     f.write("0,")

            f.write(str(current_center[0]) + "," + str(current_center[1]) + ",")
            #Перебираем все запомненные векторы
            prevpair = None
            for key, value in vec_dir_dict.items():
                # if prevpair is not None:
                #     new_dir = prevpair[0] - key
                #     y = value * math.cos(math.radians(new_dir))
                #     x = value * math.sin(math.radians(new_dir))
                #     #
                #     if list(vec_dir_dict.keys()).index(key) in list(flips.keys()) and flips[
                #         list(vec_dir_dict.keys()).index(key)]:
                #         y = -y
                #         x = -x
                #     proj = (current_center[0] + int(x), current_center[1] + int(y))
                #     # print("B======D", frameId, int(x), int(y))
                #     # Отображаем
                #     cv2.circle(frame, proj, 1, (127, 127, 0), -1)

                #Считаем значения, на которых бы лежал конец вектора

                y = value * math.cos(math.radians(key))
                x = value * math.sin(math.radians(key))
                #
                if list(vec_dir_dict.keys()).index(key) in list(flips.keys()) and flips[
                    list(vec_dir_dict.keys()).index(key)]:
                    y = -y
                    x = -x

                #1 вектор, отложенный из центра
                proj = (current_center[0] + int(x), current_center[1] + int(y))
                #print("B======D", frameId, int(x), int(y))
                #Отображаем
                cv2.circle(frame, proj, 1, (0, 127, 0), -1)

                #Ищем самый близкий к 1 вектору синий пиксель
                distances = np.sqrt((nonzero[:, :, 0] - proj[0]) ** 2 + (nonzero[:, :, 1] - proj[1]) ** 2)
                nearest_index = np.argmin(distances)
                #отображаем
                cv2.circle(frame, nonzero[nearest_index][0], 2, (0, 127, 127), -1)

                #2ой вектор - из центра через самый близкий к 1 вектору синий пиксель (определяем угол)
                x1 = abs(current_center[0] - nonzero[nearest_index][0][0])
                y1 = abs(current_center[1] - nonzero[nearest_index][0][1])

                vector1 = vec.Vector2(x1, y1)
                #Теперь увеличиваем длину 2 вектора до длины оригинального вектора
                if x1 != 0:
                    vector1.x *= abs(value) / x1
                if y1 != 0:
                    vector1.y *= abs(value) / y1

                #print("::::::", vector1.x, vector1.y, x, value)

                #Отображаем
                proj1 = (
                    current_center[0] + int(vector1.x * (x / abs(x))),
                    current_center[1] + int(vector1.y * (y / abs(y))))
                cv2.circle(frame, proj1, 2, (0, 0, 255), -1)

                # if abs(dist((current_center[0], current_center[1]), proj1) - value) >= 10:
                #     proj15 = (
                #         current_center[0] + int(vector1.x * (x / abs(x)) * 0.5),
                #         current_center[1] + int(vector1.y * (y / abs(y)) * 0.5))
                #     cv2.circle(frame, proj15, 2, (255, 0, 255), -1)
                #     proj1 = proj15

                #Теперь ищем ближайший к концу 2 вектора синий пиксель
                distances = np.sqrt((nonzero[:, :, 0] - proj1[0]) ** 2 + (nonzero[:, :, 1] - proj1[1]) ** 2)
                nearest_index_1 = np.argmin(distances)

                #Отображаем
                true_point = nonzero[nearest_index_1][0]
                #Погрешность в <10 пикселей
                if dist(nonzero[nearest_index_1][0], proj1) <= 1:
                    true_point = proj1
                cv2.circle(frame, true_point, 2, (255, 255, 255), -1)

                vector2 = vec.Vector2(
                    int(vector1.x * (x / abs(x))),
                    int(vector1.y * (y / abs(y))))

                vp = vec.Vector2(vector2.x * key, vector2.y * key)

                # idea - remember last vector, compare and minusovat' ya v rot yebal
                if prevpair is not None:
                    l = vec.Vector2(x - prevpair[0], y - prevpair[1])
                    # print("::: ", l.x, l.y)
                    # l.x /= value
                    # l.y /= value

                    #cv2.circle(frame, (int(true_point[0] + l.x), int(true_point[1] + l.y)), 1, (255, 0, 255), -1)

                prevpair = (x, y)
                #Записываем в файл
                f.write(str(true_point[0]) + "," + str(true_point[1]) + ",")

            f.write(str(frameId) + "\n")
            if show_video:
                cv2.imshow("frame", frame)
            v.append(frame)
            if frameId % 10 == 0 or frameId == 0:
                cv2.imwrite("frame_" + str(frameId) + ".png", frame)
            k = cv2.waitKey(25) & 0xFF
            if k == 27:
                break

    #Вызовы функций
    waitUserInput(_)
    cv2.destroyAllWindows()
    track()
    cv2.destroyAllWindows()
    #Оборачиваем кадры в видео
    video = cv2.VideoWriter(
        filename=(output_name + ".mp4"), fourcc=cv2.VideoWriter_fourcc(*"mp4v"), fps=frameRate,
        frameSize=size
    )
    for i in range(len(v)):
        video.write(v[i])
    #Записываем видео
    video.release()
    return True


#track_video("bend_4.gif.mp4", "nigger", True, points_count=3)
