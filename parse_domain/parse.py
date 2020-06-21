import socket
import logging

from typing import Dict
from pprint import pprint

file_handler = logging.FileHandler("parse_domain.log")

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)


logger = logging.getLogger(__name__)
logger.addHandler(file_handler)
logger.setLevel("INFO")


def parse_domain(addrs) -> Dict[str, str]:
    ips = {}
    for addr in addrs:
        try:
            addr_ip = socket.getaddrinfo(addr, None)
        except Exception as e:
            logger.error(e)
            continue
        for item in addr_ip:
            ips[addr] = item[-1][0]
 
    return ips


addrs = ["github.githubassets.com",
         "camo.githubusercontent.com",
         "github.map.fastly.net",
         "github.global.ssl.fastly.net",
         "github.com",
         "api.github.com",
         "raw.githubusercontent.com",
         "favicons.githubusercontent.com",
         "avatars5.githubusercontent.com",
         "avatars4.githubusercontent.com",
         "avatars3.githubusercontent.com",
         "avatars2.githubusercontent.com",
         "avatars1.githubusercontent.com",
         "avatars0.githubusercontent.com",
         "notexist"]


ips = parse_domain(addrs)

for addr, ip in ips.items():
    print("{:<30} {:<4}".format(addr,ip))

