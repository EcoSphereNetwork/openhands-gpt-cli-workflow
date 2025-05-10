# OpenHands Workflow

Eine vollständige Integration von OpenHands (GUI & CLI) mit gpt-cli und GitHub CLI für automatisierte Tests, Issue-Management und Fix-Generierung.

![OpenHands Workflow](https://placeholder-image.com/openhands-workflow.png)

## Inhaltsverzeichnis

- [Übersicht](#übersicht)
- [Architektur](#architektur)
- [Voraussetzungen](#voraussetzungen)
- [Installation](#installation)
- [Konfiguration](#konfiguration)
- [Verwendung](#verwendung)
- [Workflow-Beschreibung](#workflow-beschreibung)
- [Dateien und Komponenten](#dateien-und-komponenten)
- [Fehlerbehebung](#fehlerbehebung)
- [Erweiterungsmöglichkeiten](#erweiterungsmöglichkeiten)
- [Lizenz](#lizenz)

## Übersicht

Dieses Projekt bietet eine nahtlose Integration zwischen OpenHands, gpt-cli und GitHub CLI, um einen vollautomatisierten Workflow für Tests, Fehlererkennung und -behebung zu ermöglichen. Es ermöglicht:

- Automatische Ausführung von Tests mittels gpt-cli
- Automatische Erstellung von GitHub-Issues bei fehlgeschlagenen Tests
- Automatische Fehleranalyse und Fix-Erstellung durch OpenHands
- Automatische Überprüfung und ggf. Genehmigung der generierten Pull Requests

Die Integration ist so konzipiert, dass sie in CI/CD-Pipelines integriert werden kann oder als eigenständiges Entwicklungstool funktioniert.

## Architektur

```
[Docker-Container]
├── OpenHands GUI (Port 17243)
└── OpenHands CLI/Python-API
[Host-System]
├── gpt-cli (lokale Tests)
└── GitHub CLI (Issue-Erstellung)
```

**Datenfluss:**

1. gpt-cli führt Tests aus → bei Fehlern → GitHub Issue erstellen
2. GitHub Issue → OpenHands analysiert → erstellt Fix als PR
3. gpt-cli überprüft PR → bei Erfolg → automatische Genehmigung

## Voraussetzungen

Bevor Sie beginnen, stellen Sie sicher, dass folgende Software installiert ist:

- **Docker** und **Docker Compose** (neueste Version)
- **Python 3.6+** mit pip
- **Node.js** und npm
- **GitHub CLI** (`gh`) installiert und konfiguriert
- **gpt-cli** installiert
- **Anthropic API-Schlüssel** für Claude 3.7 Sonnet

## Installation

### 1. Repository klonen

```bash
git clone https://github.com/yourusername/openhands-workflow.git
cd openhands-workflow
```

### 2. Setup-Skript ausführen

```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

Das Setup-Skript führt folgende Aktionen aus:
- Erstellt die Verzeichnisstruktur
- Installiert benötigte Python-Abhängigkeiten
- Konfiguriert GitHub CLI
- Startet den OpenHands Docker-Container
- Richtet die notwendigen Konfigurationsdateien ein

### 3. Manueller Start (alternative zum Setup-Skript)

Wenn Sie das Setup-Skript nicht verwenden möchten, können Sie auch manuell starten:

```bash
# Verzeichnisstruktur erstellen
mkdir -p docker workspace config scripts gpt-cli

# Python-Abhängigkeiten installieren
pip install requests

# Docker-Container starten
cd docker
docker-compose up -d
cd ..
```

## Konfiguration

### OpenHands GUI konfigurieren

1. Öffnen Sie die OpenHands GUI unter http://localhost:17243
2. Navigieren Sie zu "Settings" → "Git Settings"
3. Fügen Sie einen GitHub-Token hinzu (mit Berechtigungen: `repo, workflows:write`)
4. Wählen Sie Ihr Repository aus
5. Unter "LLM Settings":
   - Wählen Sie "Anthropic" als Provider
   - Geben Sie Ihren Anthropic API-Schlüssel ein
   - Wählen Sie "claude-3-7-sonnet-20250219" als Modell

### Konfigurationsdateien

Die Hauptkonfigurationsdateien befinden sich in:

- **Docker**: `docker/docker-compose.yml`
- **OpenHands**: `config/openhands.toml`
- **gpt-cli**: `~/.config/gpt-cli/gpt.yml`

#### Wichtige Konfigurationsparameter

**docker-compose.yml**:
```yaml
ports:
  - "17243:3000"  # Externer Port:Interner Port
```

**openhands.toml**:
```toml
[llm]
provider = "anthropic"
model = "claude-3-7-sonnet-20250219"

[llm.providers.anthropic]
api_base = "https://api.anthropic.com/v1"
```

**gpt.yml**:
```yaml
assistants:
  openhands-integration:
    model: gpt-4
    temperature: 0.2
```

## Verwendung

### Tests ausführen

Um Tests auszuführen und Fehler automatisch zu behandeln:

```bash
gpt openhands-integration -e "Run tests and handle errors" --execute
```

oder mit dem konfigurierten Befehl:

```bash
gpt run-tests
```

### PR überprüfen

Um einen von OpenHands erstellten PR zu überprüfen:

```bash
gpt check-pr <PR_NUMBER>
```

Beispiel:
```bash
gpt check-pr 123
```

### Manueller API-Aufruf an OpenHands

```bash
curl -X POST http://localhost:17243/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"command": "fix-test-errors", "context": {"issue_number": "123"}}'
```

### OpenHands direkt über CLI steuern

Sie können den OpenHands-Container auch direkt über die CLI steuern:

```bash
docker exec -it openhands-app poetry run python -m openhands.core.cli
```

## Workflow-Beschreibung

Der automatisierte Workflow funktioniert wie folgt:

1. **Test-Ausführung**: 
   - gpt-cli führt lokale Tests aus (`npm run test`)
   - Die Testergebnisse werden erfasst und analysiert

2. **Fehlererkennung und Issue-Erstellung**:
   - Bei fehlgeschlagenen Tests erstellt das System automatisch ein GitHub-Issue
   - Das Issue enthält detaillierte Fehlerinformationen, Test-Logs und Metadaten
   - Es wird mit dem Label "fix-me" markiert

3. **OpenHands-Trigger**:
   - Die OpenHands-API wird aufgerufen
   - Die Issue-Nummer und Repository-Information werden als Kontext übergeben

4. **Fix-Generierung**:
   - OpenHands analysiert das Issue und die Fehlermeldungen
   - Es identifiziert die Ursache des Problems
   - Es generiert einen Fix und erstellt einen Pull Request

5. **PR-Verifizierung**:
   - gpt-cli checkt den PR lokal aus
   - Es führt Tests auf dem PR-Branch aus
   - Es kommentiert das Ergebnis auf dem PR

6. **Genehmigung**:
   - Wenn die Tests auf dem PR-Branch bestanden werden, wird der PR automatisch genehmigt
   - Das System dokumentiert die Genehmigung mit einem Kommentar

## Dateien und Komponenten

Das Projekt besteht aus folgenden Hauptkomponenten:

### Docker-Konfiguration
- `docker/docker-compose.yml`: Docker-Compose-Konfiguration für OpenHands

### Python-Skripte
- `scripts/test_and_report.py`: Hauptskript für Test-Ausführung und Issue-Erstellung
- `scripts/check_pr.py`: Skript zur PR-Überprüfung und -Genehmigung
- `scripts/setup.sh`: Setup-Skript für die initiale Einrichtung

### Konfigurationsdateien
- `config/openhands.toml`: OpenHands-Konfiguration mit Claude 3.7 Sonnet-Setup
- `config/github_config.sh`: Skript zur GitHub-Konfiguration
- `gpt-cli/gpt.yml`: gpt-cli Konfiguration mit benutzerdefinierten Befehlen

## Fehlerbehebung

### OpenHands GUI nicht erreichbar

**Problem**: Die OpenHands GUI ist unter http://localhost:17243 nicht erreichbar.

**Lösungen**:
1. Prüfen Sie, ob der Docker-Container läuft:
   ```bash
   docker ps | grep openhands-app
   ```
2. Überprüfen Sie die Logs auf Fehler:
   ```bash
   docker logs openhands-app
   ```
3. Prüfen Sie, ob der Port bereits verwendet wird:
   ```bash
   netstat -tuln | grep 17243
   ```

### GitHub-Authentifizierungsprobleme

**Problem**: GitHub CLI kann keine Issues erstellen oder PRs kommentieren.

**Lösungen**:
1. Überprüfen Sie Ihre GitHub-Authentifizierung:
   ```bash
   gh auth status
   ```
2. Führen Sie eine neue Authentifizierung durch:
   ```bash
   gh auth login
   ```
3. Setzen Sie das Default-Repository:
   ```bash
   gh repo set-default <owner>/<repo>
   ```

### API-Trigger schlägt fehl

**Problem**: Der Aufruf der OpenHands-API schlägt fehl.

**Lösungen**:
1. Überprüfen Sie, ob OpenHands läuft und erreichbar ist
2. Überprüfen Sie, ob der richtige Port verwendet wird (17243)
3. Prüfen Sie die Docker-Logs auf Fehler in der API

### Tests schlagen wiederholt fehl

**Problem**: Tests schlagen wiederholt fehl, und OpenHands kann das Problem nicht beheben.

**Lösungen**:
1. Überprüfen Sie, ob Claude 3.7 Sonnet korrekt konfiguriert ist
2. Prüfen Sie, ob der Anthropic API-Schlüssel gültig ist
3. Analysieren Sie die Issue-Beschreibungen und PR-Kommentare auf Hinweise

## Erweiterungsmöglichkeiten

Dieses Projekt kann auf verschiedene Weise erweitert werden:

1. **CI/CD-Integration**: Integrieren Sie den Workflow in CI/CD-Pipelines
2. **Automatisierte Berichterstellung**: Generieren Sie Berichte über behobene Probleme
3. **Erweiterte Analyse**: Fügen Sie statische Code-Analyse vor der PR-Erstellung hinzu
4. **Multi-Repo-Unterstützung**: Erweitern Sie den Workflow für mehrere Repositories
5. **Sicherheitsverbesserungen**: Fügen Sie Sicherheitsscans für generierten Code hinzu

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Siehe die `LICENSE`-Datei für Details.

---

Entwickelt mit ❤️ für das OpenHands-Ökosystem
