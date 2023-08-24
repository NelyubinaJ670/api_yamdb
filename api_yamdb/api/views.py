from rest_framework import viewsets

from api.serializers import (
    TitleSerializer,
    GenreSerializer,
    CategorySerializer,
    UserSerializer)
from api.permissions import IsAdmin, IsAuthorModerAdminOrReadOnly
from reviews.models import Title, Genre, Category, User


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


class UserViewSet(viewsets.ModelViewSet):
    '''Вьюсет для Пользователя. Доступ только у администратора'''
    queryset = User.objects.all()
    permission_classes = (IsAdmin,)
    serializer_class = UserSerializer


def signup_user(request):
    '''Регистрация пользователя через API'''


def get_token(request):
    '''Получение токена через API'''
