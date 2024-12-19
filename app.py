from flask import Flask, render_template, request, flash
from response2 import generate_classification
from detect_text import detect_text
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'  # Store images in the static directory
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the uploads directory exists
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')  # Set a secret key for flashing messages

@app.route('/', methods=['GET', 'POST'])
def index():
    detected_text = None
    response = None
    file = None

    if request.method == 'POST':
        # Handle file upload
        if 'file' not in request.files:
            flash("No file part in the request.")
            return render_template('index.html', detected_text=detected_text, response=response)

        file = request.files['file']

        if file.filename == '':
            flash("No file selected. Please choose a file to upload.")
            return render_template('index.html', detected_text=detected_text, response=response)

        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            try:
                # Detect text using your method (e.g., AWS Textract or Tesseract)
                detected_text = detect_text(file_path)

                # Generate response based on detected text
                response = generate_classification(detected_text)

            except Exception as e:
                flash(f"An error occurred: {str(e)}")

    return render_template('index3.html', detected_text=detected_text, response=response, file=file)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
