from rest_framework import serializers
from datetime import datetime


class BookSerializer(serializers.Serializer):
    id = serializers.CharField(source="_id", read_only=True)
    title = serializers.CharField(max_length=200)
    author = serializers.CharField(max_length=200)
    published_date = serializers.DateTimeField()
    genre = serializers.CharField(max_length=100)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative")
        return float(value)

    def validate_published_date(self, value):
        if isinstance(value, datetime):
            compare_date = value.date()
        else:
            compare_date = value
            value = datetime.combine(value, datetime.min.time())

        if compare_date > datetime.now().date():
            raise serializers.ValidationError("Published date cannot be in the future")
        return value
