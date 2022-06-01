import django_tables2 as tables
from readers.models import *
from publications.models import *


class ReaderTable(tables.Table):
    class Meta:
        model = Reader
        orderable = False


class ReaderAndPublicationTable(ReaderTable):
    publication_title = tables.Column()


class PublicationTable(tables.Table):
    class Meta:
        model = Publication
        orderable = False


class LiteracyWorkTable(tables.Table):
    class Meta:
        model = LiteracyWork
        orderable = False


class LibrarianWithReadersCount(tables.Table):
    full_name = tables.Column()
    readers_count = tables.Column()

    class Meta:
        orderable = False


class LiteracyWorksWithOrdersCount(tables.Table):
    title = tables.Column()
    orders_count = tables.Column()

    class Meta:
        orderable = False


class ReaderWithLastVisitTable(ReaderTable):
    last_visit_timestamp = tables.Column()
