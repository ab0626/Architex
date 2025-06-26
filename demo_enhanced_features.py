#!/usr/bin/env python3
"""
Enhanced Architex Demo - Showcasing AI and Live Features
"""

import asyncio
import sys
import time
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.live import Live
from rich.layout import Layout

# Add the architex package to the path
sys.path.insert(0, str(Path(__file__).parent))

console = Console()


def demo_ai_features():
    """Demo AI-powered features."""
    console.print(Panel.fit(
        "[bold blue]🤖 AI-Powered Features Demo[/bold blue]\n\n"
        "This demo showcases the intelligent analysis capabilities:\n"
        "• Smart component labeling with GPT-4/Claude\n"
        "• Natural language module summaries\n"
        "• AI-driven service boundary detection\n"
        "• Confidence scoring and reasoning\n\n"
        "Press Enter to continue...",
        title="AI Features"
    ))
    input()
    
    try:
        from architex.ai.labeler import AILabeler
        from architex.ai.summarizer import AISummarizer
        from architex.core.analyzer import CodebaseAnalyzer
        
        # Initialize components
        analyzer = CodebaseAnalyzer()
        labeler = AILabeler()
        summarizer = AISummarizer()
        
        # Analyze example project
        example_path = Path(__file__).parent / "examples" / "simple_python_project"
        
        if not example_path.exists():
            console.print(f"[red]Example project not found: {example_path}[/red]")
            return
        
        console.print(f"🔍 Analyzing: {example_path}")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            # Core analysis
            task = progress.add_task("Performing core analysis...", total=None)
            result = analyzer.analyze(example_path)
            progress.update(task, description="Core analysis complete!")
            
            # AI labeling
            task = progress.add_task("Generating AI labels...", total=None)
            labels = asyncio.run(labeler.label_analysis_result(result))
            progress.update(task, description="AI labeling complete!")
            
            # AI summaries
            task = progress.add_task("Generating AI summaries...", total=None)
            summaries = asyncio.run(summarizer.summarize_analysis_result(result))
            progress.update(task, description="AI summarization complete!")
        
        # Display results
        console.print("\n[bold green]✅ AI Analysis Results[/bold green]")
        
        # Show AI labels
        if labels:
            console.print("\n[bold]🤖 AI-Generated Labels:[/bold]")
            labels_table = Table()
            labels_table.add_column("Component", style="cyan")
            labels_table.add_column("AI Label", style="green")
            labels_table.add_column("Category", style="yellow")
            labels_table.add_column("Confidence", style="blue")
            
            for element_id, label in list(labels.items())[:5]:
                element = result.get_element_by_id(element_id)
                if element:
                    labels_table.add_row(
                        element.name,
                        label.label,
                        label.category,
                        f"{label.confidence:.2f}"
                    )
            
            console.print(labels_table)
        
        # Show AI summaries
        if summaries:
            console.print("\n[bold]📝 AI-Generated Summaries:[/bold]")
            for module_name, summary in summaries.items():
                console.print(f"\n[cyan]{module_name}[/cyan]")
                console.print(f"  {summary.summary}")
                console.print(f"  Complexity: {summary.complexity_score:.2f}")
                if summary.recommendations:
                    console.print(f"  💡 {summary.recommendations[0]}")
        
    except Exception as e:
        console.print(f"[red]Error in AI demo: {e}[/red]")


def demo_live_features():
    """Demo live analysis features."""
    console.print(Panel.fit(
        "[bold blue]🔄 Live Analysis Features Demo[/bold blue]\n\n"
        "This demo showcases real-time analysis capabilities:\n"
        "• File watching with Watchdog\n"
        "• WebSocket real-time communication\n"
        "• Live diagram updates\n"
        "• Incremental analysis\n\n"
        "Press Enter to continue...",
        title="Live Features"
    ))
    input()
    
    try:
        from architex.watcher.live_analyzer import LiveAnalyzer
        
        # Initialize live analyzer
        live_analyzer = LiveAnalyzer()
        
        # Demo callback function
        def on_analysis_update(update_data):
            console.print(f"[green]🔄 Live Update: {update_data['metadata']['elements_count']} elements[/green]")
        
        live_analyzer.add_callback(on_analysis_update)
        
        # Analyze example project
        example_path = Path(__file__).parent / "examples" / "simple_python_project"
        
        if not example_path.exists():
            console.print(f"[red]Example project not found: {example_path}[/red]")
            return
        
        console.print(f"🔍 Starting live analysis: {example_path}")
        
        # Perform analysis
        result = asyncio.run(live_analyzer.analyze_codebase(str(example_path)))
        
        console.print(f"[green]✅ Live analysis complete![/green]")
        console.print(f"📊 Elements: {result['metadata']['elements_count']}")
        console.print(f"🔗 Relationships: {result['metadata']['relationships_count']}")
        console.print(f"🏗️ Service Boundaries: {result['metadata']['service_boundaries_count']}")
        
        # Show supported formats
        formats = live_analyzer.get_supported_formats()
        console.print(f"🎨 Supported formats: {', '.join(formats)}")
        
    except Exception as e:
        console.print(f"[red]Error in live demo: {e}[/red]")


