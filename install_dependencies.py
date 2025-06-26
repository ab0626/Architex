#!/usr/bin/env python3
"""
Installation script for Architex dependencies.

This script handles the installation of all required dependencies,
including system dependencies and optional components.
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


def check_python_version():
    """Check if Python version is compatible."""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"   ❌ Python {version.major}.{version.minor} is not supported. Please use Python 3.8+")
        return False
    print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True


def install_pip_dependencies():
    """Install pip dependencies."""
    print("\n📦 Installing pip dependencies...")
    
    # Upgrade pip first
    run_command("python -m pip install --upgrade pip", "Upgrading pip")
    
    # Install core requirements
    success = run_command("pip install -r requirements.txt", "Installing core dependencies")
    
    if not success:
        print("   ⚠️  Some dependencies failed to install. Trying individual packages...")
        
        # Try installing key packages individually
        key_packages = [
            "pydantic>=2.0.0",
            "networkx>=3.0",
            "click>=8.0.0",
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


def check_system_dependencies():
    """Check for system dependencies."""
    print("\n🔧 Checking system dependencies...")
    
    system = platform.system().lower()
    
    # Check for Java (needed for PlantUML)
    java_available = run_command("java -version", "Checking Java installation", check=False)
    if not java_available:
        print("   ⚠️  Java not found. PlantUML diagram generation will not work.")
        print("   💡 Install Java from: https://adoptium.net/")
    
    # Check for Node.js (needed for Mermaid CLI)
    node_available = run_command("node --version", "Checking Node.js installation", check=False)
    if not node_available:
        print("   ⚠️  Node.js not found. Mermaid CLI will not be available.")
        print("   💡 Install Node.js from: https://nodejs.org/")
    else:
        # Try to install Mermaid CLI
        run_command("npm install -g @mermaid-js/mermaid-cli", "Installing Mermaid CLI", check=False)
    
    # Check for Graphviz
    if system == "windows":
        # On Windows, check if graphviz is in PATH
        graphviz_available = run_command("dot -V", "Checking Graphviz installation", check=False)
        if not graphviz_available:
            print("   ⚠️  Graphviz not found. Graphviz diagrams will not work.")
            print("   💡 Download from: https://graphviz.org/download/")
    else:
        # On Unix-like systems, try to install via package manager
        if system == "darwin":  # macOS
            run_command("brew install graphviz", "Installing Graphviz via Homebrew", check=False)
        elif system == "linux":
            # Try different package managers
            run_command("which apt-get && sudo apt-get install -y graphviz", "Installing Graphviz via apt", check=False)
            run_command("which yum && sudo yum install -y graphviz", "Installing Graphviz via yum", check=False)
    
    return True


def install_optional_dependencies():
    """Install optional dependencies."""
    print("\n🎯 Installing optional dependencies...")
    
    optional_packages = [
        "jupyter>=1.0.0",
        "ipython>=8.0.0",
        "black>=23.0.0",
        "flake8>=6.0.0",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0"
    ]
    
    for package in optional_packages:
        run_command(f"pip install {package}", f"Installing {package}", check=False)
    
    return True


def create_virtual_environment():
    """Create a virtual environment if not already in one."""
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("   ✅ Already in a virtual environment")
        return True
    
    print("\n🌍 Creating virtual environment...")
    success = run_command("python -m venv venv", "Creating virtual environment")
    
    if success:
        print("   💡 To activate the virtual environment:")
        if platform.system().lower() == "windows":
            print("      venv\\Scripts\\activate")
        else:
            print("      source venv/bin/activate")
    
    return success


def test_installation():
    """Test the installation by importing key modules."""
    print("\n🧪 Testing installation...")
    
    test_modules = [
        "pydantic",
        "networkx", 
        "click",
        "rich",
        "pandas",
        "numpy",
        "fastapi",
        "uvicorn",
        "langchain",
        "openai",
        "watchdog"
    ]
    
    failed_modules = []
    
    for module in test_modules:
        try:
            __import__(module)
            print(f"   ✅ {module}")
        except ImportError:
            print(f"   ❌ {module}")
            failed_modules.append(module)
    
    if failed_modules:
        print(f"\n⚠️  Failed to import: {', '.join(failed_modules)}")
        return False
    else:
        print("\n🎉 All core modules imported successfully!")
        return True


def main():
    """Main installation function."""
    print("🚀 Architex Dependency Installation")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment (optional)
    create_virtual_environment()
    
    # Install pip dependencies
    if not install_pip_dependencies():
        print("\n❌ Failed to install core dependencies")
        sys.exit(1)
    
    # Check system dependencies
    check_system_dependencies()
    
    # Install optional dependencies
    install_optional_dependencies()
    
    # Test installation
    if test_installation():
        print("\n🎉 Installation completed successfully!")
        print("\n📚 Next steps:")
        print("   1. Run the demo: python demo_multi_language_analysis.py")
        print("   2. Start the CLI: python -m architex.cli.main")
        print("   3. Start the web dashboard: python -m architex.web.dashboard")
    else:
        print("\n⚠️  Installation completed with some issues.")
        print("   Some optional dependencies may not be available.")


if __name__ == "__main__":
    main() 