from rest_framework import viewsets

from reviews.models import Title, Genre, Category
from .serializers import TitleSerializer, GenreSerializer, CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    '''Вьюсет для модели Категории. Читать может любой пользователь'''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(viewsets.ModelViewSet):
    '''Вьюсет для модели Жанры. Читать может любой пользователь'''
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    '''Вьюсет для Произведений. Читать может любой пользователь'''
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
