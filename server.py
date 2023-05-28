from flask import Flask, request, jsonify, render_template, send_from_directory
import os

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

# Endpoint to serve the uploaded image
@app.route('/image', methods=['GET'])
def imagepage():
    filename = os.path.join(UPLOAD_FOLDER, 'image.jpg')
    return render_template('index.html')

# Endpoint to serve the image file
@app.route('/uploads/image.jpg', methods=['GET'])
def get_image():
    return send_from_directory(UPLOAD_FOLDER, 'image.jpg')

# Endpoint for front/mainpage
@app.route('/)
def main():
    return "Welcome to my website, go to /image to see GPT eyes"

if __name__ == '__main__':
    app.run()
