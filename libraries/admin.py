from django.contrib import admin

from .models import *


class ReadingRoomInline(admin.TabularInline):
    model = ReadingRoom
    extra = 1
    show_change_link = True


class LibrarianInline(admin.TabularInline):
    model = Librarian
    extra = 1


class StorageLocationInline(admin.TabularInline):
    model = StorageLocation
    filter_horizontal = ('publications',)
    extra = 1


@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ('title', 'address')
    inlines = [ReadingRoomInline]


@admin.register(ReadingRoom)
class ReadingRoomAdmin(admin.ModelAdmin):
    list_display = ('library', 'name', 'seats_count')
    ordering = ('library', 'name')
    list_display_links = ('name',)
    inlines = [LibrarianInline, StorageLocationInline]

    @admin.display()
    def get_library(self, obj: ReadingRoom):
        return obj.library


@admin.register(Librarian)
class LibrarianAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'reading_room', 'library')
    search_fields = ('full_name', 'reading_room__name', 'reading_room__library__title')
    list_filter = ('reading_room__library',)

    @admin.display()
    def library(self, obj: Librarian):
        return obj.reading_room.library


admin.site.register(PublicationsFlowHistory)
