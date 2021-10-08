from flask_pymongo import pymongo
import certifi
ca = certifi.where()

CONNECTION_STRING = "mongodb+srv://madhu:madhu@cluster0.fudtl.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

client = pymongo.MongoClient(CONNECTION_STRING, tlsCAFile=ca)

db = client.get_database('library')
