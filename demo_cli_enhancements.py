#!/usr/bin/env python3
"""
Demo script showcasing Architex CLI enhancements:
- Metrics calculation and display
- AI-powered architectural recommendations
- Summary export functionality
"""

import asyncio
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent))

from architex.core.analyzer import CodebaseAnalyzer
from architex.core.metrics import MetricsCalculator
from architex.ai.recommendations import AIRecommendations
from architex.ai.labeler import AILabeler
from architex.ai.summarizer import AISummarizer

console = Console()


async def demo_enhanced_cli():
    """Demonstrate the enhanced CLI features."""
    
    console.print(Panel.fit(
        "[bold blue]🚀 Architex Enhanced CLI Demo[/bold blue]\n\n"
        "This demo showcases the new CLI enhancements:\n"
        "• Comprehensive metrics calculation\n"
        "• AI-powered architectural recommendations\n"
        "• Enhanced summary display with color coding\n"
        "• Export functionality (Markdown/JSON)\n\n"
        "Using the example project for demonstration...",
        title="Enhanced CLI Features"
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
    
    # Perform analysis
    console.print(f"\n[bold blue]🔍 Analyzing: {codebase_path}[/bold blue]")
    
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
            return
    
    # Calculate metrics
    console.print("\n[bold green]📊 Calculating Metrics...[/bold green]")
    metrics = metrics_calculator.calculate_all_metrics(result)
    
    # Generate AI features
    console.print("\n[bold green]🤖 Generating AI Features...[/bold green]")
    
    labels = {}
    summaries = {}
    recommendations = []
    
    try:
        labels = await labeler.label_analysis_result(result)
        console.print("✅ AI labels generated")
    except Exception as e:
        console.print(f"[yellow]⚠ AI labeling failed: {e}[/yellow]")
    
    try:
        summaries = await summarizer.summarize_analysis_result(result)
        console.print("✅ AI summaries generated")
    except Exception as e:
        console.print(f"[yellow]⚠ AI summarization failed: {e}[/yellow]")
    
    try:
        recommendations = await ai_recommender.generate_recommendations(result)
        console.print("✅ AI recommendations generated")
    except Exception as e:
        console.print(f"[yellow]⚠ AI recommendations failed: {e}[/yellow]")
    
    # Display enhanced summary
    console.print("\n" + "="*80)
    console.print("[bold green]Enhanced Analysis Summary[/bold green]")
    console.print("="*80)
    
    # Metrics Table
    metrics_table = Table(title="📊 Key Metrics")
    metrics_table.add_column("Metric", style="cyan", width=30)
    metrics_table.add_column("Value", style="green", width=15)
    metrics_table.add_column("Unit", style="blue", width=10)
    metrics_table.add_column("Severity", style="magenta", width=12)
    
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
            metric.unit,
            f"[{sev_style}]{metric.severity.title()}[/{sev_style}]"
        )
    
    console.print(metrics_table)
    
    # AI Recommendations
    if recommendations:
        console.print("\n[bold blue]🎯 AI-Powered Architectural Recommendations[/bold blue]")
        rec_table = Table()
        rec_table.add_column("Priority", style="magenta", width=10)
        rec_table.add_column("Title", style="cyan", width=40)
        rec_table.add_column("Impact", style="yellow", width=20)
        rec_table.add_column("Confidence", style="blue", width=12)
        
        for rec in sorted(recommendations, key=lambda r: r.priority, reverse=True)[:5]:
            prio_style = {
                'critical': 'bold red',
                'high': 'red',
                'medium': 'yellow',
                'low': 'green'
            }.get(rec.priority.value, 'white')
            
            rec_table.add_row(
                f"[{prio_style}]{rec.priority.title()}[/{prio_style}]",
                rec.title[:37] + "..." if len(rec.title) > 40 else rec.title,
                rec.impact[:17] + "..." if len(rec.impact) > 20 else rec.impact,
                f"{rec.confidence:.2f}"
            )
        
        console.print(rec_table)
        
        # Show detailed recommendation
        if recommendations:
            top_rec = recommendations[0]
            console.print(f"\n[bold]Top Recommendation: {top_rec.title}[/bold]")
            console.print(f"[dim]{top_rec.description}[/dim]")
            console.print(f"Impact: {top_rec.impact} | Effort: {top_rec.effort}")
    
    # AI Labels summary
    if labels:
        console.print("\n[bold]🤖 AI-Generated Labels[/bold]")
        labels_table = Table()
        labels_table.add_column("Element", style="cyan", width=25)
        labels_table.add_column("Label", style="green", width=25)
        labels_table.add_column("Category", style="yellow", width=15)
        labels_table.add_column("Confidence", style="blue", width=12)
        
        for element_id, label in list(labels.items())[:5]:
            element = result.get_element_by_id(element_id)
            if element:
                labels_table.add_row(
                    element.name[:22] + "..." if len(element.name) > 25 else element.name,
                    label.label[:22] + "..." if len(label.label) > 25 else label.label,
                    label.category,
                    f"{label.confidence:.2f}"
                )
        
        console.print(labels_table)
    
    # AI Summaries summary
    if summaries:
        console.print("\n[bold]📝 AI-Generated Summaries[/bold]")
        for module_name, summary in list(summaries.items())[:3]:
            console.print(f"\n[cyan]{module_name}[/cyan]")
            console.print(f"  {summary.summary[:100]}...")
            console.print(f"  Complexity: {summary.complexity_score:.2f}")
    
    # Export demo
    console.print("\n" + "="*80)
    console.print("[bold blue]📤 Export Functionality Demo[/bold blue]")
    console.print("="*80)
    
    # Generate and save Markdown summary
    try:
        from architex.cli.enhanced_main import _generate_markdown_summary, _generate_json_summary
        
        md_content = _generate_markdown_summary(result, labels, summaries, metrics, recommendations, codebase_path)
        md_path = Path("demo_analysis_summary.md")
        md_path.write_text(md_content)
        console.print(f"[green]✅ Markdown summary exported to: {md_path}[/green]")
        
        json_content = _generate_json_summary(result, labels, summaries, metrics, recommendations)
        json_path = Path("demo_analysis_summary.json")
        json_path.write_text(json_content)
        console.print(f"[green]✅ JSON summary exported to: {json_path}[/green]")
        
    except Exception as e:
        console.print(f"[yellow]⚠ Export demo failed: {e}[/yellow]")
    
    # CLI Usage examples
    console.print("\n" + "="*80)
    console.print("[bold blue]💡 CLI Usage Examples[/bold blue]")
    console.print("="*80)
    
    usage_examples = [
        ("Basic analysis with AI features", "architex analyze examples/simple_python_project"),
        ("Export summary as Markdown", "architex analyze examples/simple_python_project --export-summary markdown"),
        ("Export summary as JSON", "architex analyze examples/simple_python_project --export-summary json"),
        ("Disable AI features", "architex analyze examples/simple_python_project --no-ai-labels --no-ai-summaries"),
        ("Generate Mermaid diagram", "architex analyze examples/simple_python_project --format mermaid --output diagram.md"),
        ("Live analysis with WebSocket", "architex watch examples/simple_python_project --port 8765"),
    ]
    
    for description, command in usage_examples:
        console.print(f"[cyan]{description}:[/cyan]")
        console.print(f"  [dim]{command}[/dim]\n")
    
    console.print(Panel.fit(
        "[bold green]🎉 Enhanced CLI Demo Complete![/bold green]\n\n"
        "The enhanced CLI now provides:\n"
        "• Comprehensive code quality metrics\n"
        "• AI-powered architectural insights\n"
        "• Actionable recommendations\n"
        "• Rich export capabilities\n"
        "• Color-coded severity indicators\n\n"
        "Try running the CLI commands above to explore your own codebases!",
        title="Demo Complete"
    ))


if __name__ == "__main__":
    asyncio.run(demo_enhanced_cli()) 