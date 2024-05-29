import cv2
import numpy as np
from typing import List, Tuple

def getPostion(circles: List[List[int]]) -> Tuple[List[int], List[int], List[int]]:
    min_x = 5000
    min_y = 5000

    RT = []
    LB = []
    RB = []

    for circle in circles:
        print(circle)
        if circle[0] < min_x:
            min_x = circle[0]
            LB = circle

        if circle[1] < min_y:
            min_y = circle[1]
            RT = circle

    circles = np.delete(circles, np.where(np.all(circles == RT, axis=1)), axis=0)
    circles = np.delete(circles, np.where(np.all(circles == LB, axis=1)), axis=0)

    RB = circles[0]

    return RT, LB, RB


def getCircle(RT: List[int], LB: List[int], RB: List[int]) -> Tuple[int, int, int]:
    X = int((LB[0] + RB[0])/2)
    Y = int((RT[1] + RB[1])/2)

    radius = int((RB[0] - LB[0])/2 + 60)

    return X, Y, radius

input_path = input()

origin = cv2.imread(input_path)

image = cv2.resize(origin, (2550, 3300), interpolation=cv2.INTER_LINEAR)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

blur = cv2.GaussianBlur(gray, (5, 5), 0)

circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, dp=1, minDist=2000, param1=500, param2=30, minRadius=35, maxRadius=45)

center_x = 0
center_y = 0
radius = 0

if circles is not None:
    circles = np.uint16(np.around(circles))
    
    print(circles)
    
    if len(circles[0, :]) == 3:
        RT, LB, RB = getPostion(circles[0, :])
        
        center_x, center_y, radius = getCircle(RT, LB, RB)

        # draw main circle
        # cv2.circle(image, (int(center_x), int(center_y)), int(radius), (0, 255, 0), 2)

        # crop circle and save
        mask = np.zeros_like(image)
        circle_mask = cv2.circle(mask, (int(center_x), int(center_y)), int(radius), (255, 255, 255), -1)
        cropped_image = cv2.bitwise_and(image, circle_mask)

        x, y, w, h = cv2.boundingRect(circle_mask[:,:,0])
        crop_img = cropped_image[y:y+h, x:x+w]

        crop_img[np.where((crop_img==[0,0,0]).all(axis=2))] = [255,255,255]

        cv2.imwrite(f"output/fullsize_{input_path}", crop_img)

x1, y1 = 0, 2640  # Top-left corner
x2, y2 = 1275, 3300  # Bottom-right corner

cropped_image = image[y1:y2, x1:x2]

cv2.imwrite(f"output/identity_{input_path}", cropped_image)

# cv2.imshow("Detected Circles", image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
