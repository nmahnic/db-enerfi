import requests
import urllib.parse
from pprint import pprint
import json

class Client: 

    def test():
        URL = 'http://localhost:5000/test/'
        r = requests.get(URL)

        print(r.status_code)
        pprint(r.json())
        data = json.loads(r.text)
        return data
        # print(type(r.json()))

        
    def listUser():
        URL = 'http://localhost:5000/user/'
        r = requests.get(URL)

        print(r.status_code)
        pprint(r.json())
        data = json.loads(r.text)
        return data
        # print(type(r.json()))

    def addUser(name,surname,mail,password,usernick):
        URL = 'http://localhost:5000/user/'
        payload = {
            'mail': mail,
            'name': name,
            'password': password,
            'surname': surname,
            'usernick': usernick
        }
        headers = {'content-type': 'application/json'}
        r = requests.post(URL, data=json.dumps(payload), headers=headers)

        print(r.status_code)
        pprint(r.json())
        data = json.loads(r.text)
        return data
        # print(type(r.json()))

    def listDum():
        URL = 'http://localhost:5000/dum/'
        r = requests.get(URL)

        print(r.status_code)
        pprint(r.json())
        data = json.loads(r.text)
        return data
        # print(type(r.json()))

    def listmeter():
        URL = 'http://localhost:5000/meter/'
        r = requests.get(URL)

        print(r.status_code)
        pprint(r.json())
        data = json.loads(r.text)
        return data
        # print(type(r.json()))

    def addDumMeter(userid,name,mac):
        URL = 'http://localhost:5000/dum/'
        payload = {
            'userid':userid,
            'name':name,
            'mac':mac
        }
        headers = {'content-type': 'application/json'}
        r = requests.post(URL, data=json.dumps(payload), headers=headers)

        print(r.status_code)
        pprint(r.json())
        data = json.loads(r.text)
        return data

    def listMeasure():
        URL = 'http://localhost:5000/measure/'
        r = requests.get(URL)

        print(r.status_code)
        pprint(r.json())
        data = json.loads(r.text)
        return data
        # print(type(r.json()))

    def addMeasure(
            mac,active_power,cos_phi,dumID,freq_10th,freq_1st,freq_2nd,freq_3rd,
            freq_4th,freq_5th,freq_6th,freq_7th,freq_8th,freq_9th,irms,pf,thd,vrms
        ):
        URL = 'http://localhost:5000/measure/'
        payload = {
            'mac':mac,
            'active_power': active_power,
            'cos_phi': cos_phi,
            'dumID': dumID,
            'freq_10th': freq_10th,
            'freq_1st': freq_1st,
            'freq_2nd': freq_2nd,
            'freq_3rd': freq_3rd,
            'freq_4th': freq_4th,
            'freq_5th': freq_5th,
            'freq_6th': freq_6th,
            'freq_7th': freq_7th,
            'freq_8th': freq_8th,
            'freq_9th': freq_9th,
            'irms': irms,
            'pf': pf,
            'thd': thd,
            'vrms': vrms
        }
        headers = {'content-type': 'application/json'}
        r = requests.post(URL, data=json.dumps(payload), headers=headers)

        print(r.status_code)
        pprint(r.json())
        data = json.loads(r.text)
        return data
        # print(type(r.json()))