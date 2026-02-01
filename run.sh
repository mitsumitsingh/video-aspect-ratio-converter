#!/bin/bash
# Helper script to run the video converter with the virtual environment

# Activate virtual environment and run the script
source venv/bin/activate
python video_converter.py "$@"
deactivate
