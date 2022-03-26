from app import app
from flask import request, render_template, url_for
import os
import cv2
import numpy as np
from PIL import Image
import random
import string
import pytesseract
from pytesseract import Output

pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'

app.config['INITIAL_FILE_UPLOADS'] = 'app/static/uploads'

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        full_filename = 'assets/white_bg.png'
        return render_template("index.html", full_filename = full_filename)
    
    if request.method == "POST":
        image_upload = request.files['image_upload']
        imagename = image_upload.filename
        image = Image.open(image_upload)

        image_arr = np.array(image.convert('RGB'))

        gray_img_arr = cv2.cvtColor(image_arr, cv2.COLOR_BGR2GRAY)

        image = Image.fromarray(gray_img_arr)

        letters = string.ascii_lowercase
        name = ''.join(random.choice(letters) for i in range(10)) + '.png'
        full_filename = 'uploads/' + name

        img = Image.fromarray(image_arr, 'RGB')
        img.save(os.path.join(app.config['INITIAL_FILE_UPLOADS'], name))

        custom_config = r'-l eng --oem 3 --psm 6'
        text = pytesseract.image_to_string(image,config=custom_config)

        img = cv2.imread('app/static/uploads/' + name)
        h, w, c = img.shape
        boxes = pytesseract.image_to_boxes(img)
        for b in boxes.splitlines():
            b = b.split(' ')
            img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)
        
        imagesample = Image.fromarray(img)
        imagesample.save(os.path.join(app.config['INITIAL_FILE_UPLOADS'], name))

        

        return render_template('index.html', full_filename = full_filename, text = text)







if __name__ == '__main__':
    app.run(debug=False, port=8080)