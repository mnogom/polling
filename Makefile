install:
	poetry install

run:
	poetry run python polling_app/manage.py runserver

gunicorn-run:
	source .venv/bin/activate ; \
	cd polling_app ; \
	gunicorn polling_app.wsgi ; \

django-shell:
	cd polling_app ; \
	poetry run python manage.py shell ; \

migrations:
	poetry run python polling_app/manage.py makemigrations

migrate:
	poetry run python polling_app/manage.py migrate

lint:
	poetry run flake8 polling_app