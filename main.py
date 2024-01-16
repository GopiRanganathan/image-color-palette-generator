import os
from flask import Flask, flash, request, redirect, url_for, render_template
# from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np
import random
from io import BytesIO
from base64 import b64encode


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'} 
current_directory = os.getcwd()
UPLOAD_FOLDER = os.path.join(current_directory, 'static/upload/')
app = Flask(__name__)
app.secret_key="ahoifdiehjfijedfj"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def rgb_to_hex(rgb):
    """Convert RGB to hex code."""
    return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])

def calculate_intensity(color):
    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:7], 16)
    return (r + g + b) / 3

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/',  methods=['GET', 'POST'])
def home():
    colors=[]
    img_base64=None
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part','danger')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
        img_data = file.read()
        image = Image.open(BytesIO(img_data))
        image_array = np.array(image)
        array_x=image_array.shape[0]
        array_y=image_array.shape[1]
        while len(colors)<=10:
            color=image_array[random.randint(0,array_x)][random.randint(0,array_y)]
            hex=rgb_to_hex(color)
            if hex not in colors:
                colors.append(hex)
            print(colors)
        img_data = BytesIO()
        image.save(img_data, format='JPEG')
        img_base64 = b64encode(img_data.getvalue()).decode('utf-8') 
    return render_template('index.html', image=img_base64, colors=colors, intensity=calculate_intensity)


if __name__ == "__main__":
    app.run(debug=True)
