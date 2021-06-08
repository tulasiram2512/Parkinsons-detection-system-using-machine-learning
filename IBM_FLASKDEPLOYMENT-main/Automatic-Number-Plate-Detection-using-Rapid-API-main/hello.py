# -*- coding: utf-8 -*-
#importing the libraries
#import flask library 
from flask import Flask, request, render_template
from gevent.pywsgi import WSGIServer
import os




#import request library
import requests

#Defining the app
app = Flask(__name__)

#Defining the Output Function
def check(output):

    url = "https://zyanyatech1-license-plate-recognition-v1.p.rapidapi.com/recognize_url"
    
    querystring = {"image_url":output,"sourceType":"url"}
    
    payload = '''{\r\n    \"image_url\": "'''+output+'''" ,\r\n    \"sourceType\": \"url\"\r\n}'''
    headers = {
    'x-rapidapi-key': "zBFryjZkgMEw-Yq1GkWFJTkxzpbCrW8WbEkBvIwSYaWZ", #Add your API 
    'x-rapidapi-host': "zyanyatech1-license-plate-recognition-v1.p.rapidapi.com"
    }
    
    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    print(response.text) 
    return response.json()["results"][0]["plate"],response.json()["results"][0]["confidence"]
    
 
#Routing the html page
#home page
@app.route('/')
def home():
    return render_template('base.html')

#Define Predict function
@app.route('/predict',methods=['POST'])
def predict():
    output=request.form['output']
    plate,conf=check(output)
    return render_template('base.html',output=plate+" with confidence score: "+str(round(conf))+"%")

port = os.getenv('VCAP_APP_PORT', '8080')

    
if __name__ == "__main__":
    
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=port)
