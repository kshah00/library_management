from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import re
from .exceptions import InvalidISBNError, InvalidEmailError, InvalidPhoneNumberError

class LibraryItem(models.Model):
    """Base class for all library items."""
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    item_type = models.CharField(max_length=10, choices=[('book', 'Book'), ('magazine', 'Magazine')])

    def __str__(self):
        return self.title

    @staticmethod
    def validate_isbn(isbn):
        """Validate ISBN format using regex."""
        isbn_pattern = r'^\d{10,13}$'
        if not re.match(isbn_pattern, isbn):
            raise InvalidISBNError(f"Invalid ISBN format: {isbn}. ISBN must be 10-13 digits.")
        return isbn

class Book(LibraryItem):
    """Book model inheriting from LibraryItem."""
    isbn = models.CharField(max_length=13, unique=True)
    author = models.ForeignKey('Author', on_delete=models.CASCADE, related_name='books')
    publisher = models.CharField(max_length=200)
    publication_date = models.DateField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='books')
    quantity = models.IntegerField(default=1)
    available_quantity = models.IntegerField(default=1)
    location = models.CharField(max_length=50)
    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True)

    def save(self, *args, **kwargs):
        self.item_type = 'book'
        self.clean()
        super().save(*args, **kwargs)

    def clean(self):
        """Validate ISBN before saving."""
        self.validate_isbn(self.isbn)

    @classmethod
    def get_available_books(cls):
        """Class method to get all available books."""
        return cls.objects.filter(available_quantity__gt=0)

    @staticmethod
    def get_book_statistics():
        """Static method to get book statistics."""
        from django.db.models import Count
        return {
            'total_books': Book.objects.count(),
            'available_books': Book.objects.filter(available_quantity__gt=0).count(),
            'books_by_category': Book.objects.values('category__name').annotate(count=Count('id')),
        }

class Magazine(LibraryItem):
    """Magazine model inheriting from LibraryItem."""
    issn = models.CharField(max_length=8, unique=True)
    publisher = models.CharField(max_length=200)
    publication_date = models.DateField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='magazines')
    quantity = models.IntegerField(default=1)
    available_quantity = models.IntegerField(default=1)
    location = models.CharField(max_length=50)
    cover_image = models.ImageField(upload_to='magazine_covers/', null=True, blank=True)

    def save(self, *args, **kwargs):
        self.item_type = 'magazine'
        super().save(*args, **kwargs)

    @classmethod
    def get_available_magazines(cls):
        """Class method to get all available magazines."""
        return cls.objects.filter(available_quantity__gt=0)

class Author(models.Model):
    """Author model for book authors."""
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        """Validate email and phone number formats."""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        phone_pattern = r'^\+?1?\d{9,15}$'
        
        if not re.match(email_pattern, self.email):
            raise InvalidEmailError(f"Invalid email format: {self.email}")
        if not re.match(phone_pattern, self.phone):
            raise InvalidPhoneNumberError(f"Invalid phone number format: {self.phone}")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Category(models.Model):
    """Category model for organizing library items."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Member(models.Model):
    """Member model for library users."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    membership_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def clean(self):
        """Validate email and phone number formats."""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        phone_pattern = r'^\+?1?\d{9,15}$'
        
        if not re.match(email_pattern, self.email):
            raise InvalidEmailError(f"Invalid email format: {self.email}")
        if not re.match(phone_pattern, self.phone):
            raise InvalidPhoneNumberError(f"Invalid phone number format: {self.phone}")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Borrowing(models.Model):
    """Borrowing model for tracking item loans."""
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='borrowings')
    item = models.ForeignKey(LibraryItem, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    def clean(self):
        """Validate due date is after borrow date."""
        if self.due_date <= self.borrow_date:
            raise ValidationError("Due date must be after borrow date")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.member} borrowed {self.item}"
