"""
PlantUML diagram exporter for Architex.
"""

from typing import Dict, Any, Optional, List
from pathlib import Path

from .base import BaseExporter
from ..core.models import AnalysisResult, CodeElement, Relationship, ElementType


class PlantUMLExporter(BaseExporter):
    """Exporter for PlantUML diagrams."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.diagram_type = (config or {}).get('diagram_type', 'component')  # component, class, package
    
    def export(self, analysis_result: AnalysisResult, output_path: Optional[Path] = None) -> str:
        """Export analysis result to PlantUML diagram."""
        if self.diagram_type == 'class':
            return self._export_class_diagram(analysis_result)
        elif self.diagram_type == 'package':
            return self._export_package_diagram(analysis_result)
        else:
            return self._export_component_diagram(analysis_result)
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported output formats."""
        return ['plantuml', 'puml']
    
    def _export_component_diagram(self, analysis_result: AnalysisResult) -> str:
        """Export as component diagram."""
        lines = ['@startuml', '!theme plain']
        
        # Add components
        for element in analysis_result.elements:
            if element.type in [ElementType.MODULE, ElementType.PACKAGE, ElementType.CLASS]:
                component_id = self._sanitize_id(element.id)
                component_name = self._sanitize_label(element.name)
                color = self._get_element_color(element.type.value)
                
                lines.append(f'component "{component_name}" as {component_id} #{color}')
        
        # Add relationships
        for relationship in analysis_result.relationships:
            source_id = self._sanitize_id(relationship.source_id)
            target_id = self._sanitize_id(relationship.target_id)
            style = self._get_relationship_style(relationship.type.value)
            
            arrow = self._get_plantuml_arrow(relationship.type.value, style)
            lines.append(f'{source_id} {arrow} {target_id}')
        
        lines.append('@enduml')
        return '\n'.join(lines)
    
    def _export_class_diagram(self, analysis_result: AnalysisResult) -> str:
        """Export as class diagram."""
        lines = ['@startuml', '!theme plain']
        
        # Add classes
        for element in analysis_result.elements:
            if element.type == ElementType.CLASS:
                class_id = self._sanitize_id(element.id)
                class_name = self._sanitize_label(element.name)
                color = self._get_element_color(element.type.value)
                
                lines.append(f'class "{class_name}" as {class_id} #{color} {{')
                lines.append('}')
        
        # Add inheritance relationships
        for relationship in analysis_result.relationships:
            if relationship.type.value == 'inherits':
                source_id = self._sanitize_id(relationship.source_id)
                target_id = self._sanitize_id(relationship.target_id)
                lines.append(f'{source_id} --|> {target_id}')
        
        lines.append('@enduml')
        return '\n'.join(lines)
    
    def _export_package_diagram(self, analysis_result: AnalysisResult) -> str:
        """Export as package diagram."""
        lines = ['@startuml', '!theme plain']
        
        # Group elements by module/package
        packages = {}
        for element in analysis_result.elements:
            package_name = element.module or 'default'
            if package_name not in packages:
                packages[package_name] = []
            packages[package_name].append(element)
        
        # Add packages
        for package_name, elements in packages.items():
            lines.append(f'package "{package_name}" {{')
            for element in elements:
                element_id = self._sanitize_id(element.id)
                element_name = self._sanitize_label(element.name)
                lines.append(f'    class "{element_name}" as {element_id}')
            lines.append('}')
        
        # Add relationships
        for relationship in analysis_result.relationships:
            source_id = self._sanitize_id(relationship.source_id)
            target_id = self._sanitize_id(relationship.target_id)
            arrow = self._get_plantuml_arrow(relationship.type.value, 'solid')
            lines.append(f'{source_id} {arrow} {target_id}')
        
        lines.append('@enduml')
        return '\n'.join(lines)
    
    def _get_plantuml_arrow(self, relationship_type: str, style: str) -> str:
        """Get PlantUML arrow for relationship type."""
        arrow_map = {
            'inherits': '--|>',
            'implements': '..|>',
            'depends_on': '..>',
            'imports': '-->',
            'calls': '-->',
            'uses': '..>',
            'contains': '*--',
            'associates': '..>',
            'composes': '*--',
            'aggregates': 'o--'
        }
        return arrow_map.get(relationship_type, '-->')
    
    def _sanitize_id(self, element_id: str) -> str:
        """Sanitize element ID for PlantUML."""
        # Replace special characters with underscores
        sanitized = element_id.replace(':', '_').replace('/', '_').replace('.', '_')
        # Ensure it starts with a letter
        if sanitized and not sanitized[0].isalpha():
            sanitized = 'id_' + sanitized
        return sanitized
    
    def _sanitize_label(self, label: str) -> str:
        """Sanitize label for PlantUML."""
        # Escape quotes and other special characters
        return label.replace('"', '\\"').replace('\n', ' ').replace('\r', ' ') 