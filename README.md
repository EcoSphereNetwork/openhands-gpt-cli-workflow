<div align="center">
  <img src="https://api.placeholder.com/280x100?text=OpenHands+Workflow" alt="Logo" width="280">
  <h1>OpenHands Workflow Integration</h1>
  <p>A complete, automated workflow integrating OpenHands, gpt-cli, and GitHub CLI for test-driven development and autonomous code fixing.</p>

  [![Contributors][contributors-shield]][contributors-url]
  [![Stars][stars-shield]][stars-url]
  [![Coverage][coverage-shield]][coverage-url]
  [![MIT License][license-shield]][license-url]
  <br/>
  [![Discord][discord-shield]][discord-url]
  [![Documentation][docs-shield]][docs-url]
  [![Project Credits][credits-shield]][credits-url]

  [Getting Started](#-getting-started) •
  [Report Bug](https://github.com/yourusername/openhands-workflow/issues) •
  [Request Feature](https://github.com/yourusername/openhands-workflow/issues)
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
The OpenHands Workflow Integration provides a seamless, automated workflow between OpenHands AI, gpt-cli, and GitHub CLI. This system automatically tests code, creates issues for errors, leverages AI to generate fixes, creates pull requests, and verifies fixes - all with minimal human intervention.

### Why Use This Workflow?
- 🚀 **Automation**: Reduce manual debugging time with AI-powered testing and fixing
- 🧠 **AI-Powered**: Utilizes Claude 3.7 Sonnet for sophisticated code analysis and repair
- 🔄 **Full Circle**: Complete test → error → fix → verify workflow
- 🌐 **GUI and CLI**: Access OpenHands through both interface options
- 🛠️ **Extensible**: Easily adapt to different projects and test frameworks

## ✨ Key Features

### Core Features
- 🔧 **Multi-Interface Control**: Use OpenHands via GUI (port 17243) or CLI
- 🤖 **AI Integration**: Claude 3.7 Sonnet powered code fixing
- 🔄 **Automated Testing**: Run tests and handle errors programmatically
- 🐛 **Issue Management**: Automatic GitHub issue creation with detailed error context
- ✅ **PR Verification**: Automatically check and approve fixed code

### Development Tools
- 📊 **Docker Infrastructure**: Containerized environment for consistent execution
- 🔧 **gpt-cli Integration**: Custom commands for easy workflow triggering
- 🐙 **GitHub CLI Integration**: Streamlined repository interaction
- 🧪 **Testing Framework**: Automatic test execution with npm

## 🚀 Getting Started

### Prerequisites
- Docker and Docker Compose
- Python 3.6+ with pip
- Node.js and npm
- GitHub CLI (`gh`) installed and configured
- gpt-cli installed
- Anthropic API key for Claude 3.7 Sonnet

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/openhands-workflow.git
   cd openhands-workflow
   ```

2. **Run the Setup Script**

   ```bash
   chmod +x scripts/setup.sh
   ./scripts/setup.sh
   ```

3. **Configure OpenHands**
   
   Access the OpenHands GUI at http://localhost:17243 and configure:
   - GitHub token (Settings → Git Settings)
   - Anthropic API key for Claude 3.7 Sonnet
   - Default repository

4. **Verify Installation**
   ```bash
   # Test gpt-cli integration
   gpt run-tests
   
   # Verify container is running
   docker ps | grep openhands-app
   ```

## 📁 Project Structure
```
openhands-workflow/
├── docker/                    # Docker configurations
│   └── docker-compose.yml     # Container setup with custom port
├── config/                    # Configuration files
│   ├── openhands.toml        # OpenHands config with Claude 3.7
│   └── github_config.sh      # GitHub CLI setup script
├── scripts/                   # Workflow automation scripts
│   ├── test_and_report.py    # Test runner and issue creator
│   ├── check_pr.py           # PR verification script
│   └── setup.sh              # Environment setup script
├── gpt-cli/                   # gpt-cli configuration
│   └── gpt.yml               # Custom commands configuration
├── workspace/                 # Shared workspace for OpenHands
└── README.md                 # Project documentation
```

## 💻 Development

### Setting Up for Development
1. Configure gpt-cli with workflow commands:
   ```bash
   cp gpt-cli/gpt.yml ~/.config/gpt-cli/
   ```

2. Ensure all scripts are executable:
   ```bash
   chmod +x scripts/*.py scripts/*.sh
   ```

3. Add your repositories to OpenHands:
   ```bash
   # Through the GUI at http://localhost:17243
   # Settings → Git Settings → Add Repository
   ```

### Command Reference
- **Run Tests**: `gpt run-tests`
- **Check PR**: `gpt check-pr <PR_NUMBER>`
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
   gpt run-tests
   ```
   
2. **Issue Creation and AI Fix**:
   - Creates GitHub issue with error details
   - Labels with "fix-me"
   - Triggers OpenHands to analyze and fix

3. **PR Verification**:
   ```bash
   gpt check-pr <PR_NUMBER>
   ```
   - Runs tests on the PR branch
   - Comments test results
   - Approves PR if tests pass

### Manual Testing
```bash
# Trigger just the tests
npm run test

# Create issue manually
gh issue create --title "Test Failure" --body "Error details"

# Trigger OpenHands directly
docker exec -it openhands-app poetry run python -m openhands.core.cli
```

## 🚢 Deployment

### Docker Container Management
```bash
# Start containers
cd docker && docker-compose up -d

# Stop containers
cd docker && docker-compose down

# View logs
docker logs openhands-app

# Restart service
docker restart openhands-app
```

### Configuration Management
- **Change OpenHands Port**:
  Edit `docker/docker-compose.yml` and update the port mapping (currently 17243:3000)
  
- **Update LLM Model**:
  Edit `config/openhands.toml` and change model parameters

- **Add Custom Commands**:
  Edit `~/.config/gpt-cli/gpt.yml` to add new workflow commands

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

- [Issue Tracker](https://github.com/yourusername/openhands-workflow/issues)
- [Docker Hub](https://hub.docker.com/r/all-hands-ai/openhands)
- [OpenHands Documentation](https://docs.all-hands.dev)
- [gpt-cli Documentation](https://github.com/kharvd/gpt-cli)

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

---

<div align="center">

### Workflow Architecture

```
[Docker Container]        [Host System]           [GitHub]
 +-------------+         +-------------+         +-----------+
 | OpenHands   |<------->| gpt-cli     |<------->| Issues    |
 | GUI & CLI   |         | Test Runner |         | PRs       |
 +-------------+         +-------------+         +-----------+
      ^                        ^
      |                        |
      v                        v
 +-------------+         +-------------+
 | Claude 3.7  |         | Test Suite  |
 | Sonnet      |         | npm run test|
 +-------------+         +-------------+
```

</div>

<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/yourusername/openhands-workflow?style=for-the-badge&color=blue
[contributors-url]: https://github.com/yourusername/openhands-workflow/graphs/contributors
[stars-shield]: https://img.shields.io/github/stars/yourusername/openhands-workflow?style=for-the-badge&color=blue
[stars-url]: https://github.com/yourusername/openhands-workflow/stargazers
[coverage-shield]: https://img.shields.io/badge/coverage-80%25-green?style=for-the-badge&color=blue
[coverage-url]: #
[license-shield]: https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge&color=blue
[license-url]: LICENSE
[discord-shield]: https://img.shields.io/badge/Discord-Join%20Us-purple?logo=discord&logoColor=white&style=for-the-badge
[discord-url]: https://discord.gg/all-hands-ai
[docs-shield]: https://img.shields.io/badge/Documentation-000?logo=googledocs&logoColor=FFE165&style=for-the-badge
[docs-url]: https://docs.all-hands.dev
[credits-shield]: https://img.shields.io/badge/Project-Credits-blue?style=for-the-badge&color=FFE165&logo=github&logoColor=white
[credits-url]: #
