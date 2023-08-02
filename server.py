from flask import Flask, request, jsonify, render_template, send_from_directory
import os
from tensorflow import keras
from PIL import Image
import numpy as np

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'  # Folder to store uploaded images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}  # Allowed file extensions

# Endpoint to receive the image file
@app.route('/upload', methods=['POST'])
def upload():
    # Check if an image file is included in the request
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    image = request.files['image']

    # Check if the file has a valid extension
    if image.filename.split('.')[-1].lower() not in ALLOWED_EXTENSIONS:
        return jsonify({'error': 'Invalid file extension'}), 400

    # Delete the existing image if it exists
    if os.path.exists(os.path.join(UPLOAD_FOLDER, 'image.jpg')):
        os.remove(os.path.join(UPLOAD_FOLDER, 'image.jpg'))

    # Save the new image
    image.save(os.path.join(UPLOAD_FOLDER, 'image.jpg'))

    return jsonify({'message': 'Image uploaded successfully'}), 200

#Endpoint to recieve x-ray photo
@app.route('/upload_project_1', methods=['POST'])
def project():
    UPLOAD_FOLDER = 'project_1_images'
    # Check if an image file is included in the request
    if 'imageFile' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    image = request.files['imageFile']

    # Check if the file has a valid extension
    if image.filename.split('.')[-1].lower() not in ALLOWED_EXTENSIONS:
        return jsonify({'error': 'Invalid file extension'}), 400

    # Delete the existing image if it exists
    if os.path.exists(os.path.join(UPLOAD_FOLDER, 'imageFile.jpg')):
        os.remove(os.path.join(UPLOAD_FOLDER, 'imageFile.jpg'))

    # Save the Image
    image.save(os.path.join(UPLOAD_FOLDER, 'imageFile.jpg'))

    # Run AI Analysis
    model = keras.models.load_model('./BestModel')
    img = Image.open('./project_1_images/imageFile.jpg')
    img_rgb = img.convert('RGB')  # Convert to RGB to ensure 3 channels
    x = img_rgb.resize((64, 64))
    x_data = np.asarray(x)
    y_pred = model.predict(np.expand_dims(x_data, axis=0))
    if y_pred[0][0] > 0.8:
        return jsonify({'message': 'Confidently Pneumonia'}), 200
    elif y_pred[0][0] > 0.65:
        return jsonify({'message': 'Likely Pneumonia'}), 200
    else:
        return jsonify({'message': 'No Pneumonia'}), 200

# Endpoint to serve the image page
@app.route('/image', methods=['GET'])
def imagepage():
    filename = os.path.join(UPLOAD_FOLDER, 'image.jpg')
    return render_template('image.html')

#End Point to serve the Main Page
@app.route('/', methods=['GET'])
def imagepage():
    return render_template('index.html')

# Endpoint to serve the AI model
@app.route('/project_one', methods=['GET'])
def uploadpage():
    return render_template('project_1.html')

# Endpoint to serve the image file for gpt
@app.route('/uploads/image.jpg', methods=['GET'])
def get_image():
    return send_from_directory(UPLOAD_FOLDER, 'image.jpg')

if __name__ == '__main__':
    app.run(host='50.116.61.76', port='80') 
