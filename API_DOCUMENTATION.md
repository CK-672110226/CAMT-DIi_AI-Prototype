# API Documentation - Chihuahua vs Muffin Classifier

## Base URL
```
http://localhost:5012
```

## Endpoints

### 1. Home Page
**GET** `/`

Returns the web interface for image classification.

**Response**: HTML page

**Example**:
```bash
curl http://localhost:5012/
```

---

### 2. Health Check
**GET** `/health`

Check if the application and model are running properly.

**Response**:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "classes": ["chihuahua", "muffin"]
}
```

**Example**:
```bash
curl http://localhost:5012/health
```

---

### 3. API Information
**GET** `/info`

Get information about the API and available classes.

**Response**:
```json
{
  "name": "Image Classification Web App",
  "version": "1.0",
  "classes": ["chihuahua", "muffin"],
  "description": "Classify images as Chihuahua or Muffin"
}
```

**Example**:
```bash
curl http://localhost:5012/info
```

---

### 4. Image Prediction
**POST** `/predict`

Upload an image and get classification prediction.

**Request Headers**:
```
Content-Type: multipart/form-data
```

**Parameters**:
- `file` (required): Image file (PNG, JPG, JPEG, GIF, BMP)
- Max size: 16MB

**Response**:
```json
{
  "success": true,
  "filename": "20240515_143022_image.jpg",
  "prediction": "chihuahua",
  "confidence": 85.25,
  "all_predictions": {
    "chihuahua": 85.25,
    "muffin": 14.75
  }
}
```

**Error Response**:
```json
{
  "error": "File type not allowed. Allowed types: png, jpg, jpeg, gif, bmp"
}
```

**Examples**:

Using cURL:
```bash
curl -X POST -F "file=@image.jpg" http://localhost:5012/predict
```

Using Python requests:
```python
import requests

with open('image.jpg', 'rb') as f:
    response = requests.post('http://localhost:5012/predict', files={'file': f})
    result = response.json()
    print(f"Prediction: {result['prediction']}")
    print(f"Confidence: {result['confidence']}%")
```

Using JavaScript fetch:
```javascript
const formData = new FormData();
formData.append('file', imageFile);

fetch('http://localhost:5012/predict', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => {
  console.log('Prediction:', data.prediction);
  console.log('Confidence:', data.confidence);
});
```

---

### 5. List Uploaded Images
**GET** `/list-uploads`

Get a list of all uploaded images.

**Response**:
```json
{
  "files": [
    "20240515_143022_image1.jpg",
    "20240515_143525_image2.png",
    "20240515_144010_image3.jpg"
  ]
}
```

**Example**:
```bash
curl http://localhost:5012/list-uploads
```

---

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad Request (e.g., no file provided) |
| 500 | Server Error (e.g., prediction failed) |

---

## File Upload Requirements

### Supported Formats
- PNG (`.png`)
- JPEG (`.jpg`, `.jpeg`)
- GIF (`.gif`)
- Bitmap (`.bmp`)

### Size Limits
- Maximum: 16MB per file

### Processing
- Images are automatically resized to 224×224 pixels
- Normalized to [0, 1] range for model input

---

## Response Format

All responses (except HTML) use JSON format.

### Success Response
```json
{
  "success": true,
  "data": {}
}
```

### Error Response
```json
{
  "error": "Error message description"
}
```

---

## Examples by Language

### cURL
```bash
# Simple prediction
curl -X POST -F "file=@chihuahua.jpg" http://localhost:5012/predict

# Pretty print JSON response
curl -X POST -F "file=@muffin.jpg" http://localhost:5012/predict | jq .
```

### Python
```python
import requests
import json

# Upload and predict
url = 'http://localhost:5012/predict'
with open('image.jpg', 'rb') as f:
    response = requests.post(url, files={'file': f})

# Parse response
result = response.json()
if result['success']:
    print(f"Class: {result['prediction']}")
    print(f"Confidence: {result['confidence']}%")
else:
    print(f"Error: {result['error']}")
```

### JavaScript (Node.js with axios)
```javascript
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

const form = new FormData();
form.append('file', fs.createReadStream('image.jpg'));

axios.post('http://localhost:5012/predict', form, {
  headers: form.getHeaders()
})
.then(response => {
  console.log('Prediction:', response.data.prediction);
  console.log('Confidence:', response.data.confidence);
})
.catch(error => {
  console.error('Error:', error.response.data.error);
});
```

### JavaScript (Browser)
```javascript
const fileInput = document.getElementById('fileInput');
const file = fileInput.files[0];

const formData = new FormData();
formData.append('file', file);

fetch('http://localhost:5012/predict', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => {
  console.log('Prediction:', data.prediction);
  console.log('Confidence:', data.confidence);
  console.log('All predictions:', data.all_predictions);
})
.catch(error => console.error('Error:', error));
```

### Java
```java
import okhttp3.*;
import java.io.File;

OkHttpClient client = new OkHttpClient();

File file = new File("image.jpg");
RequestBody requestBody = new MultipartBody.Builder()
    .setType(MultipartBody.FORM)
    .addFormDataPart("file", file.getName(),
        RequestBody.create(file, MediaType.parse("image/jpeg")))
    .build();

Request request = new Request.Builder()
    .url("http://localhost:5012/predict")
    .post(requestBody)
    .build();

Response response = client.newCall(request).execute();
String responseBody = response.body().string();
System.out.println(responseBody);
```

---

## Rate Limiting

Currently no rate limiting implemented. For production deployment, consider adding:
- Request throttling
- API key authentication
- CORS policies

---

## Performance Notes

- **First Request**: May take 2-5 seconds (model initialization)
- **Subsequent Requests**: Typically 200-500ms
- **GPU Support**: Install TensorFlow GPU for faster predictions
- **Concurrent Requests**: Flask development server handles 1 request at a time

---

## Troubleshooting

### Model Not Found
```
Error: Could not load model
```
**Solution**: Run `python train.py` to create the model

### Port Already in Use
```
Error: Address already in use
```
**Solution**: Change port in `app.py` or kill process using port 5012

### File Type Not Allowed
```
Error: File type not allowed
```
**Solution**: Use one of the supported formats (PNG, JPG, GIF, BMP)

### Timeout
```
Error: Connection timeout
```
**Solution**: Check if Flask app is running on the correct port

---

## Integration Examples

### Using as Microservice
```python
# service.py
import requests
from concurrent.futures import ThreadPoolExecutor

def classify_image(image_path):
    with open(image_path, 'rb') as f:
        response = requests.post('http://localhost:5012/predict', 
                               files={'file': f})
    return response.json()

# Batch classification
with ThreadPoolExecutor(max_workers=4) as executor:
    results = executor.map(classify_image, image_files)
```

### With Database
```python
# Logging predictions to database
from datetime import datetime
import sqlite3

def save_prediction(image_path, prediction, confidence):
    conn = sqlite3.connect('predictions.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO predictions (filename, class, confidence, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (image_path, prediction, confidence, datetime.now()))
    conn.commit()
    conn.close()
```

---

## Security Considerations

1. **File Validation**: Only image files are accepted
2. **Size Limits**: Maximum 16MB per upload
3. **Temporary Storage**: Uploaded files are stored in `uploads/` folder
4. **CORS**: Currently allows all origins (configure for production)

---

For more information, see:
- [README.md](README.md) - Project overview
- [SETUP.md](SETUP.md) - Setup instructions
