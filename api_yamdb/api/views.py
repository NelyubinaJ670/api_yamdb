from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.permissions import IsAdmin, IsAuthorModerAdminOrReadOnly
from reviews.models import Category, Genre, Title, User, Review
from .serializers import (
  CategorySerializer, 
  GenreSerializer, 
  TitleSerializer,
  GetTokenSerializer, 
  SignUpSerializer, 
  UserSerializer,
  CommentSerializer,
  ReviewCreateSerializer,
  ReviewSerializer)


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


@api_view(['POST'])
@permission_classes([AllowAny])
def signup_user(request):
    '''Регистрация пользователя через API'''
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data['email']
    username = serializer.validated_data['username']

    '''Здесь должна быть проверка на уникальность при создании юзера'''

    confirmation_code = default_token_generator.make_token(user)
    message = (
        f'Ваш код подтвержения: {confirmation_code}\n'
        'Перейдите по адресу '
        'http://127.0.0.1:8000/api/v1/auth/token/ и введите код '
        'вместе вашим username'
    )

    send_mail(
        'Регистрация завершена',
        message,
        'webmaster@localhost',
        [email, ],
    )
    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    '''Получение токена через API'''
    serializer = GetTokenSerializer(data=request.data)
    if serializer.is_valid():
        confirmation_code = serializer.validated_data['confirmation_code']
        username = serializer.validated_data['username']
        user = get_object_or_404(User, username=username)

        if default_token_generator.check_token(user, confirmation_code):
            access = AccessToken.for_user(user)
            return Response(
                {
                    'token': f'Bearer {access}',
                },
                status=status.HTTP_201_CREATED
            )
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


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
