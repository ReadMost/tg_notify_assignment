run_redis:
	docker-compose -f docker-compose.local.yaml up redis

run_redis_bg:
	docker-compose -f docker-compose.local.yaml up redis -d

pre_commit_hooks:
	pre-commit run --all-files

run_celery_beat:
	celery -A tg_notifier_assignment beat -l INFO

run_celery_worker:
	celery -A tg_notifier_assignment worker -l INFO

run_flower:
	celery -A tg_notifier_assignment flower --port=${FLOWER_PORT} --basic_auth=${FLOWER_USER}:${FLOWER_PASS} --host=0.0.0.0
