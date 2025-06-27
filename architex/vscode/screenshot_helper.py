#!/usr/bin/env python3
"""
Screenshot helper script for Architex extension demo.
Provides utilities for taking and organizing screenshots.
"""

import os
import sys
import time
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


def create_screenshot_checklist():
    """Create a printable screenshot checklist."""
    
    console.print(Panel.fit(
        "[bold blue]📸 Architex Extension Screenshot Checklist[/bold blue]",
        border_style="blue"
    ))
    
    # Screenshot categories
    categories = {
        "Core Features": [
            "Extension sidebar (empty state)",
            "Extension sidebar (with analysis results)",
            "Architecture view with components",
            "Metrics dashboard with charts",
            "AI recommendations panel",
            "Live analysis status"
        ],
        "User Interface": [
            "Command palette integration",
            "Context menu options",
            "Settings panel",
            "Export dialog",
            "Dashboard webview",
            "Error handling/loading states"
        ],
        "Analysis Results": [
            "Component hierarchy view",
            "Dependency graph",
            "Code complexity metrics",
            "Architecture recommendations",
            "Export options dialog",
            "Analysis progress indicators"
        ]
    }
    
    for category, screenshots in categories.items():
        console.print(f"\n[bold green]{category}[/bold green]")
        for i, screenshot in enumerate(screenshots, 1):
            console.print(f"  [ ] {i}. {screenshot}")
    
    # Screenshot tips
    console.print("\n[bold yellow]📝 Screenshot Tips[/bold yellow]")
    tips = [
        "Use VS Code Dark+ theme for professional look",
        "Capture at 1920x1080 resolution",
        "Include relevant code in the editor",
        "Show the extension sidebar clearly",
        "Use descriptive filenames",
        "Take multiple angles of key features",
        "Include both empty and populated states",
        "Show error states and loading indicators"
    ]
    
    for tip in tips:
        console.print(f"  • {tip}")


def create_video_storyboard():
    """Create a video storyboard for recording."""
    
    console.print(Panel.fit(
        "[bold blue]🎬 Video Storyboard[/bold blue]",
        border_style="blue"
    ))
    
    scenes = [
        {
            "scene": "1. Introduction",
            "duration": "10s",
            "action": "Welcome message, show VS Code with extension",
            "narration": "Welcome to Architex, the AI-powered system design analyzer for VS Code."
        },
        {
            "scene": "2. Open Demo Project",
            "duration": "15s",
            "action": "Open demo-project/main.py, show code structure",
            "narration": "Let me open a Python project that demonstrates various architectural patterns."
        },
        {
            "scene": "3. Run Analysis",
            "duration": "30s",
            "action": "Show empty sidebar, run analysis command, show progress",
            "narration": "I'll run the analysis to scan the codebase and identify components and dependencies."
        },
        {
            "scene": "4. Architecture View",
            "duration": "45s",
            "action": "Show generated diagram, highlight components, demonstrate interactions",
            "narration": "Here's the generated architecture diagram showing modules, classes, and their relationships."
        },
        {
            "scene": "5. Metrics Dashboard",
            "duration": "30s",
            "action": "Open metrics view, show complexity scores, highlight insights",
            "narration": "The metrics dashboard provides code quality insights and identifies areas for improvement."
        },
        {
            "scene": "6. AI Recommendations",
            "duration": "45s",
            "action": "Show AI panel, display recommendations, explain confidence scores",
            "narration": "AI-powered recommendations suggest architectural improvements and identify potential issues."
        },
        {
            "scene": "7. Live Analysis",
            "duration": "60s",
            "action": "Enable live mode, make code changes, show real-time updates",
            "narration": "Enable live analysis to get real-time feedback as you code and modify your architecture."
        },
        {
            "scene": "8. Export & Share",
            "duration": "30s",
            "action": "Show export options, demonstrate different formats",
            "narration": "Export diagrams in multiple formats and share insights with your team."
        },
        {
            "scene": "9. Conclusion",
            "duration": "15s",
            "action": "Show final summary, call-to-action",
            "narration": "Architex makes system design analysis effortless and intelligent. Try it today!"
        }
    ]
    
    table = Table(title="Video Storyboard")
    table.add_column("Scene", style="cyan")
    table.add_column("Duration", style="yellow")
    table.add_column("Action", style="white")
    table.add_column("Narration", style="green")
    
    for scene in scenes:
        table.add_row(
            scene["scene"],
            scene["duration"],
            scene["action"],
            scene["narration"]
        )
    
    console.print(table)


