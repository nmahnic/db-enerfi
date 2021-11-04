#!/usr/bin/env python
import sys
import requests
import urllib.parse
from pprint import pprint
import json


class Client: 
        
    def listUser():
        URL = 'http://localhost:5000/user/'
        r = requests.get(URL)

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

    def listMeasure():
        URL = 'http://localhost:5000/measure/'
        r = requests.get(URL)

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

    if sys.argv[2] not in ('--user', '--dum', '--meter', '--measure'):
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
        else:
            pass
    elif sys.argv[1] == '-a':
        print("NOT IMPLEMENTED YET")
    elif sys.argv[1] == '-b':
        print("NOT IMPLEMENTED YET")
    elif sys.argv[1] == '-m':
        print("NOT IMPLEMENTED YET")
    elif sys.argv[1] == '-c':
        print("NOT IMPLEMENTED YET")
    else:
        pass
