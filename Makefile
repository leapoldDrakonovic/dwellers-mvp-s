start-compose:
	docker compose up -d
	bash scripts/ping-to-shut-error

stop-compose:
	docker compose stop
	docker compose rm
	docker system prune -a --volumes

restart-compose:
	make stop-compose
	make start-compose

clear-all-data:
	docker compose rm
	docker system prune -a --volumes

update-all:
	docker compose up --detach --build
	bash scripts/ping-to-shut-error

restart-api:
	docker compose restart web celery-worker celery-flower celery-beat

restart-db:
	docker compose restart db db-admin

restart-redis:
	docker compose restart redis redis-admin

check_local_branch_status:
	git checkout

sync_master_to_branch:
	git merge main

sync_local_to_branch:
	git push

sync_main_to_local: # также для того, чтобы добавить в ветку недостающие коммиты main
	git pull origin main

auto__logs:
	bash scripts/check-logs
