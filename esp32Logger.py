#!/usr/bin/env python
import sys
from clientModel import Client
import sched, time
import datetime


def logMeasurese(sc):
    print("REQUEST: ",datetime.datetime.now())
    active_power = 1.4
    cos_phi = .4
    dumID = .5
    irms = .5
    pf = .5
    thd = .5
    vrms = .5
    Client.addMeasure(sys.argv[1],active_power,cos_phi,dumID,irms,pf,thd,vrms)
    s.enter(2,1, logMeasurese, (sc,))


if __name__ == '__main__':
    # chequeo de los argumentos de la linea de comandos
    if len(sys.argv) != 2:
        print("Error en la linea de comandos. Cantidad de argumentos erroneos")
        print("python3 client.py B0-B2-8F-1D-4D-02")
        sys.exit()
    else:
        s = sched.scheduler(time.time, time.sleep)  
        s.enter(1,1, logMeasurese, (s,))
        s.run() 


