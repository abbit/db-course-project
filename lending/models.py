from django.db.models import *

from libraries.models import Librarian
from publications.models import Publication
from readers.models import Reader


class LendingRestriction(Model):
    class Meta:
        unique_together = ('library_rooms_only', 'time_limit')

    name = CharField(max_length=255)
    library_rooms_only = BooleanField()
    time_limit = DurationField(null=True, blank=True)


class PublicationsOrdersHistory(Model):
    publication = ForeignKey(Publication, on_delete=RESTRICT)
    reader = ForeignKey(Reader, on_delete=RESTRICT)
    lending_restriction = ForeignKey(LendingRestriction, on_delete=RESTRICT)
    given_timestamp = DateTimeField(auto_now_add=True)
    given_librarian = ForeignKey(Librarian, on_delete=RESTRICT, related_name='given_publications_orders')
    received_timestamp = DateTimeField(blank=True, null=True)
    received_librarian = ForeignKey(Librarian, blank=True, null=True, on_delete=RESTRICT,
                                    related_name='received_publications_orders')