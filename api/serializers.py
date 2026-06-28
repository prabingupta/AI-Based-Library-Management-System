from rest_framework import serializers
from django.contrib.auth import get_user_model
from books.models import Book, Author, Category, Publisher, Language, Shelf, BookCopy
from members.models import Member
from borrowing.models import BorrowRecord

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "full_name",
            "role",
            "phone",
            "is_email_verified",
            "date_joined",
        ]
        read_only_fields = ["id", "date_joined"]


class AuthorSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = Author
        fields = ["id", "first_name", "last_name", "full_name", "nationality", "bio", "website", "is_active"]


class CategorySerializer(serializers.ModelSerializer):
    book_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description", "icon", "is_active", "book_count"]

    def get_book_count(self, obj):
        return obj.books.filter(is_deleted=False).count()


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ["id", "name", "slug", "country", "website", "email", "is_active"]


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ["id", "name", "code", "is_active"]


class ShelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shelf
        fields = ["id", "code", "name", "floor", "section", "capacity", "is_active"]


class BookCopySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCopy
        fields = ["id", "barcode", "condition", "status", "shelf", "acquisition_date", "price", "notes"]


class BookListSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    publisher = PublisherSerializer(read_only=True)
    language = LanguageSerializer(read_only=True)

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "slug",
            "isbn",
            "isbn13",
            "authors",
            "publisher",
            "categories",
            "language",
            "cover_image",
            "description",
            "edition",
            "pages",
            "publication_year",
            "status",
            "total_copies",
            "available_copies",
            "is_featured",
            "tags",
            "created_at",
        ]


class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            "title",
            "isbn",
            "isbn13",
            "authors",
            "publisher",
            "categories",
            "language",
            "cover_image",
            "description",
            "edition",
            "pages",
            "publication_year",
            "publication_date",
            "status",
            "total_copies",
            "available_copies",
            "shelf",
            "call_number",
            "tags",
            "is_featured",
        ]


class MemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    can_borrow = serializers.BooleanField(read_only=True)
    current_borrow_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Member
        fields = [
            "id",
            "user",
            "card_number",
            "membership_type",
            "status",
            "membership_start",
            "membership_end",
            "max_books_allowed",
            "fine_balance",
            "can_borrow",
            "current_borrow_count",
            "created_at",
        ]


class BorrowRecordSerializer(serializers.ModelSerializer):
    member_name = serializers.CharField(source="member.user.get_full_name", read_only=True)
    book_title = serializers.CharField(source="book_copy.book.title", read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)
    days_overdue = serializers.IntegerField(read_only=True)

    class Meta:
        model = BorrowRecord
        fields = [
            "id",
            "member",
            "member_name",
            "book_copy",
            "book_title",
            "borrow_date",
            "due_date",
            "return_date",
            "status",
            "renew_count",
            "fine_amount",
            "fine_paid",
            "is_overdue",
            "days_overdue",
            "notes",
            "created_at",
        ]


class DashboardStatsSerializer(serializers.Serializer):
    total_books = serializers.IntegerField()
    total_members = serializers.IntegerField()
    active_borrows = serializers.IntegerField()
    overdue_count = serializers.IntegerField()
    available_copies = serializers.IntegerField()
    total_copies = serializers.IntegerField()
