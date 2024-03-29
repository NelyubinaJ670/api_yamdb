from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, serializers, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, Review, Title, User
from .filters import TitleFilter
from .mixins import ListCreateDestroyViewSet
from .pagination import UserPagination
from .permissions import AdminOrReadOnly, IsAdmin, IsAuthorModerAdminOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, GetTokenSerializer,
                          ReviewCreateSerializer, ReviewSerializer,
                          SignUpSerializer, TitleGETSerializer,
                          TitleSerializer, UserSerializer)


class CategoryViewSet(ListCreateDestroyViewSet):
    '''Вьюсет для модели Категории.
       Делать Get запрос может любой пользователь.
       Редактировать или удалять только админ.
    '''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = LimitOffsetPagination


class GenreViewSet(ListCreateDestroyViewSet):
    '''Вьюсет для модели Жанры.
       Делать Get запрос может любой пользователь.
       Редактировать или удалять только админ.
    '''
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = LimitOffsetPagination


class TitleViewSet(viewsets.ModelViewSet):
    '''Вьюсет для создания Произведений.
       Делать Get запрос может любой пользователь.
       Редактировать или удалять только админ.
    '''
    queryset = Title.objects.select_related(
        'category').annotate(rating=Avg('reviews__score'))
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filterset_class = TitleFilter
    pagination_class = LimitOffsetPagination
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        """Определяет какой сериализатор будет использоваться
        при чтении или записи произведений."""
        return (TitleGETSerializer
                if self.request.method == 'GET' else TitleSerializer)


class UserViewSet(viewsets.ModelViewSet):
    '''Вьюсет для Пользователя. Доступ только у администратора'''
    http_method_names = ['get', 'post', 'head', 'delete', 'patch']
    queryset = User.objects.all()
    permission_classes = (IsAdmin,)
    pagination_class = UserPagination
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        detail=False,
        methods=('GET', 'PATCH'),
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)

        serializer = self.get_serializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data.get('role'):
            serializer.validated_data['role'] = request.user.role
        serializer.save()
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup_user(request):
    '''Регистрация пользователя через API'''
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data['email']
    username = serializer.validated_data['username']

    try:
        user, _ = User.objects.get_or_create(
            email=email,
            username=username
        )
    except IntegrityError:
        raise serializers.ValidationError('Такой пользователь уже существует')

    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Регистрация завершена',
        settings.MESSAGE.format(
            confirmation_code,
            settings.DEFAULT_URL_GET_TOKEN,
        ),
        settings.DEFAULT_FROM_MAIL,
        [email]
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
    permission_classes = (IsAuthorModerAdminOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        return (ReviewCreateSerializer
                if self.action == 'create' else ReviewSerializer)

    def get_queryset(self):
        title = get_object_or_404(
            Title, id=self.kwargs.get('title_id')
        )
        return title.reviews.select_related('author', 'title')

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title, id=self.kwargs.get('title_id')
        )
        serializer.save(title=title, author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Отображение действий с комментариями"""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorModerAdminOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id'),
        )
        return review.comments.select_related('author')

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id'),
        )
        serializer.save(review=review, author=self.request.user)
