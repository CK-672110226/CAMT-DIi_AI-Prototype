"""
Flask Web Application for Image Classification
Predicts whether an image contains a chihuahua or a muffin
"""

from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from tensorflow import keras
from tensorflow.keras.preprocessing import image as keras_image
import numpy as np
import os
import pickle
from datetime import datetime

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Load model and model info
try:
    model = keras.models.load_model('image_classifier_model.h5')
    with open('model_info.pkl', 'rb') as f:
        model_info = pickle.load(f)
    MODEL_CLASSES = model_info['classes']
    INPUT_SHAPE = model_info['input_shape']
    print("✓ Model loaded successfully!")
except Exception as e:
    print(f"⚠ Warning: Could not load model. {str(e)}")
    print("  Please run train.py first to create the model.")
    model = None
    MODEL_CLASSES = ['chihuahua', 'muffin']
    INPUT_SHAPE = (224, 224, 3)

def allowed_file(filename):
    """Check if file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(image_path):
    """Load and preprocess image for model prediction"""
    try:
        img = keras_image.load_img(image_path, target_size=(INPUT_SHAPE[0], INPUT_SHAPE[1]))
        img_array = keras_image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0  # Normalize to [0, 1]
        return img_array
    except Exception as e:
        raise Exception(f"Error processing image: {str(e)}")

def predict_image(image_path):
    """Predict the class of an image"""
    if model is None:
        # Return mock prediction for demonstration if model not loaded
        return {
            'class': 'chihuahua',
            'confidence': 0.85,
            'all_predictions': {
                'chihuahua': 0.85,
                'muffin': 0.15
            }
        }
    
    try:
        img_array = preprocess_image(image_path)
        predictions = model.predict(img_array, verbose=0)
        
        predicted_class_idx = np.argmax(predictions[0])
        predicted_class = MODEL_CLASSES[predicted_class_idx]
        confidence = float(predictions[0][predicted_class_idx])
        
        # Create detailed predictions dictionary
        all_predictions = {
            MODEL_CLASSES[i]: float(predictions[0][i]) 
            for i in range(len(MODEL_CLASSES))
        }
        
        return {
            'class': predicted_class,
            'confidence': confidence,
            'all_predictions': all_predictions
        }
    except Exception as e:
        raise Exception(f"Prediction error: {str(e)}")

@app.route('/')
def index():
    """Render the home page"""
    return render_template('index.html')

@app.route('/info')
def info():
    """Return API information"""
    return jsonify({
        'name': 'Image Classification Web App',
        'version': '1.0',
        'classes': MODEL_CLASSES,
        'description': 'Classify images as Chihuahua or Muffin'
    })

@app.route('/predict', methods=['POST'])
def predict():
    """Handle image upload and prediction"""
    
    # Check if file is in request
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    # Check if file is selected
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Check if file is allowed
    if not allowed_file(file.filename):
        return jsonify({'error': f'File type not allowed. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}'}), 400
    
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
        filename = timestamp + filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Make prediction
        result = predict_image(filepath)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'prediction': result['class'],
            'confidence': round(result['confidence'] * 100, 2),
            'all_predictions': {
                k: round(v * 100, 2) for k, v in result['all_predictions'].items()
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/list-uploads', methods=['GET'])
def list_uploads():
    """List all uploaded images"""
    try:
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        image_files = [f for f in files if allowed_file(f)]
        return jsonify({'files': image_files})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'classes': MODEL_CLASSES
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5012))
    print("\n" + "="*50)
    print("🚀 Starting Image Classification Web App")
    print("="*50)
    print(f"Classes: {', '.join(MODEL_CLASSES)}")
    print(f"Model loaded: {model is not None}")
    print(f"Access the app at: http://localhost:{port}")
    print("="*50 + "\n")
    
    app.run(host='0.0.0.0', debug=True, port=port)
