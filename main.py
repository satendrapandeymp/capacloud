from flask import Flask, render_template, request, jsonify
from camera import connect_cam
from test import testing
from train import training
from process_img import process
import cv2, numpy as np, time, urllib2, os, urllib2
from werkzeug import secure_filename

app = Flask(__name__ , static_url_path='/static')

app.config['UPLOAD_FOLDER'] = 'img/'

app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/add")
def add():
    return render_template('additional.html', type=" ", result=" ")

@app.route('/train', methods=['POST'])
def train():
    uploaded_files = request.files.getlist("file[]")
    name = str(request.form['name'])
    print name
    for file in uploaded_files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = "train/" + filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    process("train")
    res = training(name)
    return render_template('additional.html', result = str(res), type="train")

@app.route('/test', methods=['POST'])
def test():
    file = request.files["file"]
    if file and allowed_file(file.filename):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], "test/test.jpg"))
        process("test")
        res = testing()
    return render_template('additional.html', result = str(res), type="test")

@app.route("/stop")
def stop():
    cv2.imwrite("static/3.jpg", np.zeros((5,5)))
    return jsonify({'status':'OK'})

@app.route("/cam", methods=['POST'])
def camera():
	cam = str(request.form['ip'])
	vend = "http://" + cam + ":4747/mjpegfeed?640x480"
	connect_cam(vend)
	return jsonify({'status':'OK','answer':lol})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, processes=3, debug=True)
