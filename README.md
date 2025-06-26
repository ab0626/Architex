# Architex - AI-Powered System Design Diagram Generator

A revolutionary developer tool that automatically generates intelligent system design diagrams from any codebase using advanced AI analysis, real-time monitoring, and natural language understanding.

## 🚀 **Revolutionary Features**

### 🤖 **AI-Powered Intelligence**
- **Smart Component Labeling**: Automatic classification of code components using GPT-4/Claude
- **Natural Language Summaries**: AI-generated descriptions of system modules and responsibilities
- **Intelligent Service Boundaries**: AI-driven detection of architectural boundaries and patterns
- **Confidence Scoring**: AI confidence levels for all generated insights
- **Context-Aware Analysis**: Deep understanding of code semantics and relationships

### 🔄 **Live Real-Time Analysis**
- **File Watching**: Monitor codebase changes in real-time with Watchdog
- **Live Updates**: Instant diagram updates as you code
- **WebSocket Server**: Real-time communication with frontend applications
- **Incremental Analysis**: Smart analysis of only changed files for performance
- **Debounced Updates**: Prevents excessive analysis during rapid changes

### 🎨 **Advanced Visualization**
- **Interactive Diagrams**: Mermaid, PlantUML, and Graphviz with AI-enhanced labels
- **Dynamic Layouts**: Automatic layout optimization based on relationships
- **Color-Coded Elements**: Visual distinction of different component types
- **Relationship Mapping**: Clear visualization of dependencies and interactions
- **3D Architecture Views**: Three.js-based 3D visualization (planned)

### 🛠️ **Developer Experience**
- **VS Code Integration**: Seamless IDE integration with real-time analysis
- **CLI with Rich UI**: Beautiful terminal interface with progress indicators
- **Configuration Management**: Comprehensive YAML configuration system
- **Plugin Architecture**: Extensible parsers and exporters
- **Performance Optimization**: Parallel processing and intelligent caching

## 🏗️ **Architecture Overview**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Codebase      │    │   AI-Powered    │    │   Live Output   │
│   Monitoring    │    │   Analysis      │    │   & Updates     │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ • File Watcher  │───▶│ • LangChain     │───▶│ • WebSocket     │
│ • Watchdog      │    │ • GPT-4/Claude  │    │ • Real-time     │
│ • Live Updates  │    │ • Smart Labels  │    │ • Interactive   │
│ • Debouncing    │    │ • Summaries     │    │ • Dashboards    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🛠️ **Enhanced Tech Stack**

### **AI & Machine Learning**
- **LangChain**: Advanced AI orchestration and prompt management
- **OpenAI GPT-4**: State-of-the-art language model for code understanding
- **Anthropic Claude**: Alternative AI model for enhanced analysis
- **Sentence Transformers**: Semantic similarity and clustering
- **Redis Caching**: Intelligent caching of AI responses

### **Real-Time & Live Updates**
- **Watchdog**: File system monitoring for live code changes
- **WebSockets**: Real-time bidirectional communication
- **Asyncio**: High-performance asynchronous processing
- **MQTT**: Lightweight messaging for distributed systems

### **Advanced Visualization**
- **Dash & Plotly**: Interactive web-based visualizations
- **Cytoscape.js**: Graph visualization and manipulation
- **Bokeh**: Advanced plotting and analytics
- **Three.js**: 3D visualization capabilities

### **Performance & Scalability**
- **Redis**: High-performance caching and session management
- **SQLAlchemy**: Database abstraction and ORM
- **Prometheus**: Metrics collection and monitoring
- **Structlog**: Structured logging for observability

### **Code Quality & Analysis**
- **Radon**: Code complexity and maintainability metrics
- **Bandit**: Security vulnerability detection
- **MCCabe**: Cyclomatic complexity analysis

## 📦 **Installation**

```bash
# Clone the repository
git clone https://github.com/yourusername/architex.git
cd architex

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .

# Set up environment variables (optional)
export OPENAI_API_KEY="your-openai-key"
export ANTHROPIC_API_KEY="your-anthropic-key"
export REDIS_URL="redis://localhost:6379"
```

## 🚀 **Quick Start**

### **Basic Analysis with AI**
```bash
# Analyze with AI-powered features
architex analyze /path/to/project --ai-labels --ai-summaries

# Export with AI-enhanced labels
architex analyze /path/to/project --format mermaid --output diagram.md
```

### **Live Analysis with File Watching**
```bash
# Start live analysis with file watching
architex watch /path/to/project --port 8765

# Connect to WebSocket for real-time updates
# ws://localhost:8765
```

