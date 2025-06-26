#!/usr/bin/env python3
"""
Demo script showcasing Architex Interactive Web Dashboard:
- Real-time metrics visualization
- AI-powered recommendations display
- Interactive architecture diagrams
- Live updates via WebSocket
"""

import asyncio
import sys
import time
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent))

from architex.web.dashboard import DashboardServer
from architex.web.websocket_handler import WebSocketHandler
from architex.core.analyzer import CodebaseAnalyzer
from architex.core.metrics import MetricsCalculator
from architex.ai.recommendations import AIRecommendations
from architex.ai.labeler import AILabeler
from architex.ai.summarizer import AISummarizer

console = Console()


async def demo_web_dashboard():
    """Demonstrate the interactive web dashboard features."""
    
    console.print(Panel.fit(
        "[bold blue]🌐 Architex Interactive Web Dashboard Demo[/bold blue]\n\n"
        "This demo showcases the new web dashboard features:\n"
        "• Real-time metrics visualization with charts\n"
        "• AI-powered recommendations with priority filtering\n"
        "• Interactive architecture diagrams (Mermaid/PlantUML/Graphviz)\n"
        "• Live updates via WebSocket\n"
        "• Beautiful responsive web interface\n\n"
        "Starting dashboard server...",
        title="Web Dashboard Features"
    ))
    
    # Use the example project
    codebase_path = "examples/simple_python_project"
    
    if not Path(codebase_path).exists():
        console.print(f"[red]Error: Example project not found at {codebase_path}[/red]")
        console.print("Please ensure the example project exists before running this demo.")
        return
    
    # Initialize components
    analyzer = CodebaseAnalyzer()
    metrics_calculator = MetricsCalculator()
    ai_recommender = AIRecommendations()
    labeler = AILabeler()
    summarizer = AISummarizer()
    
    # Create dashboard server
    dashboard_server = DashboardServer(host="localhost", port=8000)
    
    # Create WebSocket handler
    ws_handler = WebSocketHandler(host="localhost", port=8765)
    
    # Register analysis callback
    async def analysis_callback(codebase_path: str):
        """Callback for analysis requests."""
        console.print(f"[green]🔄 Analysis requested for: {codebase_path}[/green]")
        
        # Perform analysis
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Analyzing codebase...", total=None)
            
            try:
                result = analyzer.analyze(codebase_path)
                progress.update(task, description="Core analysis complete!")
                
                # Calculate metrics
                metrics = metrics_calculator.calculate_all_metrics(result)
                
                # Generate AI features
                labels = await labeler.label_analysis_result(result)
                summaries = await summarizer.summarize_analysis_result(result)
                recommendations = await ai_recommender.generate_recommendations(result)
                
                progress.update(task, description="AI features complete!")
                
                # Broadcast updates
                await ws_handler.broadcast_analysis_update({
                    "elements_count": len(result.elements),
                    "relationships_count": len(result.relationships),
                    "metrics_count": len(metrics.get_all_metrics()),
                    "recommendations_count": len(recommendations),
                    "labels_count": len(labels),
                    "summaries_count": len(summaries)
                })
                
                await ws_handler.broadcast_metrics_update({
                    "metrics": [
                        {
                            "name": metric.name,
                            "value": metric.value,
                            "unit": metric.unit,
                            "severity": metric.severity
                        }
                        for metric in metrics.get_all_metrics()
                    ]
                })
                
                await ws_handler.broadcast_recommendations_update({
                    "recommendations": [
                        {
                            "priority": rec.priority.value,
                            "title": rec.title,
                            "description": rec.description,
                            "impact": rec.impact,
                            "confidence": rec.confidence
                        }
                        for rec in recommendations
                    ]
                })
                
                console.print("[green]✅ Analysis completed and broadcasted![/green]")
                
            except Exception as e:
                console.print(f"[red]Error during analysis: {e}[/red]")
    
    ws_handler.register_analysis_callback(analysis_callback)
    
    # Start servers
    console.print("\n[bold blue]🚀 Starting Servers...[/bold blue]")
    
    # Start WebSocket server in background
    ws_task = asyncio.create_task(ws_handler.start_server())
    
    # Start dashboard server
    dashboard_task = asyncio.create_task(dashboard_server.start_async())
    
    # Wait a moment for servers to start
    await asyncio.sleep(2)
    
    console.print("\n" + "="*80)
    console.print("[bold green]✅ Web Dashboard Demo Started![/bold green]")
    console.print("="*80)
    
    console.print(f"\n[bold]🌐 Dashboard URLs:[/bold]")
    console.print(f"📊 Main Dashboard: [cyan]http://localhost:8000[/cyan]")
    console.print(f"🔌 WebSocket: [cyan]ws://localhost:8765[/cyan]")
    
    console.print(f"\n[bold]📁 Example Codebase:[/bold]")
    console.print(f"📂 Path: [cyan]{codebase_path}[/cyan]")
    
    console.print(f"\n[bold]🎯 Dashboard Features:[/bold]")
    features = [
        ("📊 Real-time Metrics", "Live charts and severity indicators"),
        ("🎯 AI Recommendations", "Priority-filtered architectural advice"),
        ("🏗️ Interactive Diagrams", "Mermaid, PlantUML, and Graphviz"),
        ("🔄 Live Updates", "WebSocket-powered real-time updates"),
        ("📱 Responsive Design", "Works on desktop and mobile"),
        ("🎨 Beautiful UI", "Modern Tailwind CSS interface")
    ]
    
    for feature, description in features:
        console.print(f"  {feature}: {description}")
    
    console.print(f"\n[bold]💡 How to Use:[/bold]")
    usage_steps = [
        "1. Open http://localhost:8000 in your browser",
        "2. Enter the codebase path: examples/simple_python_project",
        "3. Click 'Analyze' to start the analysis",
        "4. Watch real-time updates in the dashboard",
        "5. Explore metrics, recommendations, and diagrams",
        "6. Try different diagram formats (Mermaid/PlantUML/Graphviz)"
    ]
    
    for step in usage_steps:
        console.print(f"  {step}")
    
    console.print(f"\n[bold]🔧 CLI Commands:[/bold]")
    cli_commands = [
        ("Start dashboard", "architex dashboard"),
        ("Custom port", "architex dashboard --port 8080"),
        ("Custom host", "architex dashboard --host 0.0.0.0"),
        ("With analysis", "architex analyze examples/simple_python_project --export-summary markdown")
    ]
    
    for description, command in cli_commands:
        console.print(f"  {description}: [dim]{command}[/dim]")
    
    console.print(f"\n[bold]🛑 To Stop:[/bold]")
    console.print("  Press Ctrl+C to stop the demo")
    
    console.print(Panel.fit(
        "[bold green]🎉 Web Dashboard Demo Running![/bold green]\n\n"
        "The interactive web dashboard is now available at:\n"
        "http://localhost:8000\n\n"
        "Open your browser and start exploring the enhanced\n"
        "Architex features with a beautiful web interface!",
        title="Demo Active"
    ))
    
    try:
        # Keep the demo running
        await asyncio.gather(ws_task, dashboard_task)
    except KeyboardInterrupt:
        console.print("\n[green]✅ Web dashboard demo stopped[/green]")


