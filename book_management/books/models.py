from django.utils import timezone
from bson import ObjectId
from datetime import datetime
from pymongo import MongoClient
import os

# MongoDB connection
client = MongoClient(os.getenv('MONGODB_URI'))
db = client[os.getenv('MONGODB_NAME', 'book_management')]

class Book:
    collection = db['books']

    def __init__(self, title, author, published_date, genre, price, _id=None):
        self._id = _id if _id else ObjectId()
        self.title = title
        self.author = author
        if isinstance(published_date, datetime):
            self.published_date = published_date
        else:
            self.published_date = datetime.combine(published_date, datetime.min.time())
        self.genre = genre
        self.price = float(price)
        self.created_at = timezone.now()
        self.updated_at = timezone.now()

    @classmethod
    def from_db(cls, data):
        # Método de clase para crear una instancia de Book a partir de datos de la base de datos
        if not data:
            return None
        return cls(
            _id=data.get('_id'),
            title=data.get('title'),
            author=data.get('author'),
            published_date=data.get('published_date'),
            genre=data.get('genre'),
            price=data.get('price')
        )

    def to_dict(self):
        # Método de instancia para convertir los atributos del libro en un diccionario
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

    def save(self):
        data = self.to_dict()
        if hasattr(self, '_id'):
            self.collection.update_one(
                {'_id': self._id},
                {'$set': data},
                upsert=True
            )
        return self

    @classmethod
    def find_all(cls):
        return [cls.from_db(doc) for doc in cls.collection.find()]

    @classmethod
    def find_by_id(cls, id):
        doc = cls.collection.find_one({'_id': ObjectId(id)})
        return cls.from_db(doc) if doc else None

    def delete(self):
        if hasattr(self, '_id'):
            self.collection.delete_one({'_id': self._id})