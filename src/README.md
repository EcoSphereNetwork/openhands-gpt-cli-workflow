# OpenHands + GPT-CLI + Dev-Server Integration

Diese Integration verbindet OpenHands mit GPT-CLI und dem Dev-Server-Workflow, um einen automatisierten Workflow für Repository-Tests, Issue-Erstellung, automatisierte Fehlerbehebung und Entwicklungsserver-Management zu schaffen.

## Funktionen

- OpenHands im GUI-Modus (Port 17243) in einem Docker-Container ausführen
- OpenHands über die API (Port 17244) steuern
- GPT-CLI verwenden, um Tests auf Repositories auszuführen
- Automatisch GitHub-Issues für Testfehler erstellen
- OpenHands auslösen, um Issues zu beheben
- Fixes überprüfen und Issues schließen
- Dev-Server-Workflow auf dem lokalen Host installieren und verwalten
- Automatisierter Workflow-Loop zwischen OpenHands, GPT-CLI und Dev-Server

## Architektur

Die Integration besteht aus folgenden Komponenten:

1. **OpenHands Container**: Führt OpenHands im GUI-Modus aus und stellt sowohl die GUI als auch die API-Ports zur Verfügung
2. **GPT-CLI**: Auf dem Host installiert, wird verwendet, um Tests auszuführen und mit Repositories zu interagieren
3. **GitHub CLI**: Wird verwendet, um Issues zu erstellen und mit GitHub zu interagieren
4. **Python-Skripte**: Verbinden alle Komponenten miteinander

## Voraussetzungen

- Docker und Docker Compose
- Python 3.8+
- GitHub CLI (`gh`)
- Git

## Setup

1. Führe das Setup-Skript aus:
   ```bash
   ./scripts/setup.sh
   ```

2. Konfiguriere OpenHands:
   - Greife auf die OpenHands GUI unter http://localhost:17243 zu
   - Gehe zu Einstellungen → API-Schlüssel und füge deine API-Schlüssel hinzu
   - Gehe zu Einstellungen → Git-Einstellungen und füge deinen GitHub-Token hinzu

3. Installiere GPT-CLI:
   ```bash
   pip install gpt-command-line
   ```

## Verwendung

### Tests auf einem Repository ausführen

```bash
gpt run-tests --repo-path /pfad/zum/repository
```

Dies wird:
1. Tests im angegebenen Repository ausführen
2. Bei Testfehlern ein GitHub-Issue mit den Fehlerdetails erstellen
3. OpenHands auslösen, um das Issue zu beheben

### Einen Pull Request überprüfen

```bash
gpt check-pr <PR_NUMMER> --repo-path /pfad/zum/repository
```

Dies wird:
1. Den PR-Branch auschecken
2. Tests auf dem PR ausführen
3. Einen Kommentar auf dem PR mit den Testergebnissen hinterlassen
4. Optional den PR genehmigen, wenn Tests bestanden werden

### Ein Issue beheben

```bash
gpt fix-issue <ISSUE_NUMMER> --repo-path /pfad/zum/repository
```

Dies wird:
1. OpenHands auslösen, um das Issue zu beheben
2. Optional auf den Abschluss des Fixes warten

### Einen Fix überprüfen

```bash
gpt verify-fix <ISSUE_NUMMER> --repo-path /pfad/zum/repository
```

Dies wird:
1. Tests ausführen, um den Fix zu überprüfen
2. Einen Kommentar auf dem Issue mit den Überprüfungsergebnissen hinterlassen
3. Optional das Issue schließen, wenn Tests bestanden werden

### Dev-Server-Workflow installieren und verwalten

```bash
gpt dev-server --install-dir /pfad/zum/installation --start
```

Dies wird:
1. Das Dev-Server-Workflow-Repository klonen
2. Die Konfiguration erstellen
3. Die Docker-Container starten
4. Das Setup ausführen

### Dev-Server CLI verwenden

```bash
gpt dev-server-cli status
```

