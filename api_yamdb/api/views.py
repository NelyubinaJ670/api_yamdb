from rest_framework import viewsets
from rest_framework.generics import get_object_or_404

from api.serializers import (
    TitleSerializer,
    GenreSerializer,
    CategorySerializer,
    UserSerializer,
    CommentSerializer,
    ReviewCreateSerializer,
    ReviewSerializer)
from api.permissions import IsAdmin, IsAuthorModerAdminOrReadOnly
from reviews.models import Title, Genre, Category, User, Review


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


class ReviewViewSet(viewsets.ModelViewSet):
    """Отображение действий с отзывами"""
    serializer_class = ReviewSerializer
    permission_classes = IsAuthorModerAdminOrReadOnly

    def get_serializer_class(self):
        if self.action == 'create':
            return ReviewCreateSerializer
        return ReviewSerializer

    def get_queryset(self):
        title = get_object_or_404(
            Title, id=self.kwargs.get('title_id')
        )
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title, id=self.kwargs.get('title_id')
        )
        serializer.save(title=title, author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Отображение действий с комментариями"""
    serializer_class = CommentSerializer
    permission_classes = IsAuthorModerAdminOrReadOnly

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id'),
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id'),
        )
        serializer.save(review=review, author=self.request.user)
