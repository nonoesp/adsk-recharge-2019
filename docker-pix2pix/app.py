from flask import Flask, send_file, request, jsonify
import os
import socket
import subprocess
import base64
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():

    html = "<h3>Hello {name}!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>"
    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname())

@app.route("/pix")
def pix():
    modelDir = "./170330_pix-05-edges2daisies-200e--model_export"
    inputFile = "flower-in.png"
    outputFile = "flower-out.png"
    subprocess.call([
        'python',
        'pix2pix-tensorflow/server/tools/process-local.py',
		'--model_dir',
		modelDir,
		'--input_file',
		inputFile,
		'--output_file',
		outputFile
    ]) # Just run the program

    return send_file("./"+outputFile, mimetype='image/png')

@app.route("/pix64", methods=['GET', 'POST'])
def pix64():

    # pix2pix args
    modelDir = "./170330_pix-05-edges2daisies-200e--model_export"
    inputFile = "input.png"
    outputFile = "output.png"

    if request.method == 'POST':

        # decode base64 image to file
        input_base64 = request.form['photo']  
        input_data = base64.b64decode(input_base64)
        fh = open(inputFile, "wb")
        fh.write(input_data)
        fh.close()

        # process input photo with pix2pix
        subprocess.call([
            'python',
            'pix2pix-tensorflow/server/tools/process-local.py',
            '--model_dir',
            modelDir,
            '--input_file',
            inputFile,
            '--output_file',
            outputFile
        ])

        # encode pix2pix output photo to base64
        output_data = open(outputFile, "r").read()
        output_base64 = base64.b64encode(output_data)

        return output_base64

    else:
        return "you should POST"

@app.route("/get", methods=['GET', 'POST'])
def get():

    if request.method == 'GET':

        # decode base64 image to file
        input_base64 = request.args.get('photo')
        return input_base64

        # return output_base64

    else:
        return "you should GET"

@app.route("/pix64get", methods=['GET', 'POST'])
def pix64get():

    # pix2pix args
    modelDir = "./170330_pix-05-edges2daisies-200e--model_export"
    inputFile = "input.png"
    outputFile = "output.png"

    if request.method == 'GET':

        # decode base64 image to file
        input_base64 = request.args.get('photo')
        input_data = base64.b64decode(input_base64)
        fh = open(inputFile, "wb")
        fh.write(input_data)
        fh.close()

        # process input photo with pix2pix
        subprocess.call([
            'python',
            'pix2pix-tensorflow/server/tools/process-local.py',
            '--model_dir',
            modelDir,
            '--input_file',
            inputFile,
            '--output_file',
            outputFile
        ])

        # encode pix2pix output photo to base64
        output_data = open(outputFile, "r").read()
        output_base64 = base64.b64encode(output_data)

        return output_base64

    else:
        return "you should GET"

@app.route("/pix64json", methods=['GET', 'POST'])
def pix64json():

    # pix2pix args
    modelDir = "./170330_pix-05-edges2daisies-200e--model_export"
    inputFile = "input.png"
    outputFile = "output.png"

    if request.method == 'POST':

        #return request.json;

        # decode base64 image to file
        input_base64 = request.json # ['contentImage']  
        input_data = base64.b64decode(input_base64)
        fh = open(inputFile, "wb")
        fh.write(input_data)
        fh.close()

        # process input photo with pix2pix
        subprocess.call([
            'python',
            'pix2pix-tensorflow/server/tools/process-local.py',
            '--model_dir',
            modelDir,
            '--input_file',
            inputFile,
            '--output_file',
            outputFile
        ])

        # encode pix2pix output photo to base64
        output_data = open(outputFile, "r").read()
        output_base64 = base64.b64encode(output_data)

        return output_base64
        return jsonify(stylizedImage=output_base64)

    else:
        return "you should post"

@app.route("/output")
def output():
    return send_file("./output.png", mimetype='image/png')

@app.route('/serialize', methods=['GET', 'POST'])
def serialize():
    if request.method == 'POST':
        image = request.files['image']  
        image_string = base64.b64encode(image.read())
        return image_string
    else:
        return "you should post"

@app.route('/deserialize', methods=['GET', 'POST'])
def deserialize():
    if request.method == 'POST':
        image_base64 = request.form['image']  
        image_data = base64.b64decode(image_base64)
        fh = open("output.png", "wb")
        fh.write(image_data)
        fh.close()
        return "saved at output.png"
        # return send_file(image, mimetype='image/png')
    else:
        return "you should post"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
