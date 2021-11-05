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

@api.resource('/test/')
class getMeasureByDum(Resource):
    def get(self):
        a = model.getMeasureByDum()
        # print(a)
        return jsonify(a)

@api.resource('/dum/')
class dumList(Resource):
    def get(self):
        a = model.listAlldum()
        # print(a)
        return jsonify(a)

@api.resource('/meter/')
class meterList(Resource):
    def get(self):
        a = model.listAllmeter()
        # print(a)
        return jsonify(a)

@api.resource('/measure/')
class measureList(Resource):
    def get(self):
        a = model.listAllmeasure()
        # print(a)
        return jsonify(a)

    def post(self):
        args = request.get_json()
        print(args)
        dum = model.findDum(mac=args["mac"])
        if dum == None:
            print("DumNOTExist")
            return {'insert':'DumNOTExist'},200
        else:
            model.Measure(
                dum = dum,
                active_power = args["active_power"],
                cos_phi = args["active_power"],
                dumID = args["active_power"],
                freq_10th = args["freq_10th"],
                freq_1st = args["freq_1st"],
                freq_2nd = args["freq_2nd"],
                freq_3rd = args["freq_3rd"],
                freq_4th = args["freq_4th"],
                freq_5th = args["freq_5th"],
                freq_6th = args["freq_6th"],
                freq_7th = args["freq_7th"],
                freq_8th = args["freq_8th"],
                freq_9th = args["freq_9th"],
                irms = args["irms"],
                pf = args["pf"],
                thd = args["thd"],
                vrms = args["vrms"],
            )
            return {'insert':'OK'},200

if __name__ == '__main__':
    app.run(debug=True)
