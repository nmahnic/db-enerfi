# importing sys
import sys
import os
  
# adding Folder_2 to the system path
sys.path.insert(0, os.getcwd()+'/utils')

from client import Client

if __name__ == '__main__':
    # chequeo de los argumentos de la linea de comandos
    if len(sys.argv) != 3:
        print("Error en la linea de comandos. Cantidad de argumentos erroneos")
        print("python3 client.py Nicolas Lopez")
        sys.exit()

    mail = input("Ingrese mail: ")
    password = input("Ingrese password: ")
    Client.addUser(sys.argv[1],sys.argv[2],password,mail)