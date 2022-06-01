from django.contrib import admin
from django.utils.html import format_html
from rangefilter.filters import DateRangeFilter

from .models import *

READER_TYPES = ['student', 'teacher', 'worker', 'retiree']


class BaseReaderAdmin(admin.ModelAdmin):
    list_display = ('get_full_name_with_url', 'issue_date', 'issuer', 'issuer_library')
    fields = ('full_name', 'issuer')
    search_fields = ('full_name', 'issue_date')
    list_filter = (('issue_date', DateRangeFilter), 'issuer', 'issuer_library')
    additional_fields = ()

    def get_list_display(self, request):
        return self.list_display + self.additional_fields

    def get_fields(self, request, obj=None):
        return self.fields + self.additional_fields

    def get_search_fields(self, request):
        return self.search_fields + self.additional_fields

    @admin.display(description='full_name')
    def get_full_name_with_url(self, obj: Reader):
        for type_ in READER_TYPES:
            reader_type = type_ + 'reader'
            if hasattr(obj, reader_type):
                return format_html(f"<a href='/readers/{reader_type}/{obj.id}/change/'>{obj.full_name}</a>")

        return obj.full_name

    def save_model(self, request, obj: Reader, form, change):
        obj.issuer_library = obj.issuer.reading_room.library
        super().save_model(request, obj, form, change)


@admin.register(Reader)
class ReaderAdmin(BaseReaderAdmin):
    pass


@admin.register(StudentReader)
class StudentReaderAdmin(BaseReaderAdmin):
    additional_fields = ('educational_institution', 'group_no')


@admin.register(TeacherReader)
class TeacherReaderAdmin(BaseReaderAdmin):
    additional_fields = ('educational_institution',)


@admin.register(WorkerReader)
class WorkerReaderAdmin(BaseReaderAdmin):
    additional_fields = ('organization',)


@admin.register(RetireeReader)
class RetireeReaderAdmin(BaseReaderAdmin):
    additional_fields = ('years_work_experience',)
