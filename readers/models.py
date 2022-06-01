from django.core.validators import MinValueValidator
from django.db.models import *

from libraries.models import Librarian, Library


class Reader(Model):
    full_name = CharField(max_length=255)
    issue_date = DateField(auto_now_add=True)
    issuer = ForeignKey(Librarian, on_delete=RESTRICT)
    issuer_library = ForeignKey(Library, on_delete=RESTRICT)

    def __str__(self):
        return f'{self.full_name}'


class StudentReader(Reader):
    educational_institution = CharField(max_length=255)
    group_no = PositiveIntegerField()


class TeacherReader(Reader):
    educational_institution = CharField(max_length=255)


class WorkerReader(Reader):
    organization = CharField(max_length=255)


class RetireeReader(Reader):
    years_work_experience = PositiveIntegerField(validators=[MinValueValidator(1)])
