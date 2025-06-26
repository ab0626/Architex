"""
Base exporter class for diagram generation.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pathlib import Path

from ..core.models import AnalysisResult


class BaseExporter(ABC):
    """Base class for diagram exporters."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
    
    @abstractmethod
    def export(self, analysis_result: AnalysisResult, output_path: Optional[Path] = None) -> str:
        """Export analysis result to diagram format."""
        pass
    
    @abstractmethod
    def get_supported_formats(self) -> list[str]:
        """Get list of supported output formats."""
        pass
    
    def _get_element_color(self, element_type: str) -> str:
        """Get color for element type."""
        color_map = {
            'module': '#e1f5fe',
            'class': '#f3e5f5', 
            'function': '#e8f5e8',
            'method': '#fff3e0',
            'variable': '#fce4ec',
            'import': '#f1f8e9',
            'package': '#e0f2f1',
            'interface': '#fafafa',
            'enum': '#fff8e1',
            'struct': '#f9fbe7',
            'namespace': '#f5f5f5'
        }
        return color_map.get(element_type, '#ffffff')
    
    def _get_relationship_style(self, relationship_type: str) -> str:
        """Get style for relationship type."""
        style_map = {
            'inherits': 'solid',
            'implements': 'dashed',
            'depends_on': 'dotted',
            'imports': 'solid',
            'calls': 'solid',
            'uses': 'dashed',
            'contains': 'solid',
            'associates': 'dotted',
            'composes': 'solid',
            'aggregates': 'dashed'
        }
        return style_map.get(relationship_type, 'solid') 