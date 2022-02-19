# importing sys
import sys
import os
import json
  
# adding Folder_2 to the system path
sys.path.insert(0, os.getcwd()+'/utils')

from client import Client
import datetime 

print("REQUEST: ",datetime.datetime.now())
filename = 'sinRectificar/sample2022_02_19-03_57_56_PM.json'
# filename = 'measurePava.json'
# Opening JSON file
f = open(filename)
jsonData = json.load(f)
f.close()

Client.addMeasure2(jsonData)





