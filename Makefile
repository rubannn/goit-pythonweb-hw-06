.PHONY: start stop down

start:
	docker compose up -d

stop:
	docker compose stop

clean:          ## Зупинити та видалити контейнер, образ і volume
	docker compose down --volumes --rmi local
	docker container prune -f
	docker image prune -a -f
	docker volume prune -f
	docker network prune -f


makemigrations:
	alembic revision --autogenerate -m "auto"

migrate:
	alembic upgrade head

# alias
mm: makemigrations

m: migrate
