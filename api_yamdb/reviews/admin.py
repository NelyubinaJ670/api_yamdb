from django.contrib import admin

from reviews.models import Category, Genre, Title, User, TitleGenre


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
    empty_value_display = '-пусто-'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(User)
admin.site.register(TitleGenre, TitleGenreAdmin)
