import requests
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

 #####################    USER    #####################       
    def listUser():
        URL = 'http://localhost:5000/user/'
        r = requests.get(URL)

        print(r.status_code)
        pprint(r.json())
        data = json.loads(r.text)
        return data
        # print(type(r.json()))

    def addUser(name,lastname,password,email):
        URL = 'http://localhost:5000/user/'
        payload = {
            'name': name,
            'password': password,
            'lastname': lastname,
            'email':email
        }
        headers = {'content-type': 'application/json'}
        r = requests.post(URL, data=json.dumps(payload), headers=headers)

        print(r.status_code, r.json())
        data = json.loads(r.text)
        return data
        # print(type(r.json()))

    def changePasswd(name,lastname,passwd,newpasswd,email):
        URL = 'http://localhost:5000/userpasswd/'
        payload = {
            'name': name,
            'lastname': lastname,
            'email': email,
            'password': passwd,
            'newpasswd': newpasswd
        }
        headers = {'content-type': 'application/json'}
        r = requests.post(URL, data=json.dumps(payload), headers=headers)

        print(r.status_code, r.json())
        data = json.loads(r.text)
        return data
        # print(type(r.json()))

 #####################    DUM    ##################### 
    def listDum():
        URL = 'http://localhost:5000/dum/'
        r = requests.get(URL)

        print(r.status_code)
        pprint(r.json())
        data = json.loads(r.text)
        return data
        # print(type(r.json()))
    
    def listDumByUser(email,passwd):
        URL = 'http://localhost:5000/listdumbyuser/'
        payload = {'passwd':passwd, 'email':email}
        headers = {'content-type': 'application/json'}
        r = requests.post(URL, data=json.dumps(payload), headers=headers)

        print(r.status_code, r.json())
        data = json.loads(r.text)
        return data

 #####################    METER    ##################### 
    def listmeter():
        URL = 'http://localhost:5000/meter/'
        r = requests.get(URL)

        print(r.status_code)
        pprint(r.json())
        data = json.loads(r.text)
        return data
        # print(type(r.json()))

    def listMeterByUser(email,passwd):
        URL = 'http://localhost:5000/listmeterbyuser/'
        payload = {'passwd':passwd, 'email':email}
        headers = {'content-type': 'application/json'}
        r = requests.post(URL, data=json.dumps(payload), headers=headers)

        print(r.status_code, r.json())
        data = json.loads(r.text)
        return data

    def addDumMeter(email,passwd,name,mac):
        URL = 'http://localhost:5000/dum/'
        payload = {
            'email':email,
            'passwd':passwd,
            'name':name,
            'mac':mac
        }
        headers = {'content-type': 'application/json'}
        r = requests.post(URL, data=json.dumps(payload), headers=headers)

        print(r.status_code, r.json())
        data = json.loads(r.text)
        return data

    def changeDumMeter(email,passwd,omac,dmac):
        URL = 'http://localhost:5000/changedum/'
        payload = {
            'email':email,
            'passwd':passwd,
            'omac':omac,
            'dmac':dmac
        }
        headers = {'content-type': 'application/json'}
        r = requests.post(URL, data=json.dumps(payload), headers=headers)

        print(r.status_code, r.json())
        data = json.loads(r.text)
        return data

    def disableDumMeter(email,passwd,mac):
        URL = 'http://localhost:5000/disabledum/'
        payload = {'email':email,'passwd':passwd,'mac':mac}
        headers = {'content-type': 'application/json'}
        r = requests.post(URL, data=json.dumps(payload), headers=headers)

        print(r.status_code, r.json())
        data = json.loads(r.text)
        return data
 #####################    MEASURE    ##################### 
    def listMeasure():
        URL = 'http://localhost:5000/measure/'
        r = requests.get(URL)

        print(r.status_code)
        pprint(r.json())
        data = json.loads(r.text)
        return data
        # print(type(r.json()))

    def addMeasure(mac,active_power,cos_phi,dumID,irms,pf,thd,vrms):
        URL = 'http://localhost:5000/measure/'
        payload = {
            'mac':mac,
            'active_power': active_power,
            'cos_phi': cos_phi,
            'irms': irms,
            'pf': pf,
            'thd': thd,
            'vrms': vrms
        }
        headers = {'content-type': 'application/json'}
        r = requests.post(URL, data=json.dumps(payload), headers=headers)

        print(r.status_code, r.json())
        data = json.loads(r.text)
        return data
        # print(type(r.json()))
    
    def listMeasureByUser(email,passwd,mac):
        URL = 'http://localhost:5000/listmeasurebyuser/'
        payload = {'passwd':passwd, 'email':email, 'mac':mac}
        headers = {'content-type': 'application/json'}
        r = requests.post(URL, data=json.dumps(payload), headers=headers)

        print(r.status_code, r.json())
        data = json.loads(r.text)
        return data