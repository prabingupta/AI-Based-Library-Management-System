# Changelog

All notable changes to LibraryOS are documented here.

## [1.0.0] - 2024-06-28

### Added
- Custom User model with 7 role types (Super Admin, Library Admin, Librarian, Assistant Librarian, Teacher, Student, Guest)
- Full authentication system (login, logout, profile)
- Dashboard with Chart.js line chart and doughnut chart
- Book management (CRUD, categories, authors, publishers, shelves, book copies)
- Member management with membership cards and fine tracking
- Borrowing system (issue, return, renew with automatic fine calculation)
- Reservation system model
- Fine rules engine
- In-app notification system with mark-read and mark-all-read
- Global search across books, members, and borrow records
- Categories grid page with book counts
- Reports and analytics page
- Dark mode with localStorage persistence
- Professional error pages (404, 500, 403)
- Celery task queue with Redis broker
- Celery Beat scheduled tasks (due date reminders, overdue alerts)
- Docker and docker-compose configuration
- Pre-commit hooks (Black, Flake8, pre-commit-hooks)
- Seed data management command
- Makefile developer shortcuts
- AI-ready model fields (embedding_vector, ai_summary, ai_tags)

### Technical
- PostgreSQL database with UUID primary keys
- Soft delete pattern on all models
- Audit fields (created_at, updated_at, created_by)
- JWT authentication (SimpleJWT)
- Whitenoise for static file serving
- Gunicorn WSGI server
- django-celery-beat for scheduled tasks

## [Unreleased]

### Planned
- REST API endpoints (Django REST Framework)
- Book Recommendation AI (Sentence Transformers)
- OCR Book Scanner (OpenCV + Tesseract)
- ISBN Barcode Scanner
- AI-powered Smart Search (LLM)
- Library Chatbot
- PDF/Excel report export
- Email notification delivery
- SMS notification support
- Two-factor authentication
