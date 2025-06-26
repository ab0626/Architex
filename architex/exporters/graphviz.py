"""
Graphviz diagram exporter for Architex.
"""

from typing import Dict, Any, Optional, List
from pathlib import Path

from .base import BaseExporter
from ..core.models import AnalysisResult, CodeElement, Relationship, ElementType


class GraphvizExporter(BaseExporter):
    """Exporter for Graphviz DOT diagrams."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.layout_engine = (config or {}).get('layout_engine', 'dot')  # dot, neato, fdp, sfdp, twopi, circo
    
    def export(self, analysis_result: AnalysisResult, output_path: Optional[Path] = None) -> str:
        """Export analysis result to Graphviz DOT diagram."""
        return self._export_dot_diagram(analysis_result)
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported output formats."""
        return ['dot', 'gv', 'svg', 'png', 'pdf']
    
    def _export_dot_diagram(self, analysis_result: AnalysisResult) -> str:
        """Export as DOT diagram."""
        lines = [
            f'digraph G {{',
            f'    rankdir=TB;',
            f'    node [shape=box, style=filled, fontname="Arial", fontsize=10];',
            f'    edge [fontname="Arial", fontsize=8];',
            ''
        ]
        
        # Add nodes
        for element in analysis_result.elements:
            node_id = self._sanitize_id(element.id)
            node_label = self._sanitize_label(element.name)
            color = self._get_element_color(element.type.value)
            shape = self._get_element_shape(element.type.value)
            
            lines.append(f'    {node_id} [label="{node_label}", fillcolor="{color}", shape={shape}];')
        
        lines.append('')
        
        # Add edges
        for relationship in analysis_result.relationships:
            source_id = self._sanitize_id(relationship.source_id)
            target_id = self._sanitize_id(relationship.target_id)
            style = self._get_relationship_style(relationship.type.value)
            color = self._get_relationship_color(relationship.type.value)
            
            edge_attrs = []
            if style == 'dashed':
                edge_attrs.append('style=dashed')
            elif style == 'dotted':
                edge_attrs.append('style=dotted')
            
            if color:
                edge_attrs.append(f'color="{color}"')
            
            edge_attr_str = f' [{", ".join(edge_attrs)}]' if edge_attrs else ''
            lines.append(f'    {source_id} -> {target_id}{edge_attr_str};')
        
        lines.append('}')
        return '\n'.join(lines)
    
    def _get_element_shape(self, element_type: str) -> str:
        """Get shape for element type."""
        shape_map = {
            'module': 'box',
            'class': 'record',
            'function': 'ellipse',
            'method': 'ellipse',
            'variable': 'diamond',
            'import': 'parallelogram',
            'package': 'component',
            'interface': 'record',
            'enum': 'record',
            'struct': 'record',
            'namespace': 'box'
        }
        return shape_map.get(element_type, 'box')
    
    def _get_relationship_color(self, relationship_type: str) -> str:
        """Get color for relationship type."""
        color_map = {
            'inherits': '#ff6b6b',
            'implements': '#4ecdc4',
            'depends_on': '#45b7d1',
            'imports': '#96ceb4',
            'calls': '#feca57',
            'uses': '#ff9ff3',
            'contains': '#54a0ff',
            'associates': '#5f27cd',
            'composes': '#00d2d3',
            'aggregates': '#ff9f43'
        }
        return color_map.get(relationship_type, '#000000')
    
    def _sanitize_id(self, element_id: str) -> str:
        """Sanitize element ID for Graphviz."""
        # Replace special characters with underscores
        sanitized = element_id.replace(':', '_').replace('/', '_').replace('.', '_')
        # Ensure it starts with a letter
        if sanitized and not sanitized[0].isalpha():
            sanitized = 'id_' + sanitized
        return sanitized
    
    def _sanitize_label(self, label: str) -> str:
        """Sanitize label for Graphviz."""
        # Escape quotes and other special characters
        return label.replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r') 