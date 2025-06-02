from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
from ultralytics import YOLO
import google.generativeai as genai # New import
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# --- YOLO Model Loading ---
yolo_model = None
try:
    yolo_model = YOLO('yolov8n.pt')
    logger.info('YOLO model loaded successfully.')
except Exception as e:
    logger.error(f'Error loading YOLO model: {e}')

# --- Google Generative AI (Gemini) Configuration ---
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
gemini_model = None
if GOOGLE_API_KEY:
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        gemini_model = genai.GenerativeModel('gemini-pro')
        logger.info('Google Generative AI SDK configured and model loaded.')
    except Exception as e:
        logger.error(f'Error configuring Google Generative AI SDK: {e}')
else:
    logger.warning('GOOGLE_API_KEY environment variable not set. LLM functionality will be disabled.')

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def detect_food_from_image(image_path):
    if not yolo_model:
        logger.error('YOLO model is not loaded. Cannot perform detection.')
        return None, 'YOLO model not loaded'
    try:
        results = yolo_model(image_path)
        detected_food_name = None
        highest_confidence = 0.0
        for result in results:
            if result.boxes:
                for box in result.boxes:
                    conf = box.conf.item()
                    cls_id = int(box.cls.item())
                    label = yolo_model.names[cls_id]
                    if conf > highest_confidence: # Basic selection criteria
                        highest_confidence = conf
                        detected_food_name = label
        if detected_food_name:
            logger.info(f'Detected: {detected_food_name} with confidence: {highest_confidence:.2f}')
            return detected_food_name, f'Detected {detected_food_name} with {highest_confidence:.2f} confidence'
        else:
            return None, 'No food item detected with sufficient confidence'
    except Exception as e:
        logger.error(f'Error during food detection: {e}')
        return None, f'Error during detection: {str(e)}'

def get_recipe_and_instructions(food_name):
    if not gemini_model:
        logger.warning('Gemini model not available (API key missing or configuration error).')
        return 'LLM model not available.', 'Please configure the GOOGLE_API_KEY.'
    try:
        prompt = f"""Provide a detailed recipe and step-by-step cooking instructions for '{food_name}'.
        Structure the output clearly. For example:
        Recipe for {food_name}:
        Ingredients:
        - Ingredient 1
        - Ingredient 2
        Instructions:
        1. Step 1
        2. Step 2
        """
        response = gemini_model.generate_content(prompt)
        # It's good practice to check if response.parts exists and has content.
        # For simplicity, directly accessing text. More robust parsing might be needed for complex outputs.
        if response.parts:
            recipe_text = response.text
        else: # Fallback if structure is unexpected
            recipe_text = 'Could not retrieve detailed recipe information.'
        # Simple split, assuming LLM follows format. Could be more robust.
        if 'Instructions:' in recipe_text and 'Ingredients:' in recipe_text:
            parts = recipe_text.split('Instructions:')
            recipe_part = parts[0].replace('Ingredients:', '').strip()
            instructions_part = parts[1].strip()
            return f'Ingredients:\n{recipe_part}', f'Instructions:\n{instructions_part}'
        else:
            return recipe_text, 'Could not separate recipe and instructions.'
    except Exception as e:
        logger.error(f'Error generating recipe with LLM: {e}')
        return 'Error generating recipe.', str(e)

@app.route('/')
def hello_world():
    return 'Hello, Backend with YOLO and LLM integrated!'

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        temp_image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            file.save(temp_image_path)
            logger.info(f'File saved temporarily to {temp_image_path}')
            food_name, yolo_message = detect_food_from_image(temp_image_path)

            if food_name:
                recipe, instructions = get_recipe_and_instructions(food_name)
                return jsonify({
                    'food_name': food_name,
                    'yolo_message': yolo_message,
                    'recipe': recipe,
                    'instructions': instructions
                })
            else:
                return jsonify({'error': yolo_message, 'food_name': None}), 404
        except Exception as e:
            logger.error(f'Error processing file or getting recipe: {e}')
            return jsonify({'error': f'Error processing file: {str(e)}'}), 500
        finally:
            if os.path.exists(temp_image_path):
                try:
                    os.remove(temp_image_path)
                    logger.info(f'Temporary file {temp_image_path} deleted.')
                except Exception as e:
                    logger.error(f'Error deleting temporary file {temp_image_path}: {e}')
    else:
        return jsonify({'error': 'File type not allowed'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
