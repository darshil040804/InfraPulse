.PHONY: up down test reset-demo resume-telemetry

up:
	docker compose up -d

down:
	docker compose down

test:
	docker compose run --rm -e DATABASE_URL=sqlite+pysqlite:///:memory: -e ENABLE_KAFKA_CONSUMER=false backend python -m pytest -vv
	cd frontend && npm audit --audit-level=moderate && npm run build
	docker compose config --quiet

reset-demo:
	docker compose up -d postgres kafka backend
	docker compose stop telemetry-generator
	docker compose exec backend python -m app.scripts.reset_demo

resume-telemetry:
	docker compose up -d telemetry-generator