### **Advanced Configuration**
```bash
# Use custom configuration
architex analyze /path/to/project --config config.yaml

# Show AI features
architex ai-features

# Show live features
architex live-features
```

## 📊 **Enhanced CLI Features**

### **Comprehensive Metrics & Analytics**
The enhanced CLI now provides detailed code quality metrics with color-coded severity indicators:

```bash
# Analyze with full metrics display
architex analyze /path/to/project

# Output includes:
# 📊 Key Metrics Table
# • Cyclomatic Complexity (with severity)
# • Coupling & Cohesion scores
# • Architecture compliance
# • Maintainability index
# • Performance indicators
```

**Metrics Categories:**
- **Complexity Metrics**: Cyclomatic complexity, cognitive complexity, nesting depth
- **Coupling Metrics**: Afferent/efferent coupling, instability scores
- **Cohesion Metrics**: Lack of cohesion of methods (LCOM)
- **Size Metrics**: Lines of code, file counts, class/function counts
- **Quality Metrics**: Test coverage, documentation coverage, duplication ratio
- **Architecture Metrics**: Boundary violations, compliance scores, modularity
- **Performance Metrics**: Memory usage indicators, bottleneck detection
- **Security Metrics**: Vulnerability counts, input validation coverage
- **Maintainability Metrics**: Overall maintainability index

### **AI-Powered Architectural Recommendations**
Get actionable architectural advice with priority levels and impact assessment:

```bash
# Generate AI recommendations
architex analyze /path/to/project --ai-labels --ai-summaries

# Recommendations include:
# 🎯 Priority levels: Critical, High, Medium, Low
# 📈 Impact assessment: High/Medium/Low impact
# ⚡ Effort estimation: Implementation effort required
# 🎯 Confidence scores: AI confidence in recommendations
```

**Recommendation Types:**
- **Performance**: Bottlenecks, inefficient algorithms, optimization opportunities
- **Security**: Vulnerabilities, input validation, security best practices
- **Maintainability**: Code complexity, refactoring suggestions, clean code principles
- **Scalability**: Architecture patterns, scaling considerations
- **Code Quality**: Standards compliance, best practices
- **Dependencies**: Dependency management, version conflicts
- **Testing**: Coverage gaps, testing strategies

### **Rich Export Functionality**
Export comprehensive analysis summaries in multiple formats:

```bash
# Export as Markdown (with emojis and formatting)
architex analyze /path/to/project --export-summary markdown

# Export as JSON (for programmatic use)
architex analyze /path/to/project --export-summary json

# Combined analysis with export
architex analyze /path/to/project --ai-labels --ai-summaries --export-summary markdown --format mermaid --output diagram.md
```

**Export Features:**
- **Markdown Export**: Beautiful formatted reports with tables, emojis, and sections
- **JSON Export**: Structured data for integration with other tools
- **Comprehensive Data**: Includes metrics, recommendations, AI labels, and summaries
- **Custom Filenames**: Automatic naming based on project name

### **Enhanced Terminal Experience**
Rich, color-coded terminal output with progress indicators:

```bash
# Color-coded severity indicators:
# ✅ Info (Green) - Good practices
# ⚠️ Warning (Yellow) - Areas for improvement
# ❌ Error (Red) - Issues to address
# 🚨 Critical (Bold Red) - Urgent attention required

# Priority indicators for recommendations:
# 🚨 Critical - Immediate action required
# 🔴 High - Important improvements
# 🟡 Medium - Good to address
# 🟢 Low - Nice to have
```

### **Demo & Examples**
```bash
# Run the enhanced CLI demo
python demo_cli_enhancements.py

# Example output structure:
# ┌─────────────────────────────────────────────────────────────┐
# │                    Enhanced Analysis Summary                │
# ├─────────────────────────────────────────────────────────────┤
# │ 📊 Key Metrics                                              │
# │ ┌─────────────────┬─────────┬──────────┬─────────────┐     │
# │ │ Metric          │ Value   │ Unit     │ Severity    │     │
# │ ├─────────────────┼─────────┼──────────┼─────────────┤     │
# │ │ Cyclomatic Comp │ 8.5     │ units    │ ⚠️ Warning  │     │
# │ │ Architecture    │ 0.85    │ %        │ ✅ Info     │     │
# │ │ Maintainability │ 65.2    │ score    │ ⚠️ Warning  │     │
# │ └─────────────────┴─────────┴──────────┴─────────────┘     │
# │                                                             │
# │ 🎯 AI-Powered Recommendations                               │
# │ ┌─────────┬─────────────────────────┬─────────┬──────────┐  │
# │ │ Priority│ Title                   │ Impact  │ Confidence│  │
# │ ├─────────┼─────────────────────────┼─────────┼──────────┤  │
# │ │ 🔴 High │ Reduce Cyclomatic Comp  │ High    │ 0.92     │  │
# │ │ 🟡 Med  │ Add Input Validation    │ Medium  │ 0.85     │  │
# │ └─────────┴─────────────────────────┴─────────┴──────────┘  │
# └─────────────────────────────────────────────────────────────┘
```

