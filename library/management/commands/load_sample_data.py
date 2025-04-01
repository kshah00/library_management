from django.core.management.base import BaseCommand
from django.utils import timezone
from library.models import Book, Magazine, Author, Category
from datetime import timedelta
import random

class Command(BaseCommand):
    help = 'Loads sample books and magazines into the database'

    def handle(self, *args, **kwargs):
        # Create categories
        categories = [
            Category.objects.create(name='Fiction', description='Fiction books'),
            Category.objects.create(name='Non-Fiction', description='Non-fiction books'),
            Category.objects.create(name='Science', description='Science books'),
            Category.objects.create(name='Technology', description='Technology books'),
            Category.objects.create(name='Art', description='Art books'),
            Category.objects.create(name='History', description='History books'),
            Category.objects.create(name='Science Fiction', description='Science fiction books'),
            Category.objects.create(name='Mystery', description='Mystery books'),
            Category.objects.create(name='Romance', description='Romance books'),
            Category.objects.create(name='Biography', description='Biography books'),
        ]

        # Create authors
        authors = [
            Author.objects.create(
                name='John Smith',
                email='john.smith@example.com',
                phone='1234567890',
                bio='Award-winning author of multiple bestsellers'
            ),
            Author.objects.create(
                name='Jane Doe',
                email='jane.doe@example.com',
                phone='0987654321',
                bio='Contemporary fiction writer'
            ),
            Author.objects.create(
                name='Robert Johnson',
                email='robert.johnson@example.com',
                phone='5555555555',
                bio='Science fiction and fantasy author'
            ),
            Author.objects.create(
                name='Mary Wilson',
                email='mary.wilson@example.com',
                phone='1112223333',
                bio='Historical fiction writer'
            ),
            Author.objects.create(
                name='David Brown',
                email='david.brown@example.com',
                phone='4445556666',
                bio='Non-fiction author specializing in technology'
            ),
        ]

        # Sample book titles and descriptions
        book_data = [
            {
                'title': 'The Art of Programming',
                'description': 'A comprehensive guide to programming fundamentals',
                'isbn': '1234567890123',
                'publisher': 'Tech Books Publishing',
                'publication_date': timezone.now().date() - timedelta(days=365),
                'quantity': 5,
                'available_quantity': 3,
                'location': 'Shelf A-1'
            },
            {
                'title': 'Mystery of the Ancient World',
                'description': 'An exploration of ancient civilizations',
                'isbn': '2345678901234',
                'publisher': 'History Press',
                'publication_date': timezone.now().date() - timedelta(days=180),
                'quantity': 3,
                'available_quantity': 2,
                'location': 'Shelf B-2'
            },
            {
                'title': 'Love in the Digital Age',
                'description': 'A modern romance novel',
                'isbn': '3456789012345',
                'publisher': 'Romance Books',
                'publication_date': timezone.now().date() - timedelta(days=90),
                'quantity': 4,
                'available_quantity': 4,
                'location': 'Shelf C-3'
            },
            {
                'title': 'The Future of AI',
                'description': 'Exploring artificial intelligence and its impact',
                'isbn': '4567890123456',
                'publisher': 'Science Publications',
                'publication_date': timezone.now().date() - timedelta(days=60),
                'quantity': 2,
                'available_quantity': 1,
                'location': 'Shelf D-4'
            },
            {
                'title': 'Biography of a Genius',
                'description': 'The life story of a remarkable individual',
                'isbn': '5678901234567',
                'publisher': 'Biography Books',
                'publication_date': timezone.now().date() - timedelta(days=30),
                'quantity': 3,
                'available_quantity': 2,
                'location': 'Shelf E-5'
            }
        ]

        # Sample magazine data
        magazine_data = [
            {
                'title': 'Tech Monthly',
                'description': 'Latest in technology and innovation',
                'issn': '12345678',
                'publisher': 'Tech Media',
                'publication_date': timezone.now().date() - timedelta(days=15),
                'quantity': 10,
                'available_quantity': 8,
                'location': 'Magazine Rack 1'
            },
            {
                'title': 'Science Today',
                'description': 'Breaking news in scientific research',
                'issn': '23456789',
                'publisher': 'Science Media',
                'publication_date': timezone.now().date() - timedelta(days=30),
                'quantity': 8,
                'available_quantity': 6,
                'location': 'Magazine Rack 2'
            },
            {
                'title': 'Art & Culture',
                'description': 'Contemporary art and cultural trends',
                'issn': '34567890',
                'publisher': 'Art Media',
                'publication_date': timezone.now().date() - timedelta(days=45),
                'quantity': 6,
                'available_quantity': 4,
                'location': 'Magazine Rack 3'
            },
            {
                'title': 'History Digest',
                'description': 'Historical events and discoveries',
                'issn': '45678901',
                'publisher': 'History Media',
                'publication_date': timezone.now().date() - timedelta(days=60),
                'quantity': 5,
                'available_quantity': 3,
                'location': 'Magazine Rack 4'
            },
            {
                'title': 'Fiction Weekly',
                'description': 'Short stories and literary reviews',
                'issn': '56789012',
                'publisher': 'Fiction Media',
                'publication_date': timezone.now().date() - timedelta(days=7),
                'quantity': 12,
                'available_quantity': 10,
                'location': 'Magazine Rack 5'
            }
        ]

        # Create books
        for book in book_data:
            Book.objects.create(
                **book,
                author=random.choice(authors),
                category=random.choice(categories)
            )

        # Create magazines
        for magazine in magazine_data:
            Magazine.objects.create(
                **magazine,
                category=random.choice(categories)
            )

        self.stdout.write(self.style.SUCCESS('Successfully loaded sample data')) 