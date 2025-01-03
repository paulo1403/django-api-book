from pymongo import MongoClient
from django.conf import settings

class MongoDBConnection:
    _instance = None
    _client = None
    _db = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        if MongoDBConnection._client is None:
            MongoDBConnection._client = MongoClient(settings.MONGODB_URI)
            MongoDBConnection._db = MongoDBConnection._client[settings.MONGODB_NAME]

    @property
    def db(self):
        return MongoDBConnection._db

    def get_collection(self, collection_name):
        return self.db[collection_name]

    def close(self):
        if MongoDBConnection._client:
            MongoDBConnection._client.close()
            MongoDBConnection._client = None
            MongoDBConnection._db = None