def demo_dashboard_features():
    """Showcase dashboard features without starting servers."""
    
    console.print(Panel.fit(
        "[bold blue]🌐 Architex Web Dashboard Features[/bold blue]\n\n"
        "The interactive web dashboard provides:\n\n"
        "[bold]📊 Real-Time Metrics Dashboard[/bold]\n"
        "• Live charts with Chart.js\n"
        "• Color-coded severity indicators\n"
        "• Interactive metric exploration\n"
        "• Performance trend visualization\n\n"
        "[bold]🎯 AI Recommendations Center[/bold]\n"
        "• Priority-filtered recommendations\n"
        "• Impact and effort assessment\n"
        "• Confidence scoring display\n"
        "• Actionable improvement suggestions\n\n"
        "[bold]🏗️ Interactive Architecture Diagrams[/bold]\n"
        "• Mermaid diagrams with live updates\n"
        "• PlantUML standard diagrams\n"
        "• Graphviz static diagrams\n"
        "• Zoom and pan capabilities\n\n"
        "[bold]🔄 Live Updates System[/bold]\n"
        "• WebSocket real-time communication\n"
        "• File change detection\n"
        "• Instant diagram updates\n"
        "• Multi-client support\n\n"
        "[bold]📱 Modern Web Interface[/bold]\n"
        "• Responsive Tailwind CSS design\n"
        "• Mobile-friendly layout\n"
        "• Dark/light theme support\n"
        "• Keyboard shortcuts\n\n"
        "[bold]🔧 Developer Experience[/bold]\n"
        "• RESTful API endpoints\n"
        "• WebSocket event system\n"
        "• Export functionality\n"
        "• Configuration management",
        title="Dashboard Features Overview"
    ))
    
    # Show API endpoints
    console.print("\n[bold]🔌 API Endpoints:[/bold]")
    api_endpoints = [
        ("GET /", "Main dashboard page"),
        ("GET /api/status", "Server status"),
        ("POST /api/analyze", "Analyze codebase"),
        ("GET /api/metrics", "Get metrics data"),
        ("GET /api/recommendations", "Get AI recommendations"),
        ("GET /api/diagram/{format}", "Get diagram in format"),
        ("WS /ws", "WebSocket connection")
    ]
    
    api_table = Table()
    api_table.add_column("Endpoint", style="cyan")
    api_table.add_column("Description", style="green")
    
    for endpoint, description in api_endpoints:
        api_table.add_row(endpoint, description)
    
    console.print(api_table)
    
    # Show WebSocket events
    console.print("\n[bold]🔌 WebSocket Events:[/bold]")
    ws_events = [
        ("welcome", "Connection established"),
        ("analysis_update", "Analysis results updated"),
        ("metrics_update", "Metrics data updated"),
        ("recommendations_update", "Recommendations updated"),
        ("pong", "Ping response"),
        ("status", "Server status"),
        ("error", "Error message")
    ]
    
    ws_table = Table()
    ws_table.add_column("Event", style="cyan")
    ws_table.add_column("Description", style="green")
    
    for event, description in ws_events:
        ws_table.add_row(event, description)
    
    console.print(ws_table)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Architex Web Dashboard Demo")
    parser.add_argument("--features-only", action="store_true", 
                       help="Show features overview without starting servers")
    
    args = parser.parse_args()
    
    if args.features_only:
        demo_dashboard_features()
    else:
        asyncio.run(demo_web_dashboard()) 