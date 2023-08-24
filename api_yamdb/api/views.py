from rest_framework import viewsets
from rest_framework.generics import get_object_or_404

from reviews.models import Title, Genre, Category, Review
from .serializers import TitleSerializer, GenreSerializer, CategorySerializer, ReviewSerializer, CommentSerializer, ReviewCreateSerializer


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


class ReviewViewSet(viewsets.ModelViewSet):
    """Отображение действий с отзывами"""
    serializer_class = ReviewSerializer
    # permission_classes = () Нужен пермишен:
    # админ,модер/автор отзыва или только чтение

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
    # permission_classes = () Нужен пермишен:
    # админ,модер/автор отзыва или только чтение

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
