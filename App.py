import pandas as pd
import numpy as np
from flask import Flask,redirect,url_for,request,jsonify
import joblib as jb
import pymongo
client = pymongo.MongoClient("mongodb://aravind:aravind@cluster1-shard-00-00.lkblz.mongodb.net:27017,cluster1-shard-00-01.lkblz.mongodb.net:27017,cluster1-shard-00-02.lkblz.mongodb.net:27017/alfa?ssl=true&replicaSet=atlas-3qv6aq-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.alfa
loaded_randomforest_model = jb.load("BaselineRandomForestEngine.sav")
app = Flask(__name__)
@app.route('/Home',methods=['POST','GET'])
def home():
    data = request.get_json()
    prediction_data = []
    for i in data.keys():
        prediction_data.append(data[i])
    result = str(loaded_randomforest_model.predict([prediction_data])[0])
    data['_id']=np.random.randint(1,100)
    db.project.insert_one(data)
    return jsonify({'Result':result})
client.close()
if __name__=='__main__':
    app.run(debug=True)
