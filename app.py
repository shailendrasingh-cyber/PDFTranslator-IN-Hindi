from flask import Flask, render_template, request
import fitz  # PyMuPDF
from googletrans import Translator
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    # Check if the POST request has the file part
    if 'pdf_file' not in request.files:
        return render_template('index.html', error='No file part')

    pdf_file = request.files['pdf_file']

    # If the user does not select a file, submit an empty part without filename
    if pdf_file.filename == '':
        return render_template('index.html', error='No selected file')

    # Save the uploaded file to a temporary location
    upload_folder = 'uploads'
    os.makedirs(upload_folder, exist_ok=True)
    file_path = os.path.join(upload_folder, pdf_file.filename)
    pdf_file.save(file_path)

    # Read the PDF content
    pdf_content = extract_text_from_pdf(file_path)

    # Translate the content
    translated_content = translate_text(pdf_content)

    # Delete the temporary file
    os.remove(file_path)

    return render_template('result.html', translated_content=translated_content)

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(doc.page_count):
        page = doc[page_num]
        text += page.get_text()
    return text

def translate_text(text):
    translator = Translator()
    translated_text = translator.translate(text, dest='hi').text
    return translated_text

if __name__ == '__main__':
    app.run(debug=True)
