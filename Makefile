.PHONY: run createsuperuser

run:
	python manage.py runserver

createsuperuser:
	python manage.py createsuperuser
