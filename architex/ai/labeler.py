"""
AI-powered component labeling using LangChain.
"""

import os
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from pathlib import Path

# Try to import LangChain components, with fallbacks
try:
    from langchain.chat_models import ChatOpenAI, ChatAnthropic
    from langchain.prompts import PromptTemplate
    from langchain.cache import RedisCache
    from langchain.callbacks import get_openai_callback
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    print("Warning: LangChain not available. Using mock implementation.")

from ..core.models import CodeElement, AnalysisResult


@dataclass
class ComponentLabel:
    """Represents an AI-generated label for a component."""
    element_id: str
    label: str
    description: str
    category: str
    confidence: float
    reasoning: str


class AILabeler:
    """AI-powered component labeling system."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.llm = self._initialize_llm()
        self.cache = self._initialize_cache()
        
        # Templates for different labeling tasks
        self.component_label_template = PromptTemplate(
            input_variables=["element_name", "element_type", "file_path", "code_context"],
            template="""
            Analyze this code element and provide a meaningful label and description.
            
            Element Name: {element_name}
            Element Type: {element_type}
            File Path: {file_path}
            Code Context: {code_context}
            
            Please provide:
            1. A concise, descriptive label (2-4 words)
            2. A brief description of the component's purpose
            3. The architectural category (e.g., "Service", "Model", "Controller", "Utility", "Interface")
            4. Your confidence level (0.0-1.0)
            5. Brief reasoning for your classification
            
            Format your response as JSON:
            {{
                "label": "string",
                "description": "string", 
                "category": "string",
                "confidence": 0.95,
                "reasoning": "string"
            }}
            """
        ) if LANGCHAIN_AVAILABLE else None
        
        self.service_boundary_template = PromptTemplate(
            input_variables=["elements", "relationships"],
            template="""
            Analyze these code elements and their relationships to identify service boundaries.
            
            Elements: {elements}
            Relationships: {relationships}
            
            Group these elements into logical service boundaries and provide:
            1. Service name
            2. Service description
            3. Key responsibilities
            4. External dependencies
            
            Format as JSON:
            {{
                "services": [
                    {{
                        "name": "string",
                        "description": "string",
                        "responsibilities": ["string"],
                        "dependencies": ["string"],
                        "elements": ["element_ids"]
                    }}
                ]
            }}
            """
        ) if LANGCHAIN_AVAILABLE else None
    
    def _initialize_llm(self):
        """Initialize the language model."""
        if not LANGCHAIN_AVAILABLE:
            return self._create_mock_llm()
        
        # Try OpenAI first, then Anthropic, then fallback
        try:
            if os.getenv("OPENAI_API_KEY"):
                return ChatOpenAI(
                    model_name=self.config.get("openai_model", "gpt-4"),
                    temperature=0.1,
                    max_tokens=1000
                )
            elif os.getenv("ANTHROPIC_API_KEY"):
                return ChatAnthropic(
                    model=self.config.get("anthropic_model", "claude-3-sonnet-20240229"),
                    temperature=0.1,
                    max_tokens=1000
                )
            else:
                # Fallback to local model or mock
                return self._create_mock_llm()
        except Exception as e:
            print(f"Warning: Could not initialize LLM: {e}")
            return self._create_mock_llm()
    
    def _create_mock_llm(self):
        """Create a mock LLM for testing without API keys."""
        class MockLLM:
            async def ainvoke(self, prompt):
                return self._generate_mock_response(prompt)
            
            def _generate_mock_response(self, prompt):
                if "component" in prompt.lower():
                    return type('MockResponse', (), {'content': '{"label": "MockComponent", "description": "AI-generated component", "category": "Service", "confidence": 0.8, "reasoning": "Mock response"}'})()
                else:
                    return type('MockResponse', (), {'content': '{"services": [{"name": "MockService", "description": "AI-generated service", "responsibilities": ["Mock responsibility"], "dependencies": [], "elements": []}]}'})()
        
        return MockLLM()
    
    def _initialize_cache(self):
        """Initialize caching for LLM responses."""
        if not LANGCHAIN_AVAILABLE:
            return None
            
        try:
            if os.getenv("REDIS_URL"):
                return RedisCache(redis_url=os.getenv("REDIS_URL"))
            else:
                return None
        except:
            return None
    
    async def label_component(self, element: CodeElement, code_context: str = "") -> ComponentLabel:
        """Label a single code component using AI."""
        # Create cache key
        cache_key = f"label_{element.id}_{hash(code_context)}"
        
        # Check cache first
        if self.cache:
            cached_result = self.cache.lookup(cache_key)
            if cached_result:
                return ComponentLabel(element_id=element.id, **cached_result)
        
        # Prepare context
        context = self._extract_code_context(element, code_context)
        
        # Generate prompt
        if self.component_label_template:
            prompt = self.component_label_template.format(
                element_name=element.name,
                element_type=element.type.value,
                file_path=str(element.file_path) if element.file_path else "unknown",
                code_context=context
            )
        else:
            # Fallback prompt for mock LLM
            prompt = f"Label component: {element.name} ({element.type.value})"
        
        try:
            # Get AI response
            if LANGCHAIN_AVAILABLE and hasattr(self.llm, 'ainvoke'):
                with get_openai_callback() as cb:
                    response = await self.llm.ainvoke(prompt)
                    result = self._parse_json_response(response.content)
            else:
                response = await self.llm.ainvoke(prompt)
                result = self._parse_json_response(response.content)
            
            # Create label
            label = ComponentLabel(
                element_id=element.id,
                label=result.get("label", element.name),
                description=result.get("description", ""),
                category=result.get("category", "Unknown"),
                confidence=result.get("confidence", 0.5),
                reasoning=result.get("reasoning", "")
            )
            
            # Cache result
            if self.cache:
                self.cache.update(cache_key, result)
            
            return label
            
        except Exception as e:
            print(f"Error labeling component {element.id}: {e}")
            return ComponentLabel(
                element_id=element.id,
                label=element.name,
                description="Error in AI labeling",
                category="Unknown",
                confidence=0.0,
                reasoning=f"Error: {str(e)}"
            )
    
    async def label_analysis_result(self, result: AnalysisResult) -> Dict[str, ComponentLabel]:
        """Label all components in an analysis result."""
        labels = {}
        
        # Group elements by file for context
        file_elements = self._group_elements_by_file(result.elements)
        
        for file_path, elements in file_elements.items():
            # Get file context
            context = self._get_file_context(file_path)
            
            for element in elements:
                label = await self.label_component(element, context)
                labels[element.id] = label
        
        return labels
    
    async def identify_service_boundaries(self, result: AnalysisResult) -> List[Dict[str, Any]]:
        """Use AI to identify service boundaries."""
        # Prepare data for AI
        elements_data = [
            {
                "id": elem.id,
                "name": elem.name,
                "type": elem.type.value,
                "module": elem.module
            }
            for elem in result.elements
        ]
        
        relationships_data = [
            {
                "source": rel.source_id,
                "target": rel.target_id,
                "type": rel.type.value
            }
            for rel in result.relationships
        ]
        
        # Generate prompt
        if self.service_boundary_template:
            prompt = self.service_boundary_template.format(
                elements=str(elements_data),
                relationships=str(relationships_data)
            )
        else:
            prompt = f"Identify service boundaries for: {len(elements_data)} elements"
        
        try:
            response = await self.llm.ainvoke(prompt)
            result_data = self._parse_json_response(response.content)
            return result_data.get("services", [])
        except Exception as e:
            print(f"Error identifying service boundaries: {e}")
            return []
    
    def _extract_code_context(self, element: CodeElement, code_context: str) -> str:
        """Extract relevant code context for the element."""
        if code_context:
            return code_context[:1000]  # Limit context length
        
        # Try to read the file if available
        if element.file_path and element.file_path.exists():
            try:
                with open(element.file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    return content[:1000]
            except:
                pass
        
        return ""
    
    def _group_elements_by_file(self, elements: List[CodeElement]) -> Dict[Path, List[CodeElement]]:
        """Group elements by their file path."""
        grouped = {}
        for element in elements:
            if element.file_path:
                if element.file_path not in grouped:
                    grouped[element.file_path] = []
                grouped[element.file_path].append(element)
        return grouped
    
    def _get_file_context(self, file_path: Path) -> str:
        """Get context from a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()[:1000]
        except:
            return ""
    
    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """Parse JSON response from LLM."""
        try:
            # Try to extract JSON from response
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