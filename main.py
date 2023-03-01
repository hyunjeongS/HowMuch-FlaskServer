from flask import Flask, request, jsonify, render_template
import subprocess


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
dic = {'chair': '의자', 'sofa': '소파', 'table': '식탁', 'vacuum cleaner': '청소기', '' : '측정실패'}
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload')
def upload_file():
     return render_template('upload.html')

@app.route('/uploader', methods = ['POST'])
def uploader_file():
    if request.method == 'POST':
        file = request.files.get('file')
        if file is None or file.filename=="":
            return jsonify({'error': 'no file'})
        if not allowed_file(file.filename):
            return jsonify({'error': 'format not supported'})
        try:

            file.save("./image/" + file.filename)
            val_path = "./image/" + file.filename
            result = subprocess.run(
                "python ./yolov5/detect.py --weights ./yolov5/runs/train/gun_yolov5s_results/weights/best4.pt --img 416 --conf 0.3 --source " + val_path,
                stdout=subprocess.PIPE, text=True)
            return (result.stdout.strip("\n"))
            #return jsonify({'name': result.stdout.strip('\n')})

        except:
            return jsonify({'error': 'error during prediction'})

@app.route('/image', methods = ['POST'])
def getimage():
    if request.method == 'POST':
        file = request.files.get('file')
        if file is None or file.filename=="":
            return jsonify({'error': 'no file'})
        if not allowed_file(file.filename):
            return jsonify({'error': 'format not supported'})
        try:
            file.save("./image/" + file.filename)
            val_path = "./image/" + file.filename
            result = subprocess.run(
                "python ./yolov5/detect.py --weights ./yolov5/runs/train/gun_yolov5s_results/weights/best4.pt --img 416 --conf 0.3 --source " + val_path,
                stdout=subprocess.PIPE, text=True)
            print(result.stdout)
            # return (result.stdout.strip("\n"))
            return jsonify({'name': dic[result.stdout.strip("\n")]})

        except:
            return jsonify({'error': 'error during prediction'})


if __name__ == '__main__': #서버실행
    app.run('0.0.0.0', port=5000, debug = True)