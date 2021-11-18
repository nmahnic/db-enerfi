import subprocess
import multiprocessing

def logger1():
    subprocess.call("python3 esp32Logger.py 84-D8-1B-0C-5B-C1", shell=True)

def logger2():
    subprocess.call("python3 esp32Logger.py B0-B2-8F-1D-4D-02", shell=True)

if __name__ == '__main__':
    p1 = multiprocessing.Process(name='p1', target=logger1)
    p = multiprocessing.Process(name='p', target=logger2)
    p1.start()
    p.start()