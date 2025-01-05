FROM python:3.12

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT=8000

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create static directory and collect static files
RUN mkdir -p staticfiles
RUN python manage.py collectstatic --noinput

# Set up start script
COPY start.sh .
RUN chmod +x start.sh

CMD ["./start.sh"]
