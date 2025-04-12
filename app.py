# app.py
import os
from flask import Flask, render_template, request, send_file
from pdf2image import convert_from_path
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['CONVERTED_FOLDER'] = 'converted'

# 폴더가 없다면 생성
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['CONVERTED_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_pdf():
    if 'pdf_file' not in request.files:
        return "No file uploaded", 400

    file = request.files['pdf_file']
    if file.filename == '':
        return "No selected file", 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        # 첫 페이지만 변환 (full list: convert_from_path(filepath))
        images = convert_from_path(filepath, dpi=200, first_page=1, last_page=1)
        img_path = os.path.join(app.config['CONVERTED_FOLDER'], 'converted.jpg')
        images[0].save(img_path, 'JPEG')

        return send_file(img_path, as_attachment=True)
    except Exception as e:
        return f"변환 중 오류 발생: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
