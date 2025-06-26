"""
Live analyzer that coordinates real-time analysis with AI features.
"""

import asyncio
import json
from typing import Dict, List, Optional, Any, Callable
from pathlib import Path

from ..core.analyzer import CodebaseAnalyzer
from ..core.models import AnalysisResult
from ..ai.labeler import AILabeler
from ..ai.summarizer import AISummarizer
from ..exporters import MermaidExporter, PlantUMLExporter, GraphvizExporter


class LiveAnalyzer:
    """Coordinates live analysis with AI features and real-time updates."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.analyzer = CodebaseAnalyzer(config)
        self.labeler = AILabeler(config)
        self.summarizer = AISummarizer(config)
        
        # Exporters
        self.exporters = {
            'mermaid': MermaidExporter(),
            'plantuml': PlantUMLExporter(),
            'graphviz': GraphvizExporter()
        }
        
        # State
        self.last_analysis = None
        self.last_labels = {}
        self.last_summaries = {}
        self.callbacks = []
    
    def add_callback(self, callback: Callable[[Dict[str, Any]], None]):
        """Add a callback for analysis updates."""
        self.callbacks.append(callback)
    
    async def analyze_codebase(self, codebase_path: str) -> Dict[str, Any]:
        """Perform full analysis with AI features."""
        print(f"🔍 Analyzing codebase: {codebase_path}")
        
        # Perform core analysis
        result = self.analyzer.analyze(codebase_path)
        self.last_analysis = result
        
        # Generate AI labels
        print("🤖 Generating AI labels...")
        labels = await self.labeler.label_analysis_result(result)
        self.last_labels = labels
        
        # Generate AI summaries
        print("📝 Generating AI summaries...")
        summaries = await self.summarizer.summarize_analysis_result(result)
        self.last_summaries = summaries
        
        # Generate diagrams
        print("🎨 Generating diagrams...")
        diagrams = {}
        for format_name, exporter in self.exporters.items():
            try:
                diagram = exporter.export(result)
                diagrams[format_name] = diagram
            except Exception as e:
                print(f"Error generating {format_name} diagram: {e}")
                diagrams[format_name] = ""
        
        # Prepare response
        response = {
            'analysis': result.dict(),
            'labels': {k: v.__dict__ for k, v in labels.items()},
            'summaries': {k: v.__dict__ for k, v in summaries.items()},
            'diagrams': diagrams,
            'metadata': {
                'codebase_path': codebase_path,
                'timestamp': asyncio.get_event_loop().time(),
                'elements_count': len(result.elements),
                'relationships_count': len(result.relationships),
                'service_boundaries_count': len(result.service_boundaries)
            }
        }
        
        # Notify callbacks
        for callback in self.callbacks:
            try:
                callback(response)
            except Exception as e:
                print(f"Error in callback: {e}")
        
        return response
    
    async def analyze_incremental(self, changed_file: Path, event_type: str) -> Optional[Dict[str, Any]]:
        """Perform incremental analysis for file changes."""
        if not self.last_analysis:
            return None
        
        print(f"🔄 Incremental analysis for {changed_file} ({event_type})")
        
        # For now, perform full analysis (can be optimized later)
        return await self.analyze_codebase(str(self.last_analysis.metadata.get('codebase_path', '.')))
    
    def get_analysis_summary(self) -> Dict[str, Any]:
        """Get a summary of the current analysis."""
        if not self.last_analysis:
            return {'status': 'no_analysis'}
        
        return {
            'status': 'analyzed',
            'elements_count': len(self.last_analysis.elements),
            'relationships_count': len(self.last_analysis.relationships),
            'service_boundaries_count': len(self.last_analysis.service_boundaries),
            'labels_count': len(self.last_labels),
            'summaries_count': len(self.last_summaries),
            'metrics': self.last_analysis.metrics
        }
    
    def get_element_details(self, element_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific element."""
        if not self.last_analysis:
            return None
        
        # Find element
        element = self.last_analysis.get_element_by_id(element_id)
        if not element:
            return None
        
        # Get relationships
        relationships = self.last_analysis.get_relationships_for_element(element_id)
        
        # Get AI label
        label = self.last_labels.get(element_id)
        
        return {
            'element': element.dict(),
            'relationships': [rel.dict() for rel in relationships],
            'label': label.__dict__ if label else None
        }
    
    def get_service_boundary_details(self, boundary_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a service boundary."""
        if not self.last_analysis:
            return None
        
        # Find boundary
        boundary = None
        for b in self.last_analysis.service_boundaries:
            if b.name == boundary_name:
                boundary = b
                break
        
        if not boundary:
            return None
        
        # Get elements in boundary
        elements = []
        for element_id in boundary.elements:
            element = self.last_analysis.get_element_by_id(element_id)
            if element:
                elements.append(element.dict())
        
        return {
            'boundary': boundary.dict(),
            'elements': elements,
            'summary': self.last_summaries.get(boundary_name, {}).__dict__
        }
    
    def export_diagram(self, format_name: str, output_path: Optional[Path] = None) -> str:
        """Export diagram in specified format."""
        if not self.last_analysis:
            raise ValueError("No analysis available")
        
        exporter = self.exporters.get(format_name)
        if not exporter:
            raise ValueError(f"Unsupported format: {format_name}")
        
        return exporter.export(self.last_analysis, output_path)
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported export formats."""
        return list(self.exporters.keys()) 