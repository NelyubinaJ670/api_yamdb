from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)

from .validators import validate_username

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
    message='Недопустимые символы: ^[-a-zA-Z0-9_]+$'
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
        'Год выпуска'
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
        ordering = ('id',)

    def __str__(self):
        return f'{self.title} принадлежит жанру/ам {self.genre}'


class User(AbstractUser):
    '''Переопределяем модель User'''
    username = models.CharField(
        max_length=150,
        verbose_name='Пользователь',
        unique=True,
        blank=False,
        validators=[validate_username]
    )
    email = models.EmailField(
        max_length=254,
        verbose_name='Эл.почта',
        unique=True,
        blank=False,
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


class Review(models.Model):
    """Модель отзывов на произведения"""
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField(
        verbose_name='Текст отзыва'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Баллы отзыва',
        validators=[MinValueValidator(1, 'Наинизшая балл'),
                    MaxValueValidator(10, 'Наивысший балл')]
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author'
            )
        ]
        ordering = ['-pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель комментариев к отзывам"""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментарий'
    )
    text = models.TextField(
        verbose_name='Текст комментария'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
