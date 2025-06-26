"""
Enhanced CLI with AI features and live updates.
"""

import asyncio
import sys
from pathlib import Path
from typing import Optional, List
import typer
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.live import Live
from rich.layout import Layout

from ..core.analyzer import CodebaseAnalyzer
from ..ai.labeler import AILabeler
from ..ai.summarizer import AISummarizer
from ..watcher.file_watcher import FileWatcher
from ..watcher.live_analyzer import LiveAnalyzer
from ..exporters import MermaidExporter, PlantUMLExporter, GraphvizExporter
from ..core.metrics import MetricsCalculator
from ..ai.recommendations import AIRecommendations, ArchitecturalRecommendation, RecommendationType, Priority

app = typer.Typer(help="Architex Enhanced - AI-Powered System Design Analysis")
console = Console()


@app.command()
def analyze(
    codebase_path: str = typer.Argument(..., help="Path to the codebase to analyze"),
    format: str = typer.Option("mermaid", "--format", "-f", help="Output format (mermaid, plantuml, graphviz)"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file path"),
    ai_labels: bool = typer.Option(True, "--ai-labels/--no-ai-labels", help="Generate AI labels for components"),
    ai_summaries: bool = typer.Option(True, "--ai-summaries/--no-ai-summaries", help="Generate AI summaries for modules"),
    export_summary: Optional[str] = typer.Option(None, "--export-summary", help="Export summary as 'markdown' or 'json'"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output")
):
    """Analyze a codebase with AI-powered features."""
    
    if not Path(codebase_path).exists():
        console.print(f"[red]Error: Codebase path does not exist: {codebase_path}[/red]")
        sys.exit(1)
    
    asyncio.run(_run_enhanced_analysis(
        codebase_path, format, output, ai_labels, ai_summaries, export_summary, verbose
    ))


@app.command()
def watch(
    codebase_path: str = typer.Argument(..., help="Path to the codebase to watch"),
    port: int = typer.Option(8765, "--port", "-p", help="WebSocket server port"),
    host: str = typer.Option("localhost", "--host", help="WebSocket server host")
):
    """Start live analysis with file watching and WebSocket server."""
    
    if not Path(codebase_path).exists():
        console.print(f"[red]Error: Codebase path does not exist: {codebase_path}[/red]")
        sys.exit(1)
    
    asyncio.run(_run_live_analysis(codebase_path, host, port))


@app.command()
def ai_features():
    """Show available AI features and configuration."""
    console.print(Panel.fit(
        "[bold blue]🤖 AI Features Available[/bold blue]\n\n"
        "[green]✓[/green] Component Labeling\n"
        "   - Automatic classification of code components\n"
        "   - Confidence scoring and reasoning\n"
        "   - Support for OpenAI GPT-4 and Anthropic Claude\n\n"
        "[green]✓[/green] Module Summarization\n"
        "   - Natural language summaries of system modules\n"
        "   - Key responsibilities and dependencies\n"
        "   - Complexity assessment and recommendations\n\n"
        "[green]✓[/green] Service Boundary Detection\n"
        "   - AI-powered service boundary identification\n"
        "   - Relationship analysis and grouping\n"
        "   - Architectural pattern recognition\n\n"
        "[yellow]⚠[/yellow] Configuration Required:\n"
        "   - Set OPENAI_API_KEY or ANTHROPIC_API_KEY environment variables\n"
        "   - Optional: REDIS_URL for response caching",
        title="AI Features"
    ))


@app.command()
def live_features():
    """Show available live analysis features."""
    console.print(Panel.fit(
        "[bold blue]🔄 Live Analysis Features[/bold blue]\n\n"
        "[green]✓[/green] File Watching\n"
        "   - Real-time monitoring of codebase changes\n"
        "   - Debounced updates to prevent excessive analysis\n"
        "   - Support for multiple file extensions\n\n"
        "[green]✓[/green] WebSocket Server\n"
        "   - Real-time communication with frontend\n"
        "   - Live diagram updates\n"
        "   - Multi-client support\n\n"
        "[green]✓[/green] Incremental Analysis\n"
        "   - Smart analysis of changed files only\n"
        "   - Performance optimization for large codebases\n"
        "   - Change tracking and metadata\n\n"
        "[green]✓[/green] Interactive Dashboard\n"
        "   - Real-time metrics and statistics\n"
        "   - Live component exploration\n"
        "   - Dynamic diagram generation",
        title="Live Features"
    ))


@app.command()
def dashboard(
    host: str = typer.Option("localhost", "--host", help="Dashboard server host"),
    port: int = typer.Option(8000, "--port", "-p", help="Dashboard server port"),
    websocket_port: int = typer.Option(8765, "--ws-port", help="WebSocket server port")
):
    """Start the interactive web dashboard."""
    
    console.print(f"[bold blue]🌐 Starting Architex Dashboard[/bold blue]")
    console.print(f"📊 Dashboard: http://{host}:{port}")
    console.print(f"🔌 WebSocket: ws://{host}:{websocket_port}")
    
    try:
        from ..web.dashboard import DashboardServer
        dashboard_server = DashboardServer(host, port)
        
        console.print("[green]✅ Dashboard started![/green]")
        console.print("💡 Open your browser to view the interactive dashboard")
        console.print("🛑 Press Ctrl+C to stop")
        
        dashboard_server.start()
        
    except ImportError as e:
        console.print(f"[red]Error starting dashboard: {e}[/red]")
        console.print("💡 Make sure all web dependencies are installed")
        sys.exit(1)


async def _run_enhanced_analysis(
    codebase_path: str,
    format: str,
    output: Optional[Path],
    ai_labels: bool,
    ai_summaries: bool,
    export_summary: Optional[str],
    verbose: bool
):
    """Run enhanced analysis with AI features."""
    
    console.print(f"[bold blue]🔍 Enhanced Analysis: {codebase_path}[/bold blue]")
    
    # Initialize components
    analyzer = CodebaseAnalyzer()
    labeler = AILabeler() if ai_labels else None
    summarizer = AISummarizer() if ai_summaries else None
    metrics_calculator = MetricsCalculator()
    ai_recommender = AIRecommendations()
    
    # Perform core analysis
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Analyzing codebase...", total=None)
        
        try:
            result = analyzer.analyze(codebase_path)
            progress.update(task, description="Core analysis complete!")
            
        except Exception as e:
            console.print(f"[red]Error during analysis: {e}[/red]")
            sys.exit(1)
    
    # Generate AI labels
    labels = {}
    if ai_labels and labeler:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Generating AI labels...", total=None)
            
            try:
                labels = await labeler.label_analysis_result(result)
                progress.update(task, description="AI labeling complete!")
                
            except Exception as e:
                console.print(f"[yellow]Warning: AI labeling failed: {e}[/yellow]")
    
    # Generate AI summaries
    summaries = {}
    if ai_summaries and summarizer:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Generating AI summaries...", total=None)
            
            try:
                summaries = await summarizer.summarize_analysis_result(result)
                progress.update(task, description="AI summarization complete!")
                
            except Exception as e:
                console.print(f"[yellow]Warning: AI summarization failed: {e}[/yellow]")
    
    # Calculate metrics
    metrics = metrics_calculator.calculate_all_metrics(result)
    
    # Generate AI recommendations
    recommendations = await ai_recommender.generate_recommendations(result)
    
    # Display enhanced results
    _display_enhanced_summary(result, labels, summaries, metrics, recommendations)
    
    # Export summary if requested
    if export_summary:
        _export_analysis_summary(
            result, labels, summaries, metrics, recommendations, 
            export_summary, codebase_path
        )
    
    # Export diagram
    _export_enhanced_diagram(result, format, output, labels, verbose)


def _export_analysis_summary(result, labels, summaries, metrics, recommendations, format_type: str, codebase_path: str):
    """Export analysis summary in the specified format."""
    # Clean the codebase path for filename
    clean_path = codebase_path.replace('/', '_').replace('\\', '_')
    
    if format_type == "markdown":
        summary_content = _generate_markdown_summary(result, labels, summaries, metrics, recommendations, codebase_path)
        output_file = f"architex_summary_{clean_path}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(summary_content)
        console.print(f"[green]✅ Summary exported to: {output_file}[/green]")
    elif format_type == "json":
        summary_content = _generate_json_summary(result, labels, summaries, metrics, recommendations)
        output_file = f"architex_summary_{clean_path}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(summary_content)
        console.print(f"[green]✅ Summary exported to: {output_file}[/green]")
    else:
        console.print(f"[red]❌ Unsupported export format: {format_type}[/red]")


def _generate_markdown_summary(result, labels, summaries, metrics, recommendations, codebase_path: str):
    """Generate Markdown summary."""
    md_content = f"""# Architex Analysis Summary

## Codebase: {codebase_path}

### Key Metrics

| Metric | Value | Severity |
|--------|-------|----------|
"""
    
    for metric in metrics.get_all_metrics():
        severity_emoji = {
            'info': '✅',
            'warning': '⚠️',
            'error': '❌',
            'critical': '🚨'
        }.get(metric.severity, 'ℹ️')
        if isinstance(metric.value, float):
            value_str = f"{metric.value:.2f}"
        else:
            value_str = str(metric.value)
        md_content += f"| {metric.name.replace('_', ' ').title()} | {value_str} | {severity_emoji} {metric.severity.title()} |\n"
    
    if recommendations:
        md_content += "\n### AI-Powered Recommendations\n\n"
        for rec in sorted(recommendations, key=lambda r: r.priority, reverse=True)[:10]:
            priority_emoji = {
                'critical': '🚨',
                'high': '🔴',
                'medium': '🟡',
                'low': '🟢'
            }.get(rec.priority.value, '⚪')
            
            md_content += f"#### {priority_emoji} {rec.title}\n\n"
            md_content += f"**Priority:** {rec.priority.title()}\n"
            md_content += f"**Impact:** {rec.impact}\n"
            md_content += f"**Effort:** {rec.effort}\n"
            md_content += f"**Confidence:** {rec.confidence:.2f}\n\n"
            md_content += f"{rec.description}\n\n"
            
            if rec.code_examples:
                md_content += "**Code Examples:**\n"
                for example in rec.code_examples:
                    md_content += f"```\n{example}\n```\n"
            
            if rec.references:
                md_content += "**References:**\n"
                for ref in rec.references:
                    md_content += f"- {ref}\n"
            md_content += "\n---\n\n"
    
    return md_content


def _generate_json_summary(result, labels, summaries, metrics, recommendations):
    """Generate JSON summary."""
    import json
    
    summary_data = {
        "metadata": {
            "codebase_path": str(result.metadata.get('codebase_path', '')),
            "total_files": result.metadata.get('total_files', 0),
            "elements_count": len(result.elements),
            "relationships_count": len(result.relationships),
            "service_boundaries_count": len(result.service_boundaries)
        },
        "metrics": {
            metric.name: {
                "value": metric.value,
                "unit": metric.unit,
                "description": metric.description,
                "category": metric.category.value,
                "threshold": metric.threshold,
                "severity": metric.severity
            }
            for metric in metrics.get_all_metrics()
        },
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
            for rec in recommendations
        ],
        "ai_labels": {
            element_id: {
                "label": label.label,
                "category": label.category,
                "confidence": label.confidence,
                "reasoning": getattr(label, 'reasoning', '')
            }
            for element_id, label in labels.items()
        },
        "ai_summaries": {
            module_name: {
                "summary": summary.summary,
                "complexity_score": summary.complexity_score,
                "recommendations": summary.recommendations
            }
            for module_name, summary in summaries.items()
        }
    }
    
    return json.dumps(summary_data, indent=2)


async def _run_live_analysis(codebase_path: str, host: str, port: int):
    """Run live analysis with file watching."""
    
    console.print(f"[bold blue]🔄 Starting Live Analysis[/bold blue]")
    console.print(f"📁 Watching: {codebase_path}")
    console.print(f"🌐 WebSocket: ws://{host}:{port}")
    
    # Initialize live analyzer
    live_analyzer = LiveAnalyzer()
    
    # Create file watcher
    def on_analysis_update(update_data):
        console.print(f"[green]✅ Analysis updated: {update_data['metadata']['elements_count']} elements[/green]")
    
    watcher = FileWatcher(codebase_path, on_analysis_update)
    
    # Start file watcher
    watcher.start()
    
    # Perform initial analysis
    console.print("🔍 Performing initial analysis...")
    await live_analyzer.analyze_codebase(codebase_path)
    
    # Start WebSocket server
    try:
        from ..watcher.websocket_server import WebSocketServer
        ws_server = WebSocketServer(host, port)
        
        console.print("[green]✅ Live analysis started![/green]")
        console.print("💡 Connect to the WebSocket server for real-time updates")
        console.print("🛑 Press Ctrl+C to stop")
        
        await ws_server.start()
        
    except ImportError:
        console.print("[yellow]⚠ WebSocket server not available[/yellow]")
        console.print("💡 Install websockets package for full live features")
        
        # Keep the file watcher running
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            watcher.stop()
            console.print("\n[green]✅ Live analysis stopped[/green]")


def _display_enhanced_summary(result, labels, summaries, metrics, recommendations):
    """Display enhanced analysis summary with AI features, metrics, and recommendations."""
    console.print("\n[bold green]Enhanced Analysis Summary[/bold green]")
    
    # Metrics Table
    metrics_table = Table(title="Key Metrics")
    metrics_table.add_column("Metric", style="cyan")
    metrics_table.add_column("Value", style="green")
    metrics_table.add_column("Severity", style="magenta")
    for metric in metrics.get_all_metrics():
        sev_style = {
            'info': 'green',
            'warning': 'yellow',
            'error': 'red',
            'critical': 'bold red'
        }.get(metric.severity, 'white')
        metrics_table.add_row(
            metric.name.replace('_', ' ').title(),
            f"{metric.value:.2f}" if isinstance(metric.value, float) else str(metric.value),
            f"[{sev_style}]{metric.severity.title()}[/{sev_style}]"
        )
    console.print(metrics_table)
    
    # AI Recommendations
    if recommendations:
        console.print("\n[bold blue]AI-Powered Architectural Recommendations[/bold blue]")
        rec_table = Table()
        rec_table.add_column("Priority", style="magenta")
        rec_table.add_column("Title", style="cyan")
        rec_table.add_column("Impact", style="yellow")
        rec_table.add_column("Confidence", style="blue")
        for rec in sorted(recommendations, key=lambda r: r.priority, reverse=True)[:10]:
            prio_style = {
                'critical': 'bold red',
                'high': 'red',
                'medium': 'yellow',
                'low': 'green'
            }.get(rec.priority.value, 'white')
            rec_table.add_row(
                f"[{prio_style}]{rec.priority.title()}[/{prio_style}]",
                rec.title,
                rec.impact,
                f"{rec.confidence:.2f}"
            )
        console.print(rec_table)
    
    # AI Labels summary
    if labels:
        console.print("\n[bold]🤖 AI-Generated Labels[/bold]")
        labels_table = Table()
        labels_table.add_column("Element", style="cyan")
        labels_table.add_column("Label", style="green")
        labels_table.add_column("Category", style="yellow")
        labels_table.add_column("Confidence", style="blue")
        for element_id, label in list(labels.items())[:10]:  # Show first 10
            element = result.get_element_by_id(element_id)
            if element:
                labels_table.add_row(
                    element.name,
                    label.label,
                    label.category,
                    f"{label.confidence:.2f}"
                )
        console.print(labels_table)
    
    # AI Summaries summary
    if summaries:
        console.print("\n[bold]📝 AI-Generated Summaries[/bold]")
        for module_name, summary in summaries.items():
            console.print(f"\n[cyan]{module_name}[/cyan]")
            console.print(f"  {summary.summary}")
            console.print(f"  Complexity: {summary.complexity_score:.2f}")
            if summary.recommendations:
                console.print(f"  Recommendations: {', '.join(summary.recommendations[:2])}")


def _export_enhanced_diagram(result, format: str, output_path: Optional[Path], labels, verbose: bool):
    """Export enhanced diagram with AI labels."""
    # Select exporter
    exporters = {
        'mermaid': MermaidExporter(),
        'plantuml': PlantUMLExporter(),
        'graphviz': GraphvizExporter()
    }
    
    exporter = exporters.get(format.lower())
    if not exporter:
        console.print(f"[red]Unsupported format: {format}[/red]")
        console.print("Use 'architex formats' to see supported formats")
        sys.exit(1)
    
    # Generate diagram
    try:
        diagram_content = exporter.export(result, output_path)
        
        # Write to file or stdout
        if output_path:
            output_path.write_text(diagram_content)
            console.print(f"[green]Enhanced diagram saved to: {output_path}[/green]")
        else:
            console.print("\n[bold]Generated Enhanced Diagram:[/bold]")
            console.print(diagram_content)
            
    except Exception as e:
        console.print(f"[red]Error generating enhanced diagram: {e}[/red]")
        sys.exit(1)


def main():
    """Main entry point."""
    app()


if __name__ == "__main__":
    main() 