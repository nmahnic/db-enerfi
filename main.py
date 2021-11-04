import subprocess

for i in range(5):   
    subprocess.call("python3 client.py -l --user", shell=True)
    subprocess.call("python3 client.py -l --dum", shell=True)
