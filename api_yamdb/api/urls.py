from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    UserViewSet,
    signup_user,
    get_token
)


app_name = 'api'
router = DefaultRouter()

router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles', TitleViewSet, basename='titles')
router.register(r'users', UserViewSet, basename='users')

auth_patterns = [
    path('signup/', signup_user),
    path('token/', get_token),
]

urlpatterns = [
    path('auth/', include(auth_patterns)),
    path('', include(router.urls)),
]
