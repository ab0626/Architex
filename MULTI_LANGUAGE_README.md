# Architex Multi-Language Analysis

Architex now supports comprehensive analysis of multiple programming languages with advanced AST parsing, dependency extraction, and service detection capabilities.

## 🌍 Supported Languages

### Currently Supported
- **Python** (`.py`) - Full AST parsing with tree-sitter
- **JavaScript** (`.js`, `.mjs`) - Regex-based parsing with ES6+ support
- **Java** (`.java`) - Comprehensive class and method analysis
- **TypeScript** (`.ts`, `.tsx`) - Type-aware analysis
- **C#** (`.cs`) - .NET framework analysis
- **Go** (`.go`) - Go module and package analysis
- **Rust** (`.rs`) - Rust crate and module analysis
- **PHP** (`.php`) - PHP class and function analysis
- **Ruby** (`.rb`) - Ruby class and method analysis
- **Swift** (`.swift`) - iOS/macOS development analysis
- **Kotlin** (`.kt`) - Android and JVM analysis
- **Scala** (`.scala`) - Functional programming analysis
- **Dart** (`.dart`) - Flutter and Dart analysis
- **R** (`.r`, `.R`) - Data science and statistics
- **MATLAB** (`.m`) - Scientific computing analysis

### Language-Specific Features

#### Python
- **AST Parsing**: Full Abstract Syntax Tree analysis
- **Import Analysis**: `import` and `from ... import` statements
- **Class Analysis**: Inheritance, decorators, methods
- **Function Analysis**: Parameters, decorators, docstrings
- **Type Hints**: Support for type annotations

#### JavaScript/TypeScript
- **ES6+ Support**: Classes, modules, arrow functions
- **Import/Export**: ES6 modules and CommonJS require
- **Class Analysis**: Inheritance, methods, properties
- **TypeScript**: Type definitions and interfaces

#### Java
- **Package Analysis**: Package declarations and imports
- **Class Analysis**: Inheritance, interfaces, annotations
- **Method Analysis**: Access modifiers, return types
- **Spring Framework**: @Controller, @Service, @Repository

## 🏗️ Internal Models

### AST (Abstract Syntax Tree)
```python
class ASTNode(BaseModel):
    node_type: str                    # Type of AST node
    value: Optional[str]              # Node value
    children: List['ASTNode']         # Child nodes
    metadata: Dict[str, Any]          # Additional metadata
    position: Optional[Dict[str, int]] # Source position
```

### Code Elements
```python
class CodeElement(BaseModel):
    id: str                           # Unique identifier
    name: str                         # Element name
    type: ElementType                 # Element type
    language: LanguageType            # Programming language
    file_path: Optional[Path]         # Source file
    line_number: Optional[int]        # Line number
    end_line: Optional[int]           # End line
    module: Optional[str]             # Module/package
    namespace: Optional[str]          # Namespace
    visibility: Optional[str]         # Visibility modifier
    modifiers: List[str]              # Additional modifiers
    ast_node: Optional[ASTNode]       # AST representation
    dependencies: List[DependencyInfo] # Direct dependencies
    metadata: Dict[str, Any]          # Additional metadata
```

### Relationships
```python
class Relationship(BaseModel):
    id: str                           # Unique relationship ID
    source_id: str                    # Source element ID
    target_id: str                    # Target element ID
    type: RelationshipType            # Relationship type
    strength: float                   # Relationship strength (0.0-1.0)
    bidirectional: bool               # Bidirectional relationship
    metadata: Dict[str, Any]          # Additional metadata
```

### Service Boundaries
```python
class ServiceBoundary(BaseModel):
    id: str                           # Unique service ID
    name: str                         # Service name
    type: ServiceType                 # Service type
    elements: Set[str]                # Element IDs in service
    dependencies: Set[str]            # External dependencies
    cohesion_score: float             # Cohesion score (0.0-1.0)
    coupling_score: float             # Coupling score (0.0-1.0)
    complexity_score: float           # Complexity score
    metadata: Dict[str, Any]          # Additional metadata
```

