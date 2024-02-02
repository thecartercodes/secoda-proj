up:
	docker compose -f docker-compose-local.yml up -d

down:
	docker compose -f docker-compose-local.yml down

tests:
	python -m unittest test.pipeline

install:
	pip install .

db-shell:
	psql -h $$POSTGRES_HOST -p $$POSTGRES_PORT -U $$POSTGRES_USER -d $$POSTGRES_DB

redis-shell:
	redis-cli

migrate:
	psql -h $$POSTGRES_HOST -p $$POSTGRES_PORT -U $$POSTGRES_USER -d $$POSTGRES_DB -f migrations/price_metrics.sql
