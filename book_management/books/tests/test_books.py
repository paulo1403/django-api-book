import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from datetime import datetime
from ..models import Book
from ..utils.mongo_connection import MongoDBConnection
from bson import ObjectId

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def test_user():
    user = User.objects.create_user(
        username='testuser',
        password='testpass123'
    )
    return user

@pytest.fixture
def auth_client(api_client, test_user):
    api_client.force_authenticate(user=test_user)
    return api_client

@pytest.fixture
def mongo_connection():
    connection = MongoDBConnection.get_instance()
    # Limpiar la colección antes de cada test
    connection.get_collection(Book.collection_name).delete_many({})
    return connection

@pytest.fixture
def sample_book():
    return {
        "title": "Test Book",
        "author": "Test Author",
        "published_date": "2023-01-01",
        "genre": "Test Genre",
        "price": 29.99
    }

@pytest.mark.django_db
class TestBookAPI:
    def test_create_book(self, auth_client, mongo_connection, sample_book):
        response = auth_client.post('/api/books/', sample_book, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == sample_book['title']
        
        # Verificar en MongoDB
        book_collection = mongo_connection.get_collection(Book.collection_name)
        saved_book = book_collection.find_one({'title': sample_book['title']})
        assert saved_book is not None
        assert saved_book['author'] == sample_book['author']

    def test_list_books(self, auth_client, mongo_connection, sample_book):
        # Crear un libro primero
        book_collection = mongo_connection.get_collection(Book.collection_name)
        book_collection.insert_one({
            **sample_book,
            'published_date': datetime.strptime(sample_book['published_date'], '%Y-%m-%d'),
            '_id': ObjectId()
        })

        response = auth_client.get('/api/books/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['title'] == sample_book['title']

    def test_retrieve_book(self, auth_client, mongo_connection, sample_book):
        # Crear un libro
        book_collection = mongo_connection.get_collection(Book.collection_name)
        book_id = ObjectId()
        book_collection.insert_one({
            **sample_book,
            'published_date': datetime.strptime(sample_book['published_date'], '%Y-%m-%d'),
            '_id': book_id
        })

        response = auth_client.get(f'/api/books/{book_id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == sample_book['title']

    def test_update_book(self, auth_client, mongo_connection, sample_book):
        # Crear un libro
        book_collection = mongo_connection.get_collection(Book.collection_name)
        book_id = ObjectId()
        book_collection.insert_one({
            **sample_book,
            'published_date': datetime.strptime(sample_book['published_date'], '%Y-%m-%d'),
            '_id': book_id
        })

        updated_data = {
            **sample_book,
            'title': 'Updated Title'
        }

        response = auth_client.put(f'/api/books/{book_id}/', updated_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Updated Title'

        # Verificar en MongoDB
        updated_book = book_collection.find_one({'_id': book_id})
        assert updated_book['title'] == 'Updated Title'

    def test_delete_book(self, auth_client, mongo_connection, sample_book):
        # Crear un libro
        book_collection = mongo_connection.get_collection(Book.collection_name)
        book_id = ObjectId()
        book_collection.insert_one({
            **sample_book,
            'published_date': datetime.strptime(sample_book['published_date'], '%Y-%m-%d'),
            '_id': book_id
        })

        response = auth_client.delete(f'/api/books/{book_id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verificar que el libro fue eliminado
        deleted_book = book_collection.find_one({'_id': book_id})
        assert deleted_book is None

    def test_year_stats(self, auth_client, mongo_connection, sample_book):
        # Crear varios libros del mismo año
        book_collection = mongo_connection.get_collection(Book.collection_name)
        books = [
            {
                **sample_book,
                'price': 20.00,
                'published_date': datetime(2023, 1, 1)
            },
            {
                **sample_book,
                'price': 30.00,
                'published_date': datetime(2023, 6, 1)
            }
        ]
        book_collection.insert_many(books)

        response = auth_client.get('/api/books/stats/year/2023/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['average_price'] == 25.00
        assert response.data['total_books'] == 2

    def test_unauthorized_access(self, api_client, sample_book):
        response = api_client.post('/api/books/', sample_book, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_invalid_book_data(self, auth_client):
        invalid_book = {
            "title": "Test Book",
            # Falta el autor
            "published_date": "2023-01-01",
            "genre": "Test Genre",
            "price": -10.00  # Precio negativo
        }
        response = auth_client.post('/api/books/', invalid_book, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST