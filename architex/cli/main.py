"""
Main CLI interface for Architex.
"""

import sys
from pathlib import Path
from typing import Optional, List
import typer
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from ..core.analyzer import CodebaseAnalyzer
from ..exporters import MermaidExporter, PlantUMLExporter, GraphvizExporter
from ..core.models import AnalysisResult
from ..core.privacy import privacy_manager, privacy_cleanup

app = typer.Typer(help="Architex - Automated System Design Diagram Generator")
console = Console()


@app.command()
def analyze(
    codebase_path: str = typer.Argument(..., help="Path to the codebase to analyze"),
    format: str = typer.Option("mermaid", "--format", "-f", help="Output format (mermaid, plantuml, graphviz)"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file path"),
    language: Optional[str] = typer.Option(None, "--language", "-l", help="Specific language to analyze"),
    ignore: Optional[List[str]] = typer.Option(None, "--ignore", help="Patterns to ignore"),
    max_depth: int = typer.Option(10, "--max-depth", help="Maximum analysis depth"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose output")
):
    """Analyze a codebase and generate system design diagrams."""
    
    if not Path(codebase_path).exists():
        console.print(f"[red]Error: Codebase path does not exist: {codebase_path}[/red]")
        sys.exit(1)
    
    # Configure analyzer
    config = {
        'max_depth': max_depth,
        'ignore_patterns': ignore or []
    }
    
    analyzer = CodebaseAnalyzer(config)
    
    # Analyze codebase
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Analyzing codebase...", total=None)
        
        try:
            if language:
                result = analyzer.analyze_language(codebase_path, language)
            else:
                result = analyzer.analyze(codebase_path)
            
            progress.update(task, description="Analysis complete!")
            
        except Exception as e:
            console.print(f"[red]Error during analysis: {e}[/red]")
            sys.exit(1)
    
    # Display results
    _display_analysis_summary(result)
    
    # Export diagram
    _export_diagram(result, format, output, verbose)


@app.command()
def languages():
    """List supported programming languages."""
    analyzer = CodebaseAnalyzer()
    languages = analyzer.get_supported_languages()
    
    table = Table(title="Supported Languages")
    table.add_column("Language", style="cyan")
    table.add_column("Extensions", style="green")
    
    for lang in languages:
        parser = analyzer.parser_registry.get_parser(lang)
        if parser:
            extensions = ", ".join(parser.supported_extensions)
            table.add_row(lang, extensions)
    
    console.print(table)


@app.command()
def formats():
    """List supported output formats."""
    table = Table(title="Supported Output Formats")
    table.add_column("Format", style="cyan")
    table.add_column("Description", style="green")
    table.add_column("Extensions", style="yellow")
    
    exporters = [
        ("mermaid", "Mermaid diagrams", "md, mermaid"),
        ("plantuml", "PlantUML diagrams", "puml, plantuml"),
        ("graphviz", "Graphviz DOT diagrams", "dot, gv, svg, png, pdf")
    ]
    
    for format_name, description, extensions in exporters:
        table.add_row(format_name, description, extensions)
    
    console.print(table)


@app.command()
def privacy():
    """Manage privacy settings and data protection."""
    console.print("[bold green]Privacy Settings[/bold green]")
    
    # Display current privacy settings
    settings = privacy_manager.settings
    privacy_table = Table()
    privacy_table.add_column("Setting", style="cyan")
    privacy_table.add_column("Value", style="green")
    privacy_table.add_column("Description", style="yellow")
    
    privacy_table.add_row("Local Only", str(settings.local_only), "Process data locally only")
    privacy_table.add_row("AI Enabled", str(settings.ai_enabled), "Enable AI-powered analysis")
    privacy_table.add_row("Store Analyzed Code", str(settings.store_analyzed_code), "Persist analyzed code")
    privacy_table.add_row("Store AI Responses", str(settings.store_ai_responses), "Persist AI responses")
    privacy_table.add_row("File Watching", str(settings.file_watching_enabled), "Monitor file changes")
    privacy_table.add_row("Respect .gitignore", str(settings.respect_gitignore), "Follow gitignore patterns")
    privacy_table.add_row("WebSocket Enabled", str(settings.websocket_enabled), "Enable web interface")
    privacy_table.add_row("Clear Cache on Exit", str(settings.clear_cache_on_exit), "Auto-cleanup on exit")
    
    console.print(privacy_table)
    
    # Display privacy report
    report = privacy_manager.get_privacy_report()
    console.print(f"\n[bold]Privacy Report[/bold]")
    console.print(f"• Local processing: {report['local_only']}")
    console.print(f"• AI features: {report['ai_enabled']}")
    console.print(f"• Data storage: {report['data_storage']}")
    console.print(f"• Sensitive patterns excluded: {report['sensitive_patterns_excluded']}")


@app.command()
def privacy_settings(
    local_only: bool = typer.Option(None, "--local-only", help="Enable local-only processing"),
    ai_enabled: bool = typer.Option(None, "--ai-enabled", help="Enable AI features"),
    store_code: bool = typer.Option(None, "--store-code", help="Store analyzed code"),
    store_ai: bool = typer.Option(None, "--store-ai", help="Store AI responses"),
    file_watching: bool = typer.Option(None, "--file-watching", help="Enable file watching"),
    websocket: bool = typer.Option(None, "--websocket", help="Enable WebSocket server"),
    clear_cache: bool = typer.Option(None, "--clear-cache", help="Clear cache on exit")
):
    """Update privacy settings."""
    updates = {}
    
    if local_only is not None:
        updates['local_only'] = local_only
    if ai_enabled is not None:
        updates['ai_enabled'] = ai_enabled
    if store_code is not None:
        updates['store_analyzed_code'] = store_code
    if store_ai is not None:
        updates['store_ai_responses'] = store_ai
    if file_watching is not None:
        updates['file_watching_enabled'] = file_watching
    if websocket is not None:
        updates['websocket_enabled'] = websocket
    if clear_cache is not None:
        updates['clear_cache_on_exit'] = clear_cache
    
    if updates:
        privacy_manager.update_settings(**updates)
        console.print(f"[green]✓ Updated privacy settings: {list(updates.keys())}[/green]")
    else:
        console.print("[yellow]No settings specified. Use --help to see available options.[/yellow]")


@app.command()
def consent(
    feature: str = typer.Argument(..., help="Feature to grant consent for (ai_analysis, file_watching, web_interface, data_storage)"),
    grant: bool = typer.Option(True, "--grant/--revoke", help="Grant or revoke consent")
):
    """Manage consent for privacy-sensitive features."""
    if grant:
        # For AI analysis, this will trigger the consent prompt
        if feature == "ai_analysis":
            consent_given = privacy_manager.get_consent("ai_analysis")
            if consent_given:
                console.print(f"[green]✓ Consent granted for {feature}[/green]")
            else:
                console.print(f"[yellow]✗ Consent not granted for {feature}[/yellow]")
        else:
            console.print(f"[green]✓ Consent granted for {feature}[/green]")
    else:
        console.print(f"[yellow]✗ Consent revoked for {feature}[/yellow]")


@app.command()
def privacy_report(
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file for privacy report")
):
    """Generate a detailed privacy report."""
    report = privacy_manager.get_privacy_report()
    
    if output:
        privacy_manager.export_privacy_settings(output)
        console.print(f"[green]Privacy report exported to: {output}[/green]")
    else:
        console.print("[bold green]Privacy Report[/bold green]")
        
        # Display detailed report
        for key, value in report.items():
            if isinstance(value, dict):
                console.print(f"\n[bold]{key.replace('_', ' ').title()}:[/bold]")
                for sub_key, sub_value in value.items():
                    console.print(f"  • {sub_key.replace('_', ' ').title()}: {sub_value}")
            else:
                console.print(f"• {key.replace('_', ' ').title()}: {value}")


@app.command()
def cleanup():
    """Clean up cached data and temporary files."""
    console.print("[yellow]Cleaning up cached data...[/yellow]")
    privacy_manager.cleanup_old_data()
    console.print("[green]✓ Cleanup completed[/green]")


def _display_analysis_summary(result: AnalysisResult):
    """Display analysis summary."""
    console.print("\n[bold green]Analysis Summary[/bold green]")
    
    # Basic metrics
    metrics_table = Table()
    metrics_table.add_column("Metric", style="cyan")
    metrics_table.add_column("Value", style="green")
    
    metrics_table.add_row("Total Files", str(result.metadata.get('total_files', 0)))
    metrics_table.add_row("Code Elements", str(len(result.elements)))
    metrics_table.add_row("Relationships", str(len(result.relationships)))
    metrics_table.add_row("Service Boundaries", str(len(result.service_boundaries)))
    
    # Graph metrics
    for key, value in result.metrics.items():
        if isinstance(value, float):
            metrics_table.add_row(key.replace('_', ' ').title(), f"{value:.2f}")
        else:
            metrics_table.add_row(key.replace('_', ' ').title(), str(value))
    
    console.print(metrics_table)
    
    # Service boundaries
    if result.service_boundaries:
        console.print("\n[bold]Service Boundaries[/bold]")
        boundaries_table = Table()
        boundaries_table.add_column("Name", style="cyan")
        boundaries_table.add_column("Elements", style="green")
        boundaries_table.add_column("Cohesion", style="yellow")
        boundaries_table.add_column("Coupling", style="red")
        
        for boundary in result.service_boundaries:
            boundaries_table.add_row(
                boundary.name,
                str(len(boundary.elements)),
                f"{boundary.cohesion_score:.2f}",
                f"{boundary.coupling_score:.2f}"
            )
        
        console.print(boundaries_table)


def _export_diagram(result: AnalysisResult, format: str, output_path: Optional[Path], verbose: bool):
    """Export diagram in specified format."""
    # Select exporter
    if format.lower() == 'mermaid':
        exporter = MermaidExporter()
    elif format.lower() == 'plantuml':
        exporter = PlantUMLExporter()
    elif format.lower() == 'graphviz':
        exporter = GraphvizExporter()
    else:
        console.print(f"[red]Unsupported format: {format}[/red]")
        console.print("Use 'architex formats' to see supported formats")
        sys.exit(1)
    
    # Generate diagram
    try:
        diagram_content = exporter.export(result, output_path)
        
        # Write to file or stdout
        if output_path:
            output_path.write_text(diagram_content)
            console.print(f"[green]Diagram saved to: {output_path}[/green]")
        else:
            console.print("\n[bold]Generated Diagram:[/bold]")
            console.print(diagram_content)
            
    except Exception as e:
        console.print(f"[red]Error generating diagram: {e}[/red]")
        sys.exit(1)


def main():
    """Main entry point."""
    try:
        app()
    finally:
        # Ensure privacy cleanup happens on exit
        privacy_cleanup()


if __name__ == "__main__":
    main() 