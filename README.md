# Book Management API

A RESTful API built with Django REST Framework for managing books with MongoDB integration and JWT authentication.

## Prerequisites

- Python 3.8+
- MongoDB
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd book_management
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with the following variables:
```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
MONGODB_URI=mongodb://localhost:27017
MONGODB_NAME=book_management
```

5. Apply database migrations:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

## Running the Project

1. Start the development server:
```bash
python manage.py runserver
```

2. Access the API at: http://localhost:8000/api/

## API Documentation

The API documentation is available at:
- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/

## Authentication

The API supports both JWT and Token authentication.

### JWT Authentication

1. Obtain access token:
```bash
POST /api/token/
{
    "username": "your_username",
    "password": "your_password"
}
```

2. Use the token in requests:
```bash
Authorization: Bearer <your_access_token>
```

3. Refresh token:
```bash
POST /api/token/refresh/
{
    "refresh": "<your_refresh_token>"
}
```

## API Endpoints

- `POST /api/token/` - Obtain JWT token
- `POST /api/token/refresh/` - Refresh JWT token
- `GET /api/books/` - List all books
- `POST /api/books/` - Create a new book
- `GET /api/books/{id}/` - Retrieve a book
- `PUT /api/books/{id}/` - Update a book
- `DELETE /api/books/{id}/` - Delete a book
- `GET /api/books/stats/{year}/` - Get book statistics for a specific year

## Book Model Fields

- `title` (string): Book title
- `author` (string): Book author
- `published_date` (date): Publication date
- `isbn` (string): ISBN number
- `price` (decimal): Book price
- `quantity` (integer): Available quantity
- `created_at` (datetime): Creation timestamp
- `updated_at` (datetime): Last update timestamp

## Development

To run tests:
```bash
python manage.py test
```

## Security Notes

- Never commit the `.env` file
- Change the SECRET_KEY in production
- Set DEBUG=False in production
- Update ALLOWED_HOSTS for production environment
