from django.core.validators import MinValueValidator
from django.db.models import *

from libraries.validators import validate_not_zero
from publications.models import Publication


class Library(Model):
    class Meta:
        verbose_name_plural = "libraries"

    title = CharField(max_length=255, unique=True)
    address = CharField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.title}'


class ReadingRoom(Model):
    class Meta:
        unique_together = ('library', 'name')

    name = CharField(max_length=255)
    seats_count = PositiveIntegerField()
    library = ForeignKey(Library, on_delete=CASCADE)

    def __str__(self):
        return f'{self.name}'


class Librarian(Model):
    full_name = CharField(max_length=255)
    reading_room = ForeignKey(ReadingRoom, on_delete=CASCADE)

    def __str__(self):
        return f'{self.full_name}'


class StorageLocation(Model):
    class Meta:
        unique_together = ('reading_room', 'rack_no', 'shelf_no')

    rack_no = PositiveIntegerField(validators=[MinValueValidator(1)])
    shelf_no = PositiveIntegerField(validators=[MinValueValidator(1)])
    reading_room = ForeignKey(ReadingRoom, on_delete=CASCADE)
    publications = ManyToManyField(Publication, blank=True)

    def __str__(self):
        return f'Rack №{self.rack_no}, shelf №{self.shelf_no}'


class PublicationsFlowHistory(Model):
    class Meta:
        verbose_name_plural = 'publications flow history'

    librarian = ForeignKey(Librarian, on_delete=RESTRICT)
    publication = ForeignKey(Publication, on_delete=RESTRICT)
    count = IntegerField(validators=[validate_not_zero])
