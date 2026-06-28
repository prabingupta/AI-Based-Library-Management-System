<div align="center">

# 📚 LibraryOS

### AI-Based Library Management System

**A production-grade, enterprise-ready Library Management System**
built with Django 6, PostgreSQL, Redis, and Celery.
Designed with a clean architecture that supports future AI module integration.

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-6.0-green.svg)](https://djangoproject.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue.svg)](https://postgresql.org)
[![Redis](https://img.shields.io/badge/Redis-7-red.svg)](https://redis.io)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## Features

- **Authentication** — JWT + Session login, role-based access (7 roles)
- **Dashboard** — Real-time stats, Chart.js line + doughnut charts
- **Books** — Full CRUD, categories, authors, publishers, shelves, copies
- **Members** — Membership cards, fine tracking, borrow history
- **Borrowing** — Issue, return, renew with automatic fine calculation
- **Notifications** — In-app notification system with mark-read
- **Reports** — Analytics overview with most-borrowed books
- **Search** — Global search across books, members, borrow records
- **Dark Mode** — System-wide dark mode with localStorage persistence
- **AI-Ready** — Embedding fields, AI summary fields, modular architecture

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.13, Django 6, Django REST Framework |
| Database | PostgreSQL 16 |
| Cache/Queue | Redis 7, Celery 5, Celery Beat |
| Frontend | Bootstrap 5.3, Chart.js, FontAwesome 6, Inter font |
| Auth | JWT (SimpleJWT) + Session |
| Server | Gunicorn + Nginx (Docker) |
| Dev Tools | Black, Flake8, Pre-commit |

---

## Project Structure
AI-Based-Library-Management-System/

├── accounts/           # Custom user model, auth views

├── books/              # Book, Author, Publisher, Category, Shelf

├── members/            # Member profiles, membership management

├── borrowing/          # Issue, Return, Renew, Reserve

├── notifications/      # In-app notifications + Celery tasks

├── dashboard/          # Analytics and statistics

├── reports/            # Report generation

├── api/                # REST API (in progress)

├── core/               # Base views, seed data command

├── config/             # Django settings, URLs, Celery

├── templates/          # All HTML templates

│   ├── base.html

│   ├── partials/

│   ├── accounts/

│   ├── books/

│   ├── members/

│   ├── borrowing/

│   ├── notifications/

│   ├── reports/

│   └── errors/

├── static/             # CSS, JS

├── Dockerfile

├── docker-compose.yml

└── Makefile

---

## Quick Start

### Local Development

```bash
# Clone
git clone https://github.com/prabingupta/AI-Based-Library-Management-System.git
cd AI-Based-Library-Management-System

# Environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Config
cp .env.example .env
# Edit .env with your database credentials

# Database
python manage.py migrate
python manage.py seed_data
python manage.py createsuperuser

# Run
python manage.py runserver
```

### Docker

```bash
cp .env.example .env
docker-compose up --build
```

### Makefile Shortcuts

```bash
make run          # Start dev server
make migrate      # Run migrations
make seed         # Seed sample data
make lint         # Flake8 check
make format       # Black format
make docker-up    # Docker compose up
```

---

## Default Credentials

| Role | Email | Password |
|---|---|---|
| Super Admin | admin@library.com | Admin@1234 |
| Seeded Members | (see seed data) | Member@1234 |

---

## Module Status

| Module | Status | Notes |
|---|---|---|
| Authentication | ✅ Complete | Login, logout, profile |
| Dashboard | ✅ Complete | Charts, stats, activity |
| Books | ✅ Complete | CRUD, search, categories |
| Members | ✅ Complete | Full management |
| Borrowing | ✅ Complete | Issue, return, renew |
| Notifications | ✅ Complete | In-app, Celery tasks |
| Reports | ✅ Complete | Analytics overview |
| Search | ✅ Complete | Global search |
| Dark Mode | ✅ Complete | localStorage persistence |
| Docker | ✅ Complete | Production ready |
| REST API | 🔄 In Progress | DRF endpoints |
| AI - Recommendations | 📋 Planned | Sentence Transformers |
| AI - OCR Scanner | 📋 Planned | OpenCV + Tesseract |
| AI - Smart Search | 📋 Planned | LLM-powered search |
| AI - Chatbot | 📋 Planned | LLM Assistant |

---

## AI-Ready Architecture

Every model includes fields prepared for future AI integration:

```python
# books/models.py
embedding_vector = models.TextField(blank=True, null=True)
ai_summary = models.TextField(blank=True, null=True)
ai_tags = models.TextField(blank=True, null=True)
```

Future AI modules will plug into the existing architecture without requiring significant database changes.

---

## Developer

**Prabin Kumar Gupta**
BSc (Hons) Computing with AI
Islington College, Kathmandu (London Metropolitan University)

GitHub: [@prabingupta](https://github.com/prabingupta)

---

## License

MIT License — 2024
