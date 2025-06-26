#!/usr/bin/env python3
"""
Test script to demonstrate Architex functionality.
"""

import sys
from pathlib import Path

# Add the architex package to the path
sys.path.insert(0, str(Path(__file__).parent))

from architex.core.analyzer import CodebaseAnalyzer
from architex.exporters import MermaidExporter, PlantUMLExporter, GraphvizExporter


def test_analysis():
    """Test the analysis functionality."""
    print("🧪 Testing Architex Analysis")
    print("=" * 50)
    
    # Create analyzer
    analyzer = CodebaseAnalyzer()
    
    # Analyze the example project
    example_path = Path(__file__).parent / "examples" / "simple_python_project"
    
    if not example_path.exists():
        print(f"❌ Example project not found at: {example_path}")
        return
    
    print(f"📁 Analyzing: {example_path}")
    
    try:
        # Perform analysis
        result = analyzer.analyze(example_path)
        
        print(f"✅ Analysis complete!")
        print(f"   📊 Found {len(result.elements)} code elements")
        print(f"   🔗 Found {len(result.relationships)} relationships")
        print(f"   🏗️  Detected {len(result.service_boundaries)} service boundaries")
        
        # Display some metrics
        print("\n📈 Metrics:")
        for key, value in result.metrics.items():
            if isinstance(value, float):
                print(f"   {key.replace('_', ' ').title()}: {value:.2f}")
            else:
                print(f"   {key.replace('_', ' ').title()}: {value}")
        
        # Test exporters
        test_exporters(result)
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc()


def test_exporters(result):
    """Test the diagram exporters."""
    print("\n🎨 Testing Diagram Exporters")
    print("=" * 50)
    
    exporters = [
        ("Mermaid", MermaidExporter()),
        ("PlantUML", PlantUMLExporter()),
        ("Graphviz", GraphvizExporter())
    ]
    
    for name, exporter in exporters:
        try:
            print(f"\n📝 Testing {name} exporter...")
            diagram = exporter.export(result)
            
            # Save to file
            output_file = Path(f"test_output_{name.lower()}.txt")
            output_file.write_text(diagram)
            print(f"   ✅ Saved to: {output_file}")
            
            # Show first few lines
            lines = diagram.split('\n')
            print(f"   📄 Preview (first 5 lines):")
            for i, line in enumerate(lines[:5]):
                print(f"      {i+1}: {line}")
            if len(lines) > 5:
                print(f"      ... ({len(lines) - 5} more lines)")
                
        except Exception as e:
            print(f"   ❌ {name} export failed: {e}")


def test_cli_interface():
    """Test the CLI interface."""
    print("\n🖥️  Testing CLI Interface")
    print("=" * 50)
    
    try:
        from architex.cli.main import app
        print("✅ CLI interface loaded successfully")
        print("   💡 You can now use: architex --help")
        
    except Exception as e:
        print(f"❌ CLI interface failed: {e}")


if __name__ == "__main__":
    print("🚀 Architex Test Suite")
    print("=" * 50)
    
    test_analysis()
    test_cli_interface()
    
    print("\n✨ Test completed!")
    print("\n📚 Next steps:")
    print("   1. Install the package: pip install -e .")
    print("   2. Try the CLI: architex analyze examples/simple_python_project")
    print("   3. View generated diagrams in test_output_*.txt files") 