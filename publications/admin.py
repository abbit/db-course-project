from django.contrib import admin
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from .models import *


# class LiteracyWorkInline(admin.TabularInline):
#     model = LiteracyWork.authors.through
#     show_change_link = True
#     extra = 1
#     verbose_name = 'literacy work'
#     verbose_name_plural = 'literacy works'
#     template = 'admin_tabular_inline_literacy_works.html'

class AuthorAdminForm(forms.ModelForm):
    literacy_works = forms.ModelMultipleChoiceField(
        queryset=LiteracyWork.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name='Literacy works',
            is_stacked=False,
        ),

    )

    class Meta:
        model = Author
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AuthorAdminForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['literacy_works'].initial = self.instance.literacy_works.all()

    def save(self, commit=True):
        author = super(AuthorAdminForm, self).save(commit=False)

        if commit:
            author.save()

        if author.pk:
            author.literacy_works.set(self.cleaned_data['literacy_works'])
            self.save_m2m()

        return author


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    # list_display = ('full_name', 'nationality', 'birth_date', 'death_date')
    # filter_horizontal = ('literacy_works',)
    # inlines = [LiteracyWorkInline]
    form = AuthorAdminForm


@admin.register(LiteracyWork)
class LiteracyWorkAdmin(admin.ModelAdmin):
    list_display = ('title',)
    filter_horizontal = ('authors',)


admin.site.register(TextbookLiteracyWork)
admin.site.register(NovelLiteracyWork)
admin.site.register(PoemLiteracyWork)
admin.site.register(ArticleLiteracyWork)
admin.site.register(ScientificLiteracyWork)


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'item_no', 'publisher', 'language', 'pages', 'publication_date', 'count')
    filter_horizontal = ('literacy_works',)
    list_filter = ('literacy_works', 'literacy_works__authors')


admin.site.register(BookPublication)
admin.site.register(JournalPublication)
admin.site.register(PaperPublication)