## 🔗 Dependency Analysis

### Dependency Graph
- **Nodes**: Code elements (classes, functions, modules)
- **Edges**: Relationships (inheritance, calls, imports)
- **Cycles**: Circular dependency detection
- **Metrics**: Coupling, cohesion, complexity scores

### Relationship Types
- **Inheritance**: `inherits`, `extends`, `implements`
- **Dependencies**: `depends_on`, `imports`, `requires`
- **Function Calls**: `calls`, `invokes`, `references`
- **Data Flow**: `uses`, `assigns`, `returns`
- **Structural**: `contains`, `belongs_to`, `part_of`
- **Associations**: `associates`, `composes`, `aggregates`

### Analysis Metrics
- **Coupling Score**: Measures interdependencies between modules
- **Cohesion Score**: Measures internal relationships within modules
- **Complexity Score**: Measures code complexity
- **Impact Score**: Measures how many elements depend on a given element

## 🏛️ Service Detection

### Service Types
- **API Service**: Controllers, endpoints, routes
- **Data Service**: Repositories, DAOs, database access
- **Business Service**: Business logic, domain services
- **Infrastructure Service**: Configuration, utilities
- **Utility Service**: Helper functions, tools

### Architectural Layers
- **Presentation**: Controllers, views, UI components
- **Application**: Services, application logic
- **Domain**: Entities, models, business rules
- **Infrastructure**: Repositories, external services

### Detection Patterns
```python
service_patterns = {
    ServiceType.API_SERVICE: [
        r'api[_-]?service', r'controller', r'endpoint', r'route',
        r'@app\.route', r'@api\.route', r'@RestController', r'@Controller'
    ],
    ServiceType.DATA_SERVICE: [
        r'data[_-]?service', r'repository', r'dao', r'database',
        r'@Repository', r'@Entity', r'@Table', r'Model'
    ],
    # ... more patterns
}
```

## 🚀 Usage Examples

### Basic Multi-Language Analysis
```python
from architex.core.parsers import ParserRegistry
from architex.core.analyzer import CodeAnalyzer

# Initialize parser registry
registry = ParserRegistry()

# Analyze a multi-language project
analyzer = CodeAnalyzer()
result = analyzer.analyze_project("path/to/project")

# Get language statistics
print(f"Languages found: {result.language_stats}")
print(f"Total elements: {len(result.elements)}")
print(f"Total relationships: {len(result.relationships)}")
```

### Service Detection
```python
from architex.core.service_detector import ServiceDetector

# Detect services
detector = ServiceDetector()
services = detector.detect_services(analysis_result)

for service in services:
    print(f"Service: {service.name}")
    print(f"Type: {service.type}")
    print(f"Cohesion: {service.cohesion_score:.2f}")
    print(f"Coupling: {service.coupling_score:.2f}")
```

### Dependency Analysis
```python
from architex.core.dependency_analyzer import DependencyAnalyzer

# Analyze dependencies
analyzer = DependencyAnalyzer()
dependency_graph = analyzer.build_dependency_graph(analysis_result)

# Find high-impact elements
high_impact = analyzer.find_high_impact_elements(analysis_result, threshold=0.1)

# Generate dependency report
report = analyzer.generate_dependency_report(analysis_result)
```

## 📊 Analysis Capabilities

### AST Analysis
- **Node Types**: Class, function, method, variable, import
- **Position Tracking**: Line numbers, start/end positions
- **Metadata Extraction**: Decorators, modifiers, annotations
- **Language-Specific**: Tailored parsing for each language

### Dependency Extraction
- **Import Analysis**: Module dependencies, package imports
- **Function Calls**: Method invocations, function references
- **Inheritance**: Class inheritance, interface implementation
- **Data Flow**: Variable usage, assignment tracking

### Service Detection
- **Pattern Matching**: Regex-based service identification
- **Metrics Calculation**: Cohesion, coupling, complexity
- **Boundary Detection**: Service boundary identification
- **Anti-Pattern Detection**: God objects, circular dependencies

