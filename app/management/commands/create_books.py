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
        users = [
            User(
                username='user1',
                email='user1@example.com',
                first_name='First',
                last_name='User',
                password=make_password('password123')
            ),
            User(
                username='user2',
                email='user2@example.com',
                first_name='Second',
                last_name='User',
                password=make_password('password123')
            ),
        ]
        
        User.objects.bulk_create(users)

        user1 = User.objects.get(username='user1')
        user2 = User.objects.get(username='user2')

        books = [
            Book(
                title=f'Book {i}',
                author=user1 if i % 2 == 0 else user2,
                published_date=timezone.now(),
                summary=f'Summary of Book {i}',
                content=f'Content of Book {i}'
            ) for i in range(1, 6)
        ]

        Book.objects.bulk_create(books)

        self.stdout.write(self.style.SUCCESS('Successfully created 2 users and 5 books.'))
