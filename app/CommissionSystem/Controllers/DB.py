from pymongo import MongoClient
from pymongo.database import Database, Collection
from gridfs import GridFS
from . import Env


client: MongoClient = MongoClient(Env.MONGO_URI)
db: Database = client[Env.DATABASE_NAME]

fs: GridFS = GridFS(db)

collection_user: Collection = db["users"]
collection_user_token: Collection = db["user_tokens"]
collection_commission: Collection = db["commissions"]
