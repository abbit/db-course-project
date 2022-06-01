from django.contrib import admin
from .models import *


@admin.register(LendingRestriction)
class LendingRestrictionAdmin(admin.ModelAdmin):
    list_display = ('name', 'library_rooms_only', 'time_limit')


admin.site.register(PublicationsOrdersHistory)
