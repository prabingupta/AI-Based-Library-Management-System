from django import forms
from .models import Book, BookCopy, Category, Author, Publisher, Language, Shelf


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'title', 'isbn', 'isbn13', 'authors', 'publisher',
            'categories', 'language', 'cover_image', 'description',
            'edition', 'pages', 'publication_year', 'publication_date',
            'status', 'total_copies', 'available_copies',
            'shelf', 'call_number', 'tags', 'is_featured', 'is_active',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Book title'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ISBN-10'}),
            'isbn13': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ISBN-13'}),
            'authors': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'publisher': forms.Select(attrs={'class': 'form-select'}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'language': forms.Select(attrs={'class': 'form-select'}),
            'cover_image': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'edition': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2nd Edition'}),
            'pages': forms.NumberInput(attrs={'class': 'form-control'}),
            'publication_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'publication_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'total_copies': forms.NumberInput(attrs={'class': 'form-control'}),
            'available_copies': forms.NumberInput(attrs={'class': 'form-control'}),
            'shelf': forms.Select(attrs={'class': 'form-select'}),
            'call_number': forms.TextInput(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'fiction, science, history'}),
        }


class BookCopyForm(forms.ModelForm):
    class Meta:
        model = BookCopy
        fields = ['barcode', 'shelf', 'condition', 'status', 'acquisition_date', 'price', 'notes']
        widgets = {
            'barcode': forms.TextInput(attrs={'class': 'form-control'}),
            'shelf': forms.Select(attrs={'class': 'form-select'}),
            'condition': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'acquisition_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'icon', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'icon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'fa-solid fa-book'}),
        }


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'bio', 'photo', 'email', 'website', 'nationality', 'birth_date']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
