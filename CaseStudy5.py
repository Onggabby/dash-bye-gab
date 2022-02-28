#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 14:40:12 2022

@author: gabrielmartinong
"""

#%%
from flask import Flask, request, jsonify
app = Flask(__name__)
import numpy as np
import pandas as pd
from sklearn import linear_model
from sklearn.linear_model import LinearRegression
from app import app, server

deltime = pd.read_csv('deliverytime.csv')
deltime.insert(1, 'id', range(1,1+len(deltime))) 
column_names = ["id", "deltime", "ncases", "distance"]

deltime = deltime.reindex(columns=column_names)

def _find_next_id():
    return max(deltime["id"]) +1
 
#data = {"deltime": 18.788, "ncases": 10, "distance": 20}
#data["id"] = 26
#desired_order_list = ["id", "deltime", "ncases", "distance"]
#data = {k: data[k] for k in desired_order_list}
#data = pd.DataFrame(data)
#data
#deltime.append(data, ignore_index=True)
#data = data.to_json() 

@app.get('/querydfs')
def querydfs():
    headers = request.headers
    auth = headers.get("api-key")
    if auth == 'mypassword':
        df = pd.read_csv('deliverytime.csv')
        
        pred1 = int(headers.get("x1"))
        pred2 = int(headers.get("x2"))
        
        x = df[['ncases', 'distance']]
        y = df['deltime']
     
        regressor=LinearRegression()
        regressor.fit(x,y)
        b0 = regressor.intercept_
        b1 = regressor.coef_[0]
        b2 = regressor.coef_[1]

        prediction = (b1*pred1) + (b2*pred2)+ b0
        regression = [{"ncases": pred1, "Distance": pred2, "Response": "deltime", "Prediction": prediction}]
        v = pd.DataFrame(regression)
        v = v.to_json()
        return jsonify(v), 200
        
    else:
        return jsonify({"message": "ERROR: Unauthorized"}), 401

@app.post("/querydfs")
def add_row():
    if request.is_json:
        data = request.get_json()
        data["id"] = _find_next_id()
        desired_order_list = ["id", "deltime", "ncases", "distance"]
        data = {k: data[k] for k in desired_order_list}
        deltime.append(data, ignore_index=True)
        #data = data.to_json()
        return data, 201
    return {"error": "Request must be JSON"}, 415


if __name__ == '__main__':
    app.run()
      
