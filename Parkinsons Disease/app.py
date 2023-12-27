from urllib import request
from flask import *
from flask import render_template
from flask import jsonify
import pickle
import numpy as np
load_model_DT=pickle.load(open('static/Sav_Models/DT_model.sav','rb'))
load_model_KNN=pickle.load(open('static/Sav_Models/knn.sav','rb'))
load_model_RF=pickle.load(open('static/Sav_Models/RF_model.sav','rb'))
load_model_XG=pickle.load(open('static/Sav_Models/GB_model.sav','rb'))

#import and models for spiral
import matplotlib.pyplot as plt
from keras.utils import load_img, img_to_array
from keras.preprocessing import image
from keras.models import load_model
model = load_model('spiral_modelfinal.h5') # load the trained model from a file
#end of import models and spiral
import os
from flask_mail import Mail
from flask_mail import Message
#mail config
os.environ['API_USER']=''
os.environ['API_PASSWORD']=''

app= Flask(__name__)

#mail initiate
app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = os.environ.get('API_USER')
app.config["MAIL_PASSWORD"] = os.environ.get('API_PASSWORD')


mail = Mail(app)

@app.route('/')
def home():
    return render_template("index.html")
@app.route('/select')
def select():
    return render_template("service.html")
@app.route('/data')
def prediction_data():
    return render_template("prediction-data-entry.html")

@app.route('/predict',methods=['POST'])
def predict():
        name = request.form['name']
        email = request.form['email']
        MDVP_Fo = float(request.form['MDVP_Fo'])
        MDVP_Fhi = float(request.form['MDVP_Fhi'])
        MDVP_Flo = float(request.form['MDVP_Flo'])
        mdvp_jitter_percent = float(request.form['mdvp_jitter_percent'])
        mdvp_jitter_abs = float(request.form['mdvp_jitter_abs'])
        mdvp_rap = float(request.form['mdvp_rap'])
        mdvp_ppq = float(request.form['mdvp_ppq'])
        jitter_ddp = float(request.form['jitter_ddp'])
        jitter_ddp = float(request.form['mdvp_shimmer'])
        mdvp_shimmer_db = float(request.form['mdvp_shimmer_db'])
        shimmer_apq3 = float(request.form['shimmer_apq3'])
        shimmer_apq5 = float(request.form['shimmer_apq5'])
        mdvp_apq = float(request.form['mdvp_apq'])
        shimmer_dda = float(request.form['shimmer_dda'])
        nhr = float(request.form['nhr'])
        hnr = float(request.form['hnr'])
        rped=float(request.form['rped'])
        dfa=float(request.form['dfa'])
        spread1=float(request.form['spread1'])
        spread2=float(request.form['spread2'])
        df=float(request.form['df'])
        ppe=float(request.form['ppe'])

        input_data = (MDVP_Fo,MDVP_Fhi,MDVP_Flo,mdvp_jitter_percent,mdvp_jitter_abs,mdvp_rap,mdvp_ppq,jitter_ddp,jitter_ddp,mdvp_shimmer_db,shimmer_apq3,shimmer_apq5,mdvp_apq,shimmer_dda,nhr,hnr,rped,dfa,spread1,spread2,df,ppe)
        print(input_data)
        # changing input data to a numpy array
        input_data_as_numpy_array = np.asarray(input_data)

        # reshape the numpy array
        input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

        # standardize the data
        #std_data = scaler.transform(input_data_reshaped)
        print(name)
        print(email)
        prediction_DT = load_model_DT.predict(input_data_reshaped)
        print(prediction_DT)
        prediction_KNN = load_model_KNN.predict(input_data_reshaped)
        print(prediction_KNN)
        prediction_RF = load_model_RF.predict(input_data_reshaped)
        print(prediction_RF)
        prediction_XG = load_model_XG.predict(input_data_reshaped)
        print(prediction_XG)          
        total = ((prediction_DT+prediction_KNN+prediction_RF+prediction_XG)/4)*100
        if total>=0 and total<=25:
             ps="According to the prediction results you don’t have parkinson disease"
             msg="According to the prediction results you don’t have parkinson disease"
             print("According to the prediction results you don’t have parkinson disease")
        elif total>25 and total<75:
             ps="According to the prediction results you are likely to have Parkinson’s disease.\nContact your doctor as soon as possible"
             msg="According to the prediction results you are likely to have Parkinson’s disease.\nContact your doctor as soon as possible"
             print("According to the prediction results you are likely to have Parkinson’s disease.\nContact your doctor as soon as possible")
        elif total>=75 and total<=100:
             ps="According to the prediction results you have parkinson disease.\nContact your doctor immediately."
             msg="According to the prediction results you have parkinson disease.\nContact your doctor immediately."
             print("According to the prediction results you have parkinson disease.\nContact your doctor immediately.")
     #mailers code
        subject = "Parkinson's Disease Prediction Report"
        emails=[]
        emails.append(email)
        names=[]
        names.append(name)
        result=[]
        result.append(msg)
        sendEmail(recipientsArr=emails,subject=subject,msgBody="<html><body><br>Dear %s,  %s<br>Thank you, <br><br> With Regards, <br>PMDL Team  </body></html>" %(names[0],result[0]))
        return render_template('results.html',resultsofprediction=ps)

