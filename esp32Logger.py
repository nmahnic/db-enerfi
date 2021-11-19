# importing sys
import sys
import os
  
# adding Folder_2 to the system path
sys.path.insert(0, os.getcwd()+'/utils')

from client import Client
import sched, time
import datetime 
import random


def logMeasurese(sc):
    print("REQUEST: ",datetime.datetime.now())
    active_power = round(random.uniform(100, 4000),2)
    cos_phi = round(random.random(),2)
    dumID = round(random.random(),2)
    pf = round(random.random(),2)
    thd = round(random.random(),2)
    vrms = round(random.uniform(180, 240),2)
    irms = round(random.uniform(1, 10),2)
    Client.addMeasure(sys.argv[1],active_power,cos_phi,dumID,irms,pf,thd,vrms)
    s.enter(2,1, logMeasurese, (sc,))


if __name__ == '__main__':
    # chequeo de los argumentos de la linea de comandos
    if len(sys.argv) != 2:
        print("Error en la linea de comandos. Cantidad de argumentos erroneos")
        print("python3 esp32Logger.py B0-B2-8F-1D-4D-02")
        sys.exit()
    else:
        s = sched.scheduler(time.time, time.sleep)  
        s.enter(1,1, logMeasurese, (s,))
        s.run() 


