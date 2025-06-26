"""
Comprehensive metrics and analytics for code quality and architectural health.
"""

import math
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, Counter

from .models import AnalysisResult, CodeElement, Relationship


class MetricType(str, Enum):
    """Types of metrics that can be calculated."""
    COMPLEXITY = "complexity"
    COUPLING = "coupling"
    COHESION = "cohesion"
    SIZE = "size"
    QUALITY = "quality"
    ARCHITECTURE = "architecture"
    PERFORMANCE = "performance"
    SECURITY = "security"
    MAINTAINABILITY = "maintainability"


@dataclass
class MetricValue:
    """Represents a calculated metric value."""
    name: str
    value: float
    unit: str
    description: str
    category: MetricType
    threshold: Optional[float] = None
    severity: str = "info"  # info, warning, error, critical


@dataclass
class CodeMetrics:
    """Comprehensive code metrics for a codebase."""
    complexity_metrics: Dict[str, float] = field(default_factory=dict)
    coupling_metrics: Dict[str, float] = field(default_factory=dict)
    cohesion_metrics: Dict[str, float] = field(default_factory=dict)
    size_metrics: Dict[str, float] = field(default_factory=dict)
    quality_metrics: Dict[str, float] = field(default_factory=dict)
    architecture_metrics: Dict[str, float] = field(default_factory=dict)
    performance_metrics: Dict[str, float] = field(default_factory=dict)
    security_metrics: Dict[str, float] = field(default_factory=dict)
    maintainability_metrics: Dict[str, float] = field(default_factory=dict)
    
    def get_all_metrics(self) -> List[MetricValue]:
        """Get all metrics as a list of MetricValue objects."""
        metrics = []
        
        for category, metric_dict in [
            (MetricType.COMPLEXITY, self.complexity_metrics),
            (MetricType.COUPLING, self.coupling_metrics),
            (MetricType.COHESION, self.cohesion_metrics),
            (MetricType.SIZE, self.size_metrics),
            (MetricType.QUALITY, self.quality_metrics),
            (MetricType.ARCHITECTURE, self.architecture_metrics),
            (MetricType.PERFORMANCE, self.performance_metrics),
            (MetricType.SECURITY, self.security_metrics),
            (MetricType.MAINTAINABILITY, self.maintainability_metrics)
        ]:
            for name, value in metric_dict.items():
                metrics.append(MetricValue(
                    name=name,
                    value=value,
                    unit=self._get_unit_for_metric(name),
                    description=self._get_description_for_metric(name),
                    category=category,
                    threshold=self._get_threshold_for_metric(name),
                    severity=self._get_severity_for_metric(name, value)
                ))
        
        return metrics

    @staticmethod
    def _get_unit_for_metric(metric_name: str) -> str:
        units = {
            'cyclomatic_complexity': 'complexity units',
            'cognitive_complexity': 'complexity units',
            'nesting_depth': 'levels',
            'coupling': 'dependencies',
            'lcom': 'cohesion units',
            'lines_of_code': 'lines',
            'files': 'files',
            'classes': 'classes',
            'functions': 'functions',
            'coverage': 'percentage',
            'compliance': 'percentage',
            'index': 'score'
        }
        for key, unit in units.items():
            if key in metric_name:
                return unit
        return 'units'

    @staticmethod
    def _get_description_for_metric(metric_name: str) -> str:
        descriptions = {
            'cyclomatic_complexity_avg': 'Average cyclomatic complexity across all code elements',
            'max_nesting_depth': 'Maximum nesting depth found in the codebase',
            'afferent_coupling_avg': 'Average number of incoming dependencies',
            'efferent_coupling_avg': 'Average number of outgoing dependencies',
            'instability_avg': 'Average instability score (higher = more unstable)',
            'lcom_avg': 'Average lack of cohesion of methods',
            'architecture_compliance': 'Percentage of architecture rules followed',
            'maintainability_index': 'Overall maintainability score (0-100)'
        }
        return descriptions.get(metric_name, f'Metric: {metric_name}')

    @staticmethod
    def _get_threshold_for_metric(metric_name: str) -> Optional[float]:
        thresholds = {
            'cyclomatic_complexity_avg': 10.0,
            'max_nesting_depth': 5.0,
            'afferent_coupling_avg': 10.0,
            'efferent_coupling_avg': 10.0,
            'instability_avg': 0.7,
            'lcom_avg': 0.8,
            'architecture_compliance': 0.8,
            'maintainability_index': 50.0
        }
        return thresholds.get(metric_name)

    @staticmethod
    def _get_severity_for_metric(metric_name: str, value: float) -> str:
        threshold = CodeMetrics._get_threshold_for_metric(metric_name)
        if threshold is None:
            return 'info'
        higher_is_better = metric_name in [
            'architecture_compliance', 'maintainability_index', 'test_coverage'
        ]
        if higher_is_better:
            if value >= threshold:
                return 'info'
            elif value >= threshold * 0.8:
                return 'warning'
            else:
                return 'error'
        else:
            if value <= threshold:
                return 'info'
            elif value <= threshold * 1.2:
                return 'warning'
            else:
                return 'error'


