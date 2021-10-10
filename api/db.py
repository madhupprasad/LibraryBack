from dotenv import load_dotenv
from flask_pymongo import pymongo
import certifi
import os
from os.path import join, dirname
ca = certifi.where()

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

SECRET_KEY = os.environ.get("SECRET_KEY")

client = pymongo.MongoClient(SECRET_KEY, tlsCAFile=ca)

db = client.get_database('library')
