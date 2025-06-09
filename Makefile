# Makefile for RPAL_Project using PyInstaller

PYTHON=./env/Scripts/python.exe
MAIN=myrpal.py
BUILD_NAME=RPALProject

.PHONY: help env install run build clean clean_build

help:
	@echo "Usage:"
	@echo "  make env          - Create virtual environment"
	@echo "  make install      - Install dependencies into venv"
	@echo "  make run          - Run the application"
	@echo "  make build        - Build executable using PyInstaller"
	@echo "  make clean        - Remove __pycache__ and *.pyc"
	@echo "  make clean_build  - Remove build artifacts"

# Create a virtual environment
env:
	python -m venv env

# Install dependencies into the virtual environment
install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install pyinstaller
	@if exist requirements.txt $(PYTHON) -m pip install -r requirements.txt

# Run the main Python file
run:
	$(PYTHON) $(MAIN)

# Build an executable with PyInstaller
build:
	$(PYTHON) -m PyInstaller --onefile --name $(BUILD_NAME) $(MAIN)

# Clean Python cache
clean:
	del /s /q __pycache__ 2>nul || exit 0
	del /s /q *.pyc 2>nul || exit 0

# Clean build artifacts
clean_build:
	rmdir /s /q build dist 2>nul || exit 0
	del /q *.spec 2>nul || exit 0