#send mail code function
def sendEmail(recipientsArr,subject,msgBody):
    try:
        msg = Message(subject, sender='4jn19cs091shreyasadiga@gmail.com',recipients=recipientsArr)
        msg.body = msgBody
        msg.html = msgBody
        mail.send(msg)
        return 1
    except:
        return 0
#spiral one codes
@app.route('/spiral-file-upload')    
def spiral_data():
     return render_template('prediction-spiral-upload.html')
# #file upload for spirals
@app.route('/image-uploads',methods=['GET','POST'])
def image_upload_file():
     file = request.files['file']
     filename = file.filename
     file.save('static/uploads-data/spiral-images/' + filename)
     img_path = 'static/uploads-data/spiral-images/'+filename
     name = request.form['name']
     email = request.form['email']
     # print(img_path)
     img = load_img(img_path, target_size=(128, 128))
     img_array = img_to_array(img)
     img_array = np.expand_dims(img_array, axis=0)
     img_array /= 255.

     # make a prediction using the model
     prediction = model.predict(img_array)

     if prediction < 0.5:
          result = "According to the prediction results you don’t have parkinson disease."
          s="According to the prediction results you don’t have parkinson disease."
          print("According to the prediction results you don’t have parkinson disease.")
     else:
          result = "According to the prediction results you have parkinson disease.\nContact your doctor as soon as possible"
          s="According to the prediction results you have parkinson disease.\nContact your doctor as soon as possible"
          print("According to the prediction results you have parkinson disease.\nContact your doctor as soon as possible")

     #mailers code
     subject = "Parkinson's Disease Prediction Report"
     emails=[]
     emails.append(email)
     names=[]
     names.append(name)
     results=[]
     results.append(s)
     sendEmail(recipientsArr=emails,subject=subject,msgBody="<html><body><br>Dear %s,  %s <br>Thank you, <br><br> With Regards, <br>PMDL Team  </body></html>" %(name[0],results[0]))
     return render_template('spiral-results.html',result=result)


#File Upload Codes for Voice 
@app.route('/voice-file-upload')
def voice_data():
    return render_template('voice-file-upload.html')

@app.route('/voice-uploads',methods=['GET','POST'])
def upload_file():
     file = request.files['file']
     filename = file.filename
     file.save('static/uploads-data/voice/' + filename)
     return 'File uploaded successfully!'

#404 error code
@app.errorhandler(404)
def not_found_error(error):
    return '404.html'

if __name__ =='__main__':
<<<<<<< HEAD
    app.run(host='0.0.0.0', port=3000,debug = True)
    
=======
    app.run(host='0.0.0.0', port=5000,debug = True)
    
>>>>>>> 60d760609708a9db7103649acd9f53b5bdb9e0be
