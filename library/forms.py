from django import forms
from django.core.validators import RegexValidator
from .models import Book, Magazine, Author, Category, Member, Borrowing, LibraryItem
from .exceptions import InvalidISBNError, InvalidEmailError, InvalidPhoneNumberError
import re
from django.utils import timezone

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'isbn', 'author', 'publisher', 'publication_date', 
                 'category', 'quantity', 'available_quantity', 'location', 
                 'cover_image', 'description']
        widgets = {
            'publication_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_isbn(self):
        isbn = self.cleaned_data['isbn']
        isbn_pattern = r'^\d{10,13}$'
        if not re.match(isbn_pattern, isbn):
            raise InvalidISBNError(f"Invalid ISBN format: {isbn}. ISBN must be 10-13 digits.")
        return isbn

class MagazineForm(forms.ModelForm):
    class Meta:
        model = Magazine
        fields = ['title', 'issn', 'publisher', 'publication_date', 
                 'category', 'quantity', 'available_quantity', 'location', 
                 'cover_image', 'description']
        widgets = {
            'publication_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'email', 'phone', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise InvalidEmailError(f"Invalid email format: {email}")
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        phone_pattern = r'^\+?1?\d{9,15}$'
        if not re.match(phone_pattern, phone):
            raise InvalidPhoneNumberError(f"Invalid phone number format: {phone}")
        return phone

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'email', 'phone', 'address']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise InvalidEmailError(f"Invalid email format: {email}")
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        phone_pattern = r'^\+?1?\d{9,15}$'
        if not re.match(phone_pattern, phone):
            raise InvalidPhoneNumberError(f"Invalid phone number format: {phone}")
        return phone

class BorrowingForm(forms.ModelForm):
    item = forms.ModelChoiceField(
        queryset=LibraryItem.objects.filter(is_active=True),
        label="Item to Borrow"
    )

    class Meta:
        model = Borrowing
        fields = ['member', 'item', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        due_date = cleaned_data.get('due_date')
        if due_date and due_date <= timezone.now().date():
            raise forms.ValidationError("Due date must be in the future")
        return cleaned_data 