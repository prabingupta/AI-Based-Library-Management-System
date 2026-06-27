from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views import View
from django.db.models import Q
from .models import Book, Category, Author, Publisher, BookCopy
from .forms import BookForm, CategoryForm, AuthorForm


@method_decorator(login_required, name='dispatch')
class BookListView(View):
    template_name = 'books/list.html'

    def get(self, request):
        books = Book.objects.filter(is_deleted=False).prefetch_related('authors', 'categories')
        query = request.GET.get('q', '')
        category = request.GET.get('category', '')
        status = request.GET.get('status', '')

        if query:
            books = books.filter(
                Q(title__icontains=query) |
                Q(isbn__icontains=query) |
                Q(authors__first_name__icontains=query) |
                Q(authors__last_name__icontains=query)
            ).distinct()

        if category:
            books = books.filter(categories__slug=category)

        if status:
            books = books.filter(status=status)

        categories = Category.objects.filter(is_active=True)

        context = {
            'books': books,
            'categories': categories,
            'query': query,
            'selected_category': category,
            'selected_status': status,
            'total_count': books.count(),
            'page_title': 'Books',
        }
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class BookDetailView(View):
    template_name = 'books/detail.html'

    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk, is_deleted=False)
        copies = book.copies.filter(is_deleted=False)
        context = {
            'book': book,
            'copies': copies,
            'page_title': book.title,
        }
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class BookCreateView(View):
    template_name = 'books/form.html'

    def get(self, request):
        form = BookForm()
        return render(request, self.template_name, {'form': form, 'page_title': 'Add Book', 'action': 'Add'})

    def post(self, request):
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.created_by = request.user
            book.save()
            form.save_m2m()
            messages.success(request, f'"{book.title}" has been added successfully.')
            return redirect('books:detail', pk=book.pk)
        return render(request, self.template_name, {'form': form, 'page_title': 'Add Book', 'action': 'Add'})


@method_decorator(login_required, name='dispatch')
class BookEditView(View):
    template_name = 'books/form.html'

    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk, is_deleted=False)
        form = BookForm(instance=book)
        return render(request, self.template_name, {'form': form, 'book': book, 'page_title': 'Edit Book', 'action': 'Update'})

    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk, is_deleted=False)
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'"{book.title}" has been updated.')
            return redirect('books:detail', pk=book.pk)
        return render(request, self.template_name, {'form': form, 'book': book, 'page_title': 'Edit Book', 'action': 'Update'})


@method_decorator(login_required, name='dispatch')
class BookDeleteView(View):
    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk, is_deleted=False)
        book.is_deleted = True
        book.save()
        messages.success(request, f'"{book.title}" has been deleted.')
        return redirect('books:list')


@method_decorator(login_required, name='dispatch')
class CategoryListView(View):
    template_name = 'books/categories.html'

    def get(self, request):
        categories = Category.objects.filter(is_active=True, is_deleted=False)
        cats_with_counts = []
        for cat in categories:
            count = cat.books.filter(is_deleted=False).count()
            cats_with_counts.append({'category': cat, 'count': count})

        context = {
            'cats_with_counts': cats_with_counts,
            'page_title': 'Categories',
        }
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class GlobalSearchView(View):
    template_name = 'books/search_results.html'

    def get(self, request):
        query = request.GET.get('q', '').strip()
        books = []
        members = []
        borrow_records = []

        if query:
            from members.models import Member
            from borrowing.models import BorrowRecord

            books = Book.objects.filter(
                is_deleted=False
            ).filter(
                Q(title__icontains=query) |
                Q(isbn__icontains=query) |
                Q(description__icontains=query) |
                Q(authors__first_name__icontains=query) |
                Q(authors__last_name__icontains=query) |
                Q(categories__name__icontains=query)
            ).distinct()[:10]

            members = Member.objects.filter(
                is_deleted=False
            ).filter(
                Q(card_number__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query) |
                Q(user__email__icontains=query)
            ).distinct()[:5]

            borrow_records = BorrowRecord.objects.filter(
                Q(book_copy__book__title__icontains=query) |
                Q(member__user__first_name__icontains=query) |
                Q(book_copy__barcode__icontains=query)
            ).select_related('member__user', 'book_copy__book').distinct()[:5]

        context = {
            'query': query,
            'books': books,
            'members': members,
            'borrow_records': borrow_records,
            'total_results': len(list(books)) + len(list(members)) + len(list(borrow_records)),
            'page_title': f'Search: {query}',
        }
        return render(request, self.template_name, context)
