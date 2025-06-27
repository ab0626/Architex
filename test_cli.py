#!/usr/bin/env python3
"""
Test script to verify Architex CLI installation.
"""

import subprocess
import sys
import os
from pathlib import Path


def test_architex_cli():
    """Test if the architex CLI is available and working."""
    print("🧪 Testing Architex CLI installation...")
    
    # Test 1: Check if architex command exists
    try:
        result = subprocess.run(["architex", "--help"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ architex command is available and working")
            print(f"   Output: {result.stdout[:200]}...")
            return True
        else:
            print(f"❌ architex command failed with return code {result.returncode}")
            print(f"   Error: {result.stderr}")
            return False
    except FileNotFoundError:
        print("❌ architex command not found in PATH")
        return False
    except subprocess.TimeoutExpired:
        print("❌ architex command timed out")
        return False
    except Exception as e:
        print(f"❌ Error testing architex command: {e}")
        return False


def test_python_module():
    """Test if architex can be run as a Python module."""
    print("\n🧪 Testing Python module execution...")
    
    try:
        result = subprocess.run([sys.executable, "-m", "architex.cli.main", "--help"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Python module execution works")
            print(f"   Output: {result.stdout[:200]}...")
            return True
        else:
            print(f"❌ Python module execution failed with return code {result.returncode}")
            print(f"   Error: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ Python module execution timed out")
        return False
    except Exception as e:
        print(f"❌ Error testing Python module: {e}")
        return False


def test_direct_script():
    """Test if the main.py script can be run directly."""
    print("\n🧪 Testing direct script execution...")
    
    script_path = Path(__file__).parent / "architex" / "cli" / "main.py"
    
    if not script_path.exists():
        print(f"❌ Script not found at {script_path}")
        return False
    
    try:
        result = subprocess.run([sys.executable, str(script_path), "--help"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Direct script execution works")
            print(f"   Output: {result.stdout[:200]}...")
            return True
        else:
            print(f"❌ Direct script execution failed with return code {result.returncode}")
            print(f"   Error: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ Direct script execution timed out")
        return False
    except Exception as e:
        print(f"❌ Error testing direct script: {e}")
        return False


def check_python_path():
    """Check Python PATH and installation."""
    print("\n🔍 Checking Python installation...")
    
    print(f"   Python executable: {sys.executable}")
    print(f"   Python version: {sys.version}")
    print(f"   Python path: {sys.path[:3]}...")
    
    # Check if we're in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("   ✅ Running in a virtual environment")
    else:
        print("   ⚠️  Not running in a virtual environment")


def main():
    """Main test function."""
    print("🚀 Architex CLI Test")
    print("=" * 40)
    
    check_python_path()
    
    # Run tests
    cli_works = test_architex_cli()
    module_works = test_python_module()
    script_works = test_direct_script()
    
    print("\n📊 Test Results:")
    print(f"   CLI command: {'✅' if cli_works else '❌'}")
    print(f"   Python module: {'✅' if module_works else '❌'}")
    print(f"   Direct script: {'✅' if script_works else '❌'}")
    
    if cli_works:
        print("\n🎉 Architex CLI is working correctly!")
        print("   The VS Code extension should work now.")
    elif module_works:
        print("\n⚠️  CLI command not found, but Python module works.")
        print("   You may need to:")
        print("   1. Run: pip install -e .")
        print("   2. Restart your terminal")
        print("   3. Or set VS Code extension setting 'architex.architexPath' to 'python -m architex.cli.main'")
    elif script_works:
        print("\n⚠️  CLI command not found, but direct script works.")
        print("   You may need to:")
        print("   1. Run: pip install -e .")
        print("   2. Restart your terminal")
        print("   3. Or set VS Code extension setting 'architex.architexPath' to the full path of main.py")
    else:
        print("\n❌ All tests failed. Architex CLI is not properly installed.")
        print("   Please run: python install_architex.py")


if __name__ == "__main__":
    main() 