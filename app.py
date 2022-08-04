
from random import randrange
from flask import Flask, render_template
from flask_restful import Resource, Api
from flask import request
import pandas as pd
import os
from cryptography.fernet import Fernet

from flask_cors import CORS, cross_origin

app = Flask(__name__)
api = Api(app)

cors = CORS(app, resources={r"*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/foo', methods=['POST','OPTIONS'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def foo():
    return request.json['inputVar']


data = pd.read_excel("data.xlsx")

class Users(Resource):
    def get(self):
        query_parameters = request.args

        INN = query_parameters.get('INN')
        hist = query_parameters.get('hist')
        score = query_parameters.get('score')
        print("score:", score)
        flag = 0
        for i in range(0, len(data['ИНН'])):
            if str(data['ИНН'][i]) == INN:
                s = str(data['Сумма выдачи номинал'][i]) 
                s = s + ","+ str(data['Дата выдачи'][i])
                s = s + ", " + str(data['Дата окончание срока'][i])
                s = s + "," + str(data['Просрочки за цикл (кумулятивный)'][i])
                flag = 1
        if flag == 0:
            return "ERROR"
        if score == "true":
            s = s + ',' + str(randrange(50, 100))
        return s

#b'3nCDoFY680OghKyBykxny2SIsdD-My20JhzcnilIark='
#867924025

                 
        
class Locations(Resource):
    # methods go here
    pass
    
api.add_resource(Users, '/users')  # '/users' is our entry point for Users
api.add_resource(Locations, '/locations')  # and '/locations' is our entry point for Locations

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