class MetricsCalculator:
    """Calculates comprehensive metrics for code analysis."""
    
    def __init__(self):
        self.thresholds = self._initialize_thresholds()
    
    def calculate_all_metrics(self, result: AnalysisResult) -> CodeMetrics:
        """Calculate all metrics for the analysis result."""
        metrics = CodeMetrics()
        
        # Calculate different types of metrics
        metrics.complexity_metrics = self._calculate_complexity_metrics(result)
        metrics.coupling_metrics = self._calculate_coupling_metrics(result)
        metrics.cohesion_metrics = self._calculate_cohesion_metrics(result)
        metrics.size_metrics = self._calculate_size_metrics(result)
        metrics.quality_metrics = self._calculate_quality_metrics(result)
        metrics.architecture_metrics = self._calculate_architecture_metrics(result)
        metrics.performance_metrics = self._calculate_performance_metrics(result)
        metrics.security_metrics = self._calculate_security_metrics(result)
        metrics.maintainability_metrics = self._calculate_maintainability_metrics(result)
        
        return metrics
    
    def _calculate_complexity_metrics(self, result: AnalysisResult) -> Dict[str, float]:
        """Calculate complexity-related metrics."""
        metrics = {}
        
        # Cyclomatic complexity
        total_complexity = sum(
            getattr(element, 'complexity', 1) for element in result.elements
        )
        avg_complexity = total_complexity / len(result.elements) if result.elements else 0
        metrics['cyclomatic_complexity_avg'] = avg_complexity
        metrics['cyclomatic_complexity_total'] = total_complexity
        
        # Cognitive complexity
        cognitive_complexity = sum(
            getattr(element, 'cognitive_complexity', 1) for element in result.elements
        )
        metrics['cognitive_complexity_total'] = cognitive_complexity
        
        # Nesting depth
        max_nesting = max(
            getattr(element, 'nesting_depth', 1) for element in result.elements
        ) if result.elements else 0
        metrics['max_nesting_depth'] = max_nesting
        
        return metrics
    
    def _calculate_coupling_metrics(self, result: AnalysisResult) -> Dict[str, float]:
        """Calculate coupling-related metrics."""
        metrics = {}
        
        # Afferent coupling (incoming dependencies)
        afferent_coupling = defaultdict(int)
        for rel in result.relationships:
            afferent_coupling[rel.target_id] += 1
        
        avg_afferent = sum(afferent_coupling.values()) / len(afferent_coupling) if afferent_coupling else 0
        metrics['afferent_coupling_avg'] = avg_afferent
        metrics['afferent_coupling_max'] = max(afferent_coupling.values()) if afferent_coupling else 0
        
        # Efferent coupling (outgoing dependencies)
        efferent_coupling = defaultdict(int)
        for rel in result.relationships:
            efferent_coupling[rel.source_id] += 1
        
        avg_efferent = sum(efferent_coupling.values()) / len(efferent_coupling) if efferent_coupling else 0
        metrics['efferent_coupling_avg'] = avg_efferent
        metrics['efferent_coupling_max'] = max(efferent_coupling.values()) if efferent_coupling else 0
        
        # Instability (efferent / (efferent + afferent))
        instability_scores = []
        for element_id in set(afferent_coupling.keys()) | set(efferent_coupling.keys()):
            efferent = efferent_coupling.get(element_id, 0)
            afferent = afferent_coupling.get(element_id, 0)
            total = efferent + afferent
            if total > 0:
                instability = efferent / total
                instability_scores.append(instability)
        
        metrics['instability_avg'] = sum(instability_scores) / len(instability_scores) if instability_scores else 0
        
        return metrics
    
    def _calculate_cohesion_metrics(self, result: AnalysisResult) -> Dict[str, float]:
        """Calculate cohesion-related metrics."""
        metrics = {}
        
        # Lack of cohesion of methods (LCOM)
        lcom_scores = []
        for element in result.elements:
            if hasattr(element, 'methods') and element.methods:
                # Simplified LCOM calculation
                method_count = len(element.methods)
                if method_count > 1:
                    # Mock LCOM calculation
                    lcom = method_count * 0.3  # Simplified
                    lcom_scores.append(lcom)
        
        metrics['lcom_avg'] = sum(lcom_scores) / len(lcom_scores) if lcom_scores else 0
        
        return metrics
    
    def _calculate_size_metrics(self, result: AnalysisResult) -> Dict[str, float]:
        """Calculate size-related metrics."""
        metrics = {}
        
        # Lines of code
        total_loc = sum(getattr(element, 'lines_of_code', 0) for element in result.elements)
        metrics['total_lines_of_code'] = total_loc
        
        # Number of files
        metrics['total_files'] = len(result.elements)
        
        # Average file size
        metrics['avg_file_size'] = total_loc / len(result.elements) if result.elements else 0
        
        # Number of classes
        class_count = sum(1 for element in result.elements if element.type == 'class')
        metrics['total_classes'] = class_count
        
        # Number of functions
        function_count = sum(1 for element in result.elements if element.type == 'function')
        metrics['total_functions'] = function_count
        
        return metrics
    
    def _calculate_quality_metrics(self, result: AnalysisResult) -> Dict[str, float]:
        """Calculate quality-related metrics."""
        metrics = {}
        
        # Code duplication (simplified)
        metrics['duplication_ratio'] = 0.05  # Mock value
        
        # Test coverage (if available)
        metrics['test_coverage'] = getattr(result, 'test_coverage', 0.0)
        
        # Documentation coverage
        documented_elements = sum(
            1 for element in result.elements 
            if hasattr(element, 'has_documentation') and element.has_documentation
        )
        metrics['documentation_coverage'] = documented_elements / len(result.elements) if result.elements else 0
        
        return metrics
    
    def _calculate_architecture_metrics(self, result: AnalysisResult) -> Dict[str, float]:
        """Calculate architecture-related metrics."""
        metrics = {}
        
        # Service boundary violations
        boundary_violations = 0
        for rel in result.relationships:
            if hasattr(rel, 'crosses_boundary') and rel.crosses_boundary:
                boundary_violations += 1
        
        metrics['boundary_violations'] = boundary_violations
        
        # Architecture compliance score
        total_relationships = len(result.relationships)
        if total_relationships > 0:
            compliance_score = 1 - (boundary_violations / total_relationships)
            metrics['architecture_compliance'] = compliance_score
        else:
            metrics['architecture_compliance'] = 1.0
        
        # Modularity index
        modules = len(result.service_boundaries) if result.service_boundaries else 1
        metrics['modularity_index'] = modules / len(result.elements) if result.elements else 0
        
        return metrics
    
    def _calculate_performance_metrics(self, result: AnalysisResult) -> Dict[str, float]:
        """Calculate performance-related metrics."""
        metrics = {}
        
        # Memory usage indicators
        metrics['memory_usage_score'] = 0.7  # Mock value
        
        # Performance bottlenecks
        metrics['performance_bottlenecks'] = 2  # Mock value
        
        return metrics
    
    def _calculate_security_metrics(self, result: AnalysisResult) -> Dict[str, float]:
        """Calculate security-related metrics."""
        metrics = {}
        
        # Security vulnerabilities
        metrics['security_vulnerabilities'] = 0  # Mock value
        
        # Input validation coverage
        metrics['input_validation_coverage'] = 0.8  # Mock value
        
        return metrics
    
    def _calculate_maintainability_metrics(self, result: AnalysisResult) -> Dict[str, float]:
        """Calculate maintainability-related metrics."""
        metrics = {}
        
        # Maintainability index (simplified)
        complexity = self._calculate_complexity_metrics(result)
        coupling = self._calculate_coupling_metrics(result)
        
        # Simplified maintainability index calculation
        avg_complexity = complexity.get('cyclomatic_complexity_avg', 1)
        avg_coupling = coupling.get('afferent_coupling_avg', 0) + coupling.get('efferent_coupling_avg', 0)
        
        maintainability_index = 100 - (avg_complexity * 2 + avg_coupling * 3)
        metrics['maintainability_index'] = max(0, maintainability_index)
        
        return metrics
    
    def _initialize_thresholds(self) -> Dict[str, float]:
        """Initialize metric thresholds."""
        return {
            'cyclomatic_complexity_avg': 10.0,
            'max_nesting_depth': 5.0,
            'afferent_coupling_avg': 10.0,
            'efferent_coupling_avg': 10.0,
            'instability_avg': 0.7,
            'lcom_avg': 0.8,
            'architecture_compliance': 0.8,
            'maintainability_index': 50.0
        } 