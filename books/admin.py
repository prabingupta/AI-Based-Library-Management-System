from django.contrib import admin
from .models import Category, Author, Publisher, Language, Shelf, Book, BookCopy


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'nationality', 'is_active', 'created_at']
    list_filter = ['is_active', 'nationality']
    search_fields = ['first_name', 'last_name', 'email']
    prepopulated_fields = {'slug': ('first_name', 'last_name')}


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'founded_year', 'is_active', 'created_at']
    list_filter = ['is_active', 'country']
    search_fields = ['name', 'country']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'code']


@admin.register(Shelf)
class ShelfAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'floor', 'section', 'capacity', 'is_active']
    list_filter = ['is_active', 'floor']
    search_fields = ['code', 'name', 'section']


class BookCopyInline(admin.TabularInline):
    model = BookCopy
    extra = 1
    fields = ['barcode', 'condition', 'status', 'shelf', 'price']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'isbn', 'status', 'total_copies', 'available_copies', 'is_featured', 'created_at']
    list_filter = ['status', 'is_featured', 'is_active', 'language']
    search_fields = ['title', 'isbn', 'isbn13']
    filter_horizontal = ['authors', 'categories']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [BookCopyInline]
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'isbn', 'isbn13', 'cover_image', 'description')
        }),
        ('Details', {
            'fields': ('authors', 'publisher', 'categories', 'language', 'edition', 'pages', 'publication_date', 'publication_year')
        }),
        ('Library Info', {
            'fields': ('status', 'total_copies', 'available_copies', 'shelf', 'call_number', 'tags')
        }),
        ('Flags', {
            'fields': ('is_featured', 'is_active', 'is_deleted')
        }),
        ('AI Ready Fields', {
            'fields': ('embedding_vector', 'ai_summary', 'ai_tags'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(BookCopy)
class BookCopyAdmin(admin.ModelAdmin):
    list_display = ['barcode', 'book', 'condition', 'status', 'shelf', 'created_at']
    list_filter = ['condition', 'status']
    search_fields = ['barcode', 'book__title']
