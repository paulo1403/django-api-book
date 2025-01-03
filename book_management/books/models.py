from django.utils import timezone
from bson import ObjectId
from datetime import datetime

class Book:
    collection_name = 'books'

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