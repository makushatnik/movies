from django.contrib import admin
from models import Filmwork, PersonRole


class PersonRoleInline(admin.TabularInline):
    model = PersonRole
    extra = 0


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'creation_date', 'rating', 'created', 'modified')
    list_filter = ('type',)
    search_fields = ('title', 'description', 'id')
    fields = (
        'title', 'type', 'description', 'creation_date',
        'certificate',
        'file_path', 'rating', 'genres'
    )
    inlines = [
        PersonRoleInline
    ]
