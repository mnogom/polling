install:
	poetry install

run:
	poetry run python manage.py runserver

django-shell:
	poetry run python manage.py shell

migrations:
	poetry run python manage.py makemigrations

migrate:
	poetry run python manage.py migrate

lint:
	poetry run flake8 polling_app