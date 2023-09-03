import csv

import logging

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import (Category, Comment, Genre,
                            TitleGenre, Review, Title, User)

logging.basicConfig(
    level=logging.DEBUG,
    filename='program.log',
    filemode='w',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
)

TABLES = {
    User: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
    TitleGenre: 'genre_title.csv',
}


class Command(BaseCommand):
    """
    Для запуска команды создайте и примените миграции
    и примените команду python manage.py load_CSV_file
    Базу нужно заполнить на чистую и только один раз.
    Чтобы повторно заполнить базу - удалите файл db.sqlite3
    и примените миграции, иначе будет ошибка.
    """
    help = 'Заполняет базу данных тестовыми данными'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Начат импорт данных'))
        for model, file_name in TABLES.items():
            try:
                with open(
                    f'{settings.BASE_DIR}/static/data/{file_name}',
                    newline='',
                    encoding='utf-8'
                ) as csvfile:
                    reader = csv.DictReader(csvfile, delimiter=',')
                    if file_name == 'titles.csv':
                        for data in reader:
                            category = Category.objects.get(
                                pk=data.pop('category')
                            )
                            obj = model(
                                category=category,
                                **data
                            )
                            obj.save()
                    elif file_name in ['review.csv', 'comments.csv']:
                        for data in reader:
                            user = User.objects.get(pk=data.pop('author'))
                            obj = model(
                                author=user,
                                **data
                            )
                            obj.save()
                    else:
                        model.objects.bulk_create(
                            [model(**data) for data in reader])
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Даннные {file_name} успешно загружены')
                )
            except Exception as error:
                logging.error(f'Ошибка при выполнении команды: {error}')
