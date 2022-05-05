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

load-demo:
	poetry run python manage.py loaddata polling_api/apps/quiz/tests/fixtures.yaml; \
	poetry run python manage.py loaddata polling_api/apps/question/tests/fixtures.yaml; \
	poetry run python manage.py loaddata polling_api/apps/choice/tests/fixtures.yaml; \
	poetry run python manage.py loaddata polling_api/apps/user/tests/fixtures.yaml; \
	poetry run python manage.py loaddata polling_api/apps/journal/tests/fixtures.yaml
