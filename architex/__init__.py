"""
Architex - Automated System Design Diagram Generator

A powerful developer tool that automatically generates high-level system design 
diagrams from any codebase by analyzing structure, dependencies, and relationships.
"""

__version__ = "0.1.0"
__author__ = "Architex Team"
__email__ = "team@architex.dev"

from .core.analyzer import CodebaseAnalyzer
from .core.models import AnalysisResult, CodeElement, Relationship
from .exporters import DiagramExporter

__all__ = [
    "CodebaseAnalyzer",
    "AnalysisResult", 
    "CodeElement",
    "Relationship",
    "DiagramExporter",
] 