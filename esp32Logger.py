# importing sys
import sys
import os
import json
  
# adding Folder_2 to the system path
sys.path.insert(0, os.getcwd()+'/utils')

from client import Client
import datetime 

print("REQUEST: ",datetime.datetime.now())
filename = 'rectifcadorDiodo/sample2022_02_19-03_40_35_PM.json'
# filename = 'sinRectificar/sample2022_02_19-03_57_45_PM.json'

f = open(filename)
jsonData = json.load(f)
f.close()

Client.addMeasure2(jsonData)





