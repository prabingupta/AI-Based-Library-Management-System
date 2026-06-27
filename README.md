# AI-Based Library Management System

A production-grade, enterprise-ready Library Management System built with Django, PostgreSQL, Redis, and Celery. Designed with a clean architecture that supports future AI module integration.

## Tech Stack

- **Backend:** Python 3.13, Django 6, Django REST Framework
- **Database:** PostgreSQL
- **Cache/Queue:** Redis, Celery
- **Frontend:** Bootstrap 5.3, Chart.js, FontAwesome 6, Google Fonts (Inter)
- **Auth:** JWT (SimpleJWT), Session-based login
- **Dev Tools:** Black, Flake8, Pre-commit

## Features

- Custom User model with 7 role types
- Book management (categories, authors, publishers, shelves, copies)
- Member management with membership cards and fine tracking
- Borrowing system (issue, return, renew, reserve)
- Real-time dashboard with Chart.js analytics
- Notification system (in-app, email-ready)
- Professional error pages (404, 500, 403)
- AI-ready architecture (embedding fields, future module hooks)

## Modules

| Module | Status |
|---|---|
| Authentication | Complete |
| Dashboard | Complete |
| Books | Complete |
| Members | Complete |
| Borrowing | Complete |
| Notifications | Complete |
| Reports | In Progress |
| API | In Progress |
| AI Features | Future |

## Setup

```bash
git clone https://github.com/prabingupta/AI-Based-Library-Management-System.git
cd AI-Based-Library-Management-System
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # configure your .env
python manage.py migrate
python manage.py seed_data
python manage.py createsuperuser
python manage.py runserver
```

## Project Structure
├── accounts/       # Custom user model, authentication

├── books/          # Book, Author, Publisher, Category, Shelf

├── members/        # Member profiles, membership management

├── borrowing/      # Borrow, Return, Renew, Reserve

├── notifications/  # In-app notification system

├── dashboard/      # Analytics and statistics

├── reports/        # Report generation (in progress)

├── api/            # REST API endpoints (in progress)

├── core/           # Base views, utilities, seed data

├── config/         # Django settings, URLs, WSGI

├── templates/      # All HTML templates

└── static/         # CSS, JS, images

## Default Credentials

- **Admin:** admin@library.com / Admin@1234
- **Members (seeded):** Member@1234

## License

MIT License — Prabin Kumar Gupta, 2024
