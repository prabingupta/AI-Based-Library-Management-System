from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.views import View
from django.utils import timezone
from datetime import timedelta
from books.models import Book
from members.models import Member
from borrowing.models import BorrowRecord


@method_decorator(login_required, name="dispatch")
class ReportsIndexView(View):
    template_name = "reports/index.html"

    def get(self, request):
        today = timezone.now()
        last_30 = today - timedelta(days=30)

        total_books = Book.objects.filter(is_deleted=False).count()
        total_members = Member.objects.filter(is_deleted=False).count()
        total_borrows = BorrowRecord.objects.count()
        borrows_this_month = BorrowRecord.objects.filter(borrow_date__gte=last_30).count()
        returns_this_month = BorrowRecord.objects.filter(status="returned", return_date__gte=last_30).count()
        active_borrows = BorrowRecord.objects.filter(status__in=["borrowed", "renewed"]).count()
        overdue_list = [b for b in BorrowRecord.objects.filter(status__in=["borrowed", "renewed"]) if b.is_overdue]
        total_fines = sum(b.fine_amount for b in BorrowRecord.objects.all())

        top_books = (
            BorrowRecord.objects.values("book_copy__book__title")
            .annotate(borrow_count=__import__("django").db.models.Count("id"))
            .order_by("-borrow_count")[:5]
        )

        context = {
            "total_books": total_books,
            "total_members": total_members,
            "total_borrows": total_borrows,
            "borrows_this_month": borrows_this_month,
            "returns_this_month": returns_this_month,
            "active_borrows": active_borrows,
            "overdue_count": len(overdue_list),
            "total_fines": total_fines,
            "top_books": top_books,
            "page_title": "Reports",
        }
        return render(request, self.template_name, context)


@method_decorator(login_required, name="dispatch")
class ExportBooksPDFView(View):
    def get(self, request):
        from reports.services.export import generate_books_pdf

        buffer = generate_books_pdf()
        response = HttpResponse(buffer, content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="libraryos-books-report.pdf"'
        return response


@method_decorator(login_required, name="dispatch")
class ExportMembersPDFView(View):
    def get(self, request):
        from reports.services.export import generate_members_pdf

        buffer = generate_members_pdf()
        response = HttpResponse(buffer, content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="libraryos-members-report.pdf"'
        return response


@method_decorator(login_required, name="dispatch")
class ExportBooksExcelView(View):
    def get(self, request):
        from reports.services.export import generate_books_excel

        buffer = generate_books_excel()
        response = HttpResponse(
            buffer,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = 'attachment; filename="libraryos-books-report.xlsx"'
        return response


@method_decorator(login_required, name="dispatch")
class ExportBorrowingExcelView(View):
    def get(self, request):
        from reports.services.export import generate_borrowing_excel

        buffer = generate_borrowing_excel()
        response = HttpResponse(
            buffer,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = 'attachment; filename="libraryos-borrowing-report.xlsx"'
        return response
