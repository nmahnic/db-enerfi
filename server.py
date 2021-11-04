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

if __name__ == '__main__':
    app.run(debug=True)
