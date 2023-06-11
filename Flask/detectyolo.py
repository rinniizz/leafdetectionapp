import cv2
import torch
from PIL import Image
import os
import glob
import pandas as pd
import numpy as np
import json

model = torch.hub.load('ultralytics/yolov5', 'custom', path='C:/Users/Rosary/yolov5/data/Disbest.pt',force_reload=False)
model.conf = 0.4
model.iou = 0.8
model.multilabel = True
model.max_det = 1000

image_list = []
results_dict = {}
folder_path = './images/'
for file in os.listdir(folder_path):
    if file.endswith(".jpg"):
        image = cv2.imread(os.path.join(folder_path, file))[..., ::-1]
        image_np = np.array(image)
        image_list.append(image_np)


    results = model(image,size=640)
# results = model(img,size=460)

# print(results.xyxy)
# Iterate over the results and store the detections in the dictionary
    for i, result in enumerate(results.xyxy):
        # Get the filename corresponding to the current image
        filename = os.listdir(folder_path)[i]
        
        # Store the detections in the dictionary
        results_dict[filename] = result.tolist()

# Convert the dictionary to a JSON format
    json_dict = {'detections': results_dict}

    with open('data.json', 'w') as f:
        json.dump(json_dict, f,indent=1)

def detect(path):
    image = Image.open(path+"/image.jpg")
    results = model(image,size=640)
    for i, result in enumerate(results.xyxy):
        # Get the filename corresponding to the current image
        filename = os.listdir(path)[i]
        
        # Store the detections in the dictionary
        results_dict[filename] = result.tolist()

# Convert the dictionary to a JSON format
    json_dict = {'detections': results_dict}

    with open('data.json', 'w') as f:
        json.dump(json_dict, f,indent=1)

    return json_dict

