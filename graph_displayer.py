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
with open(file, 'r') as f:
    for line in f:
        line = line.rstrip()
        params = line.split(sepr)
        if params[ind_x].isdigit():
            points[i] = (int(params[ind_x]), int(params[ind_y]))
            i += 1
img_res = Image.new("RGB", (int(vid_x), int(vid_y)), "black")
img_res.save("img_res.png")
img_res = cv2.imread("img_res.png")
os.remove("img_res.png")
for index, cords in points.items():
    cv2.circle(img_res, cords, 5, (255, 255, 255), -1)
plt.imshow(img_res), plt.show()
