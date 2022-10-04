.PHONY: run createsuperuser

run:
	python manage.py runserver

createsuperuser:
	python manage.py createsuperuser

bootstrap:
	rm -rf db.sqlite3 events/migrations/00*.py
	python manage.py makemigrations
	python manage.py migrate
