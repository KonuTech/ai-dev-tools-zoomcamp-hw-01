.PHONY: help up down build restart logs migrate test shell createsuperuser clean

help:
	@echo "Django TODO App - Available commands:"
	@echo "  make up              - Start the application"
	@echo "  make down            - Stop the application"
	@echo "  make build           - Build and start the application"
	@echo "  make restart         - Restart the application"
	@echo "  make logs            - View application logs"
	@echo "  make migrate         - Run database migrations"
	@echo "  make test            - Run tests"
	@echo "  make shell           - Open Django shell"
	@echo "  make createsuperuser - Create a superuser"
	@echo "  make clean           - Stop and remove all containers, volumes, and networks"

up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose up -d --build

restart:
	docker compose restart

logs:
	docker compose logs -f

migrate:
	docker compose run --rm web python manage.py migrate

test:
	docker compose run --rm web python manage.py test

shell:
	docker compose run --rm web python manage.py shell

createsuperuser:
	docker compose run --rm web python manage.py createsuperuser

clean:
	docker compose down -v
	docker system prune -f
