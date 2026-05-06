# Image Classification Web App - Setup Guide

## Project Structure
```
.
├── app.py                    # Flask application
├── train.py                  # Model training script
├── requirements.txt          # Python dependencies
├── templates/
│   └── index.html           # Frontend HTML
├── static/
│   └── style.css            # Frontend CSS
└── uploads/                 # Uploaded images (auto-created)
```

## Features

✨ **Image Classification Web App** for Chihuahua vs Muffin classification
- 🎨 Modern, responsive web interface
- 🖼️ Image upload with drag-and-drop support
- 🔮 Real-time AI predictions using TensorFlow
- 📊 Detailed confidence scores and predictions
- 🎯 Mobile-friendly design

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Train the Model (Optional)
```bash
python train.py
```
This creates:
- `image_classifier_model.h5` - Trained model
- `model_info.pkl` - Model metadata

### 3. Run the Flask App
```bash
python app.py
```

The app will start at: **http://localhost:5012**

## API Endpoints

### GET `/`
- Returns the web interface

### GET `/health`
- Health check endpoint
- Response: `{ status: "healthy", model_loaded: bool, classes: [] }`

### GET `/info`
- Returns API information
- Response: `{ name: str, version: str, classes: [], description: str }`

### POST `/predict`
- Upload an image for classification
- Parameters: `file` (multipart/form-data)
- Response: `{ success: bool, prediction: str, confidence: float, all_predictions: {} }`

### GET `/list-uploads`
- List all uploaded images

## Supported Image Formats
- PNG (.png)
- JPG/JPEG (.jpg, .jpeg)
- GIF (.gif)
- BMP (.bmp)
- Maximum file size: 16MB

## Example Usage

### Using the Web Interface
1. Open http://localhost:5012
2. Upload or drag an image
3. View instant predictions and confidence scores

### Using cURL
```bash
curl -X POST -F "file=@image.jpg" http://localhost:5012/predict
```

### Using Python
```python
import requests

with open('image.jpg', 'rb') as f:
    response = requests.post('http://localhost:5012/predict', files={'file': f})
    print(response.json())
```

## Model Information
- **Architecture**: MobileNetV2 with Transfer Learning
- **Input Size**: 224x224 pixels
- **Classes**: 
  - 🐕 Chihuahua
  - 🧁 Muffin
- **Framework**: TensorFlow/Keras

## Troubleshooting

### Model not loading?
```bash
# Create and save the model
python train.py

# Then run the app
python app.py
```

### Port already in use?
Edit `app.py` line with `app.run()`:
```python
app.run(host='0.0.0.0', debug=True, port=5013)  # Change 5012 to another port
```

### Permission denied on uploads?
```bash
mkdir uploads
chmod 755 uploads
```

## Performance Notes
- First prediction may take longer (model initialization)
- Subsequent predictions are faster
- Model runs on CPU by default
- For GPU acceleration, install TensorFlow with GPU support

## Production Deployment

### Using Gunicorn (Linux/Mac)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5012 app:app
```

### Using Windows Service
Create `run_app.bat`:
```batch
@echo off
python app.py
```

## Notes
- Training data should include images of chihuahuas and muffins
- Model improves with more diverse training samples
- Upload folder stores images for reference
- All predictions are performed locally

## License
Educational Project - SC664401

## Author
Your Name - CAMT-DIi AI Prototype

