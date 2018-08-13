import time
import os
import sys
import datetime

def get_time(*path):
    for _path in path[0]:
        create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getctime(_path)))
        modified_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(_path)))
        print(_path)
        print("%-15s%s"%("create_time",create_time))
        print("%-15s%s"%("modified_time",modified_time))
    return None

if __name__=="__main__":
    get_time(sys.argv[1:])
