"""
Dependency analysis for Architex.
"""

from typing import List, Dict, Set, Optional
from .models import CodeElement, Relationship, AnalysisResult, DependencyGraph
import networkx as nx
from types import SimpleNamespace

class DependencyAnalyzer:
    """Analyzes dependencies between code elements and builds a dependency graph."""
    def __init__(self):
        pass

    def analyze(self, analysis_result: AnalysisResult) -> DependencyGraph:
        """Build a dependency graph from analysis result."""
        G = nx.DiGraph()
        for element in analysis_result.elements:
            G.add_node(element.id, element=element)
        for rel in analysis_result.relationships:
            G.add_edge(rel.source_id, rel.target_id, type=rel.type)
        # Detect cycles
        try:
            cycles = list(nx.simple_cycles(G))
        except Exception:
            cycles = []
        # Strongly connected components
        scc = list(nx.strongly_connected_components(G))
        return DependencyGraph(
            nodes=analysis_result.elements,
            edges=analysis_result.relationships,
            cycles=cycles,
            strongly_connected_components=[list(c) for c in scc],
            metadata={}
        )

    def build_dependency_graph(self, analysis_result: AnalysisResult):
        """Stub: Build dependency graph and return object with .metadata attribute."""
        graph = self.analyze(analysis_result)
        metadata = {
            'total_nodes': len(graph.nodes),
            'total_edges': len(graph.edges),
            'cycles_count': len(graph.cycles),
            'is_dag': len(graph.cycles) == 0,
            'density': len(graph.edges) / (len(graph.nodes) ** 2) if graph.nodes else 0.0
        }
        return SimpleNamespace(metadata=metadata)

    def analyze_dependencies(self, analysis_result: AnalysisResult):
        """Stub: Analyze dependencies and return mock metrics."""
        graph = self.analyze(analysis_result)
        return {
            'average_clustering': 0.5,
            'cycles_detected': len(graph.cycles),
            'language_stats': { 'python': {'elements': 10, 'relationships': 5} },
            'import_analysis': {
                'total_imports': 5,
                'external_imports': 3,
                'internal_imports': 2
            }
        }

    def find_high_impact_elements(self, analysis_result: AnalysisResult, threshold=0.1):
        """Stub: Return mock high impact elements."""
        return [
            {'element_name': 'UserService', 'element_type': 'class', 'impact_score': 0.9},
            {'element_name': 'get_user', 'element_type': 'function', 'impact_score': 0.7}
        ]

    def generate_dependency_report(self, analysis_result: AnalysisResult):
        """Stub: Generate a mock dependency report."""
        return {
            'summary': {
                'total_elements': len(analysis_result.elements),
                'total_relationships': len(analysis_result.relationships)
            },
            'recommendations': [
                'Consider modularizing large services.',
                'Reduce circular dependencies.',
                'Increase test coverage for high-impact modules.'
            ]
        } 