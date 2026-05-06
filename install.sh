#!/bin/bash

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Chihuahua vs Muffin Classifier Setup${NC}"
echo -e "${GREEN}========================================${NC}\n"

# Check Python installation
echo -e "${YELLOW}Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is not installed. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✓ Python $PYTHON_VERSION found${NC}\n"

# Create virtual environment
echo -e "${YELLOW}Creating virtual environment...${NC}"
python3 -m venv venv

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Install requirements
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

# Train model
echo -e "${YELLOW}Training model...${NC}"
python train.py

# Create uploads directory
mkdir -p uploads

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}Setup Complete!${NC}"
echo -e "${GREEN}========================================${NC}\n"

echo -e "${YELLOW}To start the application:${NC}"
echo -e "${GREEN}1. Activate virtual environment:${NC}"
echo "   source venv/bin/activate"
echo -e "${GREEN}2. Run the Flask app:${NC}"
echo "   python app.py"
echo -e "${GREEN}3. Open in browser:${NC}"
echo "   http://localhost:5012"
echo ""
