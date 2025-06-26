#!/usr/bin/env python3
"""
Demo script showcasing Architex privacy features.
"""

import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent))

from architex.core.privacy import privacy_manager

console = Console()


def demo_privacy_features():
    """Demonstrate privacy features."""
    console.print(Panel.fit(
        "[bold blue]🔒 Architex Privacy Features Demo[/bold blue]",
        border_style="blue"
    ))
    
    # Show current privacy settings
    console.print("\n[bold green]📋 Current Privacy Settings[/bold green]")
    settings = privacy_manager.settings
    
    settings_table = Table(show_header=True, header_style="bold magenta")
    settings_table.add_column("Setting", style="cyan")
    settings_table.add_column("Value", style="green")
    settings_table.add_column("Description", style="yellow")
    
    settings_table.add_row("Local Only", str(settings.local_only), "Process data locally only")
    settings_table.add_row("AI Enabled", str(settings.ai_enabled), "Enable AI-powered analysis")
    settings_table.add_row("Store Analyzed Code", str(settings.store_analyzed_code), "Persist analyzed code")
    settings_table.add_row("Store AI Responses", str(settings.store_ai_responses), "Persist AI responses")
    settings_table.add_row("File Watching", str(settings.file_watching_enabled), "Monitor file changes")
    settings_table.add_row("Respect .gitignore", str(settings.respect_gitignore), "Follow gitignore patterns")
    settings_table.add_row("WebSocket Enabled", str(settings.websocket_enabled), "Enable web interface")
    settings_table.add_row("Clear Cache on Exit", str(settings.clear_cache_on_exit), "Auto-cleanup on exit")
    
    console.print(settings_table)
    
    # Show privacy report
    console.print("\n[bold green]📊 Privacy Report[/bold green]")
    report = privacy_manager.get_privacy_report()
    
    report_table = Table(show_header=True, header_style="bold magenta")
    report_table.add_column("Metric", style="cyan")
    report_table.add_column("Value", style="green")
    
    for key, value in report.items():
        if isinstance(value, dict):
            report_table.add_row(key.replace('_', ' ').title(), str(value))
        else:
            report_table.add_row(key.replace('_', ' ').title(), str(value))
    
    console.print(report_table)
    
    # Show sensitive patterns
    console.print("\n[bold green]🚫 Sensitive File Patterns Excluded[/bold green]")
    patterns_table = Table(show_header=True, header_style="bold magenta")
    patterns_table.add_column("Pattern", style="cyan")
    patterns_table.add_column("Description", style="yellow")
    
    sensitive_patterns = [
        ("*.key", "Private keys and certificates"),
        ("*.pem", "PEM format certificates"),
        ("*.env", "Environment configuration files"),
        ("*.db", "Database files"),
        ("secrets.json", "Secret configuration files"),
        ("*.log", "Log files"),
        ("node_modules/", "Node.js dependencies"),
        (".git/", "Git version control"),
        ("venv/", "Python virtual environments")
    ]
    
    for pattern, description in sensitive_patterns:
        patterns_table.add_row(pattern, description)
    
    console.print(patterns_table)
    
    # Demo code anonymization
    console.print("\n[bold green]🔐 Code Anonymization Demo[/bold green]")
    
    sample_code = '''
# Database configuration
DATABASE_URL = "postgresql://user:password123@localhost:5432/mydb"
API_KEY = "sk-1234567890abcdef"
SECRET_TOKEN = "super_secret_token_here"

def connect_to_database():
    """Connect to the database with credentials."""
    # This function connects to the database
    pass
'''
    
    console.print("[yellow]Original Code:[/yellow]")
    console.print(Panel(sample_code, border_style="yellow"))
    
    anonymized_code = privacy_manager.anonymize_code(sample_code)
    console.print("[green]Anonymized Code:[/green]")
    console.print(Panel(anonymized_code, border_style="green"))
    
    # Show CLI commands
    console.print("\n[bold green]🛠️ Privacy CLI Commands[/bold green]")
    
    commands_table = Table(show_header=True, header_style="bold magenta")
    commands_table.add_column("Command", style="cyan")
    commands_table.add_column("Description", style="yellow")
    
    commands = [
        ("architex privacy", "View current privacy settings"),
        ("architex privacy-settings --local-only", "Enable local-only processing"),
        ("architex privacy-settings --ai-enabled false", "Disable AI features"),
        ("architex consent ai_analysis --grant", "Grant consent for AI analysis"),
        ("architex consent file_watching --revoke", "Revoke consent for file watching"),
        ("architex privacy-report --output report.json", "Export privacy report"),
        ("architex cleanup", "Clean up cached data")
    ]
    
    for command, description in commands:
        commands_table.add_row(command, description)
    
    console.print(commands_table)
    
    # Privacy best practices
    console.print("\n[bold green]✅ Privacy Best Practices[/bold green]")
    
    practices = [
        "🔒 Use local-only mode for sensitive codebases",
        "🤖 Disable AI features when not needed",
        "🧹 Enable automatic cache cleanup",
        "📁 Review sensitive file patterns",
        "🔐 Use local AI models when available",
        "📋 Regularly review privacy settings",
        "🗑️ Clean up data periodically"
    ]
    
    for practice in practices:
        console.print(f"  {practice}")
    
    # Configuration example
    console.print("\n[bold green]⚙️ Privacy Configuration Example[/bold green]")
    
    config_example = '''
privacy:
  data_handling:
    local_only: true              # Process locally only
    store_analyzed_code: false    # Don't persist code
    store_ai_responses: false     # Don't store AI responses
    clear_cache_on_exit: true     # Auto-cleanup
  
  ai_features:
    enabled: false                # AI disabled by default
    require_consent: true         # Require explicit consent
    anonymize_code_before_ai: true # Anonymize before AI
  
  file_watching:
    respect_gitignore: true       # Follow .gitignore
    exclude_sensitive_patterns:   # Skip sensitive files
      - "*.env"
      - "*.key"
      - "secrets.json"
'''
    
    console.print(Panel(config_example, border_style="blue", title="config.yaml"))
    
    # Final message
    console.print("\n[bold green]🎉 Privacy Features Demo Complete![/bold green]")
    console.print("\n[bold]Next Steps:[/bold]")
    console.print("1. Run 'architex privacy' to view your current settings")
    console.print("2. Configure privacy settings with 'architex privacy-settings'")
    console.print("3. Review the full privacy policy in PRIVACY_POLICY.md")
    console.print("4. Test privacy features with your own codebase")


if __name__ == "__main__":
    demo_privacy_features() 