<div align="center">
  <img src="https://api.placeholder.com/280x100?text=OpenHands+Workflow" alt="Logo" width="280">
  <h1>OpenHands + GPT-CLI + Dev-Server Integration</h1>
  <p>A complete, automated workflow integrating OpenHands, GPT-CLI, Dev-Server-Workflow, and GitHub CLI for test-driven development, server management, and autonomous code fixing.</p>

  [![Contributors][contributors-shield]][contributors-url]
  [![Stars][stars-shield]][stars-url]
  [![Coverage][coverage-shield]][coverage-url]
  [![MIT License][license-shield]][license-url]
  <br/>
  [![Discord][discord-shield]][discord-url]
  [![Documentation][docs-shield]][docs-url]
  [![Project Credits][credits-shield]][credits-url]

  [Getting Started](#-getting-started) •
  [Report Bug](https://github.com/EcoSphereNetwork/openhands-gpt-cli-workflow/issues) •
  [Request Feature](https://github.com/EcoSphereNetwork/openhands-gpt-cli-workflow/issues)
</div>

## 📋 Table of Contents
- [About](#-about)
- [Key Features](#-key-features)
- [Getting Started](#-getting-started)
- [Project Structure](#-project-structure)
- [Development](#-development)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [Support](#-support)
- [License](#-license)

## 🎯 About
The OpenHands + GPT-CLI + Dev-Server Integration provides a seamless, automated workflow between OpenHands AI, GPT-CLI, Dev-Server-Workflow, and GitHub CLI. This system automatically tests code, creates issues for errors, leverages AI to generate fixes, creates pull requests, verifies fixes, and manages development servers - all with minimal human intervention.

### Why Use This Workflow?
- 🚀 **Automation**: Reduce manual debugging time with AI-powered testing and fixing
- 🧠 **AI-Powered**: Utilizes Claude 3.7 Sonnet for sophisticated code analysis and repair
- 🔄 **Full Circle**: Complete test → error → fix → verify workflow
- 🌐 **GUI and CLI**: Access OpenHands and Dev-Server through both interface options
- 🛠️ **Extensible**: Easily adapt to different projects and test frameworks
- 🖥️ **Dev-Server**: Integrated development server management with MCP servers
- 🔁 **Workflow Loop**: Continuous monitoring and automation of development processes

## ✨ Key Features

### Core Features
- 🔧 **Multi-Interface Control**: Use OpenHands via GUI (port 17243) or CLI
- 🤖 **AI Integration**: Claude 3.7 Sonnet powered code fixing
- 🔄 **Automated Testing**: Run tests and handle errors programmatically
- 🐛 **Issue Management**: Automatic GitHub issue creation with detailed error context
- ✅ **PR Verification**: Automatically check and approve fixed code
- 🖥️ **Dev-Server Management**: Install, configure, and manage Dev-Server-Workflow
- 🔁 **Workflow Loop**: Continuous monitoring and automation between all components

### Development Tools
- 📊 **Docker Infrastructure**: Containerized environment for consistent execution
- 🔧 **GPT-CLI Integration**: Custom commands for easy workflow triggering
- 🐙 **GitHub CLI Integration**: Streamlined repository interaction
- 🧪 **Testing Framework**: Automatic test execution with npm
- 🔌 **MCP Integration**: Message Control Protocol servers for service management
- 🔄 **n8n Workflows**: Workflow automation with n8n integration
- 🤖 **OpenHands MCP**: AI-assisted issue resolution and code fixing

## 🚀 Getting Started

### Prerequisites
- Docker and Docker Compose
- Python 3.8+ with pip
- Node.js and npm
- GitHub CLI (`gh`) installed and configured
- GPT-CLI installed (`pip install gpt-command-line`)
- Anthropic API key for Claude 3.7 Sonnet
- Git configured with access to repositories

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/EcoSphereNetwork/openhands-gpt-cli-workflow.git
   cd openhands-gpt-cli-workflow
   ```

2. **Run the Setup Script**

   ```bash
   cd src
   chmod +x scripts/setup.sh
   ./scripts/setup.sh
   ```

3. **Configure OpenHands**
   
   Access the OpenHands GUI at http://localhost:3000 and configure:
   - GitHub token (Settings → Git Settings)
   - Anthropic API key for Claude 3.7 Sonnet
   - Default repository

4. **Install Dev-Server-Workflow**
   ```bash
   # Install and integrate Dev-Server-Workflow
   gpt integrate-dev-server --install-dir ~/Dev-Server-Workflow --start-workflow-loop
   ```

5. **Verify Installation**
   ```bash
   # Test GPT-CLI integration
   gpt run-tests
   
   # Verify OpenHands container is running
   docker ps | grep openhands-gui
   
   # Check Dev-Server status
   gpt dev-server-cli status
   ```

## 📁 Project Structure
```
openhands-gpt-cli-workflow/
├── src/                       # Source code
│   ├── docker/                # Docker configurations
│   │   ├── docker-compose.yml # Container setup with custom port
│   │   └── Dockerfile.test-runner # Test runner container
│   ├── config/                # Configuration files
│   │   ├── openhands.toml     # OpenHands config with Claude 3.7
│   │   ├── gpt.yml            # GPT-CLI custom commands
│   │   └── github_token.txt   # GitHub token storage
│   ├── scripts/               # Workflow automation scripts
│   │   ├── test_and_report.py # Test runner and issue creator
│   │   ├── check_pr.py        # PR verification script
│   │   ├── fix_issue.py       # Issue fixing script
│   │   ├── verify_fix.py      # Fix verification script
│   │   ├── dev_server_installer.py # Dev-Server installer
│   │   ├── dev_server_cli_wrapper.py # Dev-Server CLI wrapper
│   │   ├── integrate_dev_server.py # Integration script
│   │   ├── workflow_loop.py   # Workflow loop implementation
│   │   ├── start_workflow_loop.sh # Workflow loop starter
│   │   ├── openhands_api.py   # OpenHands API wrapper
│   │   └── setup.sh           # Environment setup script
│   ├── tests/                 # Test scripts
│   │   └── test_integration.py # Integration tests
│   ├── workspace/             # Shared workspace for OpenHands
│   ├── Makefile               # Make targets for common tasks
│   ├── run.sh                 # Main runner script
│   └── README.md              # Project documentation
├── CHANGES.md                 # Change log
├── INTEGRATION_SUMMARY.md     # Integration summary
└── README.md                  # Main documentation
```

### Workflow Architecture

```
[Docker Containers]                [Host System]                [GitHub]
 +----------------+               +----------------+            +-----------+
 | OpenHands      |<------------->| GPT-CLI        |<---------->| Issues    |
 | GUI & CLI      |               | Test Runner    |            | PRs       |
 +----------------+               +----------------+            +-----------+
        ^                                ^                            ^
        |                                |                            |
        v                                v                            v
 +----------------+               +----------------+            +-----------+
 | Claude 3.7     |               | Test Suite     |            | Workflow  |
 | Sonnet         |               | npm run test   |            | Loop      |
 +----------------+               +----------------+            +-----------+
        ^                                ^                            ^
        |                                |                            |
        v                                v                            v
 +----------------+               +----------------+            +-----------+
 | Dev-Server     |<------------->| Dev-Server CLI |<---------->| MCP       |
 | Workflow       |               | Commands       |            | Servers   |
 +----------------+               +----------------+            +-----------+
```

## 💻 Development

### Setting Up for Development
1. Configure GPT-CLI with workflow commands:
   ```bash
   cp src/config/gpt.yml ~/.config/gpt-cli/
   ```

2. Ensure all scripts are executable:
   ```bash
   chmod +x src/scripts/*.py src/scripts/*.sh src/run.sh
   ```

3. Add your repositories to OpenHands:
   ```bash
   # Through the GUI at http://localhost:3000
   # Settings → Git Settings → Add Repository
   ```

4. Install Dev-Server-Workflow:
   ```bash
   gpt integrate-dev-server --install-dir ~/Dev-Server-Workflow
   ```

### Command Reference
- **Run Tests**: `gpt run-tests --repo-path /path/to/repo`
- **Check PR**: `gpt check-pr <PR_NUMBER> --repo-path /path/to/repo`
- **Fix Issue**: `gpt fix-issue <ISSUE_NUMBER> --repo-path /path/to/repo`
- **Verify Fix**: `gpt verify-fix <ISSUE_NUMBER> --repo-path /path/to/repo`
- **Install Dev-Server**: `gpt dev-server --install-dir /path/to/install --start`
- **Use Dev-Server CLI**: `gpt dev-server-cli <COMMAND>`
- **Integrate Dev-Server**: `gpt integrate-dev-server --install-dir /path/to/install --start-workflow-loop`
- **Start Workflow Loop**: `gpt workflow-loop --install-dir /path/to/install`
- **Manual API Call**: 
  ```bash
  curl -X POST http://localhost:17243/api/tasks \
    -H "Content-Type: application/json" \
    -d '{"command": "fix-test-errors", "context": {"issue_number": "123"}}'
  ```

## 🧪 Testing

### Automated Workflow
The system performs these actions automatically:

1. **Test Execution**:
   ```bash
   gpt run-tests --repo-path /path/to/repo
   ```
   
2. **Issue Creation and AI Fix**:
   - Creates GitHub issue with error details
   - Labels with "fix-me"
   - Triggers OpenHands to analyze and fix

3. **PR Verification**:
   ```bash
   gpt check-pr <PR_NUMBER> --repo-path /path/to/repo
   ```
   - Runs tests on the PR branch
   - Comments test results
   - Approves PR if tests pass

4. **Dev-Server Management**:
   ```bash
   gpt dev-server-cli status
   ```
   - Manages Dev-Server-Workflow components
   - Monitors services and containers
   - Provides CLI access to all functionality

5. **Workflow Loop**:
   ```bash
   gpt workflow-loop --install-dir /path/to/install
   ```
   - Continuously monitors for issues
   - Triggers fixes automatically
   - Verifies and reports on fixes

### Manual Testing
```bash
# Trigger just the tests
npm run test

# Create issue manually
gh issue create --title "Test Failure" --body "Error details" --label "fix-me"

# Trigger OpenHands directly
docker exec -it openhands-gui poetry run python -m openhands.core.cli

# Use Dev-Server CLI directly
dev-server status
```

## 🚢 Deployment

### Docker Container Management
```bash
# Start containers
cd src/docker && docker-compose up -d

# Stop containers
cd src/docker && docker-compose down

# View logs
docker logs openhands-gui

# Restart service
docker restart openhands-gui

# Start Dev-Server containers
cd ~/Dev-Server-Workflow && ./docker-start.sh start

# Stop Dev-Server containers
cd ~/Dev-Server-Workflow && ./docker-start.sh stop
```

### Configuration Management
- **Change OpenHands Port**:
  Edit `src/docker/docker-compose.yml` and update the port mapping
  
- **Update LLM Model**:
  Edit `src/config/openhands.toml` and change model parameters

- **Add Custom Commands**:
  Edit `~/.config/gpt-cli/gpt.yml` to add new workflow commands
  
- **Configure Dev-Server**:
  Edit `~/Dev-Server-Workflow/.env` to configure Dev-Server components
  
- **Workflow Loop Settings**:
  Edit parameters in `gpt workflow-loop --help` to see available options

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create your feature branch:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. Commit your changes:
   ```bash
   git commit -m 'feat: add amazing feature'
   ```
4. Push to the branch:
   ```bash
   git push origin feature/amazing-feature
   ```
5. Open a Pull Request

## 💬 Support

- [Issue Tracker](https://github.com/EcoSphereNetwork/openhands-gpt-cli-workflow/issues)
- [Docker Hub](https://hub.docker.com/r/all-hands-ai/openhands)
- [OpenHands Documentation](https://docs.all-hands.dev)
- [GPT-CLI Documentation](https://github.com/kharvd/gpt-cli)
- [Dev-Server-Workflow Repository](https://github.com/EcoSphereNetwork/Dev-Server-Workflow)

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

---

<div align="center">



</div>

<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/EcoSphereNetwork/openhands-gpt-cli-workflow?style=for-the-badge&color=blue
[contributors-url]: https://github.com/EcoSphereNetwork/openhands-gpt-cli-workflow/graphs/contributors
[stars-shield]: https://img.shields.io/github/stars/EcoSphereNetwork/openhands-gpt-cli-workflow?style=for-the-badge&color=blue
[stars-url]: https://github.com/EcoSphereNetwork/openhands-gpt-cli-workflow/stargazers
[coverage-shield]: https://img.shields.io/badge/coverage-80%25-green?style=for-the-badge&color=blue
[coverage-url]: #
[license-shield]: https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge&color=blue
[license-url]: LICENSE
[discord-shield]: https://img.shields.io/badge/Discord-Join%20Us-purple?logo=discord&logoColor=white&style=for-the-badge
[discord-url]: https://discord.gg/all-hands-ai
[docs-shield]: https://img.shields.io/badge/Documentation-000?logo=googledocs&logoColor=FFE165&style=for-the-badge
[docs-url]: https://docs.all-hands.dev
[credits-shield]: https://img.shields.io/badge/Project-Credits-blue?style=for-the-badge&color=FFE165&logo=github&logoColor=white
[credits-url]: INTEGRATION_SUMMARY.md
