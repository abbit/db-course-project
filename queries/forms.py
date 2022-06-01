from django import forms
from django.core.exceptions import ValidationError

from publications.models import *
from readers.models import *
from libraries.models import *


class LiteracyWorkChoiceForm(forms.Form):
    literacy_work = forms.ModelChoiceField(queryset=LiteracyWork.objects.all())


class PublicationChoiceForm(forms.Form):
    publication = forms.ModelChoiceField(queryset=Publication.objects.all())


class DateRangeForm(forms.Form):
    start_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date:
            if start_date > end_date:
                raise ValidationError("Start date should be before end date")


class ReaderChoiceForm(forms.Form):
    reader = forms.ModelChoiceField(queryset=Reader.objects.all())


class StorageLocationModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj: StorageLocation):
        return f'{obj.__str__()} from {obj.reading_room} in {obj.reading_room.library}'


class StorageLocationChoiceForm(forms.Form):
    storage_location = StorageLocationModelChoiceField(queryset=StorageLocation.objects.all())


class LibrarianAndDateRangeForm(DateRangeForm):
    librarian = forms.ModelChoiceField(queryset=Librarian.objects.all())
