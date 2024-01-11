from src.lib.Program import Program
from Database.Mongodb import Mongodb
import getpass
import sys, os, time, bson
from sys import exit as logout
from os import system as bash

class PctRun:
  def login():
    bash("clear")
    db = Mongodb()
    p = '\x1b[1;97m'
    m = '\x1b[1;91m'
    h = '\x1b[1;92m'
    k = '\x1b[1;93m'
    b = '\x1b[1;94m'
    u = '\x1b[1;95m' 
    o = '\x1b[1;96m'
    n = '\x1b[0m'    
    Z = "\033[1;30m"
    print(f"""\n{h}
 __            _     
|  |   ___ ___|_|___ 
|  |__| . | . | |   |
|_____|___|_  |_|_|_|
          |___|      
{n}\n""")
    username = input(f"Username{m}*{n} : ")
    password = getpass.getpass(f"Password{m}*{n} : ")
    if username and password :
      if db.find({"username": username.lower()}, "users"):
        user = db.find({"username": username.lower()}, "users")
        if user["password"] == password :
          if user["active"]:
            print(f"\n{n}[{h}✔{n}]>{h} Login Successful!\n")
            time.sleep(3)
            Program.start();
          else:
            print(f"\n{n}[{m}✘{n}]>{m} Inactive Account!\n")
            logout()
        else:
          print(f"\n{n}[{m}✘{n}]>{m} Wrong Password!\n")
          time.sleep(3)
          bash("clear")
          PctRun.login()
      else:
        print(f"\n{n}[{m}✘{n}]>{m} Account Doesn't Exist!\n")
        time.sleep(3)
        bash("clear")
        PctRun.login()
    else :
      print(f"\n{n}[{m}✘{n}]>{m} Input Cannot Be Empty!{n}\n")
      time.sleep(3)
      bash("clear")
      PctRun.login()