import subprocess
import multiprocessing

def logger1():
    subprocess.call("python3 esp32Logger.py 9C:9C:1F:E9:5C:A0", shell=True)

def logger2():
    subprocess.call("python3 esp32Logger.py B0-B2-8F-1D-4D-02", shell=True)

if __name__ == '__main__':
    p1 = multiprocessing.Process(name='p1', target=logger1)
    # p = multiprocessing.Process(name='p', target=logger2)
    p1.start()
    # p.start()