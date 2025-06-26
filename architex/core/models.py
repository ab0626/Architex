"""
Data models for Architex analysis results.
"""

from enum import Enum
from typing import Dict, List, Optional, Set, Any, Union
from pydantic import BaseModel, Field
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime


class ElementType(str, Enum):
    """Types of code elements that can be analyzed."""
    # File/Module level
    MODULE = "module"
    PACKAGE = "package"
    NAMESPACE = "namespace"
    FILE = "file"
    
    # Class/Object level
    CLASS = "class"
    INTERFACE = "interface"
    ENUM = "enum"
    STRUCT = "struct"
    TRAIT = "trait"
    OBJECT = "object"
    PROTOCOL = "protocol"
    
    # Function/Method level
    FUNCTION = "function"
    METHOD = "method"
    CONSTRUCTOR = "constructor"
    DESTRUCTOR = "destructor"
    OPERATOR = "operator"
    
    # Variable/Data level
    VARIABLE = "variable"
    CONSTANT = "constant"
    FIELD = "field"
    PROPERTY = "property"
    PARAMETER = "parameter"
    
    # Import/Export level
    IMPORT = "import"
    EXPORT = "export"
    REQUIRE = "require"
    INCLUDE = "include"
    
    # Control flow
    CONDITION = "condition"
    LOOP = "loop"
    EXCEPTION = "exception"
    
    # Language specific
    ANNOTATION = "annotation"
    DECORATOR = "decorator"
    MACRO = "macro"
    TEMPLATE = "template"
    GENERIC = "generic"


class RelationshipType(str, Enum):
    """Types of relationships between code elements."""
    # Inheritance/Implementation
    INHERITS = "inherits"
    IMPLEMENTS = "implements"
    EXTENDS = "extends"
    
    # Dependencies
    DEPENDS_ON = "depends_on"
    IMPORTS = "imports"
    REQUIRES = "requires"
    INCLUDES = "includes"
    
    # Function calls
    CALLS = "calls"
    INVOKES = "invokes"
    REFERENCES = "references"
    
    # Data flow
    USES = "uses"
    ASSIGNS = "assigns"
    RETURNS = "returns"
    THROWS = "throws"
    
    # Structural
    CONTAINS = "contains"
    BELONGS_TO = "belongs_to"
    PART_OF = "part_of"
    
    # Associations
    ASSOCIATES = "associates"
    COMPOSES = "composes"
    AGGREGATES = "aggregates"
    ASSOCIATES_WITH = "associates_with"
    
    # Overrides
    OVERRIDES = "overrides"
    SHADOWS = "shadows"
    
    # Type relationships
    INSTANCE_OF = "instance_of"
    CASTS_TO = "casts_to"
    CONVERTS_TO = "converts_to"


class LanguageType(str, Enum):
    """Supported programming languages."""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    JAVA = "java"
    C_SHARP = "csharp"
    CPP = "cpp"
    GO = "go"
    RUST = "rust"
    PHP = "php"
    RUBY = "ruby"
    SWIFT = "swift"
    KOTLIN = "kotlin"
    SCALA = "scala"
    DART = "dart"
    R = "r"
    MATLAB = "matlab"


class ASTNode(BaseModel):
    """Represents an AST node with language-specific details."""
    node_type: str = Field(..., description="Type of AST node")
    value: Optional[str] = Field(None, description="Value of the node")
    children: List['ASTNode'] = Field(default_factory=list, description="Child nodes")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Node metadata")
    position: Optional[Dict[str, int]] = Field(None, description="Position in source code")
    
    class Config:
        arbitrary_types_allowed = True


class DependencyInfo(BaseModel):
    """Detailed dependency information."""
    name: str = Field(..., description="Dependency name")
    version: Optional[str] = Field(None, description="Version information")
    type: str = Field(..., description="Type of dependency (internal/external)")
    source: Optional[str] = Field(None, description="Source of the dependency")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class ServiceType(str, Enum):
    """Types of services that can be detected."""
    API_SERVICE = "api_service"
    DATA_SERVICE = "data_service"
    BUSINESS_SERVICE = "business_service"
    INFRASTRUCTURE_SERVICE = "infrastructure_service"
    UTILITY_SERVICE = "utility_service"
    CONTROLLER = "controller"
    REPOSITORY = "repository"
    SERVICE_LAYER = "service_layer"
    DOMAIN_SERVICE = "domain_service"
    APPLICATION_SERVICE = "application_service"


class CodeElement(BaseModel):
    """Represents a code element in the system."""
    id: str = Field(..., description="Unique identifier for the element")
    name: str = Field(..., description="Name of the element")
    type: ElementType = Field(..., description="Type of the element")
    language: LanguageType = Field(..., description="Programming language")
    file_path: Optional[Path] = Field(None, description="File containing the element")
    line_number: Optional[int] = Field(None, description="Line number in the file")
    end_line: Optional[int] = Field(None, description="End line number")
    module: Optional[str] = Field(None, description="Module/package containing the element")
    namespace: Optional[str] = Field(None, description="Namespace of the element")
    visibility: Optional[str] = Field(None, description="Visibility (public, private, etc.)")
    modifiers: List[str] = Field(default_factory=list, description="Modifiers (static, final, etc.)")
    ast_node: Optional[ASTNode] = Field(None, description="AST representation")
    dependencies: List[DependencyInfo] = Field(default_factory=list, description="Direct dependencies")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    created_at: datetime = Field(default_factory=datetime.now, description="When this element was created")
    
    class Config:
        arbitrary_types_allowed = True


