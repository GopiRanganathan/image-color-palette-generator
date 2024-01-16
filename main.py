import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np
import random


UPLOAD_FOLDER = 'static/upload/'  # Corrected path
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # Added quotes

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def rgb_to_hex(rgb):
    """Convert RGB to hex code."""
    return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])

def calculate_intensity(color):
    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:7], 16)

    return (r + g + b) / 3


@app.route('/')
def home():
    filename= request.args.get('filename')
    print(filename)
    colors=[]

    if filename:
        image = Image.open(UPLOAD_FOLDER+filename)
        image_array = np.array(image)
        array_x=image_array.shape[0]
        array_y=image_array.shape[1]
        while len(colors)<=10:
            color=image_array[random.randint(0,array_x)][random.randint(0,array_y)]
            hex=rgb_to_hex(color)
            if hex not in colors:
                colors.append(hex)
    return render_template('index.html', image=filename, colors=colors, intensity=calculate_intensity)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('home', filename=filename))


if __name__ == "__main__":
    app.run(debug=False)
