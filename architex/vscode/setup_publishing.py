#!/usr/bin/env python3
"""
Setup script for publishing Architex VS Code extension
"""

import os
import json
import subprocess
import sys
from pathlib import Path

def check_prerequisites():
    """Check if all prerequisites are met"""
    print("🔍 Checking prerequisites...")
    
    # Check Node.js
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js: {result.stdout.strip()}")
        else:
            print("❌ Node.js not found")
            return False
    except FileNotFoundError:
        print("❌ Node.js not found")
        return False
    
    # Check npm
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ npm: {result.stdout.strip()}")
        else:
            print("❌ npm not found")
            return False
    except FileNotFoundError:
        print("❌ npm not found")
        return False
    
    # Check vsce
    try:
        result = subprocess.run(['vsce', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ vsce: {result.stdout.strip()}")
        else:
            print("⚠️  vsce not found - will install")
            return "install_vsce"
    except FileNotFoundError:
        print("⚠️  vsce not found - will install")
        return "install_vsce"
    
    return True

def install_vsce():
    """Install vsce globally"""
    print("📦 Installing vsce...")
    try:
        result = subprocess.run(['npm', 'install', '-g', '@vscode/vsce'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ vsce installed successfully")
            return True
        else:
            print(f"❌ Failed to install vsce: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error installing vsce: {e}")
        return False

def update_package_json(publisher_name):
    """Update package.json with publisher name"""
    package_path = Path("package.json")
    
    if not package_path.exists():
        print("❌ package.json not found")
        return False
    
    try:
        with open(package_path, 'r') as f:
            package_data = json.load(f)
        
        # Update publisher
        package_data['publisher'] = publisher_name
        
        # Ensure version is set
        if 'version' not in package_data:
            package_data['version'] = '1.0.0'
        
        with open(package_path, 'w') as f:
            json.dump(package_data, f, indent=2)
        
        print(f"✅ Updated package.json with publisher: {publisher_name}")
        return True
    except Exception as e:
        print(f"❌ Error updating package.json: {e}")
        return False

def install_dependencies():
    """Install npm dependencies"""
    print("📦 Installing dependencies...")
    try:
        result = subprocess.run(['npm', 'install'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Dependencies installed")
            return True
        else:
            print(f"❌ Failed to install dependencies: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def compile_extension():
    """Compile TypeScript extension"""
    print("🔨 Compiling extension...")
    try:
        result = subprocess.run(['npm', 'run', 'compile'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Extension compiled successfully")
            return True
        else:
            print(f"❌ Compilation failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error compiling extension: {e}")
        return False

def package_extension():
    """Package the extension"""
    print("📦 Packaging extension...")
    try:
        result = subprocess.run(['vsce', 'package'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Extension packaged successfully")
            # Find the .vsix file
            vsix_files = list(Path('.').glob('*.vsix'))
            if vsix_files:
                print(f"📁 Package created: {vsix_files[0]}")
            return True
        else:
            print(f"❌ Packaging failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error packaging extension: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Architex VS Code Extension Publishing Setup")
    print("=" * 50)
    
    # Check prerequisites
    prereq_result = check_prerequisites()
    if prereq_result == "install_vsce":
        if not install_vsce():
            sys.exit(1)
    elif prereq_result is False:
        sys.exit(1)
    
    # Get publisher name
    publisher_name = input("\n📝 Enter your publisher name: ").strip()
    if not publisher_name:
        print("❌ Publisher name is required")
        sys.exit(1)
    
    # Update package.json
    if not update_package_json(publisher_name):
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Compile extension
    if not compile_extension():
        sys.exit(1)
    
    # Package extension
    if not package_extension():
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Create a publisher account at: https://marketplace.visualstudio.com/")
    print("2. Create a Personal Access Token at: https://dev.azure.com/")
    print("3. Run: vsce login " + publisher_name)
    print("4. Run: vsce publish")
    print("\n📖 See PUBLISHING_GUIDE.md for detailed instructions")

if __name__ == "__main__":
    main() 