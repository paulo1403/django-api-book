from django.db import models
from django.utils import timezone

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    published_date = models.DateField()
    genre = models.CharField(max_length=100)
    price = models.FloatField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'books'
        managed = True

    def __str__(self):
        return self.title