# -*- coding: utf-8 -*-
# @Author:             何睿
# @Create Date:        2018-08-16 11:20:10
# @Last Modified by:   何睿
# @Last Modified time: 2018-08-16 11:20:10
import fileinput
import sys
import os
import time

create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
_file_name = create_time[:10]+"-"+"-".join(sys.argv[1:])+".py"
with open(_file_name, 'w', encoding='utf-8') as f:
    f.seek(0)
    f.write("# -*- coding: utf-8 -*-\n")
    f.write("# @Author:             何睿\n")
    f.write("# @Create Date:        "+create_time+"\n")
    f.write("# @Last Modified by:   何睿\n")
    f.write("# @Last Modified time: "+create_time)