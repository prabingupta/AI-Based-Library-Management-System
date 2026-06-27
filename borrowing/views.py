from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views import View
from django.utils import timezone
from django.db.models import Q
from .models import BorrowRecord, Reservation
from .forms import IssueBorrowForm, ReturnBookForm
from books.models import BookCopy


@method_decorator(login_required, name='dispatch')
class BorrowListView(View):
    template_name = 'borrowing/list.html'

    def get(self, request):
        records = BorrowRecord.objects.select_related(
            'member__user', 'book_copy__book'
        ).order_by('-borrow_date')

        status = request.GET.get('status', '')
        query = request.GET.get('q', '')

        if status:
            records = records.filter(status=status)

        if query:
            records = records.filter(
                Q(member__card_number__icontains=query) |
                Q(member__user__first_name__icontains=query) |
                Q(member__user__last_name__icontains=query) |
                Q(book_copy__book__title__icontains=query) |
                Q(book_copy__barcode__icontains=query)
            )

        overdue_ids = [r.pk for r in records if r.is_overdue]

        context = {
            'records': records,
            'selected_status': status,
            'query': query,
            'total_count': records.count(),
            'overdue_ids': overdue_ids,
            'page_title': 'Borrowing',
        }
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class IssueBookView(View):
    template_name = 'borrowing/issue.html'

    def get(self, request):
        form = IssueBorrowForm()
        return render(request, self.template_name, {
            'form': form,
            'page_title': 'Issue Book',
        })

    def post(self, request):
        form = IssueBorrowForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.issued_by = request.user
            record.status = 'borrowed'
            record.save()

            copy = record.book_copy
            copy.status = 'borrowed'
            copy.save()

            book = copy.book
            if book.available_copies > 0:
                book.available_copies -= 1
                book.save()

            messages.success(request, f'Book "{copy.book.title}" issued to {record.member.user.get_full_name()} successfully.')
            return redirect('borrowing:detail', pk=record.pk)

        return render(request, self.template_name, {
            'form': form,
            'page_title': 'Issue Book',
        })


@method_decorator(login_required, name='dispatch')
class BorrowDetailView(View):
    template_name = 'borrowing/detail.html'

    def get(self, request, pk):
        record = get_object_or_404(BorrowRecord, pk=pk)
        return_form = ReturnBookForm()
        context = {
            'record': record,
            'return_form': return_form,
            'page_title': f'Borrow #{str(record.pk)[:8]}',
        }
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class ReturnBookView(View):
    def post(self, request, pk):
        record = get_object_or_404(BorrowRecord, pk=pk, status='borrowed')
        form = ReturnBookForm(request.POST)

        if form.is_valid():
            record.status = 'returned'
            record.return_date = timezone.now()
            record.returned_to = request.user
            fine = form.cleaned_data.get('fine_amount') or 0
            record.fine_amount = fine
            record.notes = form.cleaned_data.get('notes', '')
            record.save()

            copy = record.book_copy
            copy.status = 'available'
            copy.save()

            book = copy.book
            book.available_copies += 1
            book.save()

            if fine > 0:
                member = record.member
                member.fine_balance += fine
                member.save()

            messages.success(request, f'Book returned successfully. Fine: Rs. {fine}')
            return redirect('borrowing:detail', pk=record.pk)

        messages.error(request, 'Something went wrong. Please try again.')
        return redirect('borrowing:detail', pk=record.pk)


@method_decorator(login_required, name='dispatch')
class RenewBookView(View):
    def post(self, request, pk):
        record = get_object_or_404(BorrowRecord, pk=pk, status='borrowed')

        if record.renew_count >= 2:
            messages.error(request, 'Maximum renewals (2) reached for this book.')
            return redirect('borrowing:detail', pk=record.pk)

        from datetime import timedelta
        record.due_date = record.due_date + timedelta(days=14)
        record.renew_count += 1
        record.status = 'renewed'
        record.save()

        messages.success(request, f'Book renewed successfully. New due date: {record.due_date.strftime("%b %d, %Y")}')
        return redirect('borrowing:detail', pk=record.pk)
