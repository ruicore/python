# -*- coding: utf-8 -*-
import fileinput
import sys
import os
import time


_file_name = sys.argv[1]
create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getctime(_file_name)))
modified_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(_file_name)))

with open(_file_name,'r+',encoding='utf-8') as f:
    f.seek(0)
    f.write("# -*- coding: utf-8 -*-\n")
    f.write("# @Author:             何睿\n")
    f.write("# @Create Date:        "+create_time+"\n")
    f.write("# @Last Modified by:   何睿\n")
    f.write("# @Last Modified time: "+modified_time+'\n')


    
