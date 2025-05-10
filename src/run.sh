#!/bin/bash

# OpenHands + GPT-CLI Integration Runner
# Bei Fehler beenden
set -e

# Farben fur die Ausgabe
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # Keine Farbe

echo -e "${GREEN}OpenHands + GPT-CLI Integration Runner${NC}"
echo "========================================"

# Wechsle zum Hauptverzeichnis des Projekts
cd "$(dirname "$0")"

# Lade Umgebungsvariablen
if [ -f .env ]; then
    echo -e "${YELLOW}Lade Umgebungsvariablen...${NC}"
    export $(grep -v '^#' .env | xargs)
fi

# Prufe, ob Setup ausgefuhrt wurde
if [ ! -f "config/github_token.txt" ]; then
    echo -e "${YELLOW}Fuhre Setup aus...${NC}"
    make setup
fi

# Starte Docker-Container
echo -e "${YELLOW}Starte Docker-Container...${NC}"
make start

# Warte, bis OpenHands bereit ist
echo -e "${YELLOW}Warte, bis OpenHands bereit ist...${NC}"
MAX_RETRIES=30
RETRY_COUNT=0
while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if curl -s http://localhost:17243/api/status > /dev/null; then
        echo -e "${GREEN}OpenHands ist bereit!${NC}"
        break
    fi
    echo "Warte, bis OpenHands bereit ist... ($((RETRY_COUNT + 1))/$MAX_RETRIES)"
    RETRY_COUNT=$((RETRY_COUNT + 1))
    sleep 2
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
    echo -e "${RED}OpenHands ist nach $MAX_RETRIES Versuchen nicht bereit. Beende.${NC}"
    exit 1
fi

# Fuhre die Integrationstests aus
echo -e "${YELLOW}Fuhre Integrationstests aus...${NC}"
make test

# Gib Erfolgsmeldung aus
echo -e "${GREEN}Integration lauft erfolgreich!${NC}"
echo ""
echo "OpenHands GUI: http://localhost:3000"
echo "OpenHands API: http://localhost:17243"
echo ""
echo "Verfugbare Befehle:"
echo "  gpt run-tests --repo-path /pfad/zum/repository"
echo "  gpt check-pr <PR_NUMMER> --repo-path /pfad/zum/repository"
echo "  gpt fix-issue <ISSUE_NUMMER> --repo-path /pfad/zum/repository"
echo "  gpt verify-fix <ISSUE_NUMMER> --repo-path /pfad/zum/repository"
echo ""
echo "Um die Integration zu stoppen, fuhre aus: make stop"

exit 0
