# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('random_forest_classification_model.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('Index.html')


#standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    PaymentMethod_Mailed_check=0
    PaymentMethod_Credit_card_automatic=0      
    InternetService_Fiber_No=0
    Contract_One_Year=0
    if request.method == 'POST':
        tenure = int(request.form['tenure'])
        Total_Charges=int(request.form['TotalCharges'])
        Monthly_Charges=int(request.form['MonthlyCharges'])
        PaymentMethod_Electronic_check=request.form['PaymentMethod_Electronic_check']
        if(PaymentMethod_Electronic_check=='Electronic_check'):
                PaymentMethod_Electronic_check=1
                PaymentMethod_Mailed_check=0
                PaymentMethod_Credit_card_automatic=0            
        elif(PaymentMethod_Electronic_check=='Mailed_check'):
                PaymentMethod_Electronic_check=0
                PaymentMethod_Mailed_check=1
                PaymentMethod_Credit_card_automatic=0 
        elif(PaymentMethod_Electronic_check=='Credit_card_automatic'):
                PaymentMethod_Electronic_check=0
                PaymentMethod_Mailed_check=0
                PaymentMethod_Credit_card_automatic=1
        else:
                PaymentMethod_Electronic_check=0
                PaymentMethod_Mailed_check=0
                PaymentMethod_Credit_card_automatic=0
        Contract_Two_Year=request.form['Contract_Two_year']
        if(Contract_Two_Year=='Two_year'):
            Contract_Two_Year=1
            Contract_One_Year=0
        elif(Contract_Two_Year=='One_year'):
            Contract_Two_Year=0
            Contract_One_Year=1
        else:
            Contract_Two_Year=0
            Contract_One_Year=0
        InternetService_Fiber_Optic=request.form['InternetService_Fiber_optic']
        if(InternetService_Fiber_Optic=='Fiber_optic'):
            InternetService_Fiber_Optic=1
            InternetService_Fiber_No=0
        elif(InternetService_Fiber_Optic=='No'):
            InternetService_Fiber_Optic=0
            InternetService_Fiber_No=1
        else:
            InternetService_Fiber_Optic=0
            InternetService_Fiber_No=0
        prediction=model.predict([[Total_Charges,tenure,Monthly_Charges,Contract_One_Year,Contract_Two_Year,InternetService_Fiber_Optic,InternetService_Fiber_No,PaymentMethod_Credit_card_automatic,PaymentMethod_Electronic_check,PaymentMethod_Mailed_check]])
        output=prediction[0]
        if (output==0):
            return render_template('Index.html',prediction_text="The customer would not churn")
        else:
            return render_template('Index.html',prediction_text="The customer is about to leave. Please connect and take corrective measures.")
    else:
        return render_template('Index.html')

if __name__=="__main__":
    app.run(debug=True)

