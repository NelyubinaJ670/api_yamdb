from django.db import models
from django.contrib.auth.models import AbstractUser


MODERATOR = 'moderator'
ADMIN = 'admin'
USER = 'user'


ROLES = [
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Администратор'),
    (USER, 'Пользователь')   
]


class Category(models.Model):
    '''Категории (типы) произведений'''
    name = models.CharField(
        'Название',
        max_length=256
    )
    slug = models.SlugField(
        'URL-идентификатор',
        max_length=50,
        unique=True
        # ^[-a-zA-Z0-9_]+$ разобраться как это сделать 
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
        unique=True
        # ^[-a-zA-Z0-9_]+$ разобраться как это сделать 
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
    )
    description = models.TextField(
        'Описание',
        max_length=300,
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр'
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