class Relationship(BaseModel):
    """Represents a relationship between two code elements."""
    id: str = Field(..., description="Unique relationship identifier")
    source_id: str = Field(..., description="ID of the source element")
    target_id: str = Field(..., description="ID of the target element")
    type: RelationshipType = Field(..., description="Type of relationship")
    strength: float = Field(1.0, description="Relationship strength (0.0 to 1.0)")
    bidirectional: bool = Field(False, description="Whether this is a bidirectional relationship")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    created_at: datetime = Field(default_factory=datetime.now, description="When this relationship was created")


class ServiceBoundary(BaseModel):
    """Represents a service boundary in the system."""
    id: str = Field(..., description="Unique service boundary identifier")
    name: str = Field(..., description="Name of the service boundary")
    type: ServiceType = Field(..., description="Type of service")
    elements: Set[str] = Field(default_factory=set, description="Element IDs in this boundary")
    dependencies: Set[str] = Field(default_factory=set, description="External dependencies")
    cohesion_score: float = Field(0.0, description="Cohesion score (0.0 to 1.0)")
    coupling_score: float = Field(0.0, description="Coupling score (0.0 to 1.0)")
    complexity_score: float = Field(0.0, description="Complexity score")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    created_at: datetime = Field(default_factory=datetime.now, description="When this boundary was created")


class ArchitectureLayer(BaseModel):
    """Represents an architectural layer."""
    id: str = Field(..., description="Unique layer identifier")
    name: str = Field(..., description="Name of the layer")
    level: int = Field(..., description="Layer level (0 = bottom, higher = top)")
    elements: Set[str] = Field(default_factory=set, description="Element IDs in this layer")
    dependencies: Set[str] = Field(default_factory=set, description="Dependencies on other layers")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class DependencyGraph(BaseModel):
    """Represents a dependency graph."""
    nodes: List[CodeElement] = Field(default_factory=list, description="All nodes in the graph")
    edges: List[Relationship] = Field(default_factory=list, description="All edges in the graph")
    cycles: List[List[str]] = Field(default_factory=list, description="Detected cycles")
    strongly_connected_components: List[List[str]] = Field(default_factory=list, description="Strongly connected components")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Graph metadata")


class AnalysisResult(BaseModel):
    """Complete result of a codebase analysis."""
    id: str = Field(..., description="Unique analysis identifier")
    elements: List[CodeElement] = Field(default_factory=list, description="All code elements")
    relationships: List[Relationship] = Field(default_factory=list, description="All relationships")
    service_boundaries: List[ServiceBoundary] = Field(default_factory=list, description="Detected service boundaries")
    architecture_layers: List[ArchitectureLayer] = Field(default_factory=list, description="Architectural layers")
    dependency_graph: Optional[DependencyGraph] = Field(None, description="Complete dependency graph")
    metrics: Dict[str, float] = Field(default_factory=dict, description="Analysis metrics")
    language_stats: Dict[str, int] = Field(default_factory=dict, description="Statistics by language")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Analysis metadata")
    created_at: datetime = Field(default_factory=datetime.now, description="When this analysis was created")
    
    def get_element_by_id(self, element_id: str) -> Optional[CodeElement]:
        """Get an element by its ID."""
        for element in self.elements:
            if element.id == element_id:
                return element
        return None
    
    def get_relationships_for_element(self, element_id: str) -> List[Relationship]:
        """Get all relationships involving a specific element."""
        return [
            rel for rel in self.relationships
            if rel.source_id == element_id or rel.target_id == element_id
        ]
    
    def get_dependencies(self, element_id: str) -> List[CodeElement]:
        """Get all elements that the specified element depends on."""
        dependencies = []
        for rel in self.relationships:
            if rel.source_id == element_id and rel.type in [
                RelationshipType.DEPENDS_ON,
                RelationshipType.IMPORTS,
                RelationshipType.CALLS,
                RelationshipType.USES
            ]:
                dep_element = self.get_element_by_id(rel.target_id)
                if dep_element:
                    dependencies.append(dep_element)
        return dependencies
    
    def get_elements_by_type(self, element_type: ElementType) -> List[CodeElement]:
        """Get all elements of a specific type."""
        return [elem for elem in self.elements if elem.type == element_type]
    
    def get_elements_by_language(self, language: LanguageType) -> List[CodeElement]:
        """Get all elements written in a specific language."""
        return [elem for elem in self.elements if elem.language == language]
    
    def get_service_boundary_by_name(self, name: str) -> Optional[ServiceBoundary]:
        """Get a service boundary by name."""
        for boundary in self.service_boundaries:
            if boundary.name == name:
                return boundary 