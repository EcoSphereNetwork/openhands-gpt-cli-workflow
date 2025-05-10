.PHONY: setup start stop restart status test clean help

# Standardziel
help:
	@echo "OpenHands + GPT-CLI Integration"
	@echo ""
	@echo "Verfugbare Ziele:"
	@echo "  setup    - Setup-Skript ausfuhren"
	@echo "  start    - Docker-Container starten"
	@echo "  stop     - Docker-Container stoppen"
	@echo "  restart  - Docker-Container neustarten"
	@echo "  status   - Status der Docker-Container prufen"
	@echo "  test     - Integrationstests ausfuhren"
	@echo "  clean    - Temporare Dateien bereinigen"
	@echo "  help     - Diese Hilfemeldung anzeigen"

# Integration einrichten
setup:
	@echo "Richte die Integration ein..."
	@chmod +x scripts/*.py scripts/*.sh
	@scripts/setup.sh

# Docker-Container starten
start:
	@echo "Starte Docker-Container..."
	@cd docker && docker-compose up -d
	@echo "Warte, bis Container gestartet sind..."
	@sleep 5
	@docker ps --filter "name=openhands-gui"

# Docker-Container stoppen
stop:
	@echo "Stoppe Docker-Container..."
	@cd docker && docker-compose down

# Docker-Container neustarten
restart: stop start

# Status der Docker-Container prufen
status:
	@echo "Prufe Docker-Container-Status..."
	@docker ps --filter "name=openhands-gui"
	@echo ""
	@echo "Prufe OpenHands API-Status..."
	@curl -s http://localhost:17244/api/status || echo "OpenHands API nicht erreichbar"

# Integrationstests ausfuhren
test:
	@echo "Fuhre Integrationstests aus..."
	@python3 tests/test_integration.py

# Temporare Dateien bereinigen
clean:
	@echo "Bereinige temporare Dateien..."
	@find . -name "__pycache__" -type d -exec rm -rf {} +
	@find . -name "*.pyc" -delete
	@find . -name "*.pyo" -delete
	@find . -name "*.pyd" -delete
	@find . -name ".pytest_cache" -type d -exec rm -rf {} +
	@find . -name ".coverage" -delete
	@find . -name "htmlcov" -type d -exec rm -rf {} +
	@find . -name "*.log" -delete