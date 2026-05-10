#en consola

# mongod --dbpath D:\mis_datos\mongo
# instalar extension mongodb for vscode
# pip install pymongo 

#despues de ejecutar el comando mongod, se ejecuta el siguiente codigo en python para conectarse a la base de datos y crear una base de datos llamada "mydatabase"

from pymongo import MongoClient

#db_client = MongoClient().local # conecta a localhost:27017

db_client = MongoClient('mongodb+srv://jorgevalentini76_db_user:test@cluster0.zxuyf5r.mongodb.net/?appName=Cluster0').escuela # conecta a localhost:27017

db = db_client["escuela"]


