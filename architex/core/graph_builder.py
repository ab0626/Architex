"""
Dependency graph builder for analyzing code relationships.
"""

import networkx as nx
from typing import Dict, List, Set, Optional
from .models import CodeElement, Relationship, RelationshipType, ServiceBoundary, ServiceType
import uuid


class DependencyGraph:
    """Builds and analyzes dependency graphs from code elements."""
    
    def __init__(self):
        self.graph = nx.DiGraph()
        self.elements: Dict[str, CodeElement] = {}
        self.relationships: List[Relationship] = []
    
    def add_element(self, element: CodeElement):
        """Add a code element to the graph."""
        self.elements[element.id] = element
        self.graph.add_node(element.id, **element.dict())
    
    def add_relationship(self, relationship: Relationship):
        """Add a relationship between elements."""
        self.relationships.append(relationship)
        self.graph.add_edge(
            relationship.source_id,
            relationship.target_id,
            type=relationship.type,
            strength=relationship.strength,
            **relationship.metadata
        )
    
    def build_from_elements(self, elements: List[CodeElement]):
        """Build graph from a list of elements."""
        # Add all elements
        for element in elements:
            self.add_element(element)
        
        # Extract relationships
        for element in elements:
            self._extract_element_relationships(element, elements)
    
    def _extract_element_relationships(self, element: CodeElement, all_elements: List[CodeElement]):
        """Extract relationships for a specific element."""
        # Extract import relationships
        if element.type.value == 'import':
            self._extract_import_relationships(element, all_elements)
        
        # Extract inheritance relationships
        elif element.type.value == 'class':
            self._extract_inheritance_relationships(element, all_elements)
        
        # Extract function call relationships
        elif element.type.value in ['function', 'method']:
            self._extract_call_relationships(element, all_elements)
    
    def _extract_import_relationships(self, import_element: CodeElement, all_elements: List[CodeElement]):
        """Extract relationships from import statements."""
        import_name = import_element.name
        asname = import_element.metadata.get('asname')
        
        # Find elements that might be imported
        for element in all_elements:
            if element.id != import_element.id:
                # Check if this element matches the import
                if self._matches_import(import_name, element):
                    relationship = Relationship(
                        id=str(uuid.uuid4()),
                        source_id=import_element.id,
                        target_id=element.id,
                        type=RelationshipType.IMPORTS,
                        strength=1.0
                    )
                    self.add_relationship(relationship)
    
    def _matches_import(self, import_name: str, element: CodeElement) -> bool:
        """Check if an element matches an import statement."""
        # Simple matching logic - can be enhanced
        if element.name == import_name:
            return True
        
        # Handle module imports
        if '.' in import_name:
            module_part, name_part = import_name.rsplit('.', 1)
            if element.name == name_part and element.module == module_part:
                return True
        
        return False
    
    def _extract_inheritance_relationships(self, class_element: CodeElement, all_elements: List[CodeElement]):
        """Extract inheritance relationships."""
        bases = class_element.metadata.get('bases', [])
        
        for base_name in bases:
            # Find the base class
            for element in all_elements:
                if element.type.value == 'class' and element.name == base_name:
                    relationship = Relationship(
                        id=str(uuid.uuid4()),
                        source_id=class_element.id,
                        target_id=element.id,
                        type=RelationshipType.INHERITS,
                        strength=1.0
                    )
                    self.add_relationship(relationship)
                    break
    
    def _extract_call_relationships(self, function_element: CodeElement, all_elements: List[CodeElement]):
        """Extract function call relationships."""
        # This would analyze the function body to find calls
        # For now, we'll use a simplified approach
        pass
    
    def detect_service_boundaries(self) -> List[ServiceBoundary]:
        """Detect service boundaries using community detection."""
        boundaries = []
        
        # Use community detection algorithms
        communities = self._detect_communities()
        
        for i, community in enumerate(communities):
            boundary = ServiceBoundary(
                id=str(uuid.uuid4()),
                name=f"Service_{i+1}",
                type=ServiceType.API_SERVICE,  # Default type, can be improved
                elements=set(community)
            )
            
            # Calculate metrics
            boundary.cohesion_score = self._calculate_cohesion(community)
            boundary.coupling_score = self._calculate_coupling(community)
            
            boundaries.append(boundary)
        
        return boundaries
    
    def _detect_communities(self) -> List[List[str]]:
        """Detect communities in the dependency graph."""
        # Use Louvain community detection
        try:
            communities = nx.community.louvain_communities(self.graph.to_undirected())
            return [list(community) for community in communities]
        except:
            # Fallback to connected components
            components = list(nx.strongly_connected_components(self.graph))
            return [list(component) for component in components]
    
    def _calculate_cohesion(self, community: List[str]) -> float:
        """Calculate cohesion score for a community."""
        if len(community) <= 1:
            return 1.0
        
        internal_edges = 0
        total_possible_edges = len(community) * (len(community) - 1)
        
        for node in community:
            neighbors = list(self.graph.neighbors(node))
            internal_edges += sum(1 for neighbor in neighbors if neighbor in community)
        
        return internal_edges / total_possible_edges if total_possible_edges > 0 else 0.0
    
    def _calculate_coupling(self, community: List[str]) -> float:
        """Calculate coupling score for a community."""
        if len(community) == 0:
            return 0.0
        
        external_edges = 0
        total_edges = 0
        
        for node in community:
            neighbors = list(self.graph.neighbors(node))
            total_edges += len(neighbors)
            external_edges += sum(1 for neighbor in neighbors if neighbor not in community)
        
        return external_edges / total_edges if total_edges > 0 else 0.0
    
    def get_metrics(self) -> Dict[str, float]:
        """Calculate various graph metrics."""
        metrics = {}
        
        # Basic metrics
        metrics['total_nodes'] = self.graph.number_of_nodes()
        metrics['total_edges'] = self.graph.number_of_edges()
        metrics['density'] = nx.density(self.graph)
        
        # Centrality metrics
        if self.graph.number_of_nodes() > 0:
            try:
                metrics['average_clustering'] = nx.average_clustering(self.graph.to_undirected())
            except:
                metrics['average_clustering'] = 0.0
        
        # Dependency metrics
        metrics['max_depth'] = self._calculate_max_depth()
        metrics['circular_dependencies'] = len(list(nx.simple_cycles(self.graph)))
        
        return metrics
    
    def _calculate_max_depth(self) -> int:
        """Calculate the maximum dependency depth."""
        try:
            # Find all nodes with no incoming edges (roots)
            roots = [node for node in self.graph.nodes() if self.graph.in_degree(node) == 0]
            
            if not roots:
                # If no roots, use all nodes
                roots = list(self.graph.nodes())
            
            max_depth = 0
            for root in roots:
                depths = nx.single_source_shortest_path_length(self.graph, root)
                max_depth = max(max_depth, max(depths.values()) if depths else 0)
            
            return max_depth
        except:
            return 0 