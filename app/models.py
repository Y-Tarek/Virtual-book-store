""" 

  This File contains the application database models.

"""

from shared.models import TimeStampModel
from django.db import models
from django.contrib.auth.models import User


class Book(TimeStampModel):
    """Book Database Model"""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author_books"
    )
    title = models.CharField(max_length=250, unique=True)
    published_date = models.DateTimeField()
    summary = models.TextField(null=True, blank=True)
    content = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        indexes = [
            models.Index(fields=["title"]),
        ]


class Review(TimeStampModel):
    """Book Review Database Model"""

    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="book_reviews"
    )
    reviewer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_reviews"
    )
    review_text = models.TextField()
    rating = models.PositiveIntegerField()

    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.book.title}"

    class Meta:
        unique_together = ["book", "reviewer"]
