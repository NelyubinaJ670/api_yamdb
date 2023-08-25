from rest_framework import viewsets, filters

from api.serializers import (
    TitleSerializer,
    GenreSerializer,
    CategorySerializer,
    UserSerializer)
from api.permissions import IsAdmin, IsAuthorModerAdminOrReadOnly
from reviews.models import Title, Genre, Category, User

from .mixins import ListCreateDestroyViewSet


class CategoryViewSet(ListCreateDestroyViewSet):
    '''Вьюсет для модели Категории.
       Делать Get запрос может любой пользователь.
       Редактировать или удалять только админ.
    '''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDestroyViewSet):
    '''Вьюсет для модели Жанры.
       Делать Get запрос может любой пользователь.
       Редактировать или удалять только админ.
    '''
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    '''Вьюсет для создания Произведений.
       Делать Get запрос может любой пользователь.
       Редактировать или удалять только админ.
    '''
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly, IsAuthenticatedOrReadOnly)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'year',)


class UserViewSet(viewsets.ModelViewSet):
    '''Вьюсет для Пользователя. Доступ только у администратора'''
    queryset = User.objects.all()
    permission_classes = (IsAdmin,)
    serializer_class = UserSerializer


def signup_user(request):
    '''Регистрация пользователя через API'''


def get_token(request):
    '''Получение токена через API'''
