from django.core.validators import MinValueValidator
from django.db.models import *

from libraries.validators import validate_date_in_past


class Author(Model):
    full_name = CharField(max_length=255)
    nationality = CharField(max_length=255, null=True, blank=True)
    birth_date = DateField(validators=[validate_date_in_past])
    death_date = DateField(validators=[validate_date_in_past], null=True, blank=True)

    def __str__(self):
        return f'{self.full_name}'


class LiteracyWork(Model):
    title = CharField(max_length=255)
    authors = ManyToManyField(Author, related_name='literacy_works')

    def __str__(self):
        return f'{self.title}'


class TextbookLiteracyWork(LiteracyWork):
    subject = CharField(max_length=255)


class NovelLiteracyWork(LiteracyWork):
    genre = CharField(max_length=255)


class PoemLiteracyWork(LiteracyWork):
    theme = CharField(max_length=255)


class ArticleLiteracyWork(LiteracyWork):
    theme = CharField(max_length=255)


class ScientificLiteracyWork(LiteracyWork):
    subject = CharField(max_length=255)


class Publication(Model):
    item_no = CharField(max_length=255, unique=True)
    title = CharField(max_length=255)
    publisher = CharField(max_length=255)
    language = CharField(max_length=255)
    pages = PositiveIntegerField(validators=[MinValueValidator(1)])
    publication_date = DateField()
    count = PositiveIntegerField()
    literacy_works = ManyToManyField(LiteracyWork)

    def __str__(self):
        return f'{self.title}'


class BookPublication(Publication):
    category = CharField(max_length=255)
    isbn = CharField(max_length=255, unique=True)


class JournalPublication(Publication):
    discipline = CharField(max_length=255)
    editor = CharField(max_length=255)
    frequency = DurationField()


class PaperPublication(Publication):
    category = CharField(max_length=255)
    editor = CharField(max_length=255)
    frequency = DurationField()
