#!/usr/bin/env python3
"""
Demo asset creation script for Architex VS Code extension.
Creates screenshots and provides guidance for video demos.
"""

import os
import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

console = Console()


def create_demo_plan():
    """Create a comprehensive demo plan for the extension."""
    
    console.print(Panel.fit(
        "[bold blue]🎬 Architex Extension Demo Assets Plan[/bold blue]",
        border_style="blue"
    ))
    
    # Demo scenarios
    scenarios = [
        {
            "title": "📊 Initial Analysis",
            "description": "Show the extension analyzing a codebase for the first time",
            "steps": [
                "Open VS Code with a Python/JavaScript project",
                "Show the Architex sidebar (empty state)",
                "Run 'Architex: Analyze Current Workspace'",
                "Show progress indicators and analysis",
                "Display the results in the Architecture view"
            ],
            "duration": "30-45 seconds"
        },
        {
            "title": "🏗️ Architecture Visualization",
            "description": "Demonstrate the generated architecture diagrams",
            "steps": [
                "Show the Architecture view with components",
                "Highlight different element types (modules, classes, functions)",
                "Show relationship lines and dependencies",
                "Demonstrate zoom and pan functionality",
                "Show different diagram layouts"
            ],
            "duration": "45-60 seconds"
        },
        {
            "title": "📈 Metrics Dashboard",
            "description": "Show code quality metrics and insights",
            "steps": [
                "Open the Metrics view",
                "Show complexity metrics with color coding",
                "Display coupling and cohesion scores",
                "Show maintainability indicators",
                "Highlight areas needing attention"
            ],
            "duration": "30-45 seconds"
        },
        {
            "title": "🤖 AI-Powered Recommendations",
            "description": "Demonstrate AI-generated insights and suggestions",
            "steps": [
                "Open the AI Recommendations view",
                "Show component labeling and categorization",
                "Display code summarization",
                "Show architectural recommendations",
                "Highlight confidence scores"
            ],
            "duration": "45-60 seconds"
        },
        {
            "title": "🔄 Live Analysis",
            "description": "Show real-time analysis as you code",
            "steps": [
                "Start live analysis mode",
                "Make changes to code files",
                "Show real-time updates in the sidebar",
                "Demonstrate file watching capabilities",
                "Show incremental analysis"
            ],
            "duration": "60-90 seconds"
        },
        {
            "title": "📤 Export & Share",
            "description": "Show export capabilities and sharing options",
            "steps": [
                "Export diagram as Mermaid/PlantUML",
                "Generate analysis summary",
                "Show different export formats",
                "Demonstrate sharing capabilities",
                "Show integration with other tools"
            ],
            "duration": "30-45 seconds"
        }
    ]
    
    console.print("\n[bold green]🎯 Demo Scenarios[/bold green]")
    
    for i, scenario in enumerate(scenarios, 1):
        console.print(f"\n[bold cyan]{i}. {scenario['title']}[/bold cyan]")
        console.print(f"[yellow]Duration: {scenario['duration']}[/yellow]")
        console.print(f"[white]{scenario['description']}[/white]")
        
        console.print("\n[bold]Steps:[/bold]")
        for j, step in enumerate(scenario['steps'], 1):
            console.print(f"  {j}. {step}")
    
    # Screenshot checklist
    console.print("\n[bold green]📸 Screenshot Checklist[/bold green]")
    
    screenshots = [
        "Extension sidebar (empty state)",
        "Extension sidebar (with analysis results)",
        "Architecture view with components",
        "Metrics dashboard with charts",
        "AI recommendations panel",
        "Live analysis status",
        "Command palette integration",
        "Context menu options",
        "Settings panel",
        "Export dialog",
        "Dashboard webview",
        "Error handling/loading states"
    ]
    
    for i, screenshot in enumerate(screenshots, 1):
        console.print(f"  {i}. {screenshot}")
    
    # Video recording tips
    console.print("\n[bold green]🎥 Video Recording Tips[/bold green]")
    
    tips = [
        "Use a clean, professional VS Code theme",
        "Record at 1080p or higher resolution",
        "Keep cursor movements smooth and deliberate",
        "Use keyboard shortcuts to show efficiency",
        "Include voice narration explaining features",
        "Show both success and error scenarios",
        "Keep each demo focused and concise",
        "Use consistent naming conventions",
        "Include captions for accessibility",
        "Show the extension working with real codebases"
    ]
    
    for tip in tips:
        console.print(f"  • {tip}")
    
    # Technical setup
    console.print("\n[bold green]⚙️ Technical Setup[/bold green]")
    
    setup_steps = [
        "Install screen recording software (OBS Studio, Camtasia, etc.)",
        "Set up a clean development environment",
        "Prepare sample codebases (Python, JavaScript, Java)",
        "Configure VS Code with a professional theme",
        "Test all extension features before recording",
        "Prepare script/narration for each demo",
        "Set up proper lighting and audio",
        "Test recording quality and settings"
    ]
    
    for step in setup_steps:
        console.print(f"  • {step}")
    
    # File organization
    console.print("\n[bold green]📁 File Organization[/bold green]")
    
    file_structure = """
    demo-assets/
    ├── screenshots/
    │   ├── sidebar-empty.png
    │   ├── sidebar-with-results.png
    │   ├── architecture-view.png
    │   ├── metrics-dashboard.png
    │   ├── ai-recommendations.png
    │   └── live-analysis.png
    ├── videos/
    │   ├── initial-analysis.mp4
    │   ├── architecture-visualization.mp4
    │   ├── metrics-dashboard.mp4
    │   ├── ai-recommendations.mp4
    │   ├── live-analysis.mp4
    │   └── export-capabilities.mp4
    ├── gifs/
    │   ├── analysis-progress.gif
    │   ├── live-updates.gif
    │   └── export-process.gif
    └── thumbnails/
        ├── main-thumbnail.png
        └── feature-thumbnails/
    """
    
    console.print(Panel(file_structure, border_style="green", title="Recommended Structure"))
    
    # Next steps
    console.print("\n[bold green]🚀 Next Steps[/bold green]")
    
    next_steps = [
        "1. Set up screen recording software",
        "2. Prepare sample codebases for demo",
        "3. Create a recording script",
        "4. Record each demo scenario",
        "5. Take screenshots of key features",
        "6. Edit and polish videos",
        "7. Create GIFs for quick demos",
        "8. Upload to marketplace and documentation"
    ]
    
    for step in next_steps:
        console.print(f"  {step}")


