from rest_framework import serializers

from reviews.models import Title, Genre, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = (
            'id', 'name', 'category', 'genre',
            'description', 'year',
        )
