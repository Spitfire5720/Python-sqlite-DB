import sqlite3
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

#initialize FastAPI 

app = FastAPI()

#connect to database https://www.sqlite.org/download.html / https://www.tutorialspoint.com/sqlite/sqlite_python.htm

try:
    conn = sqlite3.connect('PhotonVars.db')
    print ("Opened database succsessfully.")
except sqlite3.error as error:
    print("Failed to connect with sqlite3 database.", error)
    
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS nodes")

#defining API response structure https://docs.pydantic.dev/latest/

class NodeRequest(BaseModel):
    parent_path: str
    node_name: str

class NodeResponse(BaseModel):
    message: str

#defining node structure for database
#define the Node class https://stackoverflow.com/questions/69878375/how-to-create-tree-structure-from-hierarchical-data-in-python

class Node:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.children = []
        self.value = None
        self.properties = None

    def add_child(self, child):
        self.children.append(child)

# define the function to recursively insert nodes into the database

def insert_node(cursor, node, parent_path=""):
    path = f"{parent_path}/{node.name}" if parent_path else node.name

    if node.properties:
        cursor.execute("INSERT INTO nodes (path, value) VALUES (?, ?)", (path, node.properties[1]))

    if node.value:
        cursor.execute("INSERT INTO nodes (path, value) VALUES (?, ?)", (path, node.value[1]))

    for child in node.children:
        insert_node(cursor, child, path)

# initialize the root node

root = Node("Rocket", None)
root.properties = ("Rocket", None)

# populate the hierarchical structure

height = Node("Height", root)
height.properties = ("Rocket/Height", 18.000)
root.add_child(height)

mass = Node("Mass", root)
mass.value = ("Rocket/Mass", 12000.000)
root.add_child(mass)

stage1 = Node("Stage1", root)
root.add_child(stage1)

engine1 = Node("Engine1", stage1)
engine1.value = ("Rocket/Stage1/Engine1", None)
stage1.add_child(engine1)

thrust1 = Node("Thrust", engine1)
thrust1.value = ("Rocket/Stage1/Engine1/Thrust", 9.493)
engine1.add_child(thrust1)

isp1 = Node("ISP", engine1)
isp1.value = ("Rocket/Stage1/Engine1/ISP", 12.156)
engine1.add_child(isp1)

thrust2 = Node("Thrust", engine1)
thrust2.value = ("Rocket/Stage1/Engine2/Thrust", 9.413)
engine1.add_child(thrust2)

isp2 = Node("ISP", engine1)
isp2.value = ("Rocket/Stage1/Engine2/ISP", 11.632)
engine1.add_child(isp2)

thrust3 = Node("Thrust", engine1)
thrust3.value = ("Rocket/Stage1/Engine3/Thrust", 9.899)
engine1.add_child(thrust3)

isp3 = Node("ISP", engine1)
isp3.value = ("Rocket/Stage1/Engine3/ISP", 12.551)
engine1.add_child(isp3)

# create and connect to the SQLite database

conn = sqlite3.connect('PhotonVars.db')
cursor = conn.cursor()

# create a table to store the nodes

cursor.execute('''CREATE TABLE IF NOT EXISTS nodes
                (id INTEGER PRIMARY KEY,
                path TEXT,
                value REAL)''')
print("Database created successfully.")

# insert the root node and its descendants into the database

insert_node(cursor, root)

#output values in database to terminal

cursor.execute('''SELECT * FROM NODES''')
print(cursor.fetchall())
conn.commit()
print("Table successfully populated.")

if conn:
  conn.close()
  print("Connection to sqlite3 is closed.")

#defining endpoints https://fastapi.tiangolo.com / https://code.visualstudio.com/docs/python/tutorial-fastapi

@app.post('/create_node')
async def create_node(request: Request, node_request: NodeRequest):
  data = await request.json()
  parent_path = data.get('parent_path')
  node_name = data.get('node_name')
  parent_node = cursor.execute("SELECT * FROM nodes WHERE path = ?", (parent_path,)).fetchone()
  if parent_node: 
    new_node= Node(node_name, parent_node)
    cursor.execute("INSERT INTO nodes (path) VALUES (?)", (f"{parent_path}/{node_name}",))
    conn.commit()
    return {'message': f"Node {node_name} created under {parent_path}"}
  else: 
    raise HTTPException(status_code=404, detail='Parent node not found')

#endpoint to add a property on a specific node

@app.post('/add_property')
async def add_property(request: Request):
  data = await request.json()
  node_path = data.get('node_path')
  property_name = data.get('property_name')
  property_value = data.get('property_value')
  node = cursor.execute("SELECT * FROM nodes WHERE path = ?", (node_path,)).fetchone()
  if node: 
      cursor.execute("INSERT INTO nodes (path, value) VALUES (?,?)", (f"{node_path}/{property_name}", property_value))
      conn.commit() 
      return {'message': f'Property {property_name} added to node {node_path}'}
  else:
      raise HTTPException(status_code=404, detail='Node not found')

# endpoint to return the subtree of nodes with their properties for a provided node path

@app.get('/get_subtree')
async def get_subtree(node_path: str):
  subtree = cursor.execute ("SELECT * FROM nodes WHERE path LIKE ?",(f"{node_path}%",)).fetchall()
  if subtree: 
    return subtree
  else: 
    raise HTTPException(status_code=404, detail='Subtree not found')

if __name__ == '__main__':
  import uvicorn
  uvicorn.run(app, host="0.0.0.0", port=8000)