def create_sample_script():
    """Create a sample script for video narration."""
    
    console.print("\n[bold green]📝 Sample Video Script[/bold green]")
    
    script = """
    [INTRO - 10 seconds]
    "Welcome to Architex, the AI-powered system design analyzer for VS Code. 
    Let me show you how it can automatically generate architecture diagrams 
    and insights from your codebase."
    
    [ANALYSIS DEMO - 30 seconds]
    "First, I'll open a Python project and run the analysis. 
    Notice how Architex scans your codebase and identifies components, 
    dependencies, and architectural patterns. The analysis is powered by 
    advanced AI that understands code semantics and relationships."
    
    [ARCHITECTURE VIEW - 45 seconds]
    "Here's the generated architecture diagram. You can see modules, 
    classes, and functions clearly organized. The relationships show 
    dependencies and interactions. You can zoom, pan, and explore 
    different views of your system architecture."
    
    [METRICS DASHBOARD - 30 seconds]
    "The metrics dashboard provides code quality insights. 
    Complexity scores, coupling metrics, and maintainability 
    indicators help you identify areas for improvement."
    
    [AI RECOMMENDATIONS - 45 seconds]
    "AI-powered recommendations suggest architectural improvements, 
    identify potential issues, and provide actionable insights. 
    Each recommendation comes with confidence scores and explanations."
    
    [LIVE ANALYSIS - 60 seconds]
    "Enable live analysis to get real-time updates as you code. 
    The extension monitors file changes and provides instant feedback 
    on architectural impact and code quality."
    
    [EXPORT & SHARE - 30 seconds]
    "Export diagrams in multiple formats including Mermaid, PlantUML, 
    and Graphviz. Share insights with your team or integrate with 
    other development tools."
    
    [CONCLUSION - 15 seconds]
    "Architex makes system design analysis effortless and intelligent. 
    Try it today and transform how you understand and document your codebase."
    """
    
    console.print(Panel(script, border_style="yellow", title="Narration Script"))


def main():
    """Main function to run the demo asset creation."""
    create_demo_plan()
    create_sample_script()
    
    console.print("\n[bold green]🎉 Demo Asset Plan Complete![/bold green]")
    console.print("\n[bold]Ready to create amazing demos for Architex![/bold]")


if __name__ == "__main__":
    main() 