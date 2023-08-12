import base64
import cv2
import tensorflow as tf
import logging

from flask import Flask, request, jsonify
import numpy as np
import os

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='server.log', level=logging.INFO)

# Load your Python model here
optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
model = tf.keras.models.load_model('my_model.h5', compile=False)
model.compile(optimizer=optimizer)

@app.route('/predict', methods=['POST'])
def predict():
    if request.method != 'POST':
        return jsonify({'error': 'Invalid request method'})

    if 'image_data' not in request.json:
        return jsonify({'error': 'Missing image_data'})

    # Get the image data from the request body
    data = request.json.get('image_data')

    try:
        # Decode the base64-encoded image data to a numpy array
        data = base64.b64decode(data.split(',')[1])
        data = np.frombuffer(data, dtype=np.uint8)
        img = cv2.imdecode(data, cv2.IMREAD_GRAYSCALE)

    except Exception as e:
        logging.error('Failed to decode image: {}'.format(str(e)))
        return jsonify({'error': 'Failed to decode image: {}'.format(str(e))})

    try:
        # Reshape the image array to match the input shape
        img = img.reshape(1, 32, 32, 1)

        # Make the prediction using your model
        pred = model.predict(img)

        logging.info('Request: {}\nPrediction: {}\n'.format(request.json, pred.tolist()))

    except Exception as e:
        logging.error('Failed to make prediction: {}'.format(str(e)))
        return jsonify({'error': 'Failed to make prediction: {}'.format(str(e))})

    # Return the prediction result as JSON
    return jsonify({'prediction': pred.tolist()})


app.config['SECRET_KEY'] = os.urandom(24)
