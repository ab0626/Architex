#!/usr/bin/env python3
"""
Demo script for Architex Multi-Language Analysis

This script demonstrates the enhanced capabilities of Architex to parse multiple
languages, generate comprehensive AST models, extract dependencies, and detect
service boundaries.
"""

import json
import time
from pathlib import Path
from architex.core.parsers import ParserRegistry
from architex.core.service_detector import ServiceDetector
from architex.core.dependency_analyzer import DependencyAnalyzer
from architex.core.models import AnalysisResult, LanguageType
from architex.core.analyzer import CodebaseAnalyzer


def demo_multi_language_parsing():
    """Demonstrate multi-language parsing capabilities."""
    
    print("🌍 Multi-Language Parsing Demo")
    print("=" * 50)
    
    # Initialize parser registry
    registry = ParserRegistry()
    
    print(f"\n📦 Supported Languages: {registry.get_supported_languages()}")
    print(f"📁 Supported Extensions: {registry.get_supported_extensions()}")
    
    # Create sample files for different languages
    sample_files = create_sample_files()
    
    print("\n🔍 Parsing Sample Files:")
    print("-" * 30)
    
    all_elements = []
    all_relationships = []
    
    for file_path, language in sample_files:
        print(f"\n📄 Parsing: {file_path.name} ({language})")
        
        # Get appropriate parser
        parser = registry.get_parser_for_file(file_path)
        if parser:
            # Parse file
            elements = parser.parse_file(file_path)
            relationships = parser.extract_relationships(elements)
            
            print(f"   ✅ Found {len(elements)} elements")
            print(f"   ✅ Found {len(relationships)} relationships")
            
            # Show element types
            element_types = {}
            for elem in elements:
                elem_type = elem.type.value
                element_types[elem_type] = element_types.get(elem_type, 0) + 1
            
            print(f"   📊 Element types: {element_types}")
            
            all_elements.extend(elements)
            all_relationships.extend(relationships)
        else:
            print(f"   ❌ No parser found for {file_path.suffix}")
    
    return all_elements, all_relationships


def demo_ast_analysis(elements):
    """Demonstrate AST analysis capabilities."""
    
    print("\n🌳 AST Analysis Demo")
    print("=" * 30)
    
    # Analyze AST nodes by language
    ast_stats = {}
    for element in elements:
        lang = element.language.value
        if lang not in ast_stats:
            ast_stats[lang] = {'elements_with_ast': 0, 'total_elements': 0}
        
        ast_stats[lang]['total_elements'] += 1
        if element.ast_node:
            ast_stats[lang]['elements_with_ast'] += 1
    
    print("\n📊 AST Coverage by Language:")
    for lang, stats in ast_stats.items():
        coverage = (stats['elements_with_ast'] / stats['total_elements']) * 100
        print(f"   {lang}: {stats['elements_with_ast']}/{stats['total_elements']} ({coverage:.1f}%)")
    
    # Show detailed AST examples
    print("\n🔍 AST Node Examples:")
    elements_with_ast = [e for e in elements if e.ast_node]
    for i, element in enumerate(elements_with_ast[:5]):  # Show first 5
        print(f"\n   {i+1}. {element.name} ({element.type.value})")
        print(f"      Language: {element.language.value}")
        print(f"      AST Node Type: {element.ast_node.node_type}")
        if element.ast_node.position:
            print(f"      Position: {element.ast_node.position}")
        if element.ast_node.value:
            print(f"      Value: {element.ast_node.value}")


