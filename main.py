import cv2
import numpy as np
from typing import List, Tuple
import os

def getCircle(RT: List[int], LB: List[int], RB: List[int]) -> Tuple[int, int, int]:
    print(RT, LB, RB)
    X = int((LB[0] + RB[0])/2)
    Y = (RT[1] + RB[1])/2
    
    y_v = RB[1] - RT[1]
    y_h = RT[0] - RB[0]

    y_offset = (y_h * y_h)/(2 * y_v)

    Y = int(Y + y_offset)

    radius = int((RB[0] - LB[0])/2 + 70)

    return X, Y, radius

def getPostion(path: str) -> Tuple[List[int], List[int], List[int]]:
    image = cv2.imread(path)
    
    RT = []
    LB = []
    RB = []

    XY = [(2230, 0, 2550, 415), (0, 2065, 320, 2730), (2230, 2065, 2550, 2730)]
    
    for index, xy in enumerate(XY):
        roi = image[xy[1]:xy[3], xy[0]:xy[2]]

        # Convert ROI to grayscale
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        # Threshold to get just the black areas
        _, black_areas = cv2.threshold(gray_roi, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # Find contours
        contours, _ = cv2.findContours(black_areas, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Optional: Filter contours based on size or other properties
        filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 500]

        center_xs = []
        center_ys = []

        # Draw contours (can draw on either the ROI or the original image for visualization)
        for cnt in filtered_contours:
            # Offset the contour coordinates and draw on the original image
            offset_cnt = cnt + np.array([xy[0], xy[1]])

            M = cv2.moments(offset_cnt)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                center_xs.append(cX)
                center_ys.append(cY)

        average_cX = int(sum(center_xs) / len(center_xs))
        average_cY = int(sum(center_ys) / len(center_ys))
            
        if index == 0:
            RT = [average_cX, average_cY]
        elif index == 1:
            LB = [average_cX, average_cY]
        else:
            RB = [average_cX, average_cY]

    return RT, LB, RB

folder_path = "input"
files = os.listdir(folder_path)

for file in files:
    input_path = os.path.join("input", file)

    image = cv2.imread(input_path)

    RT, LB, RB = getPostion(input_path)

    # cv2.circle(image, (RT[0], RT[1]), 30, (0, 255, 0), 2)
    # cv2.circle(image, (LB[0], LB[1]), 30, (0, 255, 0), 2)
    # cv2.circle(image, (RB[0], RB[1]), 30, (0, 255, 0), 2)

    # cv2.imwrite(f"middle/fullsize_{file}", image)

    center_x, center_y, radius = getCircle(RT, LB, RB)
    # crop circle and save
    mask = np.zeros_like(image)
    circle_mask = cv2.circle(mask, (int(center_x), int(center_y)), int(radius), (255, 255, 255), -1)
    cropped_image = cv2.bitwise_and(image, circle_mask)

    x, y, w, h = cv2.boundingRect(circle_mask[:,:,0])
    crop_img = cropped_image[y:y+h, x:x+w]

    crop_img[np.where((crop_img==[0,0,0]).all(axis=2))] = [255,255,255]

    cv2.imwrite(f"output/fullsize_{file}", crop_img)

    x1, y1 = 0, 2640  # Top-left corner
    x2, y2 = 1275, 3300  # Bottom-right corner

    cropped_image = image[y1:y2, x1:x2]

    cv2.imwrite(f"output/identity_{file}", cropped_image)

