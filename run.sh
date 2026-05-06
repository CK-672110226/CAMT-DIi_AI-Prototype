#!/bin/bash

# Script to start the Flask application
# Assumes virtual environment is already set up

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Starting Chihuahua vs Muffin Classifier${NC}"
echo -e "${GREEN}========================================${NC}\n"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment not found. Running install.sh...${NC}"
    bash install.sh
fi

# Activate virtual environment
source venv/bin/activate

# Check if model exists
if [ ! -f "image_classifier_model.h5" ]; then
    echo -e "${YELLOW}Model not found. Training model...${NC}"
    python train.py
fi

# Start the application
echo -e "${GREEN}Starting Flask application...${NC}"
echo -e "${GREEN}Access the app at: http://localhost:5012${NC}\n"
python app.py
