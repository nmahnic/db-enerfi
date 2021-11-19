#!/usr/bin/env python

# importing sys
import sys
import os
  
# adding Folder_2 to the system path
sys.path.insert(0, os.getcwd()+'/utils')

from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import model
import functions

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
        users = model.listAlluser()
        a = [{'name':user['name'],'lastname':user['lastname'],'email':user['email'],'password':str(user['password']),'salt':str(user['salt']),} for user in users]
        return jsonify(a)
    def post(self):
        args = request.get_json()
        userExist = model.findUser(
                name = args["name"],
                lastname = args["lastname"],
                email=args["email"]
            )
        if userExist:
            return {'message':'User already exist'}, 405
        else:
            salt = functions.generate_salt()
            password = args["password"].encode('utf-8')
            model.User(
                name= args["name"],
                lastname= args["lastname"],
                password= (functions.get_hashed_password(password,salt)),
                email= args["email"],
                salt= (salt)
            )
            print("POST ->", args)
            return {'message':'User created'}, 201

@api.resource('/userpasswd/')
class userPassword(Resource):
    def post(self):
        args = request.get_json()
        user = model.validUser(
                passwd = args["passwd"],
                email=args["email"]
            )
        if user:
            salt = user.salt
            newpasswd = args["newpasswd"].encode('utf-8')
            user.password  = (functions.get_hashed_password(newpasswd,salt))
            return {'message':'Password updated'}, 202
        else:
            return {'message':'User is not valid'}, 203

 #####################    METER    ##################### 
@api.resource('/meter/')
class meter(Resource):
    def get(self):
        a = model.listAllmeter()
        # print(a)
        return jsonify(a)

@api.resource('/listmeterbyuser/')
class listmeterbyuser(Resource):
    def post(self):
        args = request.get_json()
        userValid = model.validUser(
                passwd = args["passwd"],
                email=args["email"]
            )
        if userValid:
            meters = model.listMeterByUser(userValid)
            return jsonify(meters)
        else:
            return {'message':'User is not valid'}, 203

 #####################    DUM    ##################### 
@api.resource('/dum/')
class dum(Resource):
    def get(self):
        a = model.listAlldum()
        # print(a)
        return jsonify(a)
    def post(self):
        args = request.get_json()
        meter = model.findMeterByMac(mac=args["mac"])
        if meter == None:

            userValid = model.validUser(
                    passwd = args["passwd"],
                    email=args["email"]
                )
            if userValid == None:
                return {'message':'User is not valid'}, 203
            else:
                model.Dum(
                    name= args["name"],
                    userID = userValid.id,
                    enable = True
                )
                dumId = model.findLastDumIdGenerated()
                model.Meter(
                    macAddress= args["mac"],
                    dumID = dumId,
                    userID = userValid.id
                )
                return {'message':'DUM and Meter created'},201
        else:
            return {'message':'DUM already exist'},405

@api.resource('/changedum/')
class changedum(Resource):
    def post(self):
        args = request.get_json()
        meter = model.findMeterByMac(mac=args["omac"])
        if meter == None:
            return {'message':'DUM does not exist with this MAC'},405
        else:
            userValid = model.validUser(
                    passwd = args["passwd"],
                    email=args["email"]
                )
            if userValid:
                if (meter.user.id != userValid.id):
                    return {'message':'User is not valid'},405
                else:
                    meter.macAddress= args["dmac"]
                    return {'message':'mac was updated'},200
            else:
                return {'message':'User is not valid'}, 203
            


@api.resource('/disabledum/')
class disabledum(Resource):
    def post(self):
        args = request.get_json()
        dum = model.findDumByMac(mac=args["mac"])
        if dum == None:
            return {'message':'DUM does not exist'},405
        else:
            userValid = model.validUser(
                    passwd = args["passwd"],
                    email=args["email"]
                )
            if userValid:
                if (dum.user.id != userValid.id):
                    return {'message':'User is not valid'},405
                else:
                    dum.enable = False
                    return {'message':'dum was deleted'},200
            else:
                return {'message':'User is not valid'}, 203


@api.resource('/listdumbyuser/')
class listdumbyuser(Resource):
    def post(self):
        args = request.get_json()
        userValid = model.validUser(
                passwd = args["passwd"],
                email=args["email"]
            )
        if userValid:
            dums = model.listDumByUser(userValid)
            return jsonify(dums)
        else:
            return {'message':'User is not valid'}, 203


  #####################    MEASURE    ##################### 
@api.resource('/measure/')
class measure(Resource):
    def get(self):
        a = model.listAllmeasure()
        # print(a)
        return jsonify(a)

    def post(self):
        args = request.get_json()
        print(args)
        dum = model.findDumByMac(mac=args["mac"])
        if dum == None:
            return {'message':'DUM does not exist with this MAC'},405
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

@api.resource('/listmeasurebyuser/')
class listmeasurebyuser(Resource):
    def post(self):
        args = request.get_json()
        userValid = model.validUser(
                passwd = args["passwd"],
                email=args["email"]
            )
        if userValid:
            dum = model.findDumByMac(mac=args["mac"])
            if(dum.enable == False):
                return {'message':'This DUM was deleted'}, 203 
            else:
                measures = model.listMeasureByUser(dum)
                return jsonify(measures)
        else:
            return {'message':'User is not valid'}, 203

if __name__ == '__main__':
    app.run(host='0.0.0.0')
