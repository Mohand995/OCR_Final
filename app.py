from flask import Flask, request, redirect, url_for, send_from_directory, render_template
from National_ID import  Run
import os
from werkzeug.utils import secure_filename
#import preprocessing

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
        filename = secure_filename(img.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        img.save(file_path)
        #img=preprocessing.extractIdCard(img_path)
        N,I = Run(file_path)

    return render_template("index.html", id=I, name=N)


if __name__=='__main__':
    app.run(debug=True)