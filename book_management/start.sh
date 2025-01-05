#!/bin/bash

# Verify MongoDB connection
python << END
from pymongo import MongoClient
import os, sys

try:
    client = MongoClient(os.getenv('MONGODB_URI'))
    db = client[os.getenv('MONGODB_NAME', 'book_management')]
    # Test the connection
    db.command('ping')
    print("MongoDB connection successful")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    sys.exit(1)
END

# Start Gunicorn
exec gunicorn book_management.wsgi:application --bind 0.0.0.0:$PORT
