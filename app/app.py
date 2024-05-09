from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from PIL import Image
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resize', methods=['POST'])
def resize():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file:
        # Save the uploaded file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Get the desired size from the form
        target_size = int(request.form['size'])

        # Resize the image
        img = Image.open(file_path)
        img_resized = img.resize((target_size, target_size))
        img_resized.save(file_path)

        return render_template('index.html', resized=True, filename=file.filename)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory('uploads', filename)

if __name__ == '__main__':
    app.run(debug=True)
