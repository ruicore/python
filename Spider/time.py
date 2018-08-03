import time
import os
import sys
import datetime

def get_time(path):
    create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getctime(path)))
    modified_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(path)))
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("create_time  :",create_time)
    print("modified_time:",modified_time)
    print("time_now     :",now_time)
    return create_time, modified_time,now_time

if __name__=="__main__":
    get_time(sys.argv[1])
