from datetime import datetime
from bson import ObjectId
from .utils.mongo_connection import MongoDBConnection

class Book:
    collection_name = 'books'

    def __init__(self, title, author, published_date, genre, price, _id=None):
        self._id = ObjectId(_id) if _id else ObjectId()
        self.title = title
        self.author = author
        self.published_date = published_date
        self.genre = genre
        self.price = float(price)
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    @classmethod
    def get_collection(cls):
        mongo = MongoDBConnection.get_instance()
        return mongo.get_collection(cls.collection_name)

    def to_dict(self):
        return {
            '_id': self._id,
            'title': self.title,
            'author': self.author,
            'published_date': self.published_date,
            'genre': self.genre,
            'price': self.price,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    @classmethod
    def from_dict(cls, data):
        if not data:
            return None
        return cls(
            _id=str(data['_id']),
            title=data['title'],
            author=data['author'],
            published_date=data['published_date'],
            genre=data['genre'],
            price=data['price']
        )