## 🌐 **Interactive Web Dashboard**

### **Real-Time Web Interface**
Access all Architex features through a beautiful, responsive web dashboard with real-time updates:

```bash
# Start the interactive web dashboard
architex dashboard

# Custom configuration
architex dashboard --host 0.0.0.0 --port 8080 --ws-port 8765

# Access the dashboard
# Open http://localhost:8000 in your browser
```

### **Dashboard Features**

#### **📊 Real-Time Metrics Dashboard**
- **Live Charts**: Interactive charts powered by Chart.js
- **Severity Indicators**: Color-coded metrics (Info/Warning/Error/Critical)
- **Performance Trends**: Track metrics over time
- **Responsive Design**: Works on desktop and mobile devices

#### **🎯 AI Recommendations Center**
- **Priority Filtering**: Filter by Critical/High/Medium/Low priority
- **Impact Assessment**: Visual impact and effort indicators
- **Confidence Scoring**: AI confidence levels for each recommendation
- **Actionable Insights**: Detailed improvement suggestions

#### **🏗️ Interactive Architecture Diagrams**
- **Multiple Formats**: Mermaid, PlantUML, and Graphviz
- **Live Updates**: Real-time diagram updates as code changes
- **Interactive Elements**: Zoom, pan, and explore diagrams
- **Export Options**: Download diagrams in various formats

#### **🔄 Live Updates System**
- **WebSocket Communication**: Real-time bidirectional updates
- **File Change Detection**: Instant updates when code changes
- **Multi-Client Support**: Multiple users can view simultaneously
- **Connection Status**: Visual indicators for connection health

### **Dashboard Architecture**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Browser   │    │   FastAPI       │    │   WebSocket     │
│   (React/HTML)  │◄──►│   Dashboard     │◄──►│   Server        │
│                 │    │   Server        │    │                 │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ • Real-time UI  │    │ • REST API      │    │ • Live Updates  │
│ • Charts        │    │ • Static Files  │    │ • File Watching │
│ • Diagrams      │    │ • WebSocket     │    │ • Broadcasting  │
│ • Responsive    │    │ • CORS Support  │    │ • Multi-client  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### **API Endpoints**

#### **REST API**
```bash
# Dashboard pages
GET /                    # Main dashboard
GET /static/*           # Static assets

# Analysis endpoints
POST /api/analyze       # Analyze codebase
GET /api/metrics        # Get metrics data
GET /api/recommendations # Get AI recommendations
GET /api/diagram/{format} # Get diagram (mermaid/plantuml/graphviz)
GET /api/status         # Server status
```

#### **WebSocket Events**
```javascript
// Connect to WebSocket
const ws = new WebSocket('ws://localhost:8765');

// Event types
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    switch(data.type) {
        case 'welcome':           // Connection established
        case 'analysis_update':   // Analysis results updated
        case 'metrics_update':    // Metrics data updated
        case 'recommendations_update': // Recommendations updated
        case 'pong':             // Ping response
        case 'status':           // Server status
        case 'error':            // Error message
    }
};
```

### **Dashboard Usage Examples**

#### **Basic Dashboard Usage**
```bash
# Start dashboard
architex dashboard

# Open browser to http://localhost:8000
# Enter codebase path and click "Analyze"
# Explore metrics, recommendations, and diagrams
```

#### **Advanced Dashboard Configuration**
```bash
# Custom host and ports
architex dashboard --host 0.0.0.0 --port 8080 --ws-port 8765

# For production deployment
architex dashboard --host 0.0.0.0 --port 80
```

#### **Integration with CLI Analysis**
```bash
# Analyze with CLI and view in dashboard
architex analyze /path/to/project --export-summary markdown
architex dashboard  # Start dashboard to view results
```

### **Dashboard Demo**
```bash
# Run the web dashboard demo
python demo_web_dashboard.py

# Show features overview only
python demo_web_dashboard.py --features-only
```

### **Dashboard Screenshots**

