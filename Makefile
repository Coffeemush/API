
DOCKER_COMPOSE = docker compose
SERVICE_NAME = app

.PHONY: help
help:
	@echo "Available targets:"
	@echo "  start-api      : Start the API service"
	@echo "  stop-api       : Stop the API service"
	@echo "  restart-api    : Restart the API service"
	@echo "  stream-logs    : Stream logs of the API service in real-time"

.PHONY: start-api
start-api:
	$(DOCKER_COMPOSE) up -d --build $(SERVICE_NAME)

.PHONY: stop-api
stop-api:
	$(DOCKER_COMPOSE) stop $(SERVICE_NAME)
	$(DOCKER_COMPOSE) rm -f $(SERVICE_NAME)

.PHONY: restart-api
restart-api: stop-api start-api

.PHONY: stream-logs
stream-logs:
	$(DOCKER_COMPOSE) logs -f $(SERVICE_NAME)