def demo_enhanced_visualization():
    """Demo enhanced visualization features."""
    console.print(Panel.fit(
        "[bold blue]🎨 Enhanced Visualization Demo[/bold blue]\n\n"
        "This demo showcases advanced visualization capabilities:\n"
        "• Multiple export formats\n"
        "• AI-enhanced diagrams\n"
        "• Interactive features\n"
        "• Custom styling\n\n"
        "Press Enter to continue...",
        title="Visualization"
    ))
    input()
    
    try:
        from architex.core.analyzer import CodebaseAnalyzer
        from architex.exporters import MermaidExporter, PlantUMLExporter, GraphvizExporter
        
        # Initialize components
        analyzer = CodebaseAnalyzer()
        
        # Analyze example project
        example_path = Path(__file__).parent / "examples" / "simple_python_project"
        
        if not example_path.exists():
            console.print(f"[red]Example project not found: {example_path}[/red]")
            return
        
        console.print(f"🔍 Analyzing for visualization: {example_path}")
        result = analyzer.analyze(example_path)
        
        # Test different exporters
        exporters = {
            'Mermaid': MermaidExporter(),
            'PlantUML': PlantUMLExporter(),
            'Graphviz': GraphvizExporter()
        }
        
        console.print("\n[bold]🎨 Generating Diagrams:[/bold]")
        
        for name, exporter in exporters.items():
            try:
                console.print(f"  📝 Generating {name} diagram...")
                diagram = exporter.export(result)
                
                # Save to file
                output_file = Path(f"demo_{name.lower()}.txt")
                output_file.write_text(diagram)
                console.print(f"  ✅ Saved to: {output_file}")
                
                # Show preview
                lines = diagram.split('\n')
                console.print(f"  📄 Preview (first 3 lines):")
                for i, line in enumerate(lines[:3]):
                    console.print(f"    {i+1}: {line}")
                if len(lines) > 3:
                    console.print(f"    ... ({len(lines) - 3} more lines)")
                console.print()
                
            except Exception as e:
                console.print(f"  ❌ Error generating {name}: {e}")
        
    except Exception as e:
        console.print(f"[red]Error in visualization demo: {e}[/red]")


def demo_configuration():
    """Demo configuration management."""
    console.print(Panel.fit(
        "[bold blue]⚙️ Configuration Management Demo[/bold blue]\n\n"
        "This demo showcases the comprehensive configuration system:\n"
        "• YAML-based configuration\n"
        "• AI model settings\n"
        "• Live analysis options\n"
        "• Performance tuning\n\n"
        "Press Enter to continue...",
        title="Configuration"
    ))
    input()
    
    try:
        import yaml
        
        # Load configuration
        config_file = Path(__file__).parent / "config.yaml"
        
        if config_file.exists():
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f)
            
            console.print("\n[bold]📋 Configuration Overview:[/bold]")
            
            # Show AI configuration
            if 'ai' in config:
                ai_config = config['ai']
                console.print(f"\n[cyan]🤖 AI Configuration:[/cyan]")
                console.print(f"  Enabled: {ai_config.get('enabled', False)}")
                console.print(f"  Provider: {ai_config.get('llm', {}).get('provider', 'unknown')}")
                console.print(f"  Model: {ai_config.get('llm', {}).get('models', {}).get('openai', 'unknown')}")
            
            # Show live configuration
            if 'live' in config:
                live_config = config['live']
                console.print(f"\n[cyan]🔄 Live Configuration:[/cyan]")
                console.print(f"  File Watching: {live_config.get('file_watching', {}).get('enabled', False)}")
                console.print(f"  WebSocket: {live_config.get('websocket', {}).get('enabled', False)}")
                console.print(f"  Port: {live_config.get('websocket', {}).get('port', 'unknown')}")
            
            # Show export configuration
            if 'export' in config:
                export_config = config['export']
                console.print(f"\n[cyan]🎨 Export Configuration:[/cyan]")
                console.print(f"  Default Format: {export_config.get('default_format', 'unknown')}")
                console.print(f"  Include AI Labels: {export_config.get('output', {}).get('include_ai_labels', False)}")
            
        else:
            console.print("[yellow]⚠ Configuration file not found[/yellow]")
        
    except Exception as e:
        console.print(f"[red]Error in configuration demo: {e}[/red]")


