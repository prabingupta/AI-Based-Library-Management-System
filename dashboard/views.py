import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.views import View
from datetime import timedelta
from books.models import Book, BookCopy, Category
from members.models import Member
from borrowing.models import BorrowRecord


@method_decorator(login_required, name='dispatch')
class DashboardView(View):
    template_name = 'dashboard/index.html'

    def get(self, request):
        today = timezone.now()

        total_books = Book.objects.filter(is_deleted=False).count()
        total_members = Member.objects.filter(is_deleted=False).count()
        total_copies = BookCopy.objects.filter(is_deleted=False).count()
        available_copies = BookCopy.objects.filter(status='available', is_deleted=False).count()

        active_borrows = BorrowRecord.objects.filter(status__in=['borrowed', 'renewed'])
        overdue_borrows = [b for b in active_borrows if b.is_overdue]

        recent_borrows = BorrowRecord.objects.select_related(
            'member__user', 'book_copy__book'
        ).order_by('-borrow_date')[:8]

        # Borrowing trend last 7 days
        trend_labels = []
        trend_data = []
        for i in range(6, -1, -1):
            day = today - timedelta(days=i)
            count = BorrowRecord.objects.filter(
                borrow_date__date=day.date()
            ).count()
            trend_labels.append(day.strftime('%b %d'))
            trend_data.append(count)

        # Category distribution
        categories = Category.objects.filter(is_active=True)
        cat_labels = []
        cat_data = []
        for cat in categories:
            count = cat.books.filter(is_deleted=False).count()
            if count > 0:
                cat_labels.append(cat.name)
                cat_data.append(count)

        context = {
            'total_books': total_books,
            'total_members': total_members,
            'active_borrows': active_borrows.count(),
            'overdue_count': len(overdue_borrows),
            'total_copies': total_copies,
            'available_copies': available_copies,
            'recent_borrows': recent_borrows,
            'page_title': 'Dashboard',
            'trend_labels': json.dumps(trend_labels),
            'trend_data': json.dumps(trend_data),
            'cat_labels': json.dumps(cat_labels),
            'cat_data': json.dumps(cat_data),
        }
        return render(request, self.template_name, context)
