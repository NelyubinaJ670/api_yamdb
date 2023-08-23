from django.db import models


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
