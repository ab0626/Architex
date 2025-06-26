# Architex VS Code Extension

Automatically generate high-level system design diagrams and architectural insights from your codebase using AI-powered analysis.

## Features

### 🏗️ **Architecture Analysis**
- **Multi-language Support**: Python, JavaScript, TypeScript, Java
- **AST-based Parsing**: Deep code structure analysis
- **Dependency Mapping**: Visualize module relationships
- **Service Detection**: Identify microservices and boundaries

### 🤖 **AI-Powered Insights**
- **Smart Labeling**: AI-generated component descriptions
- **Architectural Summaries**: Automated documentation
- **Code Recommendations**: Best practices and improvements
- **Pattern Recognition**: Detect anti-patterns and technical debt

### 📊 **Interactive Visualizations**
- **Real-time Dashboard**: Live architecture overview
- **Metrics Panel**: Code quality and complexity metrics
- **Recommendations View**: AI-powered suggestions
- **Live Analysis**: Continuous monitoring with file watching

### 🔄 **Live Analysis**
- **File Watching**: Monitor code changes in real-time
- **WebSocket Updates**: Instant dashboard updates
- **Background Processing**: Non-blocking analysis
- **Incremental Updates**: Efficient change detection

### 📤 **Export Capabilities**
- **Multiple Formats**: Mermaid, PlantUML, Graphviz
- **Summary Reports**: Markdown and JSON exports
- **Interactive Diagrams**: Clickable component navigation
- **Custom Styling**: Configurable visual themes

## Quick Start

1. **Install the Extension**
   - Search for "Architex" in VS Code Extensions
   - Click Install

2. **Open a Workspace**
   - Open a folder containing your codebase
   - Supported languages: Python, JavaScript, TypeScript, Java

3. **Start Analysis**
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
   - Type "Architex: Analyze Current Workspace"
   - Press Enter

4. **View Results**
   - Check the Architex sidebar for architecture overview
   - Open the dashboard for detailed visualizations
   - Review AI recommendations and metrics

## Commands

| Command | Description |
|---------|-------------|
| `Architex: Analyze Current Workspace` | Analyze entire workspace |
| `Architex: Analyze Current File` | Analyze active file |
| `Architex: Show Dashboard` | Open interactive dashboard |
| `Architex: Show Metrics` | Display code metrics |
| `Architex: Show AI Recommendations` | View AI suggestions |
| `Architex: Start Live Analysis` | Begin real-time monitoring |
| `Architex: Stop Live Analysis` | Stop live monitoring |
| `Architex: Export Diagram` | Export architecture diagram |
| `Architex: Export Analysis Summary` | Export detailed report |

## Configuration

### Extension Settings

```json
{
  "architex.enabled": true,
  "architex.aiFeatures": true,
  "architex.liveAnalysis": false,
  "architex.websocketPort": 8765,
  "architex.dashboardPort": 8000,
  "architex.autoAnalyze": false,
  "architex.exportFormat": "mermaid",
  "architex.summaryFormat": "markdown"
}
```

### Settings Description

- **enabled**: Enable/disable Architex analysis
- **aiFeatures**: Enable AI-powered features
- **liveAnalysis**: Enable live file watching
- **websocketPort**: WebSocket server port for live updates
- **dashboardPort**: Dashboard web server port
- **autoAnalyze**: Automatically analyze on workspace open
- **exportFormat**: Default diagram export format
- **summaryFormat**: Default summary export format

## Views

### Architecture View
- Component hierarchy
- Module relationships
- Service boundaries
- Dependency graphs

### Metrics View
- Code complexity metrics
- File size statistics
- Dependency depth analysis
- Performance indicators

### AI Recommendations View
- Code improvement suggestions
- Architecture best practices
- Technical debt identification
- Refactoring opportunities

### Live Analysis View
- Real-time file monitoring
- Change detection status
- Analysis progress
- Error notifications

## Context Menus

### Explorer Context
- Right-click on folders to analyze specific directories
- Quick access to workspace analysis

### Editor Context
- Right-click in supported file types
- Analyze individual files
- View file-specific insights

## Requirements

- **VS Code**: 1.80.0 or higher
- **Node.js**: 14.0.0 or higher (for extension development)
- **Python**: 3.8+ (for backend analysis engine)

## Supported Languages

- **Python**: Full AST parsing, dependency analysis
- **JavaScript**: ES6+ syntax, module detection
- **TypeScript**: Type information, interface analysis
- **Java**: Class structure, package relationships

## Troubleshooting

### Common Issues

1. **Analysis Not Starting**
   - Check if workspace has supported file types
   - Verify Python backend is running
   - Check extension logs in Output panel

2. **Dashboard Not Loading**
   - Ensure port 8000 is available
   - Check firewall settings
   - Verify WebSocket connection

3. **Live Analysis Issues**
   - Check file watching permissions
   - Verify WebSocket port availability
   - Restart live analysis

### Logs and Debugging

1. Open Command Palette (`Ctrl+Shift+P`)
2. Type "Developer: Show Logs"
3. Select "Extension Host" or "Architex"
4. Check for error messages

## Contributing

We welcome contributions! Please see our [GitHub repository](https://github.com/ab0626/Architex) for:

- Bug reports
- Feature requests
- Pull requests
- Documentation improvements

## License

MIT License - see [LICENSE](https://github.com/ab0626/Architex/blob/main/LICENSE) for details.

## Support

- **GitHub Issues**: [Report bugs](https://github.com/ab0626/Architex/issues)
- **Documentation**: [Full documentation](https://github.com/ab0626/Architex)
- **Examples**: [Sample projects](https://github.com/ab0626/Architex/tree/main/examples)

---

**Made with ❤️ by the Architex Team** 