#!/usr/bin/env python

# importing sys
import sys
import os
  
# adding Folder_2 to the system path
sys.path.insert(0, os.getcwd()+'/utils')

from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import model

app = Flask(__name__)
api = Api(app)

@api.resource('/test/')
class getMeasureByDum(Resource):
    def get(self):
        a = model.getMeasureByDum()
        # print(a)
        return jsonify(a)

 #####################    USER    ##################### 
@api.resource('/user/')
class user(Resource):
    def get(self):
        a = model.listAlluser()
        # print(a)
        return jsonify(a)
    def post(self):
        args = request.get_json()
        userExist = model.findUser(
            name=args["name"],
            lastname=args["lastname"],
            password=args["password"]
        )
        if userExist:
            return args, 202
        else:
            model.User(
                name=args["name"],
                lastname=args["lastname"],
                password=args["password"]
            )
            print("POST ->", args)
            return args, 201

@api.resource('/userpasswd/')
class userPassword(Resource):
    def post(self):
        args = request.get_json()
    
        userExist = model.findUser(
            name=args["name"],
            lastname=args["lastname"],
            password=args["password"]
        )
        if userExist:
            passUpdated = model.updataPasswd(
                name=args["name"],
                lastname=args["lastname"],
                password=args["password"],
                newpasswd=args["newpasswd"]
            )
            if passUpdated:
                return {'message':'Password updated'}, 202
            else:
                return {'message':'Password was not update'}, 203
        else:
            return {'message':'User does not exist'}, 203

 #####################    METER    ##################### 
@api.resource('/meter/')
class meter(Resource):
    def get(self):
        a = model.listAllmeter()
        # print(a)
        return jsonify(a)

 #####################    DUM    ##################### 
@api.resource('/dum/')
class dumList(Resource):
    def get(self):
        a = model.listAlldum()
        # print(a)
        return jsonify(a)
    def post(self):
        args = request.get_json()
        dum = model.findDumByMac(mac=args["mac"])
        if dum == None:
            model.Dum(
                name= args["name"],
                userID = args["userid"]
            )
            dumId = model.findLastDumIdGenerated()
            model.Meter(
                macAddress= args["mac"],
                dumID = dumId,
                userID = args["userid"]
            )
            return {'message':'OK'},201
        else:
            print("DUM does exist")
            return {'message':'DUM does exist'},405

  #####################    MEASURE    ##################### 
@api.resource('/measure/')
class measureList(Resource):
    def get(self):
        a = model.listAllmeasure()
        # print(a)
        return jsonify(a)

    def post(self):
        args = request.get_json()
        print(args)
        dum = model.findDumByMac(mac=args["mac"])
        if dum == None:
            print("DUM does not exist")
            return {'message':'DUM does not exist'},405
        else:
            model.Measure(
                dum = dum,
                active_power = args["active_power"],
                cos_phi = args["cos_phi"],
                irms = args["irms"],
                pf = args["pf"],
                thd = args["thd"],
                vrms = args["vrms"],
            )
            return {'message':'OK'},201

if __name__ == '__main__':
    app.run(host='0.0.0.0')