def demo_dependency_analysis(elements, relationships):
    """Demonstrate dependency analysis capabilities."""
    
    print("\n🔗 Dependency Analysis Demo")
    print("=" * 35)
    
    # Create analysis result
    analysis_result = AnalysisResult(
        id="demo_analysis",
        elements=elements,
        relationships=relationships
    )
    
    # Initialize dependency analyzer
    analyzer = DependencyAnalyzer()
    
    # Build dependency graph
    print("\n📈 Building Dependency Graph...")
    dependency_graph = analyzer.build_dependency_graph(analysis_result)
    
    print(f"   ✅ Nodes: {dependency_graph.metadata['total_nodes']}")
    print(f"   ✅ Edges: {dependency_graph.metadata['total_edges']}")
    print(f"   ✅ Cycles: {dependency_graph.metadata['cycles_count']}")
    print(f"   ✅ Is DAG: {dependency_graph.metadata['is_dag']}")
    print(f"   ✅ Density: {dependency_graph.metadata['density']:.3f}")
    
    # Analyze dependencies
    print("\n📊 Dependency Analysis:")
    metrics = analyzer.analyze_dependencies(analysis_result)
    
    print(f"   📈 Average Clustering: {metrics['average_clustering']:.3f}")
    print(f"   🔄 Circular Dependencies: {metrics['cycles_detected']}")
    
    # Language-specific analysis
    print("\n🌍 Language-Specific Analysis:")
    for lang, stats in metrics['language_stats'].items():
        print(f"   {lang}: {stats['elements']} elements, {stats['relationships']} relationships")
    
    # Import analysis
    print("\n📦 Import Analysis:")
    import_analysis = metrics['import_analysis']
    print(f"   Total Imports: {import_analysis['total_imports']}")
    print(f"   External: {import_analysis['external_imports']}")
    print(f"   Internal: {import_analysis['internal_imports']}")
    
    # High impact elements
    print("\n🎯 High Impact Elements:")
    high_impact = analyzer.find_high_impact_elements(analysis_result, threshold=0.1)
    for i, elem in enumerate(high_impact[:5]):
        print(f"   {i+1}. {elem['element_name']} ({elem['element_type']}) - Impact: {elem['impact_score']:.2f}")
    
    return analysis_result, analyzer


def demo_service_detection(analysis_result):
    """Demonstrate service detection capabilities."""
    
    print("\n🏗️  Service Detection Demo")
    print("=" * 35)
    
    # Initialize service detector
    detector = ServiceDetector()
    
    # Detect services
    print("\n🔍 Detecting Service Boundaries...")
    services = detector.detect_services(analysis_result)
    
    print(f"   ✅ Found {len(services)} service boundaries")
    
    # Show service details
    print("\n📊 Service Analysis:")
    for i, service in enumerate(services):
        print(f"\n   {i+1}. {service.name} ({service.type.value})")
        print(f"      Elements: {service.metadata['element_count']}")
        print(f"      Languages: {', '.join(service.metadata['languages'])}")
        print(f"      Cohesion: {service.cohesion_score:.2f}")
        print(f"      Coupling: {service.coupling_score:.2f}")
        print(f"      Complexity: {service.complexity_score:.2f}")
        print(f"      Dependencies: {len(service.dependencies)}")
    
    # Detect architectural layers
    print("\n🏛️  Architectural Layer Detection:")
    layers = detector.detect_architectural_layers(analysis_result)
    
    for layer in layers:
        print(f"   {layer.name} (Level {layer.level}): {layer.metadata['element_count']} elements")
    
    # Detect microservices
    print("\n🔬 Microservice Detection:")
    microservices = detector.detect_microservices(analysis_result)
    print(f"   Potential Microservices: {len(microservices)}")
    
    # Detect anti-patterns
    print("\n⚠️  Anti-Pattern Detection:")
    anti_patterns = detector.detect_anti_patterns(analysis_result)
    print(f"   Anti-Patterns Found: {len(anti_patterns)}")
    
    for pattern in anti_patterns[:3]:  # Show first 3
        print(f"   - {pattern['type']}: {pattern['description']}")
    
    return services, layers, anti_patterns


def demo_comprehensive_analysis():
    """Demonstrate comprehensive analysis workflow."""
    
    print("\n🚀 Comprehensive Analysis Workflow")
    print("=" * 45)
    
    # Step 1: Multi-language parsing
    print("\n1️⃣  Step 1: Multi-Language Parsing")
    elements, relationships = demo_multi_language_parsing()
    
    # Step 2: AST Analysis
    print("\n2️⃣  Step 2: AST Analysis")
    demo_ast_analysis(elements)
    
    # Step 3: Dependency Analysis
    print("\n3️⃣  Step 3: Dependency Analysis")
    analysis_result, analyzer = demo_dependency_analysis(elements, relationships)
    
    # Step 4: Service Detection
    print("\n4️⃣  Step 4: Service Detection")
    services, layers, anti_patterns = demo_service_detection(analysis_result)
    
    # Step 5: Generate comprehensive report
    print("\n5️⃣  Step 5: Generate Comprehensive Report")
    report = analyzer.generate_dependency_report(analysis_result)
    
    print("\n📋 Analysis Summary:")
    print(f"   Total Elements: {report['summary']['total_elements']}")
    print(f"   Total Relationships: {report['summary']['total_relationships']}")
    print(f"   Services Detected: {len(services)}")
    print(f"   Layers Identified: {len(layers)}")
    print(f"   Anti-Patterns: {len(anti_patterns)}")
    
    print("\n💡 Recommendations:")
    for rec in report['recommendations'][:5]:
        print(f"   {rec}")
    
    return analysis_result, report


