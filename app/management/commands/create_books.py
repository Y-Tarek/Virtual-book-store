""" 
 This File contains django scripts to create
 Books that can be predifined in the system.

"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from app.models import User, Book
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Create 2 users and 5 books, assigning users as authors'

    def handle(self, *args, **options):
        user_data = [
            {
                'username': 'user1',
                'email': 'user1@example.com',
                'first_name': 'First',
                'last_name': 'User',
                'password': 'password123'
            },
            {
                'username': 'user2',
                'email': 'user2@example.com',
                'first_name': 'Second',
                'last_name': 'User',
                'password': 'password123'
            }
        ]

        existing_users = User.objects.filter(email__in=[item.get('email') for item in user_data])
        existing_user_emails = {user.email for user in existing_users}

        new_users = []
        for item in user_data:
            if item.get('email') not in existing_user_emails:
                new_users.append(User(
                    username=item.get('username'),
                    email=item.get('email'),
                    first_name=item.get('first_name'),
                    last_name=item.get('last_name'),
                    password=make_password(item.get('password'))
                ))

        if new_users:
            User.objects.bulk_create(new_users)

        users = User.objects.filter(email__in=[item.get('email') for item in user_data])

        existing_books = Book.objects.filter(title__in=[f'Book {i}' for i in range(1, 6)])
        existing_book_titles = {book.title for book in existing_books}

        new_books = []
        for i in range(1, 6):
            title = f'Book {i}'
            if title not in existing_book_titles:
                author = users[(i - 1) % len(users)]
                new_books.append(Book(
                    title=title,
                    author=author,
                    published_date=timezone.now(),
                    summary=f'Summary of {title}',
                    content=f'Content of {title}'
                ))

        if new_books:
            Book.objects.bulk_create(new_books)

        self.stdout.write(self.style.SUCCESS('Successfully ensured 2 users and 5 books exist.'))
