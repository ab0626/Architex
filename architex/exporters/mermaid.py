"""
Mermaid diagram exporter for Architex.
"""

from typing import Dict, Any, Optional, List
from pathlib import Path

from .base import BaseExporter
from ..core.models import AnalysisResult, CodeElement, Relationship, ElementType


class MermaidExporter(BaseExporter):
    """Exporter for Mermaid diagrams."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.diagram_type = (config or {}).get('diagram_type', 'graph')  # graph, flowchart, classDiagram
    
    def export(self, analysis_result: AnalysisResult, output_path: Optional[Path] = None) -> str:
        """Export analysis result to Mermaid diagram."""
        if self.diagram_type == 'classDiagram':
            return self._export_class_diagram(analysis_result)
        else:
            return self._export_dependency_graph(analysis_result)
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported output formats."""
        return ['mermaid', 'md']
    
    def _export_dependency_graph(self, analysis_result: AnalysisResult) -> str:
        """Export as dependency graph."""
        lines = ['graph TD']
        
        # Add nodes
        for element in analysis_result.elements:
            node_id = self._sanitize_id(element.id)
            node_label = self._sanitize_label(element.name)
            color = self._get_element_color(element.type.value)
            
            lines.append(f'    {node_id}["{node_label}"]')
        
        # Add edges
        for relationship in analysis_result.relationships:
            source_id = self._sanitize_id(relationship.source_id)
            target_id = self._sanitize_id(relationship.target_id)
            style = self._get_relationship_style(relationship.type.value)
            
            if style == 'dashed':
                lines.append(f'    {source_id} -.-> {target_id}')
            elif style == 'dotted':
                lines.append(f'    {source_id} ..> {target_id}')
            else:
                lines.append(f'    {source_id} --> {target_id}')
        
        return '\n'.join(lines)
    
    def _export_class_diagram(self, analysis_result: AnalysisResult) -> str:
        """Export as class diagram."""
        lines = ['classDiagram']
        
        # Add classes
        for element in analysis_result.elements:
            if element.type == ElementType.CLASS:
                class_id = self._sanitize_id(element.id)
                class_name = self._sanitize_label(element.name)
                
                lines.append(f'    class {class_id} {{')
                lines.append(f'        {class_name}')
                lines.append('    }')
        
        # Add inheritance relationships
        for relationship in analysis_result.relationships:
            if relationship.type.value == 'inherits':
                source_id = self._sanitize_id(relationship.source_id)
                target_id = self._sanitize_id(relationship.target_id)
                lines.append(f'    {source_id} --|> {target_id}')
        
        return '\n'.join(lines)
    
    def _sanitize_id(self, element_id: str) -> str:
        """Sanitize element ID for Mermaid."""
        # Replace special characters with underscores
        sanitized = element_id.replace(':', '_').replace('/', '_').replace('.', '_')
        # Ensure it starts with a letter
        if sanitized and not sanitized[0].isalpha():
            sanitized = 'id_' + sanitized
        return sanitized
    
    def _sanitize_label(self, label: str) -> str:
        """Sanitize label for Mermaid."""
        # Escape quotes and other special characters
        return label.replace('"', '\\"').replace('\n', ' ').replace('\r', ' ') 