def create_sample_files():
    """Create sample files for different languages."""
    sample_files = []
    
    # Python sample
    python_code = '''
import json
from typing import List, Dict
from fastapi import FastAPI

class UserService:
    def __init__(self):
        self.users = []
    
    def get_user(self, user_id: int) -> Dict:
        return {"id": user_id, "name": "John Doe"}
    
    def create_user(self, user_data: Dict) -> Dict:
        user = {"id": len(self.users) + 1, **user_data}
        self.users.append(user)
        return user

app = FastAPI()
user_service = UserService()

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return user_service.get_user(user_id)
'''
    
    # JavaScript sample
    js_code = '''
const express = require('express');
const app = express();

class UserController {
    constructor() {
        this.users = [];
    }
    
    getUser(req, res) {
        const userId = req.params.id;
        const user = this.users.find(u => u.id === userId);
        res.json(user);
    }
    
    createUser(req, res) {
        const user = { id: this.users.length + 1, ...req.body };
        this.users.push(user);
        res.json(user);
    }
}

const userController = new UserController();
app.get('/users/:id', userController.getUser.bind(userController));
'''
    
    # Java sample
    java_code = '''
package com.example.service;

import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.*;

@Service
public class UserService {
    private List<User> users = new ArrayList<>();
    
    public User getUser(Long id) {
        return users.stream()
                   .filter(user -> user.getId().equals(id))
                   .findFirst()
                   .orElse(null);
    }
    
    public User createUser(User user) {
        user.setId(users.size() + 1L);
        users.add(user);
        return user;
    }
}

@RestController
@RequestMapping("/api/users")
public class UserController {
    @Autowired
    private UserService userService;
    
    @GetMapping("/{id}")
    public User getUser(@PathVariable Long id) {
        return userService.getUser(id);
    }
}
'''
    
    # Write sample files
    files = [
        ("sample.py", python_code, LanguageType.PYTHON),
        ("sample.js", js_code, LanguageType.JAVASCRIPT),
        ("UserService.java", java_code, LanguageType.JAVA)
    ]
    
    for filename, code, language in files:
        file_path = Path(filename)
        with open(file_path, 'w') as f:
            f.write(code)
        sample_files.append((file_path, language.value))
    
    return sample_files


def cleanup_sample_files():
    """Clean up sample files."""
    sample_files = ["sample.py", "sample.js", "UserService.java"]
    for filename in sample_files:
        file_path = Path(filename)
        if file_path.exists():
            file_path.unlink()


if __name__ == "__main__":
    try:
        print("🏗️  Architex Multi-Language Analysis Demo")
        print("=" * 60)
        
        # Run comprehensive demo
        analysis_result, report = demo_comprehensive_analysis()
        
        print("\n✅ Demo completed successfully!")
        print("\n🎯 Key Features Demonstrated:")
        print("   • Multi-language parsing (Python, JavaScript, Java)")
        print("   • Comprehensive AST analysis")
        print("   • Dependency graph building and analysis")
        print("   • Service boundary detection")
        print("   • Architectural layer identification")
        print("   • Anti-pattern detection")
        print("   • Impact analysis and recommendations")
        
        print("\n📈 Analysis Results:")
        print(f"   • Total code elements analyzed: {len(analysis_result.elements)}")
        print(f"   • Total relationships found: {len(analysis_result.relationships)}")
        print(f"   • Languages supported: {len(set(e.language.value for e in analysis_result.elements))}")
        print(f"   • Services detected: {len(analysis_result.service_boundaries)}")
        
    except Exception as e:
        print(f"❌ Error during demo: {e}")
    
    finally:
        # Cleanup
        cleanup_sample_files()
        print("\n🧹 Cleanup completed.") 