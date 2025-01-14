dc = docker compose
dc_exec = ${dc} exec ${OPTIONS}

.SILENT:

CONTAINER ?= app
SHELL_CMD ?= bash
OPTIONS ?= -u root

# Docker
run:
	${dc} up -d --build

build:
	${dc} build --no-cache

stop:
	${dc} stop

down:
	${dc} down

logs:
	${dc} logs -f $(CONTAINER)

logs-all:
	${dc} logs -f

restart:
	$(dc) restart $(CONTAINER)

shell:
	${dc_exec} $(CONTAINER) $(SHELL_CMD)

shell-root:
	$(MAKE) shell OPTIONS="-u root"

ps:
	${dc} ps

# Django
startapp:
	$(dc) exec $(OPTIONS) $(CONTAINER) python3.13 manage.py startapp $(app) api/$(app)

createsuperuser:
	$(dc) exec $(OPTIONS) $(CONTAINER) python3.13 manage.py createsuperuser

# Migrations
migrations:
	$(dc) exec $(OPTIONS) $(CONTAINER) python3.13 manage.py makemigrations

migrate:
	$(dc) exec $(OPTIONS) $(CONTAINER) python3.13 manage.py migrate

migrate-to:
	$(dc) exec $(OPTIONS) $(CONTAINER) python3.13 manage.py migrate "$(version)"

migrations-history:
	$(dc) exec $(OPTIONS) $(CONTAINER) python3.13 manage.py showmigrations --list

# Requirements
pip-list:
	$(dc) exec $(OPTIONS) $(CONTAINER) pip list
