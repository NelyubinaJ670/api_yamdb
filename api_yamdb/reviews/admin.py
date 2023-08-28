from django.contrib import admin

from reviews.models import (Category, Genre, Title, User,
                            TitleGenre, Review, Comment)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)
    empty_value_diplay = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)
    empty_value_diplay = '-пусто-'


class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'year', 'category')
    search_fields = ('name',)
    list_filter = ('year', 'category')
    empty_value_diplay = '-пусто-'


class TitleGenreAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'genre',
        'title'
    )
    list_filter = ('genre',)
    search_fields = ('title',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'text',
                    'author', 'score', 'pub_date',)
    search_fields = ('title', 'author', 'pub_date')
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'review', 'text',
        'author', 'pub_date',
    )
    search_fields = ('review', 'author', 'pub_date')
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(User)
admin.site.register(TitleGenre, TitleGenreAdmin)
