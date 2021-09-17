from flask_pymongo import pymongo

CONNECTION_STRING = "mongodb+srv://madhu:madhu@cluster0.fudtl.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

client = pymongo.MongoClient(CONNECTION_STRING)

db = client.get_database('library')

user_collection = pymongo.collection.Collection(db, 'users')