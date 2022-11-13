from flask import Flask, request, redirect, url_for, send_from_directory, render_template
from National_ID import  Run
import os
from werkzeug.utils import secure_filename
import json

UPLOAD_FOLDER = 'uploads'



app=Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/',methods=['GET'])
def hello_world():
    return render_template("index.html")

@app.route('/submit',methods=['POST'])
def predict():
    if request.method == 'POST':
        img = request.files['my_image']
        file_path = os.path.join('uploads/' ,img.filename)
        img.save(file_path)
        result= Run(file_path,api=False)
        os.remove(file_path)
    return render_template("index.html", id=result['ID'], name=result['name'],DOB=result['DOB'],no=result['Eng_Code'])


@app.route('/submit_api',methods=['POST'])
def predict_api():
    data=request.json
    img_path=data['url']
    if request.method == 'POST':
        result= Run(img_path)
        result_json=json.dumps(result,ensure_ascii=False)

    return result_json


if __name__=='__main__':
    app.run()
