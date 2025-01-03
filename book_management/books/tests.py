from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Book
from .utils.mongo_connection import MongoDBConnection

class BookAPITests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.client = APIClient()
        
        self.mongo = MongoDBConnection.get_instance()
        self.books_collection = self.mongo.get_collection(Book.collection_name)
        
        self.valid_book_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'published_date': '2023-01-01',
            'genre': 'Test Genre',
            'price': '29.99'
        }

    def tearDown(self):
        self.books_collection.delete_many({})

    def test_create_book(self):
        self.client.force_authenticate(user=self.user)
        
        response = self.client.post('/api/books/', self.valid_book_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], self.valid_book_data['title'])

    def test_get_books_list(self):
        self.client.force_authenticate(user=self.user)
        
        book = Book(**self.valid_book_data)
        self.books_collection.insert_one(book.to_dict())
        
        response = self.client.get('/api/books/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_get_book_detail(self):
        self.client.force_authenticate(user=self.user)
        
        book = Book(**self.valid_book_data)
        result = self.books_collection.insert_one(book.to_dict())
        book_id = str(result.inserted_id)
        
        response = self.client.get(f'/api/books/{book_id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.valid_book_data['title'])

    def test_update_book(self):
        self.client.force_authenticate(user=self.user)
        
        book = Book(**self.valid_book_data)
        result = self.books_collection.insert_one(book.to_dict())
        book_id = str(result.inserted_id)
        
        updated_data = self.valid_book_data.copy()
        updated_data['title'] = 'Updated Title'
        
        response = self.client.put(f'/api/books/{book_id}/', updated_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Title')

    def test_delete_book(self):
        self.client.force_authenticate(user=self.user)
        
        book = Book(**self.valid_book_data)
        result = self.books_collection.insert_one(book.to_dict())
        book_id = str(result.inserted_id)
        
        response = self.client.delete(f'/api/books/{book_id}/')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        self.assertIsNone(self.books_collection.find_one({'_id': result.inserted_id}))

    def test_unauthorized_access(self):
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
