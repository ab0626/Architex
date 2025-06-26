"""
Main analyzer class for Architex.
"""

import os
from pathlib import Path
from typing import Dict, List, Optional, Set, Union
from tqdm import tqdm
import uuid

from .models import AnalysisResult, CodeElement, Relationship
from .parsers import ParserRegistry
from .graph_builder import DependencyGraph


class CodebaseAnalyzer:
    """Main analyzer for codebases."""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.parser_registry = ParserRegistry()
        self.ignore_patterns = self.config.get('ignore_patterns', [
            '__pycache__', 'node_modules', '.git', '.svn', '.hg',
            '*.pyc', '*.pyo', '*.pyd', '*.so', '*.dll', '*.dylib',
            '*.exe', '*.class', '*.jar', '*.war', '*.ear'
        ])
        self.max_depth = self.config.get('max_depth', 10)
    
    def analyze(self, codebase_path: Union[str, Path]) -> AnalysisResult:
        """Analyze a codebase and return analysis results."""
        codebase_path = Path(codebase_path)
        
        if not codebase_path.exists():
            raise ValueError(f"Codebase path does not exist: {codebase_path}")
        
        print(f"Analyzing codebase: {codebase_path}")
        
        # Find all source files
        source_files = self._find_source_files(codebase_path)
        print(f"Found {len(source_files)} source files")
        
        # Parse all files
        all_elements = []
        for file_path in tqdm(source_files, desc="Parsing files"):
            elements = self._parse_file(file_path)
            all_elements.extend(elements)
        
        print(f"Extracted {len(all_elements)} code elements")
        
        # Build dependency graph
        graph = DependencyGraph()
        graph.build_from_elements(all_elements)
        
        # Detect service boundaries
        service_boundaries = graph.detect_service_boundaries()
        print(f"Detected {len(service_boundaries)} service boundaries")
        
        # Calculate metrics
        metrics = graph.get_metrics()
        
        # Create analysis result
        result = AnalysisResult(
            id=str(uuid.uuid4()),
            elements=all_elements,
            relationships=graph.relationships,
            service_boundaries=service_boundaries,
            metrics=metrics,
            metadata={
                'codebase_path': str(codebase_path),
                'total_files': len(source_files),
                'supported_languages': self.parser_registry.get_supported_languages(),
                "languages": self.parser_registry.get_supported_languages()
            }
        )
        
        return result
    
    def _find_source_files(self, codebase_path: Path) -> List[Path]:
        """Find all source files in the codebase."""
        source_files = []
        
        for root, dirs, files in os.walk(codebase_path):
            # Skip ignored directories
            dirs[:] = [d for d in dirs if not self._should_ignore(d)]
            
            for file in files:
                file_path = Path(root) / file
                if not self._should_ignore(file) and self._is_source_file(file_path):
                    source_files.append(file_path)
        
        return source_files
    
    def _should_ignore(self, name: str) -> bool:
        """Check if a file or directory should be ignored."""
        for pattern in self.ignore_patterns:
            if pattern.startswith('*'):
                # File extension pattern
                if name.endswith(pattern[1:]):
                    return True
            else:
                # Directory or file name pattern
                if pattern in name:
                    return True
        return False
    
    def _is_source_file(self, file_path: Path) -> bool:
        """Check if a file is a source file that can be parsed."""
        parser = self.parser_registry.get_parser_for_file(file_path)
        return parser is not None
    
    def _parse_file(self, file_path: Path) -> List[CodeElement]:
        """Parse a single file and extract code elements."""
        parser = self.parser_registry.get_parser_for_file(file_path)
        
        if parser is None:
            return []
        
        try:
            elements = parser.parse_file(file_path)
            return elements
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return []
    
    def analyze_language(self, codebase_path: Union[str, Path], language: str) -> AnalysisResult:
        """Analyze a codebase for a specific language only."""
        # This would filter files by language and analyze only those
        # For now, we'll use the general analyze method
        return self.analyze(codebase_path)
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported programming languages."""
        return self.parser_registry.get_supported_languages()
    
    def add_custom_parser(self, language: str, parser):
        """Add a custom parser for a specific language."""
        self.parser_registry.register_parser(language, parser)
    
    def set_ignore_patterns(self, patterns: List[str]):
        """Set custom ignore patterns."""
        self.ignore_patterns = patterns
    
    def set_max_depth(self, depth: int):
        """Set maximum analysis depth."""
        self.max_depth = depth 