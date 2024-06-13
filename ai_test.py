import os
import shutil

import cv2
import numpy
import torch
from ultralytics import YOLO


def split_and_save(filename: str, save_path: str):
    cap = cv2.VideoCapture(filename)
    while True:
        frameId = cap.get(1)
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imwrite(str(save_path + "frame" + "_" + str(frameId) + ".png"), frame)


def mark_valve_on_frame(frame):
    print("----")


vid_nm = input("Video name: ")
cap = cv2.VideoCapture(vid_nm)
blank_image = None
arr = []
while True:
    frameId = cap.get(1)
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    frameRate = cap.get(cv2.CAP_PROP_FPS)
    ret, frame = cap.read()
    if not ret:
        break
    model = YOLO("runs/segment/train2/weights/best.pt")
    valves = model.predict(source=frame, show=False, save=False, show_labels=True, show_conf=True,
                           conf=0.35, save_txt=False, save_crop=False, line_width=2)

    for result in valves:
        # get array results
        if type(result) is None or not result:
            break

        masks = result.masks.data
        boxes = result.boxes.data
        # extract classes
        clss = boxes[:, 5]
        # get indices of results where class is 0 (people in COCO)
        people_indices = torch.where(clss == 0)
        # use these indices to extract the relevant masks
        people_masks = masks[people_indices]
        # scale for visualizing results
        people_mask = torch.any(people_masks, dim=0).int() * 255
        img = people_mask.cpu().numpy()
        # save to file
        nz = cv2.findNonZero(img)
        height, width = frame.shape[:2]
        blank_image = numpy.zeros((height, width, 3), numpy.uint8)
        for pt in nz:
            cv2.circle(blank_image, (int(pt[0][0] * (1280/640)), int(pt[0][1] *
                                     (720/380))), 1, (255, 0, 0), -1)
        #blank_image - mask /w blue color
        #
    # orig = cv2.imread("runs/segment/predict/image0.jpg")
    # print("frame:", frameId, "/", int(cap.get(cv2.CAP_PROP_FRAME_COUNT)), ":", orig.shape, ":", blank_image.shape)
    res_img = cv2.bitwise_or(frame, blank_image, mask=None)
    arr.append(res_img)
    # shutil.rmtree("runs/segment/predict")
print("----------")
video = cv2.VideoWriter(filename="result_video.mp4", fourcc=cv2.VideoWriter_fourcc(*"mp4v"), fps=frameRate,
                        frameSize=size)
for i in range(len(arr)):
    print(":::appended frame #", i)
    video.write(arr[i])
video.release()
#split_and_save(input("name? : "), "frames/")
