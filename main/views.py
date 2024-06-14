from django.shortcuts import render
from django.http import JsonResponse
from .models import Image
from sendfile import sendfile
from django.views.decorators.csrf import csrf_exempt

from django.http import FileResponse

import cv2
import numpy as np
from typing import List, Tuple
import uuid, os

output_folder = "main/static/output"

@csrf_exempt
def submit(request):
    if request.method == "POST":
        key = request.POST.get('key')
        value = request.POST.get('value')

        status = "rejected"
        if value == "true":
            status = "approved"

        Image.objects.filter(name=key).update(status=status)

        return JsonResponse({"status": "good"})
        
def fix(request):
    items = Image.objects.filter(status='rejected')
    rejected = []

    for item in items:
        rejected.append(item.name)

    print(rejected)
    return render(request, 'fix.html', {"items": rejected})

def source_file(request, filepath):
    file_path = f"source/{filepath}"
    response = FileResponse(open(file_path, 'rb'))
    return response

def download_file(request, filepath):
    file_path = f"main/static/output/fullsize_{filepath}"
    response = FileResponse(open(file_path, 'rb'))
    return response

def getOval(RT: List[int], LB: List[int], RB: List[int]) -> Tuple[int, int, int, int]:
    X = int((LB[0] + RB[0]) / 2)
    Y = (RT[1] + RB[1]) / 2
    
    y_v = RB[1] - RT[1]
    y_h = RT[0] - RB[0]

    y_offset = (y_h * y_h) / (2 * y_v)

    Y = int(Y + y_offset)

    major_axis = int((RB[0] - LB[0]) / 2 + 62)
    minor_axis_top = int((RB[1] - RT[1]) / 2 + 65)
    minor_axis_bottom = int((RB[1] - RT[1]) / 2 + 50)

    return X, Y, major_axis, minor_axis_top, minor_axis_bottom

def getPosition(path: str) -> Tuple[List[int], List[int], List[int]]:
    image = cv2.imread(path)
    
    print("Path =>", path)
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

def cropImage(filename: str) -> None:
    input_path = os.path.join("source", filename)

    image = cv2.imread(input_path)

    RT, LB, RB = getPosition(input_path)

    center_x, center_y, major_axis, minor_axis_top, minor_axis_bottom = getOval(RT, LB, RB)

    # Crop oval and save
    mask = np.zeros_like(image)
    
    # Create two halves of the oval mask
    top_half_mask = cv2.ellipse(mask.copy(), (int(center_x), int(center_y)), (int(major_axis), int(minor_axis_top)), 0, 0, 180, (255, 255, 255), -1)
    bottom_half_mask = cv2.ellipse(mask.copy(), (int(center_x), int(center_y)), (int(major_axis), int(minor_axis_bottom)), 0, 180, 360, (255, 255, 255), -1)
    
    # Combine the two halves
    oval_mask = cv2.add(top_half_mask, bottom_half_mask)
    
    cropped_image = cv2.bitwise_and(image, oval_mask)

    x, y, w, h = cv2.boundingRect(oval_mask[:, :, 0])
    crop_img = cropped_image[y:y+h, x:x+w]

    crop_img[np.where((crop_img == [0, 0, 0]).all(axis=2))] = [255, 255, 255]

    cv2.imwrite(os.path.join(output_folder, f"fullsize_{filename}"), crop_img)

    x1, y1 = 0, 2640  # Top-left corner
    x2, y2 = 1275, 3300  # Bottom-right corner

    cropped_image = image[y1:y2, x1:x2]

    cv2.imwrite(os.path.join(output_folder, f"identity_{filename}"), cropped_image)

def uploadImage(request):
    return render(request, 'upload.html')

def processImage(request):
    if request.method == 'POST' and request.FILES:
        files = request.FILES.getlist('files[]')
        
        filelist = []
        for file in files:
            extension = os.path.splitext(file.name)[1]
            image = Image()
            image.status = "initial"
            filename = str(uuid.uuid4()) + extension
            image.name = filename
            file.name = filename
            image.file = file
            image.save()

            cropImage(filename)

            if os.path.exists(os.path.join("main/static/output", f"fullsize_{filename}")):
                filelist.append(filename)

        return JsonResponse({"filelist": filelist})

@csrf_exempt
def updateQuantity(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        quantity = request.POST.get('quantity')

        print(name)
        try:
            Image.objects.filter(name=name).update(quantity=int(quantity))
            return JsonResponse({"status": "good"})
        except:
            Image.objects.filter(name=name).update(quantity=int(quantity))
            return JsonResponse({"status": "bad"})