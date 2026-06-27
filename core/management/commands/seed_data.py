from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta, date
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')
        self.create_languages()
        self.create_categories()
        self.create_publishers()
        self.create_authors()
        self.create_shelves()
        self.create_books()
        self.create_members()
        self.create_borrow_records()
        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))

    def create_languages(self):
        from books.models import Language
        languages = [
            ('English', 'en'), ('Nepali', 'ne'),
            ('Hindi', 'hi'), ('French', 'fr'), ('German', 'de'),
        ]
        for name, code in languages:
            Language.objects.get_or_create(name=name, code=code)
        self.stdout.write('  Languages created.')

    def create_categories(self):
        from books.models import Category
        categories = [
            ('Fiction', 'fa-solid fa-dragon'),
            ('Non-Fiction', 'fa-solid fa-book-open'),
            ('Science', 'fa-solid fa-flask'),
            ('Technology', 'fa-solid fa-microchip'),
            ('History', 'fa-solid fa-landmark'),
            ('Mathematics', 'fa-solid fa-square-root-variable'),
            ('Literature', 'fa-solid fa-feather'),
            ('Biography', 'fa-solid fa-user'),
            ('Philosophy', 'fa-solid fa-brain'),
            ('Economics', 'fa-solid fa-chart-line'),
        ]
        for name, icon in categories:
            Category.objects.get_or_create(name=name, defaults={'icon': icon})
        self.stdout.write('  Categories created.')

    def create_publishers(self):
        from books.models import Publisher
        publishers = [
            ('Penguin Random House', 'USA'),
            ('Oxford University Press', 'UK'),
            ('Cambridge University Press', 'UK'),
            ('HarperCollins', 'USA'),
            ('Ekta Books', 'Nepal'),
            ('Sajha Prakashan', 'Nepal'),
        ]
        for name, country in publishers:
            Publisher.objects.get_or_create(name=name, defaults={'country': country})
        self.stdout.write('  Publishers created.')

    def create_authors(self):
        from books.models import Author
        authors = [
            ('George', 'Orwell', 'British'),
            ('J.K.', 'Rowling', 'British'),
            ('Yuval Noah', 'Harari', 'Israeli'),
            ('Malcolm', 'Gladwell', 'Canadian'),
            ('Stephen', 'Hawking', 'British'),
            ('Laxmi Prasad', 'Devkota', 'Nepali'),
            ('Bhupi', 'Sherchan', 'Nepali'),
            ('Robert', 'Kiyosaki', 'American'),
            ('Dale', 'Carnegie', 'American'),
            ('Paulo', 'Coelho', 'Brazilian'),
        ]
        for first, last, nationality in authors:
            Author.objects.get_or_create(
                first_name=first, last_name=last,
                defaults={'nationality': nationality}
            )
        self.stdout.write('  Authors created.')

    def create_shelves(self):
        from books.models import Shelf
        shelves = [
            ('A1', 'Fiction Shelf', 'Ground Floor', 'Section A'),
            ('A2', 'Non-Fiction Shelf', 'Ground Floor', 'Section A'),
            ('B1', 'Science & Tech', 'First Floor', 'Section B'),
            ('B2', 'History & Philosophy', 'First Floor', 'Section B'),
            ('C1', 'Reference Books', 'Second Floor', 'Section C'),
        ]
        for code, name, floor, section in shelves:
            Shelf.objects.get_or_create(
                code=code,
                defaults={'name': name, 'floor': floor, 'section': section}
            )
        self.stdout.write('  Shelves created.')

    def create_books(self):
        from books.models import Book, BookCopy, Author, Publisher, Category, Language, Shelf

        english = Language.objects.filter(code='en').first()
        nepali = Language.objects.filter(code='ne').first()
        shelf_a1 = Shelf.objects.filter(code='A1').first()
        shelf_b1 = Shelf.objects.filter(code='B1').first()
        penguin = Publisher.objects.filter(name='Penguin Random House').first()
        oxford = Publisher.objects.filter(name='Oxford University Press').first()

        fiction = Category.objects.filter(name='Fiction').first()
        science = Category.objects.filter(name='Science').first()
        tech = Category.objects.filter(name='Technology').first()
        history = Category.objects.filter(name='History').first()

        orwell = Author.objects.filter(last_name='Orwell').first()
        harari = Author.objects.filter(last_name='Harari').first()
        hawking = Author.objects.filter(last_name='Hawking').first()
        kiyosaki = Author.objects.filter(last_name='Kiyosaki').first()
        coelho = Author.objects.filter(last_name='Coelho').first()

        books_data = [
            {
                'title': '1984',
                'isbn': '9780451524935',
                'description': 'A dystopian social science fiction novel.',
                'publisher': penguin,
                'language': english,
                'shelf': shelf_a1,
                'pages': 328,
                'publication_year': 1949,
                'total_copies': 5,
                'available_copies': 4,
                'authors': [orwell],
                'categories': [fiction],
            },
            {
                'title': 'Sapiens: A Brief History of Humankind',
                'isbn': '9780062316097',
                'description': 'A survey of the history of humankind from the Stone Age to the modern era.',
                'publisher': penguin,
                'language': english,
                'shelf': shelf_b1,
                'pages': 443,
                'publication_year': 2011,
                'total_copies': 4,
                'available_copies': 3,
                'authors': [harari],
                'categories': [history, science],
            },
            {
                'title': 'A Brief History of Time',
                'isbn': '9780553380163',
                'description': 'A landmark volume in science writing by one of the great minds of our time.',
                'publisher': oxford,
                'language': english,
                'shelf': shelf_b1,
                'pages': 212,
                'publication_year': 1988,
                'total_copies': 3,
                'available_copies': 3,
                'authors': [hawking],
                'categories': [science],
            },
            {
                'title': 'Rich Dad Poor Dad',
                'isbn': '9781612680194',
                'description': 'What the rich teach their kids about money that the poor and middle class do not.',
                'publisher': penguin,
                'language': english,
                'shelf': shelf_a1,
                'pages': 336,
                'publication_year': 1997,
                'total_copies': 6,
                'available_copies': 5,
                'authors': [kiyosaki],
                'categories': [Category.objects.filter(name='Economics').first()],
            },
            {
                'title': 'The Alchemist',
                'isbn': '9780062315007',
                'description': 'A philosophical novel about a young Andalusian shepherd.',
                'publisher': penguin,
                'language': english,
                'shelf': shelf_a1,
                'pages': 197,
                'publication_year': 1988,
                'total_copies': 4,
                'available_copies': 4,
                'authors': [coelho],
                'categories': [fiction],
            },
        ]

        for book_data in books_data:
            authors = book_data.pop('authors')
            categories = book_data.pop('categories')
            book, created = Book.objects.get_or_create(
                title=book_data['title'],
                defaults=book_data
            )
            if created:
                book.authors.set(authors)
                book.categories.set([c for c in categories if c])
                for i in range(book.total_copies):
                    barcode = f"BC{book.isbn[-4:]}{str(i+1).zfill(3)}"
                    status = 'available' if i < book.available_copies else 'borrowed'
                    BookCopy.objects.get_or_create(
                        barcode=barcode,
                        defaults={'book': book, 'status': status, 'condition': 'good'}
                    )
        self.stdout.write('  Books created.')

    def create_members(self):
        from members.models import Member

        members_data = [
            ('ram', 'Ram', 'Sharma', 'ram.sharma@library.com', 'student', 'MEM001'),
            ('sita', 'Sita', 'Thapa', 'sita.thapa@library.com', 'student', 'MEM002'),
            ('hari', 'Hari', 'Bahadur', 'hari.bahadur@library.com', 'teacher', 'MEM003'),
            ('gita', 'Gita', 'Poudel', 'gita.poudel@library.com', 'student', 'MEM004'),
            ('krishna', 'Krishna', 'Karki', 'krishna.karki@library.com', 'teacher', 'MEM005'),
        ]

        for username, first, last, email, role, card in members_data:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': first,
                    'last_name': last,
                    'email': email,
                    'role': role,
                }
            )
            if created:
                user.set_password('Member@1234')
                user.save()

            Member.objects.get_or_create(
                user=user,
                defaults={
                    'card_number': card,
                    'membership_type': role if role in ['student', 'teacher', 'guest'] else 'student',
                    'status': 'active',
                    'membership_start': date.today(),
                    'membership_end': date.today() + timedelta(days=365),
                    'max_books_allowed': 5 if role == 'teacher' else 3,
                }
            )
        self.stdout.write('  Members created.')

    def create_borrow_records(self):
        from members.models import Member
        from books.models import BookCopy
        from borrowing.models import BorrowRecord

        members = list(Member.objects.filter(status='active')[:3])
        copies = list(BookCopy.objects.filter(status='available')[:5])

        if not members or not copies:
            self.stdout.write('  Skipping borrow records (no members or copies).')
            return

        for i, member in enumerate(members):
            if i >= len(copies):
                break
            copy = copies[i]
            due = timezone.now() + timedelta(days=random.choice([7, 10, 14, -2, -5]))
            record, created = BorrowRecord.objects.get_or_create(
                member=member,
                book_copy=copy,
                status='borrowed',
                defaults={
                    'borrow_date': timezone.now() - timedelta(days=random.randint(1, 10)),
                    'due_date': due,
                }
            )
            if created:
                copy.status = 'borrowed'
                copy.save()

        returned_copy = copies[3] if len(copies) > 3 else None
        if returned_copy and members:
            BorrowRecord.objects.get_or_create(
                member=members[0],
                book_copy=returned_copy,
                status='returned',
                defaults={
                    'borrow_date': timezone.now() - timedelta(days=20),
                    'due_date': timezone.now() - timedelta(days=6),
                    'return_date': timezone.now() - timedelta(days=7),
                }
            )
        self.stdout.write('  Borrow records created.')
