"""
Interactive web dashboard server for Architex.
"""

import asyncio
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse, Response
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import base64

from ..core.analyzer import CodebaseAnalyzer
from ..core.metrics import MetricsCalculator
from ..ai.recommendations import AIRecommendations
from ..ai.labeler import AILabeler
from ..ai.summarizer import AISummarizer
from ..exporters import MermaidExporter, PlantUMLExporter, GraphvizExporter


class DashboardServer:
    """Interactive web dashboard server for Architex."""
    
    def __init__(self, host: str = "localhost", port: int = 8000):
        self.host = host
        self.port = port
        self.app = FastAPI(title="Architex Dashboard", version="1.0.0")
        self.active_connections: List[WebSocket] = []
        
        # Initialize components
        self.analyzer = CodebaseAnalyzer()
        self.metrics_calculator = MetricsCalculator()
        self.ai_recommender = AIRecommendations()
        self.labeler = AILabeler()
        self.summarizer = AISummarizer()
        
        # Current analysis state
        self.current_analysis = None
        self.current_metrics = None
        self.current_recommendations = []
        self.current_labels = {}
        self.current_summaries = {}
        
        self._setup_routes()
        self._setup_middleware()
    
    def _setup_middleware(self):
        """Setup CORS and other middleware."""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    def _setup_routes(self):
        """Setup API routes and static file serving."""
        
        # Serve static files (React app)
        static_path = Path(__file__).parent / "static"
        if static_path.exists():
            self.app.mount("/static", StaticFiles(directory=str(static_path)), name="static")
        
        @self.app.get("/", response_class=HTMLResponse)
        async def dashboard_home():
            """Serve the main dashboard page."""
            return self._get_dashboard_html()
        
        @self.app.get("/api/status")
        async def get_status():
            """Get dashboard status."""
            return {
                "status": "running",
                "active_connections": len(self.active_connections),
                "current_analysis": bool(self.current_analysis)
            }
        
        @self.app.post("/api/analyze")
        async def analyze_codebase(codebase_path: str):
            """Analyze a codebase and return results."""
            try:
                # Perform analysis
                result = self.analyzer.analyze(codebase_path)
                
                # Calculate metrics
                metrics = self.metrics_calculator.calculate_all_metrics(result)
                
                # Generate AI features
                labels = await self.labeler.label_analysis_result(result)
                summaries = await self.summarizer.summarize_analysis_result(result)
                recommendations = await self.ai_recommender.generate_recommendations(result)
                
                # Store current state
                self.current_analysis = result
                self.current_metrics = metrics
                self.current_recommendations = recommendations
                self.current_labels = labels
                self.current_summaries = summaries
                
                # Broadcast to all connected clients
                await self._broadcast_analysis_update(result, metrics, recommendations, labels, summaries)
                
                return {
                    "status": "success",
                    "message": "Analysis completed successfully",
                    "data": {
                        "elements_count": len(result.elements),
                        "relationships_count": len(result.relationships),
                        "metrics_count": len(metrics.get_all_metrics()),
                        "recommendations_count": len(recommendations),
                        "labels_count": len(labels),
                        "summaries_count": len(summaries)
                    }
                }
                
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/api/metrics")
        async def get_metrics():
            """Get current metrics."""
            if not self.current_metrics:
                raise HTTPException(status_code=404, detail="No analysis available")
            
            return {
                "metrics": [
                    {
                        "name": metric.name,
                        "value": metric.value,
                        "unit": metric.unit,
                        "description": metric.description,
                        "category": metric.category.value,
                        "severity": metric.severity,
                        "threshold": metric.threshold
                    }
                    for metric in self.current_metrics.get_all_metrics()
                ]
            }
        
        @self.app.get("/api/recommendations")
        async def get_recommendations():
            """Get current AI recommendations."""
            if not self.current_recommendations:
                raise HTTPException(status_code=404, detail="No analysis available")
            
            return {
                "recommendations": [
                    {
                        "id": rec.id,
                        "type": rec.type.value,
                        "priority": rec.priority.value,
                        "title": rec.title,
                        "description": rec.description,
                        "impact": rec.impact,
                        "effort": rec.effort,
                        "confidence": rec.confidence,
                        "code_examples": rec.code_examples,
                        "references": rec.references,
                        "affected_elements": rec.affected_elements
                    }
                    for rec in self.current_recommendations
                ]
            }
        
        @self.app.get("/api/diagram/{format}")
        async def get_diagram(format: str):
            """Get diagram in specified format."""
            if not self.current_analysis:
                raise HTTPException(status_code=404, detail="No analysis available")
            
            exporters = {
                'mermaid': MermaidExporter(),
                'plantuml': PlantUMLExporter(),
                'graphviz': GraphvizExporter()
            }
            
            exporter = exporters.get(format.lower())
            if not exporter:
                raise HTTPException(status_code=400, detail=f"Unsupported format: {format}")
            
            try:
                diagram_content = exporter.export(self.current_analysis)
                return {"diagram": diagram_content, "format": format}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            """WebSocket endpoint for real-time updates."""
            await websocket.accept()
            self.active_connections.append(websocket)
            
            try:
                # Send current state if available
                if self.current_analysis:
                    await websocket.send_text(json.dumps({
                        "type": "current_state",
                        "data": {
                            "elements_count": len(self.current_analysis.elements),
                            "relationships_count": len(self.current_analysis.relationships),
                            "metrics_count": len(self.current_metrics.get_all_metrics()) if self.current_metrics else 0,
                            "recommendations_count": len(self.current_recommendations)
                        }
                    }))
                
                # Keep connection alive
                while True:
                    await websocket.receive_text()
                    
            except WebSocketDisconnect:
                self.active_connections.remove(websocket)
        
        @self.app.get("/favicon.ico")
        async def favicon():
            # 16x16 transparent PNG favicon (base64-encoded)
            favicon_bytes = base64.b64decode(
                "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAQAAAC1+jfqAAAAFUlEQVR42mP8z8AARMAgYGBgAAQYAAH+AAH+QwAAAABJRU5ErkJggg=="
            )
            return Response(content=favicon_bytes, media_type="image/png")
    
    async def _broadcast_analysis_update(self, result, metrics, recommendations, labels, summaries):
        """Broadcast analysis update to all connected clients."""
        if not self.active_connections:
            return
        
        message = {
            "type": "analysis_update",
            "data": {
                "elements_count": len(result.elements),
                "relationships_count": len(result.relationships),
                "metrics": [
                    {
                        "name": metric.name,
                        "value": metric.value,
                        "unit": metric.unit,
                        "severity": metric.severity
                    }
                    for metric in metrics.get_all_metrics()
                ],
                "recommendations": [
                    {
                        "priority": rec.priority.value,
                        "title": rec.title,
                        "impact": rec.impact,
                        "confidence": rec.confidence
                    }
                    for rec in recommendations[:5]  # Top 5 recommendations
                ],
                "labels_count": len(labels),
                "summaries_count": len(summaries)
            }
        }
        
        # Broadcast to all connected clients
        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(message))
            except:
                # Remove disconnected clients
                self.active_connections.remove(connection)
    
    def _get_dashboard_html(self) -> str:
        """Generate the main dashboard HTML."""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Architex Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <style>
        .metric-card { transition: all 0.3s ease; }
        .metric-card:hover { transform: translateY(-2px); }
        .severity-info { border-left: 4px solid #10b981; }
        .severity-warning { border-left: 4px solid #f59e0b; }
        .severity-error { border-left: 4px solid #ef4444; }
        .severity-critical { border-left: 4px solid #dc2626; }
    </style>
</head>
<body class="bg-gray-50">
    <div id="app" class="min-h-screen">
        <!-- Header -->
        <header class="bg-white shadow-sm border-b">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div class="flex justify-between items-center py-4">
                    <div class="flex items-center">
                        <h1 class="text-2xl font-bold text-gray-900">🏗️ Architex Dashboard</h1>
                        <span class="ml-2 px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded-full">v1.0.0</span>
                    </div>
                    <div class="flex items-center space-x-4">
                        <div id="connection-status" class="flex items-center">
                            <div class="w-2 h-2 bg-red-500 rounded-full mr-2"></div>
                            <span class="text-sm text-gray-600">Disconnected</span>
                        </div>
                        <button id="analyze-btn" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
                            Analyze Codebase
                        </button>
                    </div>
                </div>
            </div>
        </header>

        <!-- Main Content -->
        <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <!-- Analysis Input -->
            <div class="bg-white rounded-lg shadow-sm p-6 mb-8">
                <h2 class="text-lg font-semibold text-gray-900 mb-4">📁 Codebase Analysis</h2>
                <div class="flex space-x-4">
                    <input type="text" id="codebase-path" placeholder="/path/to/your/codebase" 
                           class="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                    <button onclick="analyzeCodebase()" class="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 transition-colors">
                        🔍 Analyze
                    </button>
                </div>
            </div>

            <!-- Loading State -->
            <div id="loading" class="hidden bg-white rounded-lg shadow-sm p-8 text-center">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
                <p class="text-gray-600">Analyzing codebase...</p>
            </div>

            <!-- Dashboard Content -->
            <div id="dashboard-content" class="hidden">
                <!-- Metrics Overview -->
                <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
                    <div class="bg-white rounded-lg shadow-sm p-6">
                        <h3 class="text-lg font-semibold text-gray-900 mb-4">📊 Key Metrics</h3>
                        <div id="metrics-overview" class="space-y-3"></div>
                    </div>
                    
                    <div class="bg-white rounded-lg shadow-sm p-6">
                        <h3 class="text-lg font-semibold text-gray-900 mb-4">🎯 AI Recommendations</h3>
                        <div id="recommendations-overview" class="space-y-3"></div>
                    </div>
                    
                    <div class="bg-white rounded-lg shadow-sm p-6">
                        <h3 class="text-lg font-semibold text-gray-900 mb-4">📈 Analysis Summary</h3>
                        <div id="analysis-summary" class="space-y-3"></div>
                    </div>
                </div>

                <!-- Detailed Views -->
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    <!-- Metrics Chart -->
                    <div class="bg-white rounded-lg shadow-sm p-6">
                        <h3 class="text-lg font-semibold text-gray-900 mb-4">📊 Metrics Breakdown</h3>
                        <canvas id="metrics-chart" width="400" height="200"></canvas>
                    </div>
                    
                    <!-- Recommendations List -->
                    <div class="bg-white rounded-lg shadow-sm p-6">
                        <h3 class="text-lg font-semibold text-gray-900 mb-4">🎯 Top Recommendations</h3>
                        <div id="recommendations-list" class="space-y-4"></div>
                    </div>
                </div>

                <!-- Diagram Section -->
                <div class="mt-8 bg-white rounded-lg shadow-sm p-6">
                    <div class="flex justify-between items-center mb-4">
                        <h3 class="text-lg font-semibold text-gray-900">🏗️ Architecture Diagram</h3>
                        <div class="flex space-x-2">
                            <button onclick="showDiagram('mermaid')" class="px-3 py-1 text-sm bg-blue-100 text-blue-800 rounded hover:bg-blue-200">Mermaid</button>
                            <button onclick="showDiagram('plantuml')" class="px-3 py-1 text-sm bg-green-100 text-green-800 rounded hover:bg-green-200">PlantUML</button>
                            <button onclick="showDiagram('graphviz')" class="px-3 py-1 text-sm bg-purple-100 text-purple-800 rounded hover:bg-purple-200">Graphviz</button>
                        </div>
                    </div>
                    <div id="diagram-container" class="border rounded-lg p-4 bg-gray-50 min-h-64">
                        <p class="text-gray-500 text-center">Select a diagram format to view the architecture</p>
                    </div>
                </div>
            </div>
        </main>
    </div>

    <script>
        // Initialize Mermaid
        mermaid.initialize({ startOnLoad: true });

        // WebSocket connection
        let ws = null;
        let metricsChart = null;

        function connectWebSocket() {
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            const wsUrl = `${protocol}//${window.location.host}/ws`;
            
            ws = new WebSocket(wsUrl);
            
            ws.onopen = function() {
                updateConnectionStatus(true);
            };
            
            ws.onmessage = function(event) {
                const data = JSON.parse(event.data);
                handleWebSocketMessage(data);
            };
            
            ws.onclose = function() {
                updateConnectionStatus(false);
                // Reconnect after 5 seconds
                setTimeout(connectWebSocket, 5000);
            };
        }

        function updateConnectionStatus(connected) {
            const status = document.getElementById('connection-status');
            const indicator = status.querySelector('div');
            const text = status.querySelector('span');
            
            if (connected) {
                indicator.className = 'w-2 h-2 bg-green-500 rounded-full mr-2';
                text.textContent = 'Connected';
            } else {
                indicator.className = 'w-2 h-2 bg-red-500 rounded-full mr-2';
                text.textContent = 'Disconnected';
            }
        }

        function handleWebSocketMessage(data) {
            if (data.type === 'analysis_update') {
                updateDashboard(data.data);
            }
        }

        async function analyzeCodebase() {
            const pathInput = document.getElementById('codebase-path');
            const codebasePath = pathInput.value.trim();
            
            if (!codebasePath) {
                alert('Please enter a codebase path');
                return;
            }
            
            showLoading(true);
            
            try {
                const response = await fetch('/api/analyze', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ codebase_path: codebasePath })
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    // Load detailed data
                    await loadDashboardData();
                } else {
                    alert('Analysis failed: ' + result.detail);
                }
            } catch (error) {
                alert('Error during analysis: ' + error.message);
            } finally {
                showLoading(false);
            }
        }

        async function loadDashboardData() {
            try {
                // Load metrics
                const metricsResponse = await fetch('/api/metrics');
                const metricsData = await metricsResponse.json();
                
                // Load recommendations
                const recommendationsResponse = await fetch('/api/recommendations');
                const recommendationsData = await recommendationsResponse.json();
                
                updateDashboard({
                    metrics: metricsData.metrics,
                    recommendations: recommendationsData.recommendations
                });
                
            } catch (error) {
                console.error('Error loading dashboard data:', error);
            }
        }

        function updateDashboard(data) {
            showDashboard(true);
            
            if (data.metrics) {
                updateMetrics(data.metrics);
            }
            
            if (data.recommendations) {
                updateRecommendations(data.recommendations);
            }
            
            if (data.elements_count !== undefined) {
                updateSummary(data);
            }
        }

        function updateMetrics(metrics) {
            const container = document.getElementById('metrics-overview');
            container.innerHTML = '';
            
            metrics.forEach(metric => {
                const severityClass = `severity-${metric.severity}`;
                const severityColor = {
                    'info': 'text-green-600',
                    'warning': 'text-yellow-600',
                    'error': 'text-red-600',
                    'critical': 'text-red-800 font-bold'
                }[metric.severity] || 'text-gray-600';
                
                container.innerHTML += `
                    <div class="metric-card ${severityClass} bg-gray-50 p-3 rounded">
                        <div class="flex justify-between items-center">
                            <span class="text-sm font-medium text-gray-700">${metric.name.replace(/_/g, ' ')}</span>
                            <span class="text-sm ${severityColor}">${metric.value} ${metric.unit}</span>
                        </div>
                    </div>
                `;
            });
            
            // Update chart
            updateMetricsChart(metrics);
        }

        function updateMetricsChart(metrics) {
            const ctx = document.getElementById('metrics-chart').getContext('2d');
            
            if (metricsChart) {
                metricsChart.destroy();
            }
            
            const chartData = {
                labels: metrics.map(m => m.name.replace(/_/g, ' ')),
                datasets: [{
                    label: 'Metric Values',
                    data: metrics.map(m => m.value),
                    backgroundColor: metrics.map(m => {
                        switch(m.severity) {
                            case 'info': return 'rgba(16, 185, 129, 0.2)';
                            case 'warning': return 'rgba(245, 158, 11, 0.2)';
                            case 'error': return 'rgba(239, 68, 68, 0.2)';
                            case 'critical': return 'rgba(220, 38, 38, 0.2)';
                            default: return 'rgba(156, 163, 175, 0.2)';
                        }
                    }),
                    borderColor: metrics.map(m => {
                        switch(m.severity) {
                            case 'info': return 'rgb(16, 185, 129)';
                            case 'warning': return 'rgb(245, 158, 11)';
                            case 'error': return 'rgb(239, 68, 68)';
                            case 'critical': return 'rgb(220, 38, 38)';
                            default: return 'rgb(156, 163, 175)';
                        }
                    }),
                    borderWidth: 2
                }]
            };
            
            metricsChart = new Chart(ctx, {
                type: 'bar',
                data: chartData,
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }

        function updateRecommendations(recommendations) {
            const overview = document.getElementById('recommendations-overview');
            const list = document.getElementById('recommendations-list');
            
            // Update overview
            overview.innerHTML = '';
            recommendations.slice(0, 3).forEach(rec => {
                const priorityColor = {
                    'critical': 'text-red-800 bg-red-100',
                    'high': 'text-red-600 bg-red-50',
                    'medium': 'text-yellow-600 bg-yellow-50',
                    'low': 'text-green-600 bg-green-50'
                }[rec.priority] || 'text-gray-600 bg-gray-50';
                
                overview.innerHTML += `
                    <div class="p-3 rounded ${priorityColor}">
                        <div class="font-medium text-sm">${rec.title}</div>
                        <div class="text-xs opacity-75">${rec.impact} impact</div>
                    </div>
                `;
            });
            
            // Update detailed list
            list.innerHTML = '';
            recommendations.forEach(rec => {
                const priorityColor = {
                    'critical': 'border-red-500 bg-red-50',
                    'high': 'border-red-300 bg-red-25',
                    'medium': 'border-yellow-300 bg-yellow-25',
                    'low': 'border-green-300 bg-green-25'
                }[rec.priority] || 'border-gray-300 bg-gray-50';
                
                list.innerHTML += `
                    <div class="border-l-4 ${priorityColor} p-4 rounded">
                        <div class="flex justify-between items-start">
                            <div>
                                <h4 class="font-medium text-gray-900">${rec.title}</h4>
                                <p class="text-sm text-gray-600 mt-1">${rec.description}</p>
                            </div>
                            <div class="text-right">
                                <span class="inline-block px-2 py-1 text-xs font-medium rounded ${priorityColor.replace('border-', 'bg-').replace('-25', '-50')}">
                                    ${rec.priority.toUpperCase()}
                                </span>
                            </div>
                        </div>
                        <div class="mt-2 text-xs text-gray-500">
                            Impact: ${rec.impact} | Confidence: ${(rec.confidence * 100).toFixed(0)}%
                        </div>
                    </div>
                `;
            });
        }

        function updateSummary(data) {
            const container = document.getElementById('analysis-summary');
            container.innerHTML = `
                <div class="grid grid-cols-2 gap-4">
                    <div class="text-center p-3 bg-blue-50 rounded">
                        <div class="text-2xl font-bold text-blue-600">${data.elements_count}</div>
                        <div class="text-sm text-blue-800">Code Elements</div>
                    </div>
                    <div class="text-center p-3 bg-green-50 rounded">
                        <div class="text-2xl font-bold text-green-600">${data.relationships_count}</div>
                        <div class="text-sm text-green-800">Relationships</div>
                    </div>
                    <div class="text-center p-3 bg-purple-50 rounded">
                        <div class="text-2xl font-bold text-purple-600">${data.metrics_count}</div>
                        <div class="text-sm text-purple-800">Metrics</div>
                    </div>
                    <div class="text-center p-3 bg-orange-50 rounded">
                        <div class="text-2xl font-bold text-orange-600">${data.recommendations_count}</div>
                        <div class="text-sm text-orange-800">Recommendations</div>
                    </div>
                </div>
            `;
        }

        async function showDiagram(format) {
            const container = document.getElementById('diagram-container');
            container.innerHTML = '<div class="text-center"><div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div><p class="mt-2 text-gray-600">Loading diagram...</p></div>';
            
            try {
                const response = await fetch(`/api/diagram/${format}`);
                const data = await response.json();
                
                if (format === 'mermaid') {
                    container.innerHTML = '<div class="mermaid">' + data.diagram + '</div>';
                    mermaid.init();
                } else {
                    container.innerHTML = '<pre class="text-sm overflow-auto">' + data.diagram + '</pre>';
                }
            } catch (error) {
                container.innerHTML = '<p class="text-red-600">Error loading diagram: ' + error.message + '</p>';
            }
        }

        function showLoading(show) {
            const loading = document.getElementById('loading');
            const content = document.getElementById('dashboard-content');
            
            if (show) {
                loading.classList.remove('hidden');
                content.classList.add('hidden');
            } else {
                loading.classList.add('hidden');
            }
        }

        function showDashboard(show) {
            const content = document.getElementById('dashboard-content');
            if (show) {
                content.classList.remove('hidden');
            }
        }

        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            connectWebSocket();
        });
    </script>
</body>
</html>
        """
    
    def start(self):
        """Start the dashboard server."""
        uvicorn.run(self.app, host=self.host, port=self.port)
    
    async def start_async(self):
        """Start the dashboard server asynchronously."""
        config = uvicorn.Config(self.app, host=self.host, port=self.port)
        server = uvicorn.Server(config)
        await server.serve() 