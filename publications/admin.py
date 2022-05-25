from django.contrib import admin
from .models import *

admin.site.register(LiteracyWork)
admin.site.register(TextbookLiteracyWork)
admin.site.register(NovelLiteracyWork)
admin.site.register(PoemLiteracyWork)
admin.site.register(ArticleLiteracyWork)
admin.site.register(ScientificLiteracyWork)
admin.site.register(Author)
admin.site.register(Publication)
admin.site.register(BookPublication)
admin.site.register(JournalPublication)
admin.site.register(PaperPublication)
