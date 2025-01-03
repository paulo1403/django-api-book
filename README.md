# API de Gestión de Libros

Una API RESTful construida con Django REST Framework para la gestión de libros con integración MongoDB y autenticación JWT.

## Requisitos Previos

- Python 3.8+
- MongoDB
- pip (gestor de paquetes de Python)

## Instalación

1. Clonar el repositorio:
```bash
git clone <url-repositorio>
cd book_management
```

2. Crear y activar el entorno virtual:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/MacOS
source venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Crear un archivo `.env` en el directorio raíz con las siguientes variables:
```
SECRET_KEY=tu-clave-secreta
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
MONGODB_URI=mongodb://localhost:27017
MONGODB_NAME=book_management
```

5. Aplicar migraciones de la base de datos:
```bash
python manage.py migrate
```

6. Crear un superusuario:
```bash
python manage.py createsuperuser
```

## Ejecutar el Proyecto

1. Iniciar el servidor de desarrollo:
```bash
python manage.py runserver
```

2. Acceder a la API en: http://localhost:8000/api/

## Documentación de la API

La documentación de la API está disponible en:
- Swagger UI: http://localhost:8000/swagger/

## Autenticación

La API soporta autenticación JWT y Token.

### Autenticación JWT

1. Obtener token de acceso:
```bash
POST /api/token/
{
    "username": "tu_usuario",
    "password": "tu_contraseña"
}
```

2. Usar el token en las peticiones:
```bash
Authorization: Bearer <tu_token_de_acceso>
```

3. Refrescar token:
```bash
POST /api/token/refresh/
{
    "refresh": "<tu_token_de_refresco>"
}
```

## Endpoints de la API

- `POST /api/token/` - Obtener token JWT
- `POST /api/token/refresh/` - Refrescar token JWT
- `GET /api/books/` - Listar todos los libros
- `POST /api/books/` - Crear un nuevo libro
- `GET /api/books/{id}/` - Obtener un libro
- `PUT /api/books/{id}/` - Actualizar un libro
- `DELETE /api/books/{id}/` - Eliminar un libro
- `GET /api/books/stats/{year}/` - Obtener estadísticas de libros por año

## Campos del Modelo de Libro

- `title` (string): Título del libro
- `author` (string): Autor del libro
- `published_date` (date): Fecha de publicación
- `isbn` (string): Número ISBN
- `price` (decimal): Precio del libro
- `quantity` (integer): Cantidad disponible
- `created_at` (datetime): Fecha de creación
- `updated_at` (datetime): Fecha de última actualización

## Desarrollo

Para ejecutar las pruebas:
```bash
pytest
```

Para ejecutar las pruebas con coverage:
```bash
pytest --cov=books
```

## Notas de Seguridad

- Nunca commits del archivo `.env`
- Cambiar la SECRET_KEY en producción
- Establecer DEBUG=False en producción
- Actualizar ALLOWED_HOSTS para el entorno de producción
