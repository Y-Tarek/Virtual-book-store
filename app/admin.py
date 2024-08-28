from django.contrib import admin
from app.models import Book, Review


class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "published_date")
    search_fields = ("title", "author__username")
    list_filter = ("published_date",)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("book", "reviewer", "rating", "created_at")
    search_fields = ("book__title", "reviewer__username", "review_text")
    list_filter = (
        "rating",
        "created_at",
    )


admin.site.register(Book, BookAdmin)
admin.site.register(Review, ReviewAdmin)
