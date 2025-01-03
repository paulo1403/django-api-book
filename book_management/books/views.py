from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils import timezone
from bson import ObjectId
from datetime import datetime
from .serializers.book_serializer import BookSerializer
from .models import Book
from .utils.mongo_connection import MongoDBConnection

# User Registration
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')
        extra_kwargs = {
            'password': {'write_only': True}
        }

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        try:
            # Validar la contraseña
            validate_password(request.data.get('password'))
        except ValidationError as e:
            return Response({'password': e.messages}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            user = User.objects.create_user(
                username=serializer.validated_data['username'],
                email=serializer.validated_data.get('email', ''),
                password=serializer.validated_data['password']
            )
            return Response({
                'id': user.id,
                'username': user.username,
                'email': user.email
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Book Views
class BookListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        mongo = MongoDBConnection.get_instance()
        books_collection = mongo.get_collection(Book.collection_name)
        books = books_collection.find()
        
        # Convertir a lista y serializar
        book_list = [Book.from_db(book) for book in books]
        serializer = BookSerializer(book_list, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            # Crear nuevo libro
            book = Book(**serializer.validated_data)
            mongo = MongoDBConnection.get_instance()
            books_collection = mongo.get_collection(Book.collection_name)
            books_collection.insert_one(book.to_dict())
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            mongo = MongoDBConnection.get_instance()
            books_collection = mongo.get_collection(Book.collection_name)
            book_data = books_collection.find_one({'_id': ObjectId(pk)})
            return Book.from_db(book_data) if book_data else None
        except:
            return None

    def get(self, request, pk):
        book = self.get_object(pk)
        if book is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def put(self, request, pk):
        book = self.get_object(pk)
        if book is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            mongo = MongoDBConnection.get_instance()
            books_collection = mongo.get_collection(Book.collection_name)
            
            # Prepare update data
            updated_data = serializer.validated_data
            updated_data['published_date'] = datetime.strptime(request.data['published_date'], '%Y-%m-%d')
            updated_data['updated_at'] = timezone.now()
            
            # Use find_one_and_update to get the updated document
            result = books_collection.find_one_and_update(
                {'_id': ObjectId(pk)},
                {'$set': updated_data},
                return_document=True
            )
            
            if result:
                # Convert the result back to a Book object and serialize
                updated_book = Book.from_db(result)
                return Response(BookSerializer(updated_book).data)
            return Response({'error': 'Update failed'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        book = self.get_object(pk)
        if book is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        mongo = MongoDBConnection.get_instance()
        books_collection = mongo.get_collection(Book.collection_name)
        books_collection.delete_one({'_id': ObjectId(pk)})
        return Response(status=status.HTTP_204_NO_CONTENT)

class BookViewSet(viewsets.ViewSet):
    def update(self, request, pk=None):
        try:
            book_collection = Book.get_collection()
            book_data = request.data.copy()
            
            # Convert published_date string to datetime
            if 'published_date' in book_data:
                book_data['published_date'] = datetime.strptime(book_data['published_date'], '%Y-%m-%d')

            # Update the document and get the updated version
            result = book_collection.find_one_and_update(
                {'_id': ObjectId(pk)},
                {'$set': book_data},
                return_document=True
            )

            if result:
                # Convert ObjectId to string for serialization
                result['_id'] = str(result['_id'])
                # Convert datetime back to string for response
                result['published_date'] = result['published_date'].strftime('%Y-%m-%d')
                return Response(result)
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class BookYearStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, year):
        mongo = MongoDBConnection.get_instance()
        books_collection = mongo.get_collection(Book.collection_name)
        
        # Pipeline de agregación para calcular estadísticas del año
        pipeline = [
            {
                '$match': {
                    'published_date': {
                        '$gte': datetime(year, 1, 1),
                        '$lt': datetime(year + 1, 1, 1)
                    }
                }
            },
            {
                '$group': {
                    '_id': None,
                    'avg_price': {'$avg': '$price'},
                    'min_price': {'$min': '$price'},
                    'max_price': {'$max': '$price'},
                    'total_books': {'$sum': 1}
                }
            }
        ]
        
        stats = list(books_collection.aggregate(pipeline))
        
        if not stats:
            return Response({
                'message': f'No books found for year {year}'
            }, status=status.HTTP_404_NOT_FOUND)
            
        return Response({
            'year': year,
            'average_price': round(stats[0]['avg_price'], 2),
            'minimum_price': stats[0]['min_price'],
            'maximum_price': stats[0]['max_price'],
            'total_books': stats[0]['total_books']
        })