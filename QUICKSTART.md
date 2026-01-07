# 🚀 QUICK START GUIDE

## Running the Low-Light Video Enhancement Web App Locally

### For Windows Users:

1. **Extract all files** to a folder on your computer

2. **Double-click `setup.bat`** to install dependencies
   - This will install Flask, OpenCV, and other required packages
   - Creates necessary directories

3. **Run the application:**
   - Double-click `run.bat` OR
   - Open Command Prompt in the folder and type:
     ```
     python app.py
     ```

4. **Open your browser** and go to:
   ```
   http://localhost:5000
   ```

---

### For Mac/Linux Users:

1. **Extract all files** to a folder on your computer

2. **Open Terminal** in the folder

3. **Run setup script:**
   ```bash
   bash setup.sh
   ```
   OR install manually:
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the server:**
   ```bash
   python app.py
   ```

5. **Open your browser** and go to:
   ```
   http://localhost:5000
   ```

---

## Using the Web Interface

1. **Upload Video**
   - Drag & drop your video file OR click "Choose Video File"
   - Supported: MP4, AVI, MOV, MKV (max 500MB)

2. **Configure Settings**
   - Choose method: Adaptive (better quality) or Global (faster)
   - Adjust strength slider (1.0 - 3.0)
   - For Adaptive: adjust threshold and blur size

3. **Process**
   - Click "Start Enhancement"
   - Wait for processing to complete

4. **Download**
   - Preview the enhanced video
   - Click "Download Enhanced Video"

---

## Two Enhancement Methods

### 🎯 Adaptive Enhancement (Recommended)
- **Best for:** Mixed lighting, outdoor videos, complex scenes
- **How it works:** Detects dark regions and enhances only those areas
- **Result:** Natural-looking with preserved bright regions
- **Speed:** Slightly slower but better quality

### ⚡ Global Enhancement (Faster)
- **Best for:** Uniformly dark videos, indoor scenes
- **How it works:** Applies uniform brightness boost
- **Result:** Fast and effective for simple cases
- **Speed:** Faster processing

---

## Troubleshooting

### "Python not found"
- Install Python 3.8+ from python.org
- Make sure to check "Add Python to PATH" during installation

### "Port 5000 already in use"
- Edit `app.py` and change the port number:
  ```python
  app.run(debug=True, host='0.0.0.0', port=8080)  # Change 5000 to 8080
  ```

### "Module not found" errors
- Run: `pip install -r requirements.txt`
- If still fails: `pip install --upgrade pip` then try again

### Video won't play in browser
- Try using Chrome or Firefox
- Check if video is in MP4 format (most compatible)

---

## File Structure

```
your-folder/
├── app.py                  # Main Flask application
├── requirements.txt        # Python packages
├── README.md              # Full documentation
├── QUICKSTART.md          # This file
├── setup.sh               # Mac/Linux setup
├── setup.bat              # Windows setup
├── run.bat                # Windows run script
└── templates/
    └── index.html         # Web interface
```

---

## Performance Tips

- **For faster processing:** Use Global method
- **For better quality:** Use Adaptive method
- **For large videos:** Be patient! Processing time depends on video length
- **Real-time on CPU:** Works best with 480p videos

---

## Need More Help?

See the full **README.md** for:
- Detailed installation instructions
- Configuration options
- Technical details
- Development guide
- Troubleshooting

---

**Enjoy enhancing your low-light videos! 🎬✨**
