from flask import Flask,request,jsonify,json,send_file
import werkzeug
from flask_cors import CORS
import torch
from io import BytesIO
from PIL import Image
from flask_ngrok import run_with_ngrok
import numpy as np
import pandas as pd
import detectyolo
import db
import reshape
import base64
from flask_cors import CORS
from pyngrok import ngrok

app = Flask(__name__)
ngrok.set_auth_token("2EIasG8F5pF7JUJm7CvGp7cz00D_69nS7SRy3F85ozSDuyTej")
CORS(app)
run_with_ngrok(app)

model = torch.hub.load('ultralytics/yolov5', 'custom', path='./Disbest.pt',force_reload=False)
folder_path = './images/'
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image = request.files['image']
    img = Image.open(image)
    img.save(f"{folder_path}/image.jpg")
    # detections = detectyolo.detect(folder_path)
    # print(detections)
    # processed_data = reshape.process_data()
    # print(processed_data)
    # db.insert_disease_statics(processed_data)
    
    # top_disease_detail = db.get_top_disease_detail(processed_data)

    # response = {
    #     'disease_statics': processed_data,
    #     'disease_detail': top_disease_detail,
    # }
    # img_path = 'C:/Users/Rosary/Desktop/LeafDetectionProjectApp/imgprocess/img.jpg'
    # return jsonify(response),send_file(img_path, mimetype='image/jpeg')
    detectyolo.detect(folder_path)
    processed_data = reshape.process_data()
    db.insert_disease_statics(processed_data)
    top_disease_detail = db.get_top_disease_detail(processed_data)
    
    # Convert image to base64
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    response = {
        'image': img_str,
        'disease_statics': processed_data,
        'disease_detail': top_disease_detail,
    }
    
    return jsonify(response)

@app.route('/get_json')
def get_json():
    detections = detectyolo.detect(folder_path)
    print(detections)
    processed_data = reshape.process_data()
    print(processed_data)
    db.insert_disease_statics(processed_data)
    
    top_disease_detail = db.get_top_disease_detail(processed_data)

    response = {
        'disease_statics': processed_data,
        'disease_detail': top_disease_detail,
    }
    return jsonify(response)

@app.route('/get_image')
def get_image():
    img_path = '../imgprocess/img.jpg'
    return send_file(img_path, mimetype='image/jpeg')

@app.route('/get_stat')
def get_stat():
    stat = db.get_static()
    print(stat)
    return jsonify(stat)

if __name__ == '__main__':  
    app.run()