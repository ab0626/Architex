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
    app()


if __name__ == "__main__":
    main() 