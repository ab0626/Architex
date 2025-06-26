#!/usr/bin/env python3
"""
Simple test script to debug analysis issues.
"""

import sys
from pathlib import Path
from architex.core.parsers import ParserRegistry
from architex.core.analyzer import CodebaseAnalyzer

def test_parsing():
    """Test just the parsing step."""
    print("🔍 Testing parsing...")
    
    # Initialize parser
    registry = ParserRegistry()
    print(f"✅ Supported languages: {registry.get_supported_languages()}")
    
    # Test with example project
    project_path = Path("examples/simple_python_project")
    
    if not project_path.exists():
        print(f"❌ Project path not found: {project_path}")
        return
    
    # Parse files
    all_elements = []
    all_relationships = []
    
    for file_path in project_path.rglob("*.py"):
        print(f"📄 Parsing: {file_path}")
        
        parser = registry.get_parser_for_file(file_path)
        if parser:
            elements = parser.parse_file(file_path)
            relationships = parser.extract_relationships(elements)
            
            print(f"   ✅ Found {len(elements)} elements")
            print(f"   ✅ Found {len(relationships)} relationships")
            
            all_elements.extend(elements)
            all_relationships.extend(relationships)
        else:
            print(f"   ❌ No parser found for {file_path}")
    
    print(f"\n📊 Total: {len(all_elements)} elements, {len(all_relationships)} relationships")
    
    # Test relationship creation
    print("\n🔗 Testing relationship creation...")
    for i, rel in enumerate(all_relationships[:3]):  # Test first 3
        print(f"   Relationship {i+1}: {rel.id} -> {rel.source_id} -> {rel.target_id}")
    
    return all_elements, all_relationships

def test_analyzer():
    """Test the analyzer."""
    print("\n🔍 Testing analyzer...")
    
    analyzer = CodebaseAnalyzer()
    
    try:
        result = analyzer.analyze("examples/simple_python_project")
        print(f"✅ Analysis successful: {len(result.elements)} elements")
        return result
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("🧪 Architex Analysis Test")
    print("=" * 50)
    
    # Test parsing
    elements, relationships = test_parsing()
    
    # Test analyzer
    result = test_analyzer()
    
    print("\n✅ Test completed!") 