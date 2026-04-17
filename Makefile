.PHONY: start stop down

run:
	docker compose up -d

stop:
	docker compose stop

down:
	docker compose down -v

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

seed:
	python seed.py

db_init: m seed

db_check:
	python wait_for_db.py

db_reset: down run db_check db_init

cli:
	python main.py -h