Dies wird:
1. Prüfen, ob die Dev-Server CLI installiert ist
2. Falls nicht, die Installation anbieten
3. Den angegebenen Befehl ausführen (in diesem Fall den Status anzeigen)

### Dev-Server-Workflow mit OpenHands und GPT-CLI integrieren

```bash
gpt integrate-dev-server --install-dir /pfad/zum/installation --start-workflow-loop
```

Dies wird:
1. Den Dev-Server-Workflow installieren
2. Die Integration mit OpenHands einrichten
3. Die Integration mit GPT-CLI einrichten
4. Optional den Workflow-Loop starten

### Workflow-Loop starten

```bash
gpt workflow-loop --install-dir /pfad/zum/installation
```

Dies wird:
1. Den Workflow-Loop als Hintergrundprozess starten
2. Die PID in einer Datei speichern
3. Die Logs in eine Datei schreiben

## Konfiguration

### OpenHands-Konfiguration

Die OpenHands-Konfiguration ist in `config/openhands.toml` gespeichert. Du kannst diese Datei ändern, um die OpenHands-Konfiguration anzupassen.

### GPT-CLI-Konfiguration

Die GPT-CLI-Konfiguration ist in `config/gpt.yml` gespeichert. Diese Datei wird während des Setups nach `~/.config/gpt-cli/gpt.yml` kopiert.

### GitHub-Token

Dein GitHub-Token wird in `config/github_token.txt` gespeichert. Diese Datei wird in den OpenHands-Container gemountet.

## Docker-Konfiguration

Die Docker-Konfiguration ist in `docker/docker-compose.yml` gespeichert. Du kannst diese Datei ändern, um die Docker-Konfiguration anzupassen.

## Skripte

- `scripts/setup.sh`: Setup-Skript für die Integration
- `scripts/test_and_report.py`: Tests ausführen und Issues melden
- `scripts/check_pr.py`: Einen Pull Request überprüfen
- `scripts/fix_issue.py`: OpenHands auslösen, um ein Issue zu beheben
- `scripts/verify_fix.py`: Einen Fix überprüfen
- `scripts/openhands_api.py`: Python-Wrapper für die OpenHands-API
- `scripts/dev_server_installer.py`: Dev-Server-Workflow installieren und konfigurieren
- `scripts/dev_server_cli_wrapper.py`: Wrapper für die Dev-Server CLI
- `scripts/integrate_dev_server.py`: Dev-Server-Workflow mit OpenHands und GPT-CLI integrieren
- `scripts/workflow_loop.py`: Hauptskript für den Workflow-Loop
- `scripts/start_workflow_loop.sh`: Workflow-Loop als Hintergrundprozess starten

## Workflow

1. **Testphase**:
   - Tests auf einem Repository ausführen
   - Bei Testfehlern ein GitHub-Issue erstellen

2. **Fix-Phase**:
   - OpenHands analysiert das Issue
   - OpenHands implementiert einen Fix
   - OpenHands erstellt einen Pull Request mit dem Fix

3. **Überprüfungsphase**:
   - Tests auf dem PR ausführen
   - Bei bestandenen Tests den PR genehmigen
   - Nach dem Merge das Issue schließen

## Workflow-Loop

Der Workflow-Loop ist ein automatisierter Prozess, der kontinuierlich zwischen OpenHands, GPT-CLI und dem Dev-Server-Workflow läuft. Er führt folgende Schritte aus:

1. **Überwachung**:
   - Überwacht den Dev-Server-Workflow auf neue Issues mit dem Label "fix-me"
   - Prüft den Status der laufenden Dienste

2. **Automatisierung**:
   - Löst OpenHands aus, um Issues zu beheben
   - Überprüft die Fixes mit GPT-CLI
   - Schließt Issues, wenn die Fixes erfolgreich sind

3. **Berichterstattung**:
   - Protokolliert alle Aktivitäten
   - Erstellt Berichte über den Status des Workflows

Der Workflow-Loop kann als Hintergrundprozess gestartet werden und läuft kontinuierlich, um den Dev-Server-Workflow zu überwachen und zu verbessern.

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert - siehe die LICENSE-Datei für Details.