### Architectural Analysis
- **Layer Detection**: Presentation, application, domain, infrastructure
- **Microservice Detection**: High cohesion, low coupling services
- **Dependency Clustering**: Community detection algorithms
- **Impact Analysis**: Element impact and dependency analysis

## 🔧 Configuration

### Parser Configuration
```python
# Register custom parser
from architex.core.parsers import BaseParser

class CustomParser(BaseParser):
    def __init__(self):
        super().__init__()
        self.supported_extensions = ['.custom']
        self.language = LanguageType.CUSTOM
    
    def parse_file(self, file_path: Path) -> List[CodeElement]:
        # Custom parsing logic
        pass

# Register parser
registry = ParserRegistry()
registry.register_parser('custom', CustomParser())
```

### Service Detection Configuration
```python
# Custom service patterns
custom_patterns = {
    ServiceType.CUSTOM_SERVICE: [
        r'custom[_-]?service',
        r'@CustomService',
        r'CustomService'
    ]
}

detector = ServiceDetector()
detector.service_patterns.update(custom_patterns)
```

## 📈 Performance Considerations

### Parsing Performance
- **Python**: Fast AST parsing with built-in `ast` module
- **JavaScript**: Efficient regex-based parsing
- **Java**: Optimized pattern matching for large codebases
- **Other Languages**: Scalable parsing strategies

### Memory Usage
- **Streaming Parsing**: Process files incrementally
- **Lazy Loading**: Load AST nodes on demand
- **Memory Pooling**: Reuse AST node objects
- **Garbage Collection**: Automatic cleanup of unused objects

### Scalability
- **Parallel Processing**: Multi-threaded parsing
- **Incremental Analysis**: Update only changed files
- **Caching**: Cache parsed results for performance
- **Distributed Analysis**: Support for large codebases

## 🧪 Testing

### Unit Tests
```bash
# Run parser tests
python -m pytest tests/test_parsers.py

# Run service detection tests
python -m pytest tests/test_service_detector.py

# Run dependency analysis tests
python -m pytest tests/test_dependency_analyzer.py
```

### Integration Tests
```bash
# Run multi-language analysis tests
python -m pytest tests/test_multi_language.py

# Run comprehensive analysis tests
python -m pytest tests/test_comprehensive_analysis.py
```

### Demo Script
```bash
# Run multi-language demo
python demo_multi_language_analysis.py
```

## 🔮 Future Enhancements

### Planned Language Support
- **C++** (`.cpp`, `.hpp`) - Template and STL analysis
- **C** (`.c`, `.h`) - System programming analysis
- **Assembly** (`.asm`, `.s`) - Low-level code analysis
- **Shell Scripts** (`.sh`, `.bash`) - Script analysis
- **SQL** (`.sql`) - Database schema analysis
- **YAML/JSON** (`.yml`, `.json`) - Configuration analysis

### Advanced Features
- **Semantic Analysis**: Understanding code semantics
- **Type Inference**: Automatic type detection
- **Code Generation**: Generate code from models
- **Refactoring Support**: Suggest code improvements
- **Visualization**: Interactive dependency graphs
- **Integration**: IDE plugins and CI/CD integration

## 📚 Documentation

### API Reference
- [Parser API](docs/api/parsers.md)
- [Service Detection API](docs/api/service_detector.md)
- [Dependency Analysis API](docs/api/dependency_analyzer.md)
- [Models Reference](docs/api/models.md)

### Examples
- [Multi-Language Analysis](examples/multi_language_analysis.py)
- [Service Detection](examples/service_detection.py)
- [Dependency Analysis](examples/dependency_analysis.py)
- [Custom Parsers](examples/custom_parsers.py)

### Best Practices
- [Language-Specific Guidelines](docs/best_practices/languages.md)
- [Performance Optimization](docs/best_practices/performance.md)
- [Extending Architex](docs/best_practices/extending.md)
- [Integration Patterns](docs/best_practices/integration.md)

---

**Architex Multi-Language Analysis** provides comprehensive code analysis capabilities across multiple programming languages, enabling developers to understand, maintain, and improve complex codebases with confidence. 