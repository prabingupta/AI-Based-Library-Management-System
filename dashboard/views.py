from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from books.models import Book, BookCopy
from members.models import Member
from borrowing.models import BorrowRecord


@method_decorator(login_required, name='dispatch')
class DashboardView(View):
    template_name = 'dashboard/index.html'

    def get(self, request):
        total_books = Book.objects.filter(is_deleted=False).count()
        total_members = Member.objects.filter(is_deleted=False).count()
        active_borrows = BorrowRecord.objects.filter(status='borrowed').count()
        overdue_borrows = [b for b in BorrowRecord.objects.filter(status='borrowed') if b.is_overdue]
        total_copies = BookCopy.objects.filter(is_deleted=False).count()
        available_copies = BookCopy.objects.filter(status='available', is_deleted=False).count()
        recent_borrows = BorrowRecord.objects.select_related(
            'member__user', 'book_copy__book'
        ).order_by('-borrow_date')[:8]

        context = {
            'total_books': total_books,
            'total_members': total_members,
            'active_borrows': active_borrows,
            'overdue_count': len(overdue_borrows),
            'total_copies': total_copies,
            'available_copies': available_copies,
            'recent_borrows': recent_borrows,
            'page_title': 'Dashboard',
        }
        return render(request, self.template_name, context)
