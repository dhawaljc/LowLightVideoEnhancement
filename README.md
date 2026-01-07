# Low-Light Video Enhancement Web Application

A professional web-based application for enhancing low-light videos using classical image processing techniques. Features two enhancement methods with real-time side-by-side comparison.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)

## Features

- **Two Enhancement Methods**
  - Adaptive Enhancement: Detection-based selective enhancement for mixed lighting
  - Global Enhancement: Uniform gamma correction for faster processing
  
- **Real-Time Comparison**
  - Side-by-side video playback
  - Synchronized play/pause controls
  - Flexible layout (side-by-side or stacked)
  
- **User-Friendly Interface**
  - Clean, professional design
  - Detailed parameter explanations
  - Step-by-step workflow
  - Quality metrics and statistics

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/low-light-video-enhancement.git
   cd low-light-video-enhancement
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open in browser**
   ```
   http://localhost:5000
   ```

## Usage

### 1. Upload Video
- Click "Choose Video File" or drag and drop
- Supported formats: MP4, AVI, MOV, MKV (max 500MB)

### 2. Configure Settings

**Enhancement Method:**
- **Adaptive**: Best for mixed lighting scenes
- **Global**: Faster, best for uniformly dark videos

**Enhancement Strength** (1.0-3.0): Controls brightness increase

### 3. Process & Compare
- Click "Start Enhancement"
- View side-by-side comparison
- Use synchronized playback controls
- Download enhanced video

## Project Structure

```
low-light-video-enhancement/
├── app.py                 # Flask backend
├── requirements.txt       # Python dependencies
├── README.md             # Documentation
├── templates/
│   └── index.html        # Frontend interface
├── uploads/              # Temporary storage
└── outputs/              # Enhanced videos
```

## License

MIT License - see LICENSE file for details

## Contact

Project Link: [https://github.com/YOUR_USERNAME/low-light-video-enhancement](https://github.com/YOUR_USERNAME/low-light-video-enhancement)