def demo_performance():
    """Demo performance features."""
    console.print(Panel.fit(
        "[bold blue]⚡ Performance Features Demo[/bold blue]\n\n"
        "This demo showcases performance optimizations:\n"
        "• Parallel processing\n"
        "• Intelligent caching\n"
        "• Memory management\n"
        "• Incremental analysis\n\n"
        "Press Enter to continue...",
        title="Performance"
    ))
    input()
    
    try:
        from architex.core.analyzer import CodebaseAnalyzer
        import time
        
        # Initialize analyzer
        analyzer = CodebaseAnalyzer()
        
        # Analyze example project with timing
        example_path = Path(__file__).parent / "examples" / "simple_python_project"
        
        if not example_path.exists():
            console.print(f"[red]Example project not found: {example_path}[/red]")
            return
        
        console.print(f"⏱️ Performance test: {example_path}")
        
        # Time the analysis
        start_time = time.time()
        result = analyzer.analyze(example_path)
        end_time = time.time()
        
        analysis_time = end_time - start_time
        
        console.print(f"\n[bold]📊 Performance Results:[/bold]")
        console.print(f"  ⏱️ Analysis Time: {analysis_time:.2f} seconds")
        console.print(f"  📁 Files Analyzed: {result.metadata.get('total_files', 0)}")
        console.print(f"  🔧 Elements Found: {len(result.elements)}")
        console.print(f"  🔗 Relationships: {len(result.relationships)}")
        
        # Calculate performance metrics
        if result.metadata.get('total_files', 0) > 0:
            files_per_second = result.metadata['total_files'] / analysis_time
            console.print(f"  🚀 Files/Second: {files_per_second:.2f}")
        
        if len(result.elements) > 0:
            elements_per_second = len(result.elements) / analysis_time
            console.print(f"  🚀 Elements/Second: {elements_per_second:.2f}")
        
        # Show metrics
        console.print(f"\n[bold]📈 Analysis Metrics:[/bold]")
        for key, value in result.metrics.items():
            if isinstance(value, float):
                console.print(f"  {key.replace('_', ' ').title()}: {value:.2f}")
            else:
                console.print(f"  {key.replace('_', ' ').title()}: {value}")
        
    except Exception as e:
        console.print(f"[red]Error in performance demo: {e}[/red]")


def main():
    """Main demo function."""
    console.print(Panel.fit(
        "[bold blue]🚀 Architex Enhanced Features Demo[/bold blue]\n\n"
        "Welcome to the comprehensive demo of Architex's advanced features!\n\n"
        "This demo will showcase:\n"
        "• 🤖 AI-powered analysis and labeling\n"
        "• 🔄 Live real-time analysis\n"
        "• 🎨 Enhanced visualization\n"
        "• ⚙️ Configuration management\n"
        "• ⚡ Performance optimizations\n\n"
        "Press Enter to start the demo...",
        title="Architex Enhanced Demo"
    ))
    input()
    
    # Run all demos
    demos = [
        ("AI Features", demo_ai_features),
        ("Live Analysis", demo_live_features),
        ("Enhanced Visualization", demo_enhanced_visualization),
        ("Configuration Management", demo_configuration),
        ("Performance Features", demo_performance)
    ]
    
    for name, demo_func in demos:
        console.print(f"\n{'='*60}")
        console.print(f"[bold blue]🎯 {name} Demo[/bold blue]")
        console.print(f"{'='*60}")
        
        try:
            demo_func()
        except KeyboardInterrupt:
            console.print("\n[yellow]Demo interrupted by user[/yellow]")
            break
        except Exception as e:
            console.print(f"\n[red]Error in {name} demo: {e}[/red]")
        
        console.print(f"\n[green]✅ {name} demo completed![/green]")
        input("Press Enter to continue to next demo...")
    
    console.print(Panel.fit(
        "[bold green]🎉 Demo Completed![/bold green]\n\n"
        "You've seen all the advanced features of Architex:\n\n"
        "• 🤖 AI-powered intelligent analysis\n"
        "• 🔄 Real-time live updates\n"
        "• 🎨 Beautiful visualizations\n"
        "• ⚙️ Comprehensive configuration\n"
        "• ⚡ High-performance processing\n\n"
        "Ready to use Architex in your projects!\n\n"
        "📚 Next steps:\n"
        "• Install: pip install -e .\n"
        "• Try: architex analyze /path/to/project --ai-labels\n"
        "• Live: architex watch /path/to/project\n"
        "• Config: Copy config.yaml and customize",
        title="Demo Complete"
    ))


if __name__ == "__main__":
    main() 