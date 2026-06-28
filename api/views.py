from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from books.models import Book, Author, Category, Publisher, BookCopy
from members.models import Member
from borrowing.models import BorrowRecord
from .serializers import (
    BookListSerializer,
    BookCreateSerializer,
    AuthorSerializer,
    CategorySerializer,
    PublisherSerializer,
    BookCopySerializer,
    MemberSerializer,
    BorrowRecordSerializer,
    DashboardStatsSerializer,
)
from .permissions import IsLibrarianOrAbove, IsStaffOrReadOnly


class BookViewSet(viewsets.ModelViewSet):
    queryset = (
        Book.objects.filter(is_deleted=False)
        .prefetch_related("authors", "categories")
        .select_related("publisher", "language", "shelf")
    )
    permission_classes = [IsAuthenticated, IsStaffOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "isbn", "isbn13", "authors__first_name", "authors__last_name"]
    ordering_fields = ["title", "created_at", "available_copies"]
    ordering = ["title"]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return BookCreateSerializer
        return BookListSerializer

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

    @action(detail=False, methods=["get"])
    def available(self, request):
        books = self.get_queryset().filter(status="available", available_copies__gt=0)
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def featured(self, request):
        books = self.get_queryset().filter(is_featured=True)
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def copies(self, request, pk=None):
        book = self.get_object()
        copies = book.copies.filter(is_deleted=False)
        serializer = BookCopySerializer(copies, many=True)
        return Response(serializer.data)


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.filter(is_deleted=False)
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated, IsStaffOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["first_name", "last_name", "nationality"]
    ordering = ["last_name"]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(is_active=True, is_deleted=False)
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsStaffOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]


class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.filter(is_deleted=False)
    serializer_class = PublisherSerializer
    permission_classes = [IsAuthenticated, IsStaffOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "country"]


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.filter(is_deleted=False).select_related("user")
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated, IsLibrarianOrAbove]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["card_number", "user__first_name", "user__last_name", "user__email"]
    ordering = ["-created_at"]

    @action(detail=True, methods=["get"])
    def borrow_history(self, request, pk=None):
        member = self.get_object()
        records = BorrowRecord.objects.filter(member=member).select_related("book_copy__book").order_by("-borrow_date")
        serializer = BorrowRecordSerializer(records, many=True)
        return Response(serializer.data)


class BorrowRecordViewSet(viewsets.ModelViewSet):
    queryset = BorrowRecord.objects.select_related("member__user", "book_copy__book").order_by("-borrow_date")
    serializer_class = BorrowRecordSerializer
    permission_classes = [IsAuthenticated, IsLibrarianOrAbove]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["member__card_number", "book_copy__barcode", "book_copy__book__title"]
    ordering_fields = ["borrow_date", "due_date"]

    @action(detail=False, methods=["get"])
    def overdue(self, request):
        active = self.get_queryset().filter(status__in=["borrowed", "renewed"])
        overdue = [r for r in active if r.is_overdue]
        serializer = self.get_serializer(overdue, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def active(self, request):
        records = self.get_queryset().filter(status__in=["borrowed", "renewed"])
        serializer = self.get_serializer(records, many=True)
        return Response(serializer.data)


class DashboardStatsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        active_borrows = BorrowRecord.objects.filter(status__in=["borrowed", "renewed"])
        overdue = [b for b in active_borrows if b.is_overdue]

        data = {
            "total_books": Book.objects.filter(is_deleted=False).count(),
            "total_members": Member.objects.filter(is_deleted=False).count(),
            "active_borrows": active_borrows.count(),
            "overdue_count": len(overdue),
            "available_copies": BookCopy.objects.filter(status="available", is_deleted=False).count(),
            "total_copies": BookCopy.objects.filter(is_deleted=False).count(),
        }
        serializer = DashboardStatsSerializer(data)
        return Response(serializer.data)


class SearchAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.GET.get("q", "").strip()
        if not query:
            return Response({"query": "", "results": {}})

        books = (
            Book.objects.filter(is_deleted=False)
            .filter(
                Q(title__icontains=query)
                | Q(isbn__icontains=query)
                | Q(authors__first_name__icontains=query)
                | Q(authors__last_name__icontains=query)
            )
            .distinct()[:10]
        )

        members = (
            Member.objects.filter(is_deleted=False)
            .filter(
                Q(card_number__icontains=query)
                | Q(user__first_name__icontains=query)
                | Q(user__last_name__icontains=query)
                | Q(user__email__icontains=query)
            )
            .distinct()[:5]
        )

        return Response(
            {
                "query": query,
                "results": {
                    "books": BookListSerializer(books, many=True, context={"request": request}).data,
                    "members": MemberSerializer(members, many=True, context={"request": request}).data,
                    "total": books.count() + members.count(),
                },
            }
        )
