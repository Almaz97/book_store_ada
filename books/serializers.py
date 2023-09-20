from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Genre, Publisher, Book, BookLike, BookComment
from .utils import send_email


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ['id', 'title']


class PublisherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Publisher
        fields = ['id', 'name', 'address', 'country', 'website']


class BookSerializer(serializers.ModelSerializer):
    num_likes = serializers.IntegerField(read_only=True)

    def to_representation(self, instance):
        res = super().to_representation(instance)
        res['genre'] = GenreSerializer(instance=instance.genre.all(), many=True).data
        return res

    def validate(self, attrs):
        attrs = super().validate(attrs)
        amount_of_pages = attrs['amount_of_pages']
        if amount_of_pages < 0:
            raise serializers.ValidationError("amount_of_pages should be > 0")

        if amount_of_pages > 3000:
            raise serializers.ValidationError("amount_of_pages should be < 3000")

        return attrs

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        book = super().create(validated_data)
        return book

    class Meta:
        model = Book
        fields = ['id', 'title', 'description', 'genre', 'amount_of_pages',
                  'author', 'publisher', 'created_at', 'updated_at', 'num_likes',
                  'created_by']


class BookCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookComment
        fields = ['id', 'book', 'user', 'content']
