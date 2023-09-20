from django.contrib import admin
from .models import Book, Genre, Publisher


admin.site.register(Genre)
admin.site.register(Publisher)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "description", "amount_of_pages", "author", "publisher", "is_deleted"]
    list_filter = ["title", "is_deleted"]
