# Architex Setup Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ (3.11+ recommended)
- Node.js (for Mermaid CLI)
- Java (for PlantUML diagrams)
- Graphviz (optional, for Graphviz diagrams)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Architex
   ```

2. **Run the installation script**
   ```bash
   python install_dependencies.py
   ```

3. **Verify installation**
   ```bash
   python -c "import architex; print('✅ Architex installed successfully!')"
   ```

## 📦 Manual Installation

If the automated script doesn't work, you can install dependencies manually:

### Core Dependencies
```bash
pip install -r requirements.txt
```

### System Dependencies

#### Windows
- **Java**: Download from [Adoptium](https://adoptium.net/)
- **Node.js**: Download from [Node.js](https://nodejs.org/)
- **Graphviz**: Download from [Graphviz](https://graphviz.org/download/)

#### macOS
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install java node graphviz
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install -y openjdk-11-jdk nodejs npm graphviz
```

### Optional Dependencies
```bash
pip install -r requirements-optional.txt
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
# AI Configuration
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Database Configuration
REDIS_URL=redis://localhost:6379

# Web Dashboard
DASHBOARD_HOST=localhost
DASHBOARD_PORT=8000

# Logging
LOG_LEVEL=INFO
```

### Configuration File
The `config.yaml` file contains default settings:

```yaml
# Analysis settings
analysis:
  max_file_size: 1048576  # 1MB
  supported_languages: [python, javascript, java]
  ignore_patterns: [__pycache__, node_modules, .git]

# AI settings
ai:
  provider: openai  # or anthropic
  model: gpt-4
  max_tokens: 2000

# Export settings
export:
  formats: [mermaid, plantuml, graphviz]
  output_dir: ./output
```

## 🎯 Usage Examples

### Command Line Interface

1. **Basic analysis**
   ```bash
   python -m architex.cli.main analyze ./path/to/project
   ```

2. **With AI features**
   ```bash
   python -m architex.cli.main analyze ./path/to/project --ai
   ```

3. **Export diagrams**
   ```bash
   python -m architex.cli.main analyze ./path/to/project --export mermaid
   ```

4. **Live analysis**
   ```bash
   python -m architex.cli.main watch ./path/to/project
   ```

### Web Dashboard

1. **Start the dashboard**
   ```bash
   python -m architex.web.dashboard
   ```

2. **Open in browser**
   ```
   http://localhost:8000
   ```

### VS Code Extension

1. **Install the extension**
   - Open VS Code
   - Go to Extensions (Ctrl+Shift+X)
   - Search for "Architex"
   - Install the extension

2. **Use commands**
   - `Ctrl+Shift+P` → "Architex: Analyze Current Project"
   - `Ctrl+Shift+P` → "Architex: Show Dashboard"

## 🧪 Testing

### Run Demo Scripts
```bash
# Multi-language analysis demo
python demo_multi_language_analysis.py

# Enhanced CLI demo
python demo_cli_enhancements.py

# Web dashboard demo
python demo_web_dashboard.py

# VS Code extension demo
python demo_vscode_extension.py
```

### Run Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest test_architex.py

# Run with coverage
pytest --cov=architex
```

## 🔍 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Reinstall dependencies
   pip install --force-reinstall -r requirements.txt
   ```

2. **System Dependencies Not Found**
   - Ensure Java is in PATH: `java -version`
   - Ensure Node.js is in PATH: `node --version`
   - Ensure Graphviz is in PATH: `dot -V`

3. **Permission Errors**
   ```bash
   # On Linux/macOS
   sudo pip install -r requirements.txt
   
   # On Windows (run as Administrator)
   pip install -r requirements.txt
   ```

4. **Memory Issues**
   - Reduce `max_file_size` in config.yaml
   - Use smaller AI models
   - Increase system memory

### Getting Help

1. **Check logs**
   ```bash
   python -m architex.cli.main analyze --verbose
   ```

2. **Debug mode**
   ```bash
   export LOG_LEVEL=DEBUG
   python -m architex.cli.main analyze
   ```

3. **Report issues**
   - Check existing issues on GitHub
   - Create new issue with:
     - Python version
     - OS version
     - Error message
     - Steps to reproduce

## 📚 Next Steps

1. **Explore the codebase**
   - Read `README.md` for overview
   - Check `PROJECT_STRUCTURE.md` for architecture
   - Review `MULTI_LANGUAGE_README.md` for language support

2. **Customize configuration**
   - Modify `config.yaml` for your needs
   - Add custom parsers for new languages
   - Configure AI providers

3. **Extend functionality**
   - Add new export formats
   - Create custom analyzers
   - Integrate with other tools

## 🎉 Success!

You're now ready to use Architex! Start by analyzing a simple project:

```bash
python demo_multi_language_analysis.py
```

This will demonstrate all the key features of Architex including multi-language parsing, AI-powered analysis, and diagram generation. 