from pymongo import MongoClient
from pymongo.database import Database
from gridfs import GridFS
from . import Env

client: MongoClient = MongoClient(Env.MONGO_URI)
db: Database = client[Env.DATABASE_NAME]
fs: GridFS = GridFS(db)
