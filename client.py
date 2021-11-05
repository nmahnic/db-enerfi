#!/usr/bin/env python
import sys
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

    def addDum(userid,name,mac):
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

if __name__ == '__main__':
    # chequeo de los argumentos de la linea de comandos
    if len(sys.argv) != 3:
        print("Error en la linea de comandos. Cantidad de argumentos erroneos")
        print("python3 client.py -l --user")
        sys.exit()

    if sys.argv[1] not in ('-a', '-b', '-m', '-l', '-c'):
        print("Error en la linea de comandos. Opcion no valida (-a, -b, -m, -l, -c)")
        sys.exit()

    if sys.argv[2] not in ('--user', '--dum', '--meter', '--measure','--test'):
        print("Error en la linea de comandos. Opcion no valida (--user, --dum, --meter, --measure)")
        sys.exit()

    if sys.argv[1] == '-l':
        if sys.argv[2] == '--user':
            Client.listUser()
        elif sys.argv[2] == '--dum':
            Client.listDum()
        elif sys.argv[2] == '--meter':
            Client.listmeter()
        elif sys.argv[2] == '--measure':
            Client.listMeasure()
        elif sys.argv[2] == '--test':
            Client.test()
        else:
            pass
    elif sys.argv[1] == '-a':
        if sys.argv[2] == '--user':
            name = input("Ingrese nombre: ")
            # surname = input("Ingrese surname: ")
            # mail = input("Ingrese mail: ")
            # password = input("Ingrese password: ")
            # usernick = input("Ingrese usernick: ")
            # Client.addUser(name,surname,mail,password,usernick)
            Client.addUser(name,"lopez","hlopez@gmail.com","1234","huguito")
        elif sys.argv[2] == '--dum' or sys.argv[2] == '--meter':
            print("'-a --dum' o '-a --meter' es lo mismo")
            userid = input("UserID:")
            name = input("Ingres nombre del DUM:")
            mac = input("ingrese mac:")
            Client.addDum(userid,name,mac)
        elif sys.argv[2] == '--measure':
            mac = input("Ingrese mac: ")
            active_power = 1.4
            cos_phi = .4
            dumID = .5
            freq_10th = .5
            freq_1st = .5
            freq_2nd = .5
            freq_3rd = .5
            freq_4th = .5
            freq_5th = .5
            freq_6th = .5
            freq_7th = .5
            freq_8th = .5
            freq_9th = .5
            irms = .5
            pf = .5
            thd = .5
            vrms = .5
            Client.addMeasure(
                mac,active_power,cos_phi,dumID,freq_10th,freq_1st,freq_2nd,freq_3rd,
                freq_4th,freq_5th,freq_6th,freq_7th,freq_8th,freq_9th,irms,pf,thd,vrms
            )
        else:
            pass
    elif sys.argv[1] == '-b':
        print("NOT IMPLEMENTED YET")
    elif sys.argv[1] == '-m':
        print("NOT IMPLEMENTED YET")
    elif sys.argv[1] == '-c':
        print("NOT IMPLEMENTED YET")
    else:
        pass