def create_recording_script():
    """Create a detailed recording script."""
    
    console.print(Panel.fit(
        "[bold blue]📝 Detailed Recording Script[/bold blue]",
        border_style="blue"
    ))
    
    script = """
    [SCENE 1: INTRODUCTION - 10 seconds]
    
    VISUAL: VS Code with Architex extension sidebar visible
    AUDIO: "Welcome to Architex, the AI-powered system design analyzer for VS Code. 
    Let me show you how it can automatically generate architecture diagrams 
    and insights from your codebase."
    
    [SCENE 2: OPEN DEMO PROJECT - 15 seconds]
    
    VISUAL: Open demo-project/main.py, show the code structure
    AUDIO: "I'll start by opening a Python project that demonstrates various 
    architectural patterns including repositories, services, and API handlers."
    
    [SCENE 3: RUN ANALYSIS - 30 seconds]
    
    VISUAL: Show empty sidebar, open command palette, run "Architex: Analyze Current Workspace"
    AUDIO: "Now I'll run the analysis. Notice how Architex scans your codebase 
    and identifies components, dependencies, and architectural patterns. 
    The analysis is powered by advanced AI that understands code semantics."
    
    [SCENE 4: ARCHITECTURE VIEW - 45 seconds]
    
    VISUAL: Show generated diagram, zoom in/out, highlight different components
    AUDIO: "Here's the generated architecture diagram. You can see modules, 
    classes, and functions clearly organized. The relationships show 
    dependencies and interactions. You can zoom, pan, and explore 
    different views of your system architecture."
    
    [SCENE 5: METRICS DASHBOARD - 30 seconds]
    
    VISUAL: Open metrics view, show complexity scores, coupling metrics
    AUDIO: "The metrics dashboard provides code quality insights. 
    Complexity scores, coupling metrics, and maintainability 
    indicators help you identify areas for improvement."
    
    [SCENE 6: AI RECOMMENDATIONS - 45 seconds]
    
    VISUAL: Open AI recommendations panel, show suggestions, confidence scores
    AUDIO: "AI-powered recommendations suggest architectural improvements, 
    identify potential issues, and provide actionable insights. 
    Each recommendation comes with confidence scores and explanations."
    
    [SCENE 7: LIVE ANALYSIS - 60 seconds]
    
    VISUAL: Enable live mode, make code changes, show real-time updates
    AUDIO: "Enable live analysis to get real-time updates as you code. 
    The extension monitors file changes and provides instant feedback 
    on architectural impact and code quality."
    
    [SCENE 8: EXPORT & SHARE - 30 seconds]
    
    VISUAL: Show export dialog, demonstrate Mermaid/PlantUML export
    AUDIO: "Export diagrams in multiple formats including Mermaid, PlantUML, 
    and Graphviz. Share insights with your team or integrate with 
    other development tools."
    
    [SCENE 9: CONCLUSION - 15 seconds]
    
    VISUAL: Show final summary, extension sidebar with results
    AUDIO: "Architex makes system design analysis effortless and intelligent. 
    Try it today and transform how you understand and document your codebase."
    """
    
    console.print(Panel(script, border_style="yellow", title="Complete Script"))


def create_file_structure():
    """Create the recommended file structure for demo assets."""
    
    console.print(Panel.fit(
        "[bold blue]📁 Demo Assets File Structure[/bold blue]",
        border_style="blue"
    ))
    
    structure = """
    demo-assets/
    ├── screenshots/
    │   ├── 01-sidebar-empty.png
    │   ├── 02-sidebar-with-results.png
    │   ├── 03-architecture-view.png
    │   ├── 04-metrics-dashboard.png
    │   ├── 05-ai-recommendations.png
    │   ├── 06-live-analysis.png
    │   ├── 07-command-palette.png
    │   ├── 08-context-menu.png
    │   ├── 09-settings-panel.png
    │   ├── 10-export-dialog.png
    │   ├── 11-dashboard-webview.png
    │   └── 12-error-states.png
    ├── videos/
    │   ├── 01-initial-analysis.mp4
    │   ├── 02-architecture-visualization.mp4
    │   ├── 03-metrics-dashboard.mp4
    │   ├── 04-ai-recommendations.mp4
    │   ├── 05-live-analysis.mp4
    │   └── 06-export-capabilities.mp4
    ├── gifs/
    │   ├── analysis-progress.gif
    │   ├── live-updates.gif
    │   └── export-process.gif
    ├── thumbnails/
    │   ├── main-thumbnail.png
    │   └── feature-thumbnails/
    │       ├── analysis-thumb.png
    │       ├── metrics-thumb.png
    │       ├── ai-thumb.png
    │       └── live-thumb.png
    └── README.md
    """
    
    console.print(Panel(structure, border_style="green", title="Recommended Structure"))


def main():
    """Main function to run the screenshot helper."""
    
    console.print("[bold blue]🎬 Architex Extension Demo Assets Helper[/bold blue]\n")
    
    # Show all sections
    create_screenshot_checklist()
    create_video_storyboard()
    create_recording_script()
    create_file_structure()
    
    # Next steps
    console.print("\n[bold green]🚀 Ready to Create Amazing Demos![/bold green]")
    console.print("\n[bold]Next Steps:[/bold]")
    console.print("1. Set up screen recording software (OBS Studio recommended)")
    console.print("2. Install the Architex extension locally")
    console.print("3. Open the demo project in VS Code")
    console.print("4. Follow the storyboard to record your demos")
    console.print("5. Take screenshots using the checklist")
    console.print("6. Edit and polish your videos")
    console.print("7. Upload to the VS Code Marketplace")
    
    console.print("\n[bold yellow]💡 Pro Tip:[/bold yellow] Start with screenshots first, then move to videos!")
    console.print("[bold yellow]💡 Pro Tip:[/bold yellow] Use the demo project for consistent results!")


if __name__ == "__main__":
    main() 