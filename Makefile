.PHONY: run createsuperuser

run:
	python manage.py runserver

createsuperuser:
	python manage.py createsuperuser

bootstrap:
	python manage.py makemigrations
	python manage.py migrate
