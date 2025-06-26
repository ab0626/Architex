"""
AI-powered architectural recommendations and optimization suggestions.
"""

import asyncio
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

from ..core.models import AnalysisResult, CodeElement


class RecommendationType(str, Enum):
    """Types of architectural recommendations."""
    PERFORMANCE = "performance"
    SECURITY = "security"
    MAINTAINABILITY = "maintainability"
    SCALABILITY = "scalability"
    ARCHITECTURE = "architecture"
    CODE_QUALITY = "code_quality"
    DEPENDENCY = "dependency"
    TESTING = "testing"


class Priority(str, Enum):
    """Priority levels for recommendations."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class ArchitecturalRecommendation:
    """Represents an AI-generated architectural recommendation."""
    id: str
    type: RecommendationType
    priority: Priority
    title: str
    description: str
    impact: str
    effort: str
    code_examples: List[str]
    references: List[str]
    confidence: float
    affected_elements: List[str]


class AIRecommendations:
    """AI-powered architectural recommendations system."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.llm = self._initialize_llm()
    
    def _initialize_llm(self):
        """Initialize the language model."""
        # Mock implementation for now
        class MockLLM:
            async def ainvoke(self, prompt):
                return self._generate_mock_response(prompt)
            
            def _generate_mock_response(self, prompt):
                class MockResponse:
                    def __init__(self):
                        self.content = '{"recommendations": [{"id": "rec1", "type": "performance", "priority": "high", "title": "Mock Recommendation", "description": "Mock description", "impact": "High", "effort": "Medium", "code_examples": [], "references": [], "confidence": 0.8, "affected_elements": []}]}'
                
                return MockResponse()
        
        return MockLLM()
    
    async def generate_recommendations(self, result: AnalysisResult) -> List[ArchitecturalRecommendation]:
        """Generate comprehensive architectural recommendations."""
        recommendations = []
        
        # Analyze different aspects
        aspects = [
            self._analyze_performance,
            self._analyze_security,
            self._analyze_maintainability,
            self._analyze_scalability,
            self._analyze_architecture_patterns,
            self._analyze_code_quality,
            self._analyze_dependencies,
            self._analyze_testing_coverage
        ]
        
        for analyzer in aspects:
            try:
                aspect_recs = await analyzer(result)
                recommendations.extend(aspect_recs)
            except Exception as e:
                print(f"Error in {analyzer.__name__}: {e}")
        
        return recommendations
    
    async def _analyze_performance(self, result: AnalysisResult) -> List[ArchitecturalRecommendation]:
        """Analyze performance aspects."""
        # Prepare performance analysis data
        analysis_data = {
            'elements_count': len(result.elements),
            'relationships_count': len(result.relationships),
            'metrics': result.metrics,
            'service_boundaries': len(result.service_boundaries)
        }
        
        prompt = f"""
        Analyze this codebase for performance issues and provide recommendations.
        
        Analysis Data: {analysis_data}
        
        Look for:
        1. Performance bottlenecks
        2. Inefficient algorithms
        3. Memory usage issues
        4. Scalability concerns
        5. Database optimization opportunities
        
        Provide recommendations with:
        - Priority (low/medium/high/critical)
        - Impact assessment
        - Effort estimation
        - Code examples
        - References
        
        Format as JSON:
        {{
            "recommendations": [
                {{
                    "id": "string",
                    "type": "performance",
                    "priority": "high",
                    "title": "string",
                    "description": "string",
                    "impact": "string",
                    "effort": "string",
                    "code_examples": ["string"],
                    "references": ["string"],
                    "confidence": 0.8,
                    "affected_elements": ["element_ids"]
                }}
            ]
        }}
        """
        
        try:
            response = await self.llm.ainvoke(prompt)
            data = self._parse_json_response(response.content)
            return [self._create_recommendation(rec) for rec in data.get('recommendations', [])]
        except Exception as e:
            print(f"Error in performance analysis: {e}")
            return []
    
    async def _analyze_security(self, result: AnalysisResult) -> List[ArchitecturalRecommendation]:
        """Analyze security aspects."""
        # Mock security analysis
        return [
            ArchitecturalRecommendation(
                id="sec_001",
                type=RecommendationType.SECURITY,
                priority=Priority.HIGH,
                title="Implement Input Validation",
                description="Add comprehensive input validation to prevent injection attacks",
                impact="High - Prevents security vulnerabilities",
                effort="Medium - Requires code changes",
                code_examples=["# Add validation here"],
                references=["OWASP Top 10"],
                confidence=0.9,
                affected_elements=[]
            )
        ]
    
    async def _analyze_maintainability(self, result: AnalysisResult) -> List[ArchitecturalRecommendation]:
        """Analyze maintainability aspects."""
        # Mock maintainability analysis
        return [
            ArchitecturalRecommendation(
                id="maint_001",
                type=RecommendationType.MAINTAINABILITY,
                priority=Priority.MEDIUM,
                title="Reduce Cyclomatic Complexity",
                description="Break down complex functions into smaller, more manageable pieces",
                impact="Medium - Improves code readability",
                effort="Low - Refactoring required",
                code_examples=["# Split function here"],
                references=["Clean Code principles"],
                confidence=0.8,
                affected_elements=[]
            )
        ]
    
    async def _analyze_scalability(self, result: AnalysisResult) -> List[ArchitecturalRecommendation]:
        """Analyze scalability aspects."""
        return []
    
    async def _analyze_architecture_patterns(self, result: AnalysisResult) -> List[ArchitecturalRecommendation]:
        """Analyze architecture patterns."""
        return []
    
    async def _analyze_code_quality(self, result: AnalysisResult) -> List[ArchitecturalRecommendation]:
        """Analyze code quality."""
        return []
    
    async def _analyze_dependencies(self, result: AnalysisResult) -> List[ArchitecturalRecommendation]:
        """Analyze dependency management."""
        return []
    
    async def _analyze_testing_coverage(self, result: AnalysisResult) -> List[ArchitecturalRecommendation]:
        """Analyze testing coverage."""
        return []
    
    def _create_recommendation(self, data: Dict[str, Any]) -> ArchitecturalRecommendation:
        """Create a recommendation from data."""
        return ArchitecturalRecommendation(
            id=data.get('id', ''),
            type=RecommendationType(data.get('type', 'architecture')),
            priority=Priority(data.get('priority', 'medium')),
            title=data.get('title', ''),
            description=data.get('description', ''),
            impact=data.get('impact', ''),
            effort=data.get('effort', ''),
            code_examples=data.get('code_examples', []),
            references=data.get('references', []),
            confidence=data.get('confidence', 0.5),
            affected_elements=data.get('affected_elements', [])
        )
    
    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """Parse JSON response from LLM."""
        import json
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            if start != -1 and end != 0:
                json_str = response[start:end]
                return json.loads(json_str)
            else:
                return {}
        except json.JSONDecodeError:
            print(f"Failed to parse JSON response: {response}")
            return {} 