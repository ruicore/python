# -*- coding: utf-8 -*-
# @Author:             何睿
# @Create Date:        2018-08-11 09:23:45
# @Last Modified by:   何睿
# @Last Modified time: 2018-08-11 09:23:47

import sqlite3

conn = sqlite3.connect('food.db')
curs = conn.cursor()


def convert(value):
    if value.startswith('~'):
        return value.strip("~")
    if not value:
        value = 0
    return float(value)


try:
    curs.execute('''
        CREATE TABLE food(

        id      TEXT        PRIMARY KEY,
        desc    TEXT,
        water   FLOAT,
        kcal    FLOAT,
        protein FLOAT,
        fat     FLOAT,
        ash     FLOAT,
        carbs   FLOAT,
        fiber   FLOAT
        )
        ''')
except Exception as e:
    print(e.args)

query = "INSERT INTO food VALUES(?,?,?,?,?,?,?,?,?)"
for line in open(r"C:\HeRui\Temp\SR-Leg_ASC\DATA_SRC.txt"):
    fields = line.strip().split("^")
    vals = [convert(f) for f in fields]
    curs.execute(query, vals)
conn.commit()
conn.close()
