#!/bin/bash

# Verify MongoDB connection
python << END
from mongoengine import connect
import os

try:
    uri = os.getenv('MONGODB_URI')
    connect(host=uri)
    print("MongoDB connection successful")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    exit(1)
END

# Start Gunicorn
exec gunicorn book_management.wsgi:application --bind 0.0.0.0:$PORT
