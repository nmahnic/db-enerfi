# importing sys
import sys
import os
import json
  
# adding Folder_2 to the system path
sys.path.insert(0, os.getcwd()+'/utils')

from client import Client
import datetime 

print("REQUEST: ",datetime.datetime.now())
filename = 'measuresByDate2/sample20220206-131832.json'
# filename = 'measurePava.json'
# Opening JSON file
f = open(filename)
jsonData = json.load(f)
f.close()

Client.addMeasure2(jsonData)





