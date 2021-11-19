# importing sys
import sys
import os
  
# adding Folder_2 to the system path
sys.path.insert(0, os.getcwd()+'/utils')

from client import Client
import random

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
            print("Use addUser.py")
            
        elif sys.argv[2] == '--dum' or sys.argv[2] == '--meter':
            print("'-a --dum' o '-a --meter' es lo mismo")
            mail = input("Ingrese mail: ")
            passwd = input("Ingrese passwd: ")
            name = input("Ingres nombre del DUM: ")
            mac = input("ingrese mac: ")
            Client.addDumMeter(mail,passwd,name,mac)

        elif sys.argv[2] == '--measure':
            mac = input("Ingrese mac: ")
            active_power = round(random.uniform(100, 4000),2)
            cos_phi = round(random.random(),2)
            dumID = round(random.random(),2)
            pf = round(random.random(),2)
            thd = round(random.random(),2)
            vrms = round(random.uniform(180, 240),2)
            irms = round(random.uniform(1, 10),2)
            Client.addMeasure(mac,active_power,cos_phi,dumID,irms,pf,thd,vrms)
        else:
            pass
    elif sys.argv[1] == '-m':
        if sys.argv[2] == '--user':
            name = input("Ingrese nombre: ")
            lastname = input("Ingrese lastname: ")
            mail = input("Ingrese mail: ")
            passwd = input("Ingrese passwd: ")
            newpasswd = input("Ingrese newpasswd: ")
            Client.changePasswd(name,lastname,passwd,newpasswd,mail)

        elif sys.argv[2] == '--dum':
            userid = input("UserID :")
            omac = input("ingrese mac origen: ")
            dmac = input("ingrese mac destino: ")
            Client.changeDumMeter(userid,omac,dmac)
        else:
            print("NOT IMPLEMENTED YET")

    elif sys.argv[1] == '-b':
        if sys.argv[2] == '--dum':
            userid = input("UserID :")
            mac = input("ingrese mac: ")
            Client.disableDumMeter(userid,mac)
        else:
            print("NOT IMPLEMENTED YET")
    elif sys.argv[1] == '-c':
        if sys.argv[2] == '--dum':
            mail = input("Ingrese mail: ")
            passwd = input("Ingrese passwd: ")
            Client.listDumByUser(mail,passwd)

        elif sys.argv[2] == '--meter':
            mail = input("Ingrese mail: ")
            passwd = input("Ingrese passwd: ")
            Client.listMeterByUser(mail,passwd)
        else:
            print("NOT IMPLEMENTED YET")
    else:
        pass
