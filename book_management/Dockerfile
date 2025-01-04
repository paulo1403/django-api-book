FROM python:3.11-slim

# Establecer el directorio de trabajo
WORKDIR /app/book_management

# Instalar dependencias del sistema
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar todo el contenido del proyecto
COPY . /app/

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Recolectar archivos estáticos
RUN python manage.py collectstatic --noinput

# Puerto que expondrá la aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "book_management.wsgi"]
