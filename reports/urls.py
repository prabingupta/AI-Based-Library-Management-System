from django.urls import path
from . import views

app_name = "reports"

urlpatterns = [
    path("", views.ReportsIndexView.as_view(), name="index"),
    path("export/books/pdf/", views.ExportBooksPDFView.as_view(), name="export_books_pdf"),
    path("export/members/pdf/", views.ExportMembersPDFView.as_view(), name="export_members_pdf"),
    path("export/books/excel/", views.ExportBooksExcelView.as_view(), name="export_books_excel"),
    path("export/borrowing/excel/", views.ExportBorrowingExcelView.as_view(), name="export_borrowing_excel"),
]
