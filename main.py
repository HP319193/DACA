import cv2
import numpy as np

input_path = input()

origin = cv2.imread(input_path)

image = cv2.resize(origin, (2550, 3300), interpolation=cv2.INTER_LINEAR)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

blur = cv2.GaussianBlur(gray, (5, 5), 0)

circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, dp=1, minDist=2000, param1=500, param2=30, minRadius=35, maxRadius=40)

center_x = 0
center_y = 0
radius = 0

if circles is not None:
    circles = np.uint16(np.around(circles))
    
    print(circles)
    
    if len(circles[0, :]) == 3: 
        center_x = (circles[0, :][1][0] + circles[0, :][2][0])/2
        center_y = (circles[0, :][0][1] + circles[0, :][1][1])/2
        radius = (circles[0, :][1][0] - circles[0, :][2][0])/2 + 60

        print(center_x)
        print(center_y)
        print(radius)

    # Draw main circle
    # cv2.circle(image, (int(center_x), int(center_y)), int(radius), (0, 255, 0), 2)

    mask = np.zeros_like(image)
    circle_mask = cv2.circle(mask, (int(center_x), int(center_y)), int(radius), (255, 255, 255), -1)
    cropped_image = cv2.bitwise_and(image, circle_mask)

    x, y, w, h = cv2.boundingRect(circle_mask[:,:,0])
    crop_img = cropped_image[y:y+h, x:x+w]

    crop_img[np.where((crop_img==[0,0,0]).all(axis=2))] = [255,255,255]

    cv2.imwrite("QTY_FULLSIZE.jpg", crop_img)

thumbnail_img = cv2.resize(crop_img, (200, 330), interpolation=cv2.INTER_LINEAR)
cv2.imwrite("THUMBNAIL.jpg", thumbnail_img)

x1, y1 = 115, 2680  # Top-left corner
x2, y2 = 1210, 3160  # Bottom-right corner

cropped_image = image[y1:y2, x1:x2]

cv2.imwrite("IDENTITY.jpg", cropped_image)

# Show image
# cv2.imshow("Detected Circles", image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
