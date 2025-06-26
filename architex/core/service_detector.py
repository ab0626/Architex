"""
Service detection and architectural pattern analysis.
"""

import re
from typing import Dict, List, Set, Optional, Tuple, Any
from pathlib import Path
from .models import (
    CodeElement, ServiceBoundary, ServiceType, Relationship, 
    RelationshipType, AnalysisResult, ArchitectureLayer, ElementType
)
import uuid


class ServiceDetector:
    """Detects service boundaries and architectural patterns in code."""
    
    def __init__(self):
        self.service_patterns = {
            ServiceType.API_SERVICE: [
                r'api[_-]?service', r'controller', r'endpoint', r'route',
                r'@app\.route', r'@api\.route', r'@RestController', r'@Controller',
                r'FastAPI', r'Flask', r'Django', r'Express', r'Spring'
            ],
            ServiceType.DATA_SERVICE: [
                r'data[_-]?service', r'repository', r'dao', r'database',
                r'@Repository', r'@Entity', r'@Table', r'Model', r'Repository',
                r'DataAccess', r'Database', r'ORM', r'EntityManager'
            ],
            ServiceType.BUSINESS_SERVICE: [
                r'business[_-]?service', r'service[_-]?layer', r'domain[_-]?service',
                r'@Service', r'@Component', r'@BusinessLogic', r'Service',
                r'BusinessLogic', r'DomainService', r'ApplicationService'
            ],
            ServiceType.INFRASTRUCTURE_SERVICE: [
                r'infrastructure[_-]?service', r'config', r'util', r'helper',
                r'@Configuration', r'@Component', r'@Utility', r'Config',
                r'Infrastructure', r'Utility', r'Helper', r'Common'
            ],
            ServiceType.UTILITY_SERVICE: [
                r'utility[_-]?service', r'util', r'helper', r'tool',
                r'@Utility', r'@Helper', r'@Tool', r'Utility', r'Helper',
                r'Tool', r'Common', r'Shared'
            ]
        }
        
        self.layer_patterns = {
            'presentation': [r'controller', r'view', r'ui', r'presentation', r'@Controller', r'@RestController'],
            'application': [r'service', r'application', r'@Service', r'@Component'],
            'domain': [r'domain', r'entity', r'model', r'@Entity', r'@Model'],
            'infrastructure': [r'repository', r'dao', r'config', r'@Repository', r'@Configuration']
        }
    
    def detect_services(self, analysis_result: AnalysisResult) -> List[ServiceBoundary]:
        """Detect service boundaries in the codebase."""
        services = []
        
        # Group elements by potential service boundaries
        service_groups = self._group_elements_by_service(analysis_result.elements)
        
        for service_name, elements in service_groups.items():
            service_type = self._classify_service_type(elements)
            
            # Calculate service metrics
            cohesion_score = self._calculate_cohesion(elements, analysis_result.relationships)
            coupling_score = self._calculate_coupling(elements, analysis_result.relationships)
            complexity_score = self._calculate_complexity(elements)
            
            # Find external dependencies
            external_deps = self._find_external_dependencies(elements, analysis_result.relationships)
            
            service = ServiceBoundary(
                id=str(uuid.uuid4()),
                name=service_name,
                type=service_type,
                elements={elem.id for elem in elements},
                dependencies=external_deps,
                cohesion_score=cohesion_score,
                coupling_score=coupling_score,
                complexity_score=complexity_score,
                metadata={
                    'element_count': len(elements),
                    'languages': list(set(elem.language.value for elem in elements)),
                    'file_count': len(set(elem.file_path for elem in elements if elem.file_path))
                }
            )
            services.append(service)
        
        return services
    
    def detect_architectural_layers(self, analysis_result: AnalysisResult) -> List[ArchitectureLayer]:
        """Detect architectural layers in the codebase."""
        layers = []
        
        # Group elements by architectural layer
        layer_groups = self._group_elements_by_layer(analysis_result.elements)
        
        for layer_name, elements in layer_groups.items():
            layer_level = self._get_layer_level(layer_name)
            
            # Find dependencies on other layers
            layer_deps = self._find_layer_dependencies(elements, analysis_result.relationships, layer_groups)
            
            layer = ArchitectureLayer(
                id=str(uuid.uuid4()),
                name=layer_name,
                level=layer_level,
                elements={elem.id for elem in elements},
                dependencies=layer_deps,
                metadata={
                    'element_count': len(elements),
                    'languages': list(set(elem.language.value for elem in elements))
                }
            )
            layers.append(layer)
        
        return layers
    
    def _group_elements_by_service(self, elements: List[CodeElement]) -> Dict[str, List[CodeElement]]:
        """Group elements by potential service boundaries."""
        service_groups = {}
        
        for element in elements:
            service_name = self._identify_service_name(element)
            if service_name not in service_groups:
                service_groups[service_name] = []
            service_groups[service_name].append(element)
        
        return service_groups
    
    def _identify_service_name(self, element: CodeElement) -> str:
        """Identify the service name for an element."""
        # Check file path for service indicators
        if element.file_path:
            path_parts = element.file_path.parts
            for part in path_parts:
                if any(re.search(pattern, part.lower()) for patterns in self.service_patterns.values() for pattern in patterns):
                    return part
        
        # Check element name for service indicators
        element_name = element.name.lower()
        for service_type, patterns in self.service_patterns.items():
            if any(re.search(pattern, element_name) for pattern in patterns):
                return element.name
        
        # Check module/namespace
        if element.module:
            module_parts = element.module.split('.')
            for part in module_parts:
                if any(re.search(pattern, part.lower()) for patterns in self.service_patterns.values() for pattern in patterns):
                    return part
        
        # Default to file-based grouping
        if element.file_path:
            return element.file_path.parent.name if element.file_path.parent.name else element.file_path.stem
        
        return "default_service"
    
    def _classify_service_type(self, elements: List[CodeElement]) -> ServiceType:
        """Classify the type of service based on its elements."""
        service_indicators = {service_type: 0 for service_type in ServiceType}
        
        for element in elements:
            element_name = element.name.lower()
            element_type = element.type.value.lower()
            
            for service_type, patterns in self.service_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, element_name) or re.search(pattern, element_type):
                        service_indicators[service_type] += 1
        
        # Return the service type with the highest score
        return max(service_indicators.items(), key=lambda x: x[1])[0]
    
    def _group_elements_by_layer(self, elements: List[CodeElement]) -> Dict[str, List[CodeElement]]:
        """Group elements by architectural layer."""
        layer_groups = {
            'presentation': [],
            'application': [],
            'domain': [],
            'infrastructure': []
        }
        
        for element in elements:
            layer_name = self._identify_layer(element)
            if layer_name in layer_groups:
                layer_groups[layer_name].append(element)
        
        return layer_groups
    
    def _identify_layer(self, element: CodeElement) -> str:
        """Identify the architectural layer for an element."""
        element_name = element.name.lower()
        element_type = element.type.value.lower()
        
        for layer_name, patterns in self.layer_patterns.items():
            for pattern in patterns:
                if re.search(pattern, element_name) or re.search(pattern, element_type):
                    return layer_name
        
        # Default classification based on element type
        if element.type.value in ['controller', 'view']:
            return 'presentation'
        elif element.type.value in ['service', 'component']:
            return 'application'
        elif element.type.value in ['entity', 'model', 'domain']:
            return 'domain'
        elif element.type.value in ['repository', 'dao', 'config']:
            return 'infrastructure'
        
        return 'application'  # Default layer
    
    def _get_layer_level(self, layer_name: str) -> int:
        """Get the level of an architectural layer (0 = bottom, higher = top)."""
        layer_levels = {
            'infrastructure': 0,
            'domain': 1,
            'application': 2,
            'presentation': 3
        }
        return layer_levels.get(layer_name, 1)
    
    def _calculate_cohesion(self, elements: List[CodeElement], relationships: List[Relationship]) -> float:
        """Calculate cohesion score for a service (0.0 to 1.0)."""
        if len(elements) <= 1:
            return 1.0
        
        internal_relationships = 0
        total_possible_relationships = len(elements) * (len(elements) - 1) / 2
        
        element_ids = {elem.id for elem in elements}
        
        for rel in relationships:
            if rel.source_id in element_ids and rel.target_id in element_ids:
                internal_relationships += 1
        
        return min(1.0, internal_relationships / total_possible_relationships if total_possible_relationships > 0 else 0.0)
    
    def _calculate_coupling(self, elements: List[CodeElement], relationships: List[Relationship]) -> float:
        """Calculate coupling score for a service (0.0 to 1.0)."""
        if not elements:
            return 0.0
        
        external_relationships = 0
        element_ids = {elem.id for elem in elements}
        
        for rel in relationships:
            if (rel.source_id in element_ids and rel.target_id not in element_ids) or \
               (rel.target_id in element_ids and rel.source_id not in element_ids):
                external_relationships += 1
        
        return min(1.0, external_relationships / len(elements))
    
    def _calculate_complexity(self, elements: List[CodeElement]) -> float:
        """Calculate complexity score for a service."""
        if not elements:
            return 0.0
        
        # Simple complexity calculation based on element types and counts
        complexity_factors = {
            ElementType.CLASS: 2.0,
            ElementType.FUNCTION: 1.0,
            ElementType.METHOD: 1.5,
            ElementType.INTERFACE: 1.5,
            ElementType.ENUM: 0.5,
            ElementType.STRUCT: 1.5
        }
        
        total_complexity = 0.0
        for element in elements:
            total_complexity += complexity_factors.get(element.type, 1.0)
        
        return total_complexity / len(elements)
    
    def _find_external_dependencies(self, elements: List[CodeElement], relationships: List[Relationship]) -> Set[str]:
        """Find external dependencies for a service."""
        external_deps = set()
        element_ids = {elem.id for elem in elements}
        
        for rel in relationships:
            if rel.source_id in element_ids and rel.target_id not in element_ids:
                external_deps.add(rel.target_id)
            elif rel.target_id in element_ids and rel.source_id not in element_ids:
                external_deps.add(rel.source_id)
        
        return external_deps
    
    def _find_layer_dependencies(self, elements: List[CodeElement], relationships: List[Relationship], 
                                layer_groups: Dict[str, List[CodeElement]]) -> Set[str]:
        """Find dependencies on other layers."""
        layer_deps = set()
        element_ids = {elem.id for elem in elements}
        
        for rel in relationships:
            if rel.source_id in element_ids:
                # Find which layer the target belongs to
                for layer_name, layer_elements in layer_groups.items():
                    if any(elem.id == rel.target_id for elem in layer_elements):
                        layer_deps.add(layer_name)
                        break
        
        return layer_deps
    
    def detect_microservices(self, analysis_result: AnalysisResult) -> List[ServiceBoundary]:
        """Detect potential microservices in the codebase."""
        # This is a simplified microservice detection
        # In practice, this would be more sophisticated
        services = self.detect_services(analysis_result)
        
        # Filter for services that might be microservices
        microservices = []
        for service in services:
            # Criteria for microservice detection
            is_microservice = (
                service.cohesion_score > 0.7 and  # High cohesion
                service.coupling_score < 0.3 and  # Low coupling
                service.metadata.get('element_count', 0) > 5 and  # Sufficient size
                len(service.dependencies) > 0  # Has external dependencies
            )
            
            if is_microservice:
                service.type = ServiceType.API_SERVICE  # Mark as API service
                microservices.append(service)
        
        return microservices
    
    def detect_anti_patterns(self, analysis_result: AnalysisResult) -> List[Dict[str, Any]]:
        """Detect architectural anti-patterns."""
        anti_patterns = []
        
        # Detect God Objects (classes with too many methods)
        for element in analysis_result.elements:
            if element.type == ElementType.CLASS:
                # Count methods in the same file
                methods_in_file = [
                    e for e in analysis_result.elements 
                    if e.file_path == element.file_path and e.type == ElementType.METHOD
                ]
                
                if len(methods_in_file) > 20:  # Threshold for God Object
                    anti_patterns.append({
                        'type': 'god_object',
                        'element_id': element.id,
                        'element_name': element.name,
                        'severity': 'high',
                        'description': f'Class {element.name} has {len(methods_in_file)} methods (God Object anti-pattern)'
                    })
        
        # Detect Circular Dependencies
        if analysis_result.dependency_graph:
            for cycle in analysis_result.dependency_graph.cycles:
                anti_patterns.append({
                    'type': 'circular_dependency',
                    'element_ids': cycle,
                    'severity': 'high',
                    'description': f'Circular dependency detected involving {len(cycle)} elements'
                })
        
        # Detect High Coupling
        for service in analysis_result.service_boundaries:
            if service.coupling_score > 0.8:
                anti_patterns.append({
                    'type': 'high_coupling',
                    'service_id': service.id,
                    'service_name': service.name,
                    'severity': 'medium',
                    'description': f'Service {service.name} has high coupling score: {service.coupling_score:.2f}'
                })
        
        return anti_patterns 