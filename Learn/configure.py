# -*- coding: utf-8 -*-
# @Author:             何睿
# @Create Date:        2018-08-12 10:28:47
# @Last Modified by:   何睿
# @Last Modified time: 2018-08-12 11:28:41

from configparser import ConfigParser
import logging

logging.basicConfig(level=logging.INFO,filename='mylog.log')
logging.info("Starting program")
logging.info("Tryin to divide 1 by 0")
print(1/0)
logging.info("The divison succeeded")
logging.info("Ending program")

CONFIGFILE = 'python.txt'

config=ConfigParser()
config.read(CONFIGFILE)
print(config.get("messages","greeting"))
radius = int(input(config.get('messages','question')+" "))
print(config.get('messages','result_message'),end='')
print(config.getfloat('numbers','pi')*radius**2)


