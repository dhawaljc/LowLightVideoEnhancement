from flask import Flask, render_template, request, jsonify, send_file, url_for
from werkzeug.utils import secure_filename
import cv2
import numpy as np
from pathlib import Path
import os
import time
import json
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mov', 'mkv'}

# Create directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
os.makedirs('static', exist_ok=True)


class VideoQualityAnalyzer:
    """Analyze video quality metrics"""
    
    @staticmethod
    def calculate_brightness(frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return float(np.mean(gray))
    
    @staticmethod
    def calculate_contrast(frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return float(np.std(gray))
    
    @staticmethod
    def calculate_sharpness(frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        return float(laplacian.var())


class AdaptiveEnhancer:
    """Method 1: Adaptive enhancement with detection"""
    
    def __init__(self, strength=2.0, threshold=0.4, blur_size=15):
        self.strength = strength
        self.threshold = threshold
        self.blur_size = blur_size if blur_size % 2 == 1 else blur_size + 1
        self.lut = self._build_gamma_lut(strength)
        self.analyzer = VideoQualityAnalyzer()
    
    def _build_gamma_lut(self, strength):
        gamma_inv = 1.0 / strength
        lut = np.array([((i / 255.0) ** gamma_inv) * 255
                        for i in range(256)]).astype(np.uint8)
        return lut
    
    def enhance(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        threshold_val = int(self.threshold * 255)
        
        # Create attention map
        attention = np.clip(255 - gray, 0, 255)
        attention = np.clip(
            (attention.astype(np.float32) - (255 - threshold_val)) * 
            (255.0 / threshold_val), 0, 255
        ).astype(np.uint8)
        
        # Blur attention map
        attention_blurred = cv2.GaussianBlur(
            attention, (self.blur_size, self.blur_size), 0
        )
        
        # Apply enhancement
        enhanced = cv2.LUT(frame, self.lut)
        
        # Blend based on attention
        alpha = (attention_blurred / 255.0).astype(np.float32)
        alpha = np.stack([alpha] * 3, axis=-1)
        
        result = (alpha * enhanced.astype(np.float32) + 
                 (1 - alpha) * frame.astype(np.float32))
        
        return np.clip(result, 0, 255).astype(np.uint8)
    
    def process_video(self, input_path, output_path, progress_callback=None):
        cap = cv2.VideoCapture(str(input_path))
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
        
        start_time = time.time()
        frame_count = 0
        metrics = []
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            enhanced = self.enhance(frame)
            out.write(enhanced)
            
            # Sample metrics every 30 frames
            if frame_count % 30 == 0:
                metrics.append(self.analyzer.calculate_brightness(enhanced))
            
            frame_count += 1
            
            if progress_callback and frame_count % 10 == 0:
                progress = (frame_count / total_frames) * 100
                progress_callback(progress)
        
        processing_time = time.time() - start_time
        
        cap.release()
        out.release()
        
        return {
            'processing_time': processing_time,
            'total_frames': frame_count,
            'fps': fps,
            'avg_brightness': np.mean(metrics) if metrics else 0
        }


class GlobalEnhancer:
    """Method 2: Global gamma correction"""
    
    def __init__(self, strength=2.0):
        self.strength = strength
        self.lut = self._build_gamma_lut(strength)
        self.analyzer = VideoQualityAnalyzer()
    
    def _build_gamma_lut(self, strength):
        gamma_inv = 1.0 / strength
        lut = np.array([((i / 255.0) ** gamma_inv) * 255
                        for i in range(256)]).astype(np.uint8)
        return lut
    
    def enhance(self, frame):
        return cv2.LUT(frame, self.lut)
    
    def process_video(self, input_path, output_path, progress_callback=None):
        cap = cv2.VideoCapture(str(input_path))
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
        
        start_time = time.time()
        frame_count = 0
        metrics = []
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            enhanced = self.enhance(frame)
            out.write(enhanced)
            
            # Sample metrics every 30 frames
            if frame_count % 30 == 0:
                metrics.append(self.analyzer.calculate_brightness(enhanced))
            
            frame_count += 1
            
            if progress_callback and frame_count % 10 == 0:
                progress = (frame_count / total_frames) * 100
                progress_callback(progress)
        
        processing_time = time.time() - start_time
        
        cap.release()
        out.release()
        
        return {
            'processing_time': processing_time,
            'total_frames': frame_count,
            'fps': fps,
            'avg_brightness': np.mean(metrics) if metrics else 0
        }


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file'}), 400
    
    file = request.files['video']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'filepath': filepath
        })
    
    return jsonify({'error': 'Invalid file type'}), 400


@app.route('/enhance', methods=['POST'])
def enhance_video():
    try:
        data = request.json
        filename = data.get('filename')
        method = data.get('method', 'adaptive')
        strength = float(data.get('strength', 2.0))
        
        print(f"\n=== ENHANCEMENT REQUEST ===")
        print(f"Filename: {filename}")
        print(f"Method: {method}")
        print(f"Strength: {strength}")
        
        if method == 'adaptive':
            threshold = float(data.get('threshold', 0.4))
            blur_size = int(data.get('blur_size', 15))
            print(f"Threshold: {threshold}")
            print(f"Blur size: {blur_size}")
        
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        print(f"Input path: {input_path}")
        print(f"Input file exists: {os.path.exists(input_path)}")
        
        if not os.path.exists(input_path):
            error_msg = f'Input file not found: {input_path}'
            print(f"ERROR: {error_msg}")
            return jsonify({'error': error_msg}), 404
        
        # Generate output filename
        base_name = os.path.splitext(filename)[0]
        output_filename = f"{base_name}_{method}_enhanced.mp4"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        print(f"Output path: {output_path}")
        
        try:
            print(f"Starting {method} enhancement...")
            
            if method == 'adaptive':
                enhancer = AdaptiveEnhancer(
                    strength=strength,
                    threshold=threshold,
                    blur_size=blur_size
                )
            else:  # global
                enhancer = GlobalEnhancer(strength=strength)
            
            print("Enhancer created successfully")
            print("Processing video...")
            
            stats = enhancer.process_video(input_path, output_path)
            
            print("Video processing completed!")
            print(f"Stats: {stats}")
            print(f"Output file exists: {os.path.exists(output_path)}")
            if os.path.exists(output_path):
                print(f"Output file size: {os.path.getsize(output_path)} bytes")
            
            return jsonify({
                'success': True,
                'output_filename': output_filename,
                'download_url': url_for('download_video', filename=output_filename),
                'stats': stats
            })
        
        except Exception as e:
            error_msg = f'Error during video processing: {str(e)}'
            print(f"\nERROR: {error_msg}")
            import traceback
            traceback.print_exc()
            return jsonify({'error': error_msg, 'details': traceback.format_exc()}), 500
    
    except Exception as e:
        error_msg = f'Error in enhance endpoint: {str(e)}'
        print(f"\nERROR: {error_msg}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': error_msg, 'details': traceback.format_exc()}), 500


@app.route('/download/<filename>')
def download_video(filename):
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    if os.path.exists(output_path):
        return send_file(output_path, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404


@app.route('/preview/<filename>')
def preview_video(filename):
    try:
        video_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        print(f"=== ENHANCED VIDEO DEBUG ===")
        print(f"Requested filename: {filename}")
        print(f"Full path: {video_path}")
        print(f"File exists: {os.path.exists(video_path)}")
        if os.path.exists(video_path):
            print(f"File size: {os.path.getsize(video_path)} bytes")
            # List all files in output folder
            print(f"Files in output folder: {os.listdir(app.config['OUTPUT_FOLDER'])}")
        
        if os.path.exists(video_path):
            ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else 'mp4'
            mime_types = {
                'mp4': 'video/mp4',
                'avi': 'video/x-msvideo',
                'mov': 'video/quicktime',
                'mkv': 'video/x-matroska'
            }
            mime_type = mime_types.get(ext, 'video/mp4')
            print(f"Serving with MIME type: {mime_type}")
            return send_file(video_path, mimetype=mime_type, as_attachment=False)
        else:
            print(f"ERROR: File not found!")
            return jsonify({'error': 'File not found', 'path': video_path}), 404
    except Exception as e:
        print(f"ERROR serving video: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/preview/uploads/<filename>')
def preview_upload(filename):
    try:
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print(f"=== ORIGINAL VIDEO DEBUG ===")
        print(f"Requested filename: {filename}")
        print(f"Full path: {video_path}")
        print(f"File exists: {os.path.exists(video_path)}")
        if os.path.exists(video_path):
            print(f"File size: {os.path.getsize(video_path)} bytes")
            # List all files in upload folder
            print(f"Files in upload folder: {os.listdir(app.config['UPLOAD_FOLDER'])}")
        
        if os.path.exists(video_path):
            ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else 'mp4'
            mime_types = {
                'mp4': 'video/mp4',
                'avi': 'video/x-msvideo',
                'mov': 'video/quicktime',
                'mkv': 'video/x-matroska'
            }
            mime_type = mime_types.get(ext, 'video/mp4')
            print(f"Serving with MIME type: {mime_type}")
            return send_file(video_path, mimetype=mime_type, as_attachment=False)
        else:
            print(f"ERROR: File not found!")
            return jsonify({'error': 'File not found', 'path': video_path}), 404
    except Exception as e:
        print(f"ERROR serving video: {str(e)}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)