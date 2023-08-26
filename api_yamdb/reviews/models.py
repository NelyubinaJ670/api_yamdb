from django.db import models
from django.contrib.auth.models import AbstractUser

from django.core.validators import (RegexValidator)


MODERATOR = 'moderator'
ADMIN = 'admin'
USER = 'user'


ROLES = [
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Администратор'),
    (USER, 'Пользователь')
]

SLUG_VALIDATOR = RegexValidator(
    regex=r'^[-a-zA-Z0-9_]+$',
    message='Поле содержит недопустимый символ'
)


class Category(models.Model):
    '''Категории (типы) произведений'''
    name = models.CharField(
        'Название',
        max_length=256
    )
    slug = models.SlugField(
        'URL-идентификатор',
        max_length=50,
        unique=True,
        validators=[SLUG_VALIDATOR]
    )
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    '''Категории жанров'''
    name = models.CharField(
        'Название',
        max_length=256
    )
    slug = models.SlugField(
        'URL-идентификатор',
        max_length=50,
        unique=True,
        validators=[SLUG_VALIDATOR]
    )
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    '''
    Произведения, к которым пишут отзывы
    (определённый фильм, книга или песенка).
    '''
    name = models.CharField(
        'Название',
        max_length=200
    )
    year = models.IntegerField(
        'Год выпуска',
        # validators=Валдатор?! Посмотрим что скажут тесты
    )
    description = models.TextField(
        'Описание',
        max_length=300,
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        through='TitleGenre'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        null=True
    )
    class Meta:
        verbose_name = 'Произведения'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    """Промежуточная класс, связывает жанры и произведения."""
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )
    class Meta:
        rdering = ('id',)

    def __str__(self):
        return f'{self.title} принадлежит жанру/ам {self.genre}'


class User(AbstractUser):
    '''Переопределяем модель User'''
    username = models.CharField(
        max_length=150,
        verbose_name='Пользователь',
        unique=True,
        blank=False,
    )
    email = models.EmailField(
        max_length=254,
        verbose_name='Эл.почта',
        unique=True,
        blank=False
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
        null=True,
        blank=True
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
        null=True,
        blank=True
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
        null=True
    )
    role = models.CharField(
        max_length=100,
        verbose_name='Роль',
        choices=ROLES,
        default='user'
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь',
        verbose_name_plural = 'Пользователи'

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_admin(self):
        return (
            self.role == ADMIN
            or self.is_superuser
        )
