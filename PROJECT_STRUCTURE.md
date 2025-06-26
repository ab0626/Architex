# Architex Project Structure

## Overview

Architex is a comprehensive developer tool for automatically generating system design diagrams from codebases. The project follows a modular architecture with clear separation of concerns.

## Directory Structure

```
Architex/
├── README.md                    # Project documentation
├── requirements.txt             # Main dependencies
├── requirements-dev.txt         # Development dependencies
├── setup.py                     # Package installation script
├── test_architex.py            # Test demonstration script
├── PROJECT_STRUCTURE.md        # This file
│
├── architex/                    # Main package
│   ├── __init__.py             # Package initialization
│   │
│   ├── core/                   # Core analysis engine
│   │   ├── __init__.py         # Core module initialization
│   │   ├── models.py           # Data models (CodeElement, Relationship, etc.)
│   │   ├── parsers.py          # Language-specific parsers
│   │   ├── analyzer.py         # Main analysis orchestrator
│   │   └── graph_builder.py    # Dependency graph construction
│   │
│   ├── exporters/              # Diagram export modules
│   │   ├── __init__.py         # Exporters module initialization
│   │   ├── base.py             # Base exporter interface
│   │   ├── mermaid.py          # Mermaid diagram exporter
│   │   ├── plantuml.py         # PlantUML diagram exporter
│   │   └── graphviz.py         # Graphviz DOT exporter
│   │
│   └── cli/                    # Command-line interface
│       ├── __init__.py         # CLI module initialization
│       └── main.py             # Main CLI application
│
├── examples/                    # Example projects for testing
│   └── simple_python_project/  # Simple Python project example
│       ├── __init__.py         # Package initialization
│       ├── main.py             # Main application entry point
│       ├── models.py           # Data models
│       ├── services.py         # Business logic services
│       └── database.py         # Database abstraction layer
│
├── tests/                       # Test suite (to be implemented)
├── docs/                        # Documentation (to be implemented)
├── vscode-extension/           # VS Code extension (to be implemented)
└── web-ui/                     # Web interface (to be implemented)
```

## Core Components

### 1. Core Analysis Engine (`architex/core/`)

**Purpose**: The heart of the system that analyzes codebases and extracts architectural information.

#### Key Files:
- **`models.py`**: Defines data structures for code elements, relationships, and analysis results
- **`parsers.py`**: Language-specific parsers for extracting code elements
- **`analyzer.py`**: Main orchestrator that coordinates the analysis process
- **`graph_builder.py`**: Constructs and analyzes dependency graphs

#### Key Classes:
- `CodeElement`: Represents code elements (classes, functions, modules, etc.)
- `Relationship`: Represents relationships between code elements
- `ServiceBoundary`: Represents detected service boundaries
- `CodebaseAnalyzer`: Main analysis orchestrator
- `DependencyGraph`: Graph analysis and metrics calculation

### 2. Exporters (`architex/exporters/`)

**Purpose**: Convert analysis results into various diagram formats.

#### Key Files:
- **`base.py`**: Abstract base class for all exporters
- **`mermaid.py`**: Generates Mermaid diagrams
- **`plantuml.py`**: Generates PlantUML diagrams
- **`graphviz.py`**: Generates Graphviz DOT diagrams

#### Key Classes:
- `BaseExporter`: Abstract interface for all exporters
- `MermaidExporter`: Exports to Mermaid format
- `PlantUMLExporter`: Exports to PlantUML format
- `GraphvizExporter`: Exports to Graphviz DOT format

### 3. CLI Interface (`architex/cli/`)

**Purpose**: Command-line interface for easy tool usage.

#### Key Files:
- **`main.py`**: Main CLI application using Typer

#### Features:
- Analyze codebases with various options
- Export diagrams in multiple formats
- List supported languages and formats
- Rich terminal output with progress indicators

## Data Flow

```
Codebase → Parser → CodeElements → GraphBuilder → AnalysisResult → Exporter → Diagram
```

1. **Codebase Input**: User provides path to codebase
2. **Parsing**: Language-specific parsers extract code elements
3. **Graph Construction**: Dependency graph is built from elements
4. **Analysis**: Service boundaries and metrics are calculated
5. **Export**: Results are converted to diagram format
6. **Output**: Diagram is saved to file or displayed

## Supported Languages

Currently implemented:
- **Python**: Using AST parser

Planned:
- **JavaScript/TypeScript**: Using Tree-sitter
- **Java**: Using Tree-sitter
- **C/C++**: Using LibClang
- **Go**: Using Tree-sitter

## Supported Output Formats

- **Mermaid**: Interactive diagrams for documentation
- **PlantUML**: UML diagrams for technical documentation
- **Graphviz**: Static diagrams for presentations
- **Interactive Web**: Streamlit-based web interface (planned)

## Architecture Patterns

### 1. Plugin Architecture
- Parsers are pluggable via `ParserRegistry`
- Exporters are pluggable via inheritance from `BaseExporter`

### 2. Strategy Pattern
- Different analysis strategies can be implemented
- Different export formats can be selected at runtime

### 3. Builder Pattern
- `DependencyGraph` builds complex graph structures
- `AnalysisResult` aggregates analysis data

### 4. Factory Pattern
- `ParserRegistry` creates appropriate parsers
- Exporter factory creates appropriate exporters

## Extension Points

### Adding New Language Support
1. Create new parser inheriting from `BaseParser`
2. Register parser in `ParserRegistry`
3. Implement language-specific element extraction

### Adding New Output Format
1. Create new exporter inheriting from `BaseExporter`
2. Implement `export()` method
3. Add to CLI format selection

### Adding New Analysis Features
1. Extend `CodebaseAnalyzer` with new analysis methods
2. Add new metrics to `DependencyGraph`
3. Update data models as needed

## Testing Strategy

### Unit Tests
- Test individual parsers
- Test individual exporters
- Test graph algorithms
- Test data models

### Integration Tests
- Test complete analysis pipeline
- Test CLI interface
- Test with real codebases

### Example Tests
- Use provided example projects
- Test with various project sizes
- Test with different languages

## Performance Considerations

### Scalability
- Parallel file parsing for large codebases
- Incremental analysis for changed files
- Caching of analysis results

### Memory Usage
- Streaming parsers for large files
- Graph compression for large dependency graphs
- Lazy loading of analysis results

## Security Considerations

### Input Validation
- Validate file paths and permissions
- Sanitize file content before parsing
- Handle malicious code safely

### Output Sanitization
- Sanitize diagram output
- Prevent code injection in diagrams
- Validate export file paths

## Future Enhancements

### Planned Features
1. **VS Code Extension**: Real-time analysis in IDE
2. **Web Interface**: Interactive web-based visualization
3. **Language Server**: LSP integration for real-time analysis
4. **API Integration**: REST API for programmatic access
5. **Cloud Integration**: Analyze GitHub/GitLab repositories
6. **Advanced Analysis**: 
   - Performance impact analysis
   - Security vulnerability detection
   - Code quality metrics
   - Technical debt assessment

### Advanced Visualizations
1. **3D Diagrams**: Three.js-based 3D architecture views
2. **Interactive Graphs**: D3.js-based interactive visualizations
3. **Timeline Views**: Evolution of architecture over time
4. **Heat Maps**: Complexity and coupling heat maps

This structure provides a solid foundation for a powerful and extensible architecture analysis tool that can grow with user needs and technological advances. 