```
┌─────────────────────────────────────────────────────────────┐
│                    Architex Dashboard                      │
├─────────────────────────────────────────────────────────────┤
│ 📁 Codebase Analysis                                        │
│ [examples/simple_python_project] [🔍 Analyze]              │
├─────────────────────────────────────────────────────────────┤
│ 📊 Key Metrics    🎯 AI Recommendations    📈 Summary      │
│ ┌─────────────┐   ┌─────────────────────┐   ┌─────────────┐ │
│ │ Cyclomatic  │   │ 🔴 High Priority    │   │ 25 Elements │ │
│ │ Complexity  │   │ Reduce Complexity   │   │ 15 Relations│ │
│ │ 8.5 ⚠️      │   │ 🟡 Medium Priority  │   │ 20 Metrics  │ │
│ └─────────────┘   │ Add Validation      │   │ 8 Recs      │ │
│                   └─────────────────────┘   └─────────────┘ │
├─────────────────────────────────────────────────────────────┤
│ 📊 Metrics Chart                    🎯 Top Recommendations │
│ ┌─────────────────────────────────┐ ┌─────────────────────┐ │
│ │ ████████████████████████████████ │ │ 🚨 Critical: Security│ │
│ │ ████████████████████████████████ │ │ 🔴 High: Performance│ │
│ │ ████████████████████████████████ │ │ 🟡 Medium: Quality │ │
│ └─────────────────────────────────┘ └─────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│ 🏗️ Architecture Diagram [Mermaid] [PlantUML] [Graphviz]    │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ graph TD                                                 │ │
│ │   A[Main] --> B[Services]                               │ │
│ │   B --> C[Models]                                       │ │
│ │   C --> D[Database]                                     │ │
│ │   D --> E[External]                                     │ │
│ │   E --> F[API]                                          │ │
│ │   F --> G[Frontend]                                     │ │
│ │   G --> H[Database]                                     │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### **Deployment Options**

#### **Development**
```bash
# Local development
architex dashboard --host localhost --port 8000
```

#### **Production**
```bash
# Production deployment
architex dashboard --host 0.0.0.0 --port 80

# With reverse proxy (nginx)
# Configure nginx to proxy /api/* to FastAPI
# Serve static files directly
```

#### **Docker Deployment**
```dockerfile
# Dockerfile for dashboard
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000 8765
CMD ["architex", "dashboard", "--host", "0.0.0.0"]
```

## 🧩 **VS Code Extension**

### **Seamless IDE Integration**
Bring Architex's AI-powered architecture analysis directly into your development workflow with the official VS Code extension.

#### **Key Features**
- **Inline Analysis**: Run Architex analysis on your workspace or current file
- **Sidebar Views**: Instantly view architecture diagrams, metrics, and AI recommendations
- **Live Analysis**: Real-time updates as you code, powered by WebSocket
- **Export**: Save diagrams and summaries directly from the IDE
- **Status Bar**: Quick status and analysis feedback
- **Web Dashboard Integration**: Open the full dashboard in a VS Code webview

#### **Installation**
1. Open the `architex/vscode/` folder in VS Code
2. Run `npm install` to install dependencies
3. Press `F5` to launch the extension in a new Extension Development Host window
4. (Or, package and install the `.vsix` file via the Extensions panel)

#### **Usage**
- **Analyze Workspace**: `Architex: Analyze Current Workspace` (Command Palette)
- **Analyze File**: `Architex: Analyze Current File` (right-click or Command Palette)
- **Show Dashboard**: `Architex: Show Dashboard` (Command Palette or sidebar)
- **Show Metrics**: `Architex: Show Metrics` (sidebar)
- **Show Recommendations**: `Architex: Show AI Recommendations` (sidebar)
- **Start/Stop Live Analysis**: `Architex: Start Live Analysis` / `Architex: Stop Live Analysis`
- **Export Diagram/Summary**: `Architex: Export Diagram` / `Architex: Export Analysis Summary`

#### **Configuration**
- **Enable/Disable AI Features**: `architex.aiFeatures`
- **Live Analysis**: `architex.liveAnalysis`
- **WebSocket Port**: `architex.websocketPort`
- **Dashboard Port**: `architex.dashboardPort`
- **Default Export Format**: `architex.exportFormat` (mermaid, plantuml, graphviz)
- **Default Summary Format**: `architex.summaryFormat` (markdown, json)

#### **Screenshots**

```
┌─────────────────────────────────────────────────────────────┐
│                Architex VS Code Extension                  │
├─────────────────────────────────────────────────────────────┤
│ 🏗️ Architecture View   📊 Metrics View   🎯 Recommendations │
│ ┌─────────────┐        ┌─────────────┐   ┌───────────────┐  │
│ │ Mermaid     │        │ Complexity  │   │ 🔴 High: ...  │  │
│ │ Diagram     │        │ 8.5 ⚠️      │   │ 🟡 Medium:... │  │
│ │ (Webview)   │        │ Coverage    │   │ ...           │  │
│ └─────────────┘        └─────────────┘   └───────────────┘  │
├─────────────────────────────────────────────────────────────┤
│ 📊 Status Bar: Architex: 25 elements                        │
│ 🔄 Live Analysis: Active                                    │
│ 📤 Export: architex_diagram.md, architex_summary.md         │
└─────────────────────────────────────────────────────────────┘
```

#### **Development**
- Open `architex/vscode/` in VS Code
- Run `npm install` and `npm run compile`
- Press `F5` to launch the extension in a new window
- Use the Command Palette (`Ctrl+Shift+P`) to access all Architex commands

---

## 🤖 **AI Features Deep Dive**

### **Smart Component Labeling**
The AI system automatically analyzes each code component and provides:
- **Intelligent Labels**: "User Authentication Service" instead of "AuthService"
- **Architectural Categories**: Service, Model, Controller, Utility, Interface
- **Confidence Scores**: 0.0-1.0 confidence in the classification
- **Reasoning**: Explanation of why the component was classified this way

```python
# Example AI-generated label
{
    "label": "User Authentication Service",
    "description": "Handles user login, registration, and session management",
    "category": "Service",
    "confidence": 0.95,
    "reasoning": "Contains authentication methods and user session logic"
}
```

### **Natural Language Summaries**
AI generates comprehensive summaries for each module:
- **Purpose Description**: Clear explanation of what the module does
- **Key Responsibilities**: List of main functions and responsibilities
- **Dependencies**: External dependencies and relationships
- **Complexity Assessment**: 0.0-1.0 complexity score
- **Improvement Recommendations**: AI-suggested optimizations

### **Intelligent Service Boundaries**
AI automatically detects and groups related components:
- **Semantic Clustering**: Groups components based on functionality
- **Dependency Analysis**: Identifies internal vs external dependencies
- **Cohesion Scoring**: Measures how well components work together
- **Coupling Assessment**: Evaluates external dependencies

## 🔄 **Live Analysis Features**

### **Real-Time File Watching**
- **Instant Detection**: Monitors file system changes in real-time
- **Smart Debouncing**: Waits for changes to settle before analysis
- **Performance Optimized**: Only analyzes changed files when possible
- **Multi-Format Support**: Watches all supported programming languages

### **WebSocket Communication**
```javascript
// Connect to live analysis
const ws = new WebSocket('ws://localhost:8765');

// Request analysis
ws.send(JSON.stringify({
    command: 'analyze',
    codebase_path: '/path/to/project'
}));

// Receive real-time updates
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.type === 'analysis_update') {
        updateDiagram(data.data);
    }
};
```

### **Incremental Analysis**
- **Change Tracking**: Only re-analyzes modified components
- **Dependency Propagation**: Updates affected components automatically
- **Performance Monitoring**: Tracks analysis time and resource usage
- **Smart Caching**: Caches results to avoid redundant analysis

## 🎨 **Advanced Visualization**

### **Interactive Diagrams**
- **Zoom & Pan**: Navigate large architecture diagrams
- **Filtering**: Show/hide specific component types
- **Search**: Find components by name or type
- **Details Panel**: View detailed information on hover/click

### **Multiple Export Formats**
```bash
# Mermaid (interactive)
architex analyze /path/to/project --format mermaid

# PlantUML (UML standard)
architex analyze /path/to/project --format plantuml

# Graphviz (static)
architex analyze /path/to/project --format graphviz --output-format svg
```

### **Custom Styling**
```yaml
# config.yaml
visualization:
  colors:
    service: "#e3f2fd"
    model: "#f3e5f5"
    controller: "#e8f5e8"
  relationships:
    inherits: "solid"
    depends_on: "dotted"
    calls: "solid"
```

## ⚙️ **Configuration**

### **AI Configuration**
```yaml
ai:
  enabled: true
  llm:
    provider: "openai"
    model: "gpt-4"
    temperature: 0.1
    max_tokens: 1000
  labeling:
    confidence_threshold: 0.7
    cache_responses: true
```

### **Live Analysis Configuration**
```yaml
live:
  file_watching:
    enabled: true
    debounce_delay: 2.0
    extensions: [".py", ".js", ".java"]
  websocket:
    host: "localhost"
    port: 8765
    max_clients: 100
```

### **Performance Configuration**
```