"""
Test script to verify the Flask app and model work correctly
"""

import sys
import requests
from pathlib import Path

def test_api():
    """Test API endpoints"""
    
    BASE_URL = 'http://localhost:5012'
    
    print("\n" + "="*50)
    print("Testing Chihuahua vs Muffin Classifier API")
    print("="*50 + "\n")
    
    # Test 1: Health check
    print("📋 Test 1: Health Check")
    try:
        response = requests.get(f'{BASE_URL}/health', timeout=5)
        if response.status_code == 200:
            print("✓ Health check passed")
            print(f"  Response: {response.json()}\n")
        else:
            print(f"✗ Health check failed: {response.status_code}\n")
    except Exception as e:
        print(f"✗ Error: {e}\n")
        return False
    
    # Test 2: Info endpoint
    print("📋 Test 2: API Info")
    try:
        response = requests.get(f'{BASE_URL}/info', timeout=5)
        if response.status_code == 200:
            print("✓ Info endpoint works")
            info = response.json()
            print(f"  Name: {info['name']}")
            print(f"  Version: {info['version']}")
            print(f"  Classes: {', '.join(info['classes'])}\n")
        else:
            print(f"✗ Info endpoint failed: {response.status_code}\n")
    except Exception as e:
        print(f"✗ Error: {e}\n")
        return False
    
    # Test 3: Prediction with test image
    print("📋 Test 3: Prediction Test")
    test_image = Path('test_image.jpg')
    
    if not test_image.exists():
        print("ℹ No test image found (test_image.jpg)")
        print("  To test prediction, upload an image using the web interface")
    else:
        try:
            with open(test_image, 'rb') as f:
                files = {'file': f}
                response = requests.post(f'{BASE_URL}/predict', files=files, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                print("✓ Prediction successful")
                print(f"  Predicted class: {result['prediction']}")
                print(f"  Confidence: {result['confidence']}%")
                print(f"  All predictions: {result['all_predictions']}\n")
            else:
                print(f"✗ Prediction failed: {response.status_code}")
                print(f"  Error: {response.json()}\n")
        except Exception as e:
            print(f"✗ Error: {e}\n")
            return False
    
    print("="*50)
    print("✓ All tests completed!")
    print("="*50 + "\n")
    return True

if __name__ == '__main__':
    print("\nMake sure the Flask app is running:")
    print("  python app.py\n")
    
    try:
        success = test_api()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(1)
