from urllib import request
from flask import *
from flask import render_template
from flask import jsonify
import pickle
import numpy as np
load_model_DT=pickle.load(open('static/Sav_Models/DT_model.sav','rb'))
load_model_KNN=pickle.load(open('static/Sav_Models/KNN_model.sav','rb'))
load_model_RF=pickle.load(open('static/Sav_Models/RF_model.sav','rb'))
load_model_XG=pickle.load(open('static/Sav_Models/GB_model.sav','rb'))

app= Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")
@app.route('/select')
def select():
    return render_template("service.html")
@app.route('/data')
def pd():
    return render_template("prediction-data-entry.html")

@app.route('/predict',methods=['POST'])
def predict():
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

        # changing input data to a numpy array
        input_data_as_numpy_array = np.asarray(input_data)

        # reshape the numpy array
        input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

        # standardize the data
        #std_data = scaler.transform(input_data_reshaped)

        prediction_DT = load_model_DT.predict(input_data_reshaped)
        print(prediction_DT)
        prediction_KNN = load_model_KNN.predict(input_data_reshaped)
        print(prediction_KNN)
        prediction_RF = load_model_RF.predict(input_data_reshaped)
        print(prediction_RF)
        prediction_XG = load_model_XG.predict(input_data_reshaped)
        print(prediction_XG)
        if prediction_DT[0] == 0 and prediction_KNN[0]==0 and prediction_RF[0]==0 and prediction_XG[0]==0:
            return'KNN: no DT: no RF:no XG: no'
        elif prediction_DT[0] == 0 and prediction_KNN[0]==0 and prediction_RF[0]==0 and prediction_XG[0]==1:
             return'KNN: no DT: no RF:yes XG: yes'
        elif prediction_DT[0] == 0 and prediction_KNN[0]==0 and prediction_RF[0]==1 and prediction_XG[0]==0:
             return'KNN: no DT: no RF:yes XG: no'
        elif prediction_DT[0] == 0 and prediction_KNN[0]==0 and prediction_RF[0]==1 and prediction_XG[0]==1:
             return'KNN: no DT: no RF:yes XG: yes'
        elif prediction_DT[0] == 0 and prediction_KNN[0]==1 and prediction_RF[0]==0 and prediction_XG[0]==0:
             return'KNN: no DT: yes RF:no XG: no'
        elif prediction_DT[0] == 0 and prediction_KNN[0]==1 and prediction_RF[0]==0 and prediction_XG[0]==1:
             return'KNN: no DT: yes RF:no XG: yes'
        elif prediction_DT[0] == 0 and prediction_KNN[0]==1 and prediction_RF[0]==1 and prediction_XG[0]==0:
             return'KNN: no DT: yes RF:yes XG: no'
        elif prediction_DT[0] == 0 and prediction_KNN[0]==1 and prediction_RF[0]==1 and prediction_XG[0]==1:
             return'KNN: no DT: yes RF:yes XG: yes'
        elif prediction_DT[0] == 1 and prediction_KNN[0]==0 and prediction_RF[0]==0 and prediction_XG[0]==0:
             return'KNN: yes DT: no RF:no XG: no'
        elif prediction_DT[0] == 1 and prediction_KNN[0]==0 and prediction_RF[0]==0 and prediction_XG[0]==1:
             return'KNN: yes DT: no RF:no XG: yes'
        elif prediction_DT[0] == 1 and prediction_KNN[0]==0 and prediction_RF[0]==1 and prediction_XG[0]==0:
             return'KNN: yes DT: no RF:yes XG: no'
        elif prediction_DT[0] == 1 and prediction_KNN[0]==0 and prediction_RF[0]==1 and prediction_XG[0]==1:
             return'KNN: yes DT: no RF:yes XG: yes'
        elif prediction_DT[0] == 1 and prediction_KNN[0]==1 and prediction_RF[0]==0 and prediction_XG[0]==0:
             return'KNN: yes DT: yes RF:no XG: no'
        elif prediction_DT[0] == 1 and prediction_KNN[0]==1 and prediction_RF[0]==0 and prediction_XG[0]==1:
             return'KNN: yes DT: yes RF:no XG: yes'
        elif prediction_DT[0] == 1 and prediction_KNN[0]==1 and prediction_RF[0]==1 and prediction_XG[0]==0:
             return'KNN: yes DT: yes RF:yes XG: no'
        elif prediction_DT[0] == 1 and prediction_KNN[0]==1 and prediction_RF[0]==1 and prediction_XG[0]==1:
             result_dt="YES"
             result_knn="YES"
             result_rf="YES"
             result_xg="YES"
             #return'KNN: yes DT: yes RF:yes XG: yes'
          
        total = ((prediction_DT+prediction_KNN+prediction_RF+prediction_XG)/4)*100
        if total >50 :
             psss="Have"
        elif total<50 :
             psss="Doesn't Have"
        return render_template('results.html',knn=result_knn,dt=result_dt,rf=result_rf,xg=result_xg,psss=psss)
if __name__ =='__main__':
    app.run(host='0.0.0.0', port=5000)