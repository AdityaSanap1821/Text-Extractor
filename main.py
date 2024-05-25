import cv2
import numpy as np
from google.cloud import vision
import io
import os
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)

# Set the upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
TEMPLATES_FOLDER = 'templates'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TEMPLATES_FOLDER'] = TEMPLATES_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Check if file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Initialize Google Cloud Vision client
def initialize_vision_client():
    return vision.ImageAnnotatorClient()

# Analyze the image using Google Cloud Vision API
def analyze_image(client, image_path):
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    if response.error.message:
        raise Exception(f'Error during text detection: {response.error.message}')
    return response

# Extract text from the Vision API response
def extract_text(response):
    texts = response.text_annotations
    if not texts:
        return "No text found"
    
    extracted_text = texts[0].description  # The first text annotation is the entire text
    return extracted_text

# Segment the image using OpenCV
def segment_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 150)

    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    segments = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        segment = image[y:y+h, x:x+w]
        segments.append(segment)
    return segments

# Process the image
def process_image(image_path):
    client = initialize_vision_client()
    response = analyze_image(client, image_path)
    text = extract_text(response)
    segments = segment_image(image_path)
    return text, segments

# Generate HTML content
def generate_html(text, segments, output_folder):
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Extracted Content</title>
</head>
<body>
<h1>EXTRACTED TEXT:</h1>
"""
    html_content += "<p>{}</p>\n".format(text.replace("\n", "<br>"))
    html_content += """
<h1>IMAGE SEGMENT:</h1>
"""

    for i, segment in enumerate(segments):
        img_name = f'segment_{i}.png'
        img_path = os.path.join(output_folder, img_name)
        cv2.imwrite(img_path, segment)
        html_content += f'<img src="{img_path}" alt="Segment {i}"><br>\n'
    
    html_content += """</body>
</html>"""
    
    with open(os.path.join(output_folder, "output.html"), "w") as html_file:
        html_file.write(html_content)

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle file upload and processing
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Process the uploaded image
        text, segments = process_image(file_path)
        
        # Create output folder for the HTML and image segments
        output_folder = os.path.join(app.config['TEMPLATES_FOLDER'], 'output')
        os.makedirs(output_folder, exist_ok=True)
        
        # Generate the HTML content
        generate_html(text, segments, output_folder)
        
        return redirect(url_for('output',filename = 'output.html'))

    return redirect(request.url)

# Route to display the output HTML
@app.route('/templates/output/output.html')
def output():
    return render_template('output/output.html')

if __name__ == "__main__":
    # Set the path to your service account key file
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "G:/Projects/Testline Internship Assignment/green-entity-424407-t6-82bbcf05967b.json"
    app.run(debug=True)
