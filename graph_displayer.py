import os

import cv2
import matplotlib.pyplot as plt
from PIL import Image

file = input("Text file name: ")
vid = cv2.VideoCapture(str(file[:-4]+".mp4"))
sepr = input("Input the separator: ")
x = input("Argument 1 (X): ")
y = input("Argument 2 (Y): ")
f = open(file, 'r').readline().rstrip().split(sepr)
ind_x = f.index(x)
ind_y = f.index(y)
points = {}
vid_x = vid.get(cv2.CAP_PROP_FRAME_WIDTH)  # 1280
vid_y = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)  # 720
i = 0
arr = []
with open(file, 'r') as f:
    for line in f:
        line = line.rstrip()
        params = line.split(sepr)
        if params[ind_x].isdigit():
            points[i] = (int(params[ind_x]), int(params[ind_y]))
            i += 1
img_res = Image.new("RGB", (int(vid_x), int(vid_y)), "black")
img_res.save("img_res.png")
for index, cords in points.items():
    img_res = cv2.imread("img_res.png")
    #os.remove("img_res.png")
    cv2.circle(img_res, cords, 5, (255, 255, 255), -1)
    for index1, cords1 in points.items():
        if index1 == index:
            break
        cv2.circle(img_res, cords1, 5, (255, 255, 255), -1)
    arr.append(img_res)
video = cv2.VideoWriter(
        filename="graph.mp4", fourcc=cv2.VideoWriter_fourcc(*"mp4v"), fps=5,
        frameSize=(int(vid_x), int(vid_y))
    )
for i in range(len(arr)):
    print(":::", i)
    video.write(arr[i])
video.release()
