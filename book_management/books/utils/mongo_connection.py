from pymongo import MongoClient
from django.conf import settings

class MongoDBConnection:
    _instance = None
    _client = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        if self._client is None:
            self._client = MongoClient(
                settings.MONGODB_URI,
                ssl=True,
                ssl_cert_reqs='CERT_NONE',
                retryWrites=True,
                connectTimeoutMS=30000,
                socketTimeoutMS=None,
                connect=False,
                maxPoolSize=1
            )
            self._db = self._client[settings.MONGODB_DB.name]

    def get_collection(self, collection_name):
        return self._db[collection_name]

    def close(self):
        if self._client:
            self._client.close()