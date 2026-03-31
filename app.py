from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import subprocess
import os
import re
from werkzeug.utils import secure_filename
import logging
import time

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# Allowed languages
ALLOWED_EXTENSIONS = {'c', 'cpp', 'cc', 'cxx', 'py', 'java'}

# Tokenizers for each language
TOKENIZER_PATH = "./tokenizer"

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Check file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Detect programming language
def detect_language(filename):
    ext = filename.rsplit('.', 1)[1].lower()

    if ext == 'c':
        return 'c'
    elif ext in ['cpp', 'cc', 'cxx']:
        return 'cpp'
    elif ext == 'py':
        return 'python'
    elif ext == 'java':
        return 'java'
    else:
        return None


# Parse tokenizer output
def parse_tokenizer_output(output):
    try:
        tokens1_match = re.search(r'Total Tokens File1:\s*(\d+)', output)
        tokens2_match = re.search(r'Total Tokens File2:\s*(\d+)', output)
        matching_match = re.search(r'Matching Tokens:\s*(\d+)', output)
        similarity_match = re.search(r'Token Similarity:\s*([\d.]+)%', output)

        if all([tokens1_match, tokens2_match, matching_match, similarity_match]):
            return {
                'tokens1': int(tokens1_match.group(1)),
                'tokens2': int(tokens2_match.group(1)),
                'matching': int(matching_match.group(1)),
                'similarity': float(similarity_match.group(1))
            }
        else:
            return None

    except Exception as e:
        logger.error(e)
        return None


# Check tokenizer availability
def check_tokenizer(tokenizer_path):
    if not os.path.exists(tokenizer_path):
        return False
    if not os.access(tokenizer_path, os.X_OK):
        return False
    return True


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/analyze', methods=['POST'])
def analyze():

    if 'file1' not in request.files or 'file2' not in request.files:
        return jsonify({'error': 'Both files required'}), 400

    file1 = request.files['file1']
    file2 = request.files['file2']

    if file1.filename == '' or file2.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not (allowed_file(file1.filename) and allowed_file(file2.filename)):
        return jsonify({'error': 'Unsupported file type'}), 400

    filepath1 = None
    filepath2 = None

    try:

        filename1 = secure_filename(file1.filename)
        filename2 = secure_filename(file2.filename)

        timestamp = str(int(time.time()))

        filename1 = f"{timestamp}_{filename1}"
        filename2 = f"{timestamp}_{filename2}"

        filepath1 = os.path.join(app.config['UPLOAD_FOLDER'], filename1)
        filepath2 = os.path.join(app.config['UPLOAD_FOLDER'], filename2)

        file1.save(filepath1)
        file2.save(filepath2)

        logger.info(f"Saved {filepath1} and {filepath2}")

        # Detect language
        lang1 = detect_language(filename1)
        lang2 = detect_language(filename2)

        if lang1 != lang2:
            return jsonify({'error': 'Both files must be same language'}), 400

        tokenizer_path = TOKENIZER_PATH

        if not check_tokenizer(tokenizer_path):
            return jsonify({'error': f'Tokenizer missing for {lang1}'}), 500

        # Run tokenizer
        result = subprocess.run(
            [tokenizer_path, filepath1, filepath2],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            return jsonify({'error': result.stderr}), 500

        parsed_data = parse_tokenizer_output(result.stdout)

        if parsed_data is None:
            return jsonify({'error': 'Tokenizer output parsing failed'}), 500

        return jsonify(parsed_data)

    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Analysis timeout'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:

        # Cleanup
        for path in [filepath1, filepath2]:
            if path and os.path.exists(path):
                os.remove(path)


@app.route('/api/health')
def health():

    status = {}

    for lang, tokenizer in TOKENIZERS.items():
        status[lang] = check_tokenizer(tokenizer)

    return jsonify({
        "server": "running",
        "tokenizers": status
    })


@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'File too large (max 16MB)'}), 413


if __name__ == '__main__':

    logger.info("Server starting at http://localhost:5000")

    app.run(debug=True, host='0.0.0.0', port=5000)