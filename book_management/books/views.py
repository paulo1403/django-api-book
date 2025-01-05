from rest_framework import status, generics, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.conf import settings
from bson import ObjectId
from datetime import datetime
from .serializers.book_serializer import BookSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication

# Registro de Usuarios
class UserSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'password_confirmation')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError({
                'password_confirmation': 'Passwords do not match'
            })
        return data

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
                'message': 'User created successfully',
                'id': user.id,
                'username': user.username,
                'email': user.email
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Vistas de Libros
class BookListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        books = settings.MONGODB_DB.books.find()
        book_list = [{**book, '_id': str(book['_id'])} for book in books]
        return Response(book_list)

    def post(self, request):
        book_data = request.data.copy()
        book_data['created_at'] = datetime.utcnow()
        book_data['updated_at'] = datetime.utcnow()
        
        result = settings.MONGODB_DB.books.insert_one(book_data)
        book_data['_id'] = str(result.inserted_id)
        return Response(book_data, status=status.HTTP_201_CREATED)

class BookDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            book = settings.MONGODB_DB.books.find_one({'_id': ObjectId(pk)})
            if book:
                book['_id'] = str(book['_id'])
                return Response(book)
            return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            book_data = request.data.copy()
            book_data['updated_at'] = datetime.utcnow()
            
            result = settings.MONGODB_DB.books.find_one_and_update(
                {'_id': ObjectId(pk)},
                {'$set': book_data},
                return_document=True
            )
            
            if result:
                result['_id'] = str(result['_id'])
                return Response(result)
            return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            result = settings.MONGODB_DB.books.delete_one({'_id': ObjectId(pk)})
            if result.deleted_count:
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class BookYearStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, year):
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
        
        stats = list(settings.MONGODB_DB.books.aggregate(pipeline))
        
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

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'date_joined': user.date_joined
        })

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        # Eliminar el token del usuario
        Token.objects.filter(user=request.user).delete()
        return Response({'message': 'Successfully logged out'}, 
                      status=status.HTTP_200_OK)