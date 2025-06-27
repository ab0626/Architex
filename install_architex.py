#!/usr/bin/env python3
"""
Installation script for Architex CLI.

This script installs the Architex CLI tool so it can be used by the VS Code extension.
"""

import subprocess
import sys
import os
import platform
from pathlib import Path


def run_command(command, description, check=True):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        if result.stdout:
            print(f"   ✅ {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Error: {e.stderr.strip()}")
        return False


def install_architex_cli():
    """Install Architex CLI in development mode."""
    print("🚀 Installing Architex CLI...")
    
    # Get the current directory (should be the Architex root)
    current_dir = Path(__file__).parent.absolute()
    
    # Check if we're in the right directory
    if not (current_dir / "setup.py").exists():
        print("   ❌ setup.py not found. Please run this script from the Architex root directory.")
        return False
    
    # Install in development mode
    success = run_command(f"pip install -e {current_dir}", "Installing Architex CLI in development mode")
    
    if success:
        print("   ✅ Architex CLI installed successfully!")
        
        # Test the installation
        test_success = run_command("architex --help", "Testing Architex CLI installation", check=False)
        if test_success:
            print("   ✅ Architex CLI is working correctly!")
        else:
            print("   ⚠️  Architex CLI installed but may not be in PATH")
            print("   💡 Try restarting your terminal or adding the Python Scripts directory to PATH")
    else:
        print("   ❌ Failed to install Architex CLI")
    
    return success


def install_dependencies():
    """Install required dependencies."""
    print("\n📦 Installing dependencies...")
    
    # Install core requirements
    success = run_command("pip install -r requirements.txt", "Installing core dependencies")
    
    if not success:
        print("   ⚠️  Some dependencies failed to install. Trying individual packages...")
        
        # Try installing key packages individually
        key_packages = [
            "pydantic>=2.0.0",
            "networkx>=3.0",
            "typer>=0.9.0",
            "rich>=13.0.0",
            "tree-sitter>=0.20.0",
            "pandas>=2.0.0",
            "numpy>=1.24.0",
            "fastapi>=0.104.0",
            "uvicorn[standard]>=0.24.0",
            "langchain>=0.1.0",
            "openai>=1.0.0",
            "watchdog>=3.0.0"
        ]
        
        for package in key_packages:
            run_command(f"pip install {package}", f"Installing {package}", check=False)
    
    return success


def main():
    """Main installation function."""
    print("🚀 Architex CLI Installation")
    print("=" * 40)
    
    # Install dependencies first
    install_dependencies()
    
    # Install Architex CLI
    if install_architex_cli():
        print("\n🎉 Installation completed successfully!")
        print("\n📋 Next steps:")
        print("   1. Restart VS Code")
        print("   2. Try the 'Architex: Analyze current Workspace' command")
        print("   3. If it still doesn't work, check the VS Code extension settings")
        print("\n🔧 Troubleshooting:")
        print("   - Make sure Python is in your PATH")
        print("   - Try running 'architex --help' in your terminal")
        print("   - Check VS Code extension settings for 'architex.architexPath'")
    else:
        print("\n❌ Installation failed. Please check the error messages above.")
        sys.exit(1)


if __name__ == "__main__":
    main() 