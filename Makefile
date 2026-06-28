.PHONY: run migrate seed shell test lint format install

run:
	python manage.py runserver

migrate:
	python manage.py makemigrations
	python manage.py migrate

seed:
	python manage.py seed_data

shell:
	python manage.py shell

superuser:
	python manage.py createsuperuser

test:
	python manage.py test

lint:
	flake8 . --exclude=venv,migrations --max-line-length=120

format:
	black . --exclude=venv

install:
	pip install -r requirements.txt

collect:
	python manage.py collectstatic --noinput

celery:
	celery -A config worker --loglevel=info

celery-beat:
	celery -A config beat --loglevel=info

docker-up:
	docker-compose up --build

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f web
