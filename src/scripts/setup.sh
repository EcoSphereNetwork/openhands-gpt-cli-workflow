#!/bin/bash

# OpenHands + GPT-CLI Integration Setup Script
# Exit on error
set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}OpenHands + GPT-CLI Integration Setup${NC}"
echo "========================================"

# Wechsle zum Hauptverzeichnis des Projekts
cd "$(dirname "$0")/.."

# Lade Umgebungsvariablen
if [ -f .env ]; then
    echo -e "${YELLOW}Lade Umgebungsvariablen...${NC}"
    export $(grep -v '^#' .env | xargs)
fi

# Prüfe Voraussetzungen
echo -e "${YELLOW}Prüfe Voraussetzungen...${NC}"

# Prüfe Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Docker nicht gefunden. Bitte installiere Docker.${NC}"
    exit 1
fi

# Prüfe Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Docker Compose nicht gefunden. Bitte installiere Docker Compose.${NC}"
    exit 1
fi

# Prüfe GitHub CLI
if ! command -v gh &> /dev/null; then
    echo -e "${RED}GitHub CLI nicht gefunden. Bitte installiere GitHub CLI.${NC}"
    exit 1
fi

# Prüfe Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 nicht gefunden. Bitte installiere Python 3.${NC}"
    exit 1
fi

# Erstelle benötigte Verzeichnisse
echo -e "${YELLOW}Stelle Projektstruktur sicher...${NC}"
mkdir -p workspace config scripts docker

# Mache Skripte ausführbar
echo -e "${YELLOW}Mache Skripte ausführbar...${NC}"
chmod +x scripts/*.py
chmod +x scripts/*.sh

# Richte GitHub CLI ein
echo -e "${YELLOW}Richte GitHub CLI ein...${NC}"
if ! gh auth status &> /dev/null; then
    echo "Bitte authentifiziere dich bei GitHub:"
    gh auth login
else
    echo "GitHub CLI bereits authentifiziert."
fi

# Konfiguriere GitHub CLI
echo -e "${YELLOW}Konfiguriere GitHub CLI...${NC}"
if [ -z "$GITHUB_REPOSITORY" ]; then
    read -p "Gib das GitHub-Repository ein (z.B. benutzername/repo): " github_repo
else
    github_repo="$GITHUB_REPOSITORY"
    echo "Verwende Repository aus .env: $github_repo"
fi
gh repo set-default "$github_repo"

# Erstelle GitHub-Token falls nötig
if [ ! -s "config/github_token.txt" ] || grep -q "GITHUB_TOKEN" "config/github_token.txt"; then
    echo -e "${YELLOW}Richte GitHub-Token ein...${NC}"
    
    if [ -n "$GITHUB_TOKEN" ]; then
        echo "Verwende Token aus Umgebungsvariable."
        github_token="$GITHUB_TOKEN"
    else
        read -p "Gib dein GitHub-Token ein (oder drücke Enter, um ein neues zu erstellen): " github_token
        
        if [ -z "$github_token" ]; then
            echo "Erstelle ein neues GitHub-Token..."
            echo "Bitte folge den Anweisungen im Browser."
            gh auth token
            read -p "Gib das neu erstellte Token ein: " github_token
        fi
    fi
    
    echo "$github_token" > config/github_token.txt
    echo "GitHub-Token in config/github_token.txt gespeichert"
fi

# Konfiguriere GPT-CLI
echo -e "${YELLOW}Konfiguriere GPT-CLI...${NC}"
mkdir -p ~/.config/gpt-cli
cp config/gpt.yml ~/.config/gpt-cli/

# Installiere Python-Abhängigkeiten
echo -e "${YELLOW}Installiere Python-Abhängigkeiten...${NC}"
pip3 install requests

# Prüfe, ob GPT-CLI installiert ist
if ! command -v gpt &> /dev/null; then
    echo -e "${YELLOW}Installiere GPT-CLI...${NC}"
    pip3 install gpt-command-line
fi

# Starte Docker-Container
echo -e "${YELLOW}Starte Docker-Container...${NC}"
cd docker && docker-compose up -d
cd ..

echo -e "${GREEN}Setup erfolgreich abgeschlossen!${NC}"
echo ""
echo "Nächste Schritte:"
echo "1. Greife auf die OpenHands GUI unter http://localhost:3000 zu"
echo "2. In der OpenHands GUI, konfiguriere API-Schlüssel (Einstellungen → API-Schlüssel)"
echo "3. Führe Tests aus mit: gpt run-tests --repo-path /pfad/zum/repo"
echo "4. Überprüfe PRs mit: gpt check-pr <PR_NUMMER> --repo-path /pfad/zum/repo"
echo "5. Behebe Issues mit: gpt fix-issue <ISSUE_NUMMER> --repo-path /pfad/zum/repo"
echo "6. Überprüfe Fixes mit: gpt verify-fix <ISSUE_NUMMER> --repo-path /pfad/zum/repo"
echo ""
echo "Viel Spaß mit deinem automatisierten Workflow!"

exit 0