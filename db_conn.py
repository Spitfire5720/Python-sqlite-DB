#!/usr/bin/env python

import fastapi
import sqlite3
import requests
from pydantic import Basemodel


#setting up API endpoints
app = fastapi.FastAPI()

@app.get("/")
def read_root():
  return {"Hello": "World"}

  api_url = 'postman-echo.com/get'
response = requests.get(api_url)
response.json()

#connect to database

try:
  conn = sqlite3.connect('PhotonVars.db')
  print ("Opened database succsessfully.")
except sqlite3.error as error:
  print("Failed to connect with sqlite3 database.", error)
finally:
  if conn:
    conn.close
    print("Connection to sqlite3 is closed.")

#Dropping table if it already exists
    
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS PHOTONVARS")

# create table in database

table = ("""CREATE TABLE PHOTONVARS (
         ID    INT PRIMARY KEY NOT NULL,
         PATH  VARCHAR(40) NOT NULL,
         VALUE INT);""")
    
conn.execute(table)
print("Table created successfully.")
conn.commit()

class node:
  def __init__(self, name, value):
    self.value = value
    self.name = name
    self.children = []
  def addchild(self, child):
    self.children.append(child)
  def printn(self):
    s={} 
    for child in self.children:
      s[child.name] = child.printn(self.value)
    return s
  
#seed database reference from (https://www.tutorialspoint.com/python_data_access/python_sqlite_insert_data.htm)
    
conn.execute("INSERT INTO PHOTONVARS (ID,PATH,VALUE) VALUES (1, 'Rocket', NULL)")
conn.execute("INSERT INTO PHOTONVARS (ID,PATH,VALUE) VALUES (2, 'Rocket/Height', 18.000)")
conn.execute("INSERT INTO PHOTONVARS (ID,PATH,VALUE) VALUES (3, 'Rocket/Mass', 12000.000)")
conn.execute("INSERT INTO PHOTONVARS (ID,PATH,VALUE) VALUES (4, 'Rocket/Stage1', NULL)")
conn.execute("INSERT INTO PHOTONVARS (ID,PATH,VALUE) VALUES (5, 'Rocket/Stage1/Engine1', NULL)")
conn.execute("INSERT INTO PHOTONVARS (ID,PATH,VALUE) VALUES (6, 'Rocket/Stage1/Engine1/Thrust', 9.493)") 
conn.execute("INSERT INTO PHOTONVARS (ID,PATH,VALUE) VALUES (7, 'Rocket/Stage1/Engine1/ISP', 12.156)")
conn.execute("INSERT INTO PHOTONVARS (ID,PATH,VALUE) VALUES (8, 'Rocket/Stage1/Engine2', NULL)")
conn.execute("INSERT INTO PHOTONVARS (ID,PATH,VALUE) VALUES (9, 'Rocket/Stage1/Engine2/Thrust', 9.413)")
conn.execute("INSERT INTO PHOTONVARS (ID,PATH,VALUE) VALUES (10, 'Rocket/Stage1/Engine2/ISP', 11.632)")
conn.execute("INSERT INTO PHOTONVARS (ID,PATH,VALUE) VALUES (11, 'Rocket/Stage1/Engine3/', NULL)")
conn.execute("INSERT INTO PHOTONVARS (ID,PATH,VALUE) VALUES (12, 'Rocket/Stage1/Engine3/Thrust', 9.899)")
conn.execute("INSERT INTO PHOTONVARS (ID,PATH,VALUE) VALUES (13, 'Rocket/Stage1/Engine3/ISP', 12.551)")
conn.execute("INSERT INTO PHOTONVARS (ID,PATH,VALUE) VALUES (14, 'Rocket/Stage2/', NULL)")
conn.execute("INSERT INTO PHOTONVARS (ID,PATH,VALUE) VALUES (15, 'Rocket/Stage2/Engine1/', NULL)")
conn.execute("INSERT INTO PHOTONVARS (ID,PATH,VALUE) VALUES (16, 'Rocket/Stage2/Engine1/Thrust/', 1.622)")
conn.execute("INSERT INTO PHOTONVARS (ID,PATH,VALUE) VALUES (17, 'Rocket/Stage2/Engine1/ISP/', 15.110)")

rocketdb = cursor.execute('''SELECT * from PHOTONVARS''')
print(cursor.fetchall())
print("Table successfully populated.")
conn.commit()

