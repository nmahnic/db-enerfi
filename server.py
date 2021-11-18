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

@api.resource('/user/')
class userList(Resource):
    def get(self):
        a = model.listAlluser()
        # print(a)
        return jsonify(a)
    def post(self):
        args = request.get_json()
        userExist = model.findUser(
            name=args["name"],
            surname=args["surname"],
            usernick=args["usernick"],
            password=args["password"],
            mail=args["mail"],
        )
        if userExist:
            return args, 202
        else:
            model.User(
                name=args["name"],
                surname=args["surname"],
                usernick=args["usernick"],
                password=args["password"],
                mail=args["mail"],
            )
            print("POST ->", args)
            return args, 201


@api.resource('/meter/')
class meterList(Resource):
    def get(self):
        a = model.listAllmeter()
        # print(a)
        return jsonify(a)


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
            return {'insert':'OK'},200
        else:
            print("Exist DUM")
            return {'insert':'DUM Exist'},200

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
            print("DumNOTExist")
            return {'insert':'DumNOTExist'},200
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
            return {'insert':'OK'},200

if __name__ == '__main__':
    app.run(host='0.0.0.0')
