import os
import numpy as np
from flask import Flask, request, jsonify, render_template, redirect
from flask_cors import CORS
from skimage import transform
from matplotlib.pyplot import imread
from tensorflow.keras.models import load_model

app = Flask(__name__, template_folder='templates')
CORS(app)

# Parameters
img_width, img_height = 64, 64
num_classes = 6

# Define file paths
model_file = 'models/cnn_classification_model.h5'

def initialize_model():
    if not os.path.exists(model_file):
        raise FileNotFoundError(f"Model file not found at {model_file}. Make sure to download and extract the model before serving.")
    
    print("Loading model...")
    return load_model(model_file)

# Load the trained model
model = initialize_model()

@app.route('/')
def index():
    print("Current working directory:", os.getcwd())
    print("Templates directory exists:", os.path.exists('templates'))
    print("Index.html file exists:", os.path.exists('templates/index.html'))
    return render_template('index.html')

@app.route('/image', methods=['POST'])
def predict():
    if 'myfile' not in request.files:
        return redirect(request.url)

    file = request.files['myfile']
    if file.filename == '':
        return redirect(request.url)

    filename = os.path.join("uploaded_images", file.filename)
    file.save(filename)

    # Load and preprocess the image
    img = transform.resize(imread(filename), (img_width, img_height))
    img = np.array(img, dtype=np.float32).reshape(1, img_width, img_height, 3)

    # Make prediction
    pred = model.predict(img)
    pred_class = np.argmax(pred, axis=1)[0]

    # Define class labels
    class_labels = {
        0: "Cat",
        1: "Dog",
        2: "Rabbit",
        3: "Cow",
        4: "Horse",
        5: "Sheep"
    }

    result = class_labels.get(pred_class, "Unknown class")
    return jsonify(result)

if __name__ == '__main__':
    if not os.path.exists('uploaded_images'):
        os.makedirs('uploaded_images')
    app.run(debug=True, host='0.0.0.0', port=5000)
