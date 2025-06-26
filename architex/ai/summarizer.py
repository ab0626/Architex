"""
AI-powered system module summarization.
"""

import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from pathlib import Path

from ..core.models import AnalysisResult, CodeElement


@dataclass
class ModuleSummary:
    """Represents an AI-generated summary of a module."""
    module_name: str
    summary: str
    key_components: List[str]
    responsibilities: List[str]
    dependencies: List[str]
    complexity_score: float
    recommendations: List[str]


class AISummarizer:
    """AI-powered module summarization system."""
    
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
                return type('MockResponse', (), {
                    'content': '{"summary": "Mock module summary", "key_components": ["Component1"], "responsibilities": ["Mock responsibility"], "dependencies": [], "complexity_score": 0.5, "recommendations": ["Mock recommendation"]}'
                })()
        
        return MockLLM()
    
    async def summarize_module(self, module_name: str, elements: List[CodeElement], relationships: List) -> ModuleSummary:
        """Generate a summary for a specific module."""
        # Prepare module data
        module_elements = [elem for elem in elements if elem.module == module_name]
        
        # Generate summary using AI
        summary_data = await self._generate_summary(module_name, module_elements, relationships)
        
        return ModuleSummary(
            module_name=module_name,
            summary=summary_data.get("summary", ""),
            key_components=summary_data.get("key_components", []),
            responsibilities=summary_data.get("responsibilities", []),
            dependencies=summary_data.get("dependencies", []),
            complexity_score=summary_data.get("complexity_score", 0.5),
            recommendations=summary_data.get("recommendations", [])
        )
    
    async def summarize_analysis_result(self, result: AnalysisResult) -> Dict[str, ModuleSummary]:
        """Generate summaries for all modules in an analysis result."""
        summaries = {}
        
        # Group elements by module
        modules = {}
        for element in result.elements:
            module_name = element.module or "default"
            if module_name not in modules:
                modules[module_name] = []
            modules[module_name].append(element)
        
        # Generate summaries for each module
        for module_name, elements in modules.items():
            summary = await self.summarize_module(module_name, elements, result.relationships)
            summaries[module_name] = summary
        
        return summaries
    
    async def _generate_summary(self, module_name: str, elements: List[CodeElement], relationships: List) -> Dict[str, Any]:
        """Generate AI summary for a module."""
        # Prepare data for AI
        elements_data = [
            {
                "name": elem.name,
                "type": elem.type.value,
                "file": str(elem.file_path) if elem.file_path else "unknown"
            }
            for elem in elements
        ]
        
        # Create prompt
        prompt = f"""
        Analyze this module and provide a comprehensive summary.
        
        Module: {module_name}
        Elements: {elements_data}
        
        Please provide:
        1. A concise summary of the module's purpose
        2. Key components and their roles
        3. Main responsibilities
        4. External dependencies
        5. Complexity assessment (0.0-1.0)
        6. Improvement recommendations
        
        Format as JSON:
        {{
            "summary": "string",
            "key_components": ["string"],
            "responsibilities": ["string"],
            "dependencies": ["string"],
            "complexity_score": 0.5,
            "recommendations": ["string"]
        }}
        """
        
        try:
            response = await self.llm.ainvoke(prompt)
            return self._parse_json_response(response.content)
        except Exception as e:
            print(f"Error generating summary for module {module_name}: {e}")
            return {
                "summary": f"Error generating summary for {module_name}",
                "key_components": [],
                "responsibilities": [],
                "dependencies": [],
                "complexity_score": 0.5,
                "recommendations": ["Fix AI summarization"]
            }
    
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