# -*- coding: utf-8 -*-
# @Author:             何睿
# @Create Date:        2018-08-08 14:46:24
# @Last Modified by:   何睿
# @Last Modified time: 2018-08-08 15:11:27

import sys
import shelve


def store_person(db):
    """
    Query user for data and store it in the shelf object
    """
    pid = input("Enter unique ID number:")
    person = {}
    person.setdefault('name', input("Enter name:"))
    person.setdefault('age', input("Enter age:"))
    person.setdefault('phone', input('Enter phone number:'))
    db.setdefault(pid, person)


def lookup_person(db):
    """
    Query user for ID and desired fiele,and fecth the corresponding data from
    the shelf object
    """
    pid = input("Enter ID number:")
    field = input("What would you like to know? (name,age,phone)")
    field = field.strip("\r\n ").lower()
    print(str.capitalize(field)+":",
          db.get(pid).get(field))


def print_help():
    print('The avaiable commands are:')
    print("store  :Stores information about a person")
    print("lookup :Looks up a person from ID number")
    print("quit   :Save changes and exit!")
    print("?      :Prints this message")


def enter_command():
    cmd = input("Enter command (? for help):")
    cmd = cmd.strip("\r\n ").lower()
    return cmd


def main():
    database = shelve.open('temp')
    try:
        while True:
            cmd = enter_command()
            if cmd == "store":
                store_person(database)
            elif cmd == 'lookup':
                lookup_person(database)
            elif cmd == "?":
                print_help()
            elif cmd == "quit":
                return
    finally:
        database.close()

if __name__=="__main__":
    main()