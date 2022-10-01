.PHONY: run createsuperuser

run:
	python manage.py runserver

createsuperuser:
	python manage.py createsuperuser

bootstrap:
	rm -rf db.sqlite3
	python manage.py makemigrations
	python manage.py migrate
