# 🐕 Chihuahua vs Muffin Classifier 🧁

A modern web application for image classification using deep learning and Flask.

## 🌟 Features

- **Web-Based Interface**: Modern, responsive UI with drag-and-drop image upload
- **Real-Time Predictions**: Instant AI-powered image classification
- **Transfer Learning**: Uses MobileNetV2 pre-trained model for accurate predictions
- **Confidence Scores**: Displays detailed prediction percentages for all classes
- **Mobile Friendly**: Fully responsive design works on all devices
- **REST API**: Can be integrated with other applications

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Create & Train Model
```bash
python train.py
```

### 3. Run the Application
```bash
python app.py
```

Access the app at: **http://localhost:5012**

## 📁 Project Structure

```
CAMT-DIi_AI-Prototype/
├── app.py                    # Flask backend
├── train.py                  # Model training script
├── requirements.txt          # Dependencies
├── SETUP.md                  # Detailed setup guide
├── README.md                 # This file
├── templates/
│   └── index.html           # Web interface
├── static/
│   └── style.css            # Styling
└── uploads/                 # Uploaded images
```

## 🎯 How It Works

1. **Upload Image**: Drag and drop or click to upload an image
2. **Process**: The app preprocesses the image (resize to 224x224)
3. **Predict**: MobileNetV2 model classifies as Chihuahua or Muffin
4. **Display Results**: Shows prediction with confidence percentage

## 💻 API Usage

### Upload and Predict
```bash
curl -X POST -F "file=@image.jpg" http://localhost:5012/predict
```

### Response
```json
{
  "success": true,
  "filename": "image.jpg",
  "prediction": "chihuahua",
  "confidence": 85.5,
  "all_predictions": {
    "chihuahua": 85.5,
    "muffin": 14.5
  }
}
```

## 🤖 Model Details

- **Architecture**: MobileNetV2 + Custom Dense Layers
- **Input Shape**: 224×224×3 (RGB images)
- **Output Classes**: 2 (Chihuahua, Muffin)
- **Framework**: TensorFlow/Keras
- **Training**: Transfer learning with ImageNet weights

## 📋 Requirements

- Python 3.8+
- TensorFlow 2.12+
- Flask 2.3+
- NumPy
- Pillow

## 🛠️ Configuration

Edit `app.py` to modify:
- **Port**: Change `port=5012` to another port
- **Host**: Change `host='0.0.0.0'` to restrict access
- **Upload folder**: Modify `UPLOAD_FOLDER` path
- **Max file size**: Change `MAX_FILE_SIZE` limit

## 📊 Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Web interface |
| POST | `/predict` | Upload image and get prediction |
| GET | `/health` | Health check |
| GET | `/info` | API information |
| GET | `/list-uploads` | List all uploaded images |

## 📝 Examples

### Web Interface Example
```
Upload Image → AI Analysis → Result Display
  ↓
  Chihuahua 85.5% 🐕
  Muffin 14.5% 🧁
```

### Python Client Example
```python
import requests

with open('chihuahua.jpg', 'rb') as f:
    response = requests.post('http://localhost:5012/predict', 
                           files={'file': f})
    result = response.json()
    print(f"Prediction: {result['prediction']}")
    print(f"Confidence: {result['confidence']}%")
```

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production with Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5012 app:app
```

### Docker (Optional)
Create `Dockerfile` for containerization and deployment to cloud services.

## 📖 Documentation

See [SETUP.md](SETUP.md) for detailed setup instructions and troubleshooting.

## 🎓 Course Information

- **Course**: SC664401 - Prototyping for AI and ML Systems
- **University**: Khon Kaen University
- **Program**: SIDS
- **Semester**: 2568-2569

## 🤝 Contributing

This is a course project. For improvements or bug reports, please create an issue or pull request.

## 📄 License

Educational Project

## 👨‍💻 Author

Chanachot Khamchum - ID: 672110226

---

**Built with**: Flask, TensorFlow, HTML5, CSS3, JavaScript
**Last Updated**: May 2024
