from django.core.management.base import BaseCommand
from books.models import Book
from books.utils.mongo_connection import MongoDBConnection
from datetime import datetime

class Command(BaseCommand):
    help = 'Carga datos iniciales de libros en MongoDB'

    def handle(self, *args, **kwargs):
        initial_books = [
            {
                "title": "Cien años de soledad",
                "author": "Gabriel García Márquez",
                "published_date": datetime(1967, 5, 30),
                "genre": "Realismo mágico",
                "price": 25.99,
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            },
            {
                "title": "1984",
                "author": "George Orwell",
                "published_date": datetime(1949, 6, 8),
                "genre": "Ciencia ficción",
                "price": 19.99,
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            },
            {
                "title": "El principito",
                "author": "Antoine de Saint-Exupéry",
                "published_date": datetime(1943, 4, 6),
                "genre": "Literatura infantil",
                "price": 15.99,
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            },
            {
                "title": "Don Quijote de la Mancha",
                "author": "Miguel de Cervantes",
                "published_date": datetime(1605, 1, 1),
                "genre": "Novela",
                "price": 29.99,
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            },
            {
                "title": "Rayuela",
                "author": "Julio Cortázar",
                "published_date": datetime(1963, 6, 28),
                "genre": "Novela experimental",
                "price": 22.99,
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            },
            {
                "title": "La Casa de los Espíritus",
                "author": "Isabel Allende",
                "published_date": datetime(2000, 1, 15),
                "genre": "Realismo mágico",
                "price": 23.99,
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            },
            {
                "title": "Memoria de mis Putas Tristes",
                "author": "Gabriel García Márquez",
                "published_date": datetime(2000, 1, 15),
                "genre": "Novela",
                "price": 21.99,
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            },
            {
                "title": "La Sombra del Viento",
                "author": "Carlos Ruiz Zafón",
                "published_date": datetime(2000, 1, 15),
                "genre": "Misterio",
                "price": 24.99,
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            }
        ]

        mongo = MongoDBConnection.get_instance()
        collection = mongo.get_collection(Book.collection_name)
        
        # Limpiar colección existente
        collection.delete_many({})
        
        # Insertar nuevos libros
        collection.insert_many(initial_books)
        
        self.stdout.write(
            self.style.SUCCESS('Se cargaron los libros iniciales correctamente')
        )
