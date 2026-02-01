# Video Converter: 16:9 to 9:16

A Python script to convert videos from 16:9 (landscape) aspect ratio to 9:16 (portrait) aspect ratio.

## Installation

1. Install Python 3.7 or higher
2. Create and activate a virtual environment (recommended):

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate
```

3. Install required dependencies:

```bash
pip install -r requirements.txt
```

**Note:** When you're done working, you can deactivate the virtual environment by running:
```bash
deactivate
```

**Note:** MoviePy requires FFmpeg to be installed on your system. Install it using:
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt-get install ffmpeg` (Ubuntu/Debian) or `sudo yum install ffmpeg` (CentOS/RHEL)
- **Windows**: Download from [FFmpeg website](https://ffmpeg.org/download.html)

## Usage

**Important:** Make sure the virtual environment is activated before running the script!

### Option 1: Using the helper script (Easiest)

```bash
# Make the script executable (first time only)
chmod +x run.sh

# Run the converter
./run.sh input.mp4 output.mp4
```

### Option 2: Manual activation

```bash
# Activate virtual environment
source venv/bin/activate

# Run the script
python video_converter.py input.mp4 output.mp4

# Deactivate when done
deactivate
```

### Option 3: Direct Python path

```bash
venv/bin/python video_converter.py input.mp4 output.mp4
```

### Conversion Methods

The script supports two conversion methods:

1. **Crop (default)**: Center-crops the video to 9:16 aspect ratio
   ```bash
   ./run.sh input.mp4 output.mp4 --method crop
   # OR (with venv activated)
   python video_converter.py input.mp4 output.mp4 --method crop
   ```

2. **Scale**: Scales the video to fit 9:16 and adds black bars if needed
   ```bash
   ./run.sh input.mp4 output.mp4 --method scale
   # OR (with venv activated)
   python video_converter.py input.mp4 output.mp4 --method scale
   ```

## How It Works

- **Crop method**: Takes the center portion of the 16:9 video to create a 9:16 video. This may result in some content being cut off from the sides.
- **Scale method**: Scales the video to fit within a 9:16 frame and adds black bars (pillarboxing) if necessary. This preserves all content but may result in letterboxing.

## Example

```bash
# Convert a landscape video to portrait
python video_converter.py landscape_video.mp4 portrait_video.mp4

# Use scale method to preserve all content
python video_converter.py landscape_video.mp4 portrait_video.mp4 --method scale
```

## Requirements

- Python 3.7+
- MoviePy
- FFmpeg
