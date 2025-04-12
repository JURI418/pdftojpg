# 파일 위치: pdfproject/app.py
from flask import Flask, render_template, request, send_file
import img2pdf
from werkzeug.utils import secure_filename
import os
from io import BytesIO

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])

def convert():
    image_files = request.files.getlist('jpgFiles')

    image_streams = []
    for file in image_files:
        if file and file.filename.lower().endswith(('.jpg', '.jpeg')):
            image_streams.append(file.read())

    if not image_streams:
        return "No valid images", 400

    pdf_bytes = BytesIO()
    pdf_bytes.write(img2pdf.convert(image_streams))
    pdf_bytes.seek(0)

    return send_file(
        pdf_bytes,
        as_attachment=True,
        download_name="converted.pdf",
        mimetype='application/pdf'
    )


    # 임시 이미지 삭제
    for path in image_paths:
        os.remove(path)

    return send_file(
        pdf_bytes,
        as_attachment=True,
        download_name="converted.pdf",
        mimetype='application/pdf'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
