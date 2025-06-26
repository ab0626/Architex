"""
Diagram exporters for Architex.
"""

from .base import BaseExporter
from .mermaid import MermaidExporter
from .plantuml import PlantUMLExporter
from .graphviz import GraphvizExporter
from typing import Dict, Any, Optional
from pathlib import Path
from ..core.models import AnalysisResult


class DiagramExporter:
    """Factory class for diagram exporters."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.exporters = {
            'mermaid': MermaidExporter(config),
            'plantuml': PlantUMLExporter(config),
            'graphviz': GraphvizExporter(config)
        }
    
    def export(self, analysis_result: AnalysisResult, format: str = 'mermaid', 
               output_path: Optional[Path] = None) -> str:
        """Export analysis result to specified format."""
        if format not in self.exporters:
            raise ValueError(f"Unsupported format: {format}. Supported formats: {list(self.exporters.keys())}")
        
        return self.exporters[format].export(analysis_result, output_path)
    
    def get_supported_formats(self) -> list[str]:
        """Get list of supported output formats."""
        return list(self.exporters.keys())
    
    def get_exporter(self, format: str) -> BaseExporter:
        """Get exporter instance for specified format."""
        if format not in self.exporters:
            raise ValueError(f"Unsupported format: {format}")
        return self.exporters[format]


__all__ = [
    "BaseExporter",
    "MermaidExporter", 
    "PlantUMLExporter",
    "GraphvizExporter",
    "DiagramExporter",
] 