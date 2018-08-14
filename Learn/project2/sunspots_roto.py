# -*- coding: utf-8 -*-
# @Author:             何睿
# @Create Date:        2018-08-13 15:05:23
# @Last Modified by:   何睿
# @Last Modified time: 2018-08-14 09:00:58

from pprint import pprint
from urllib.request import urlopen
from reportlab.graphics.shapes import *
from reportlab.lib import colors
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.charts.textlabels import Label
from reportlab.graphics import renderPDF

URL = "https://services.swpc.noaa.gov/text/predicted-sunspot-radio-flux.txt"
COMMENT_CHARS = ":#"

drawing = Drawing(400, 200)
data = []

for line in urlopen(URL).readlines():
    line = line.decode('utf-8')
    if not line.isspace() and not line[0] in COMMENT_CHARS:
        data.append([float(n) for n in line.split()])

pred = [row[2] for row in data]
high = [row[3] for row in data]
low = [row[4] for row in data]
_times = [row[0] + row[1]/12.0 for row in data]

lp = LinePlot()
lp.x = 50
lp.y = 50
lp.height = 125
lp.width = 300

lp.data = [list(zip(_times, pred)), list(zip(_times, high)), list(zip(_times, low))]
lp.lines[0].strokeColor = colors.blue
lp.lines[1].strokeColor = colors.red
lp.lines[2].strokeColor = colors.green

drawing.add(lp)
drawing.add(String(250,150,'Sunspots',fontsize=14,fillColor=colors.red))
renderPDF.drawToFile(drawing,'report.pdf',"Sunspots")