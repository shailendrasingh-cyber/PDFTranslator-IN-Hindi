from flask import Flask, render_template, request, jsonify
import PyPDF2
from googletrans import Translator
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

    # Read the PDF content
    pdf_content = extract_text_from_pdf(pdf_file)

    # Translate the content
    translated_content = translate_text(pdf_content)

    return render_template('result.html', translated_content=translated_content)

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)
    text = ""
    for page_num in range(pdf_reader.getNumPages()):
        text += pdf_reader.getPage(page_num).extractText()

    return text


def translate_text(text):
    translator = Translator()
    translated_text = translator.translate(text, dest='hi').text
    return translated_text

if __name__ == '__main__':
    app.run(debug=True)