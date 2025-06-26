"""
Code parsers for different programming languages.
"""

import ast
import json
import re
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from .models import (
    CodeElement, ElementType, Relationship, RelationshipType, 
    LanguageType, ASTNode, DependencyInfo, ServiceType
)
import uuid


class BaseParser(ABC):
    """Base class for language-specific parsers."""
    
    def __init__(self):
        self.supported_extensions: List[str] = []
        self.language: LanguageType = LanguageType.PYTHON
        self.element_counter = 0
    
    @abstractmethod
    def can_parse(self, file_path: Path) -> bool:
        """Check if this parser can handle the given file."""
        pass
    
    @abstractmethod
    def parse_file(self, file_path: Path) -> List[CodeElement]:
        """Parse a file and extract code elements."""
        pass
    
    @abstractmethod
    def extract_relationships(self, elements: List[CodeElement]) -> List[Relationship]:
        """Extract relationships between elements."""
        pass
    
    def create_ast_node(self, node_type: str, value: Optional[str] = None, 
                       position: Optional[Dict[str, int]] = None) -> ASTNode:
        """Create an AST node."""
        return ASTNode(
            node_type=node_type,
            value=value,
            children=[],
            metadata={},
            position=position
        )
    
    def generate_element_id(self, file_path: Path, element_name: str, element_type: str) -> str:
        """Generate a unique element ID."""
        self.element_counter += 1
        return f"{file_path.stem}_{element_type}_{element_name}_{self.element_counter}"


class PythonParser(BaseParser):
    """Enhanced parser for Python code using AST."""
    
    def __init__(self):
        super().__init__()
        self.supported_extensions = ['.py']
        self.language = LanguageType.PYTHON
    
    def can_parse(self, file_path: Path) -> bool:
        return file_path.suffix in self.supported_extensions
    
    def parse_file(self, file_path: Path) -> List[CodeElement]:
        """Parse Python file using AST."""
        elements = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            # Create module element
            module_element = CodeElement(
                id=self.generate_element_id(file_path, file_path.stem, "module"),
                name=file_path.stem,
                type=ElementType.MODULE,
                language=self.language,
                file_path=file_path,
                line_number=1,
                end_line=len(content.splitlines()),
                module=file_path.stem,
                ast_node=self.create_ast_node("Module", position={"start": 1, "end": len(content.splitlines())})
            )
            elements.append(module_element)
            
            # Parse all nodes
            for node in ast.walk(tree):
                element = self._node_to_element(node, file_path, module_element.id)
                if element:
                    elements.append(element)
                    
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
        
        return elements
    
    def _node_to_element(self, node: ast.AST, file_path: Path, module_id: str) -> Optional[CodeElement]:
        """Convert AST node to CodeElement."""
        if isinstance(node, ast.ClassDef):
            return CodeElement(
                id=self.generate_element_id(file_path, node.name, "class"),
                name=node.name,
                type=ElementType.CLASS,
                language=self.language,
                file_path=file_path,
                line_number=getattr(node, 'lineno', None),
                end_line=getattr(node, 'end_lineno', None),
                module=file_path.stem,
                visibility='public',
                modifiers=self._extract_modifiers(node),
                ast_node=self._create_ast_node_from_python_node(node),
                metadata={
                    'bases': [self._get_name_from_expr(base) for base in node.bases],
                    'decorators': [self._get_name_from_expr(d) for d in node.decorator_list],
                    'docstring': ast.get_docstring(node)
                }
            )
        
        elif isinstance(node, ast.FunctionDef):
            return CodeElement(
                id=self.generate_element_id(file_path, node.name, "function"),
                name=node.name,
                type=ElementType.FUNCTION if not self._is_method(node) else ElementType.METHOD,
                language=self.language,
                file_path=file_path,
                line_number=getattr(node, 'lineno', None),
                end_line=getattr(node, 'end_lineno', None),
                module=file_path.stem,
                visibility='public',
                modifiers=self._extract_modifiers(node),
                ast_node=self._create_ast_node_from_python_node(node),
                metadata={
                    'args': [arg.arg for arg in node.args.args],
                    'decorators': [self._get_name_from_expr(d) for d in node.decorator_list],
                    'docstring': ast.get_docstring(node),
                    'is_method': self._is_method(node)
                }
            )
        
        elif isinstance(node, ast.Import):
            for alias in node.names:
                return CodeElement(
                    id=self.generate_element_id(file_path, f"import_{alias.name}", "import"),
                    name=alias.name,
                    type=ElementType.IMPORT,
                    language=self.language,
                    file_path=file_path,
                    line_number=getattr(node, 'lineno', None),
                    module=file_path.stem,
                    ast_node=self._create_ast_node_from_python_node(node),
                    dependencies=[DependencyInfo(
                        name=alias.name,
                        type="external" if "." in alias.name else "internal",
                        source="import"
                    )],
                    metadata={'asname': alias.asname}
                )
        
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ''
            for alias in node.names:
                return CodeElement(
                    id=self.generate_element_id(file_path, f"import_{module}.{alias.name}", "import"),
                    name=f"{module}.{alias.name}",
                    type=ElementType.IMPORT,
                    language=self.language,
                    file_path=file_path,
                    line_number=getattr(node, 'lineno', None),
                    module=file_path.stem,
                    ast_node=self._create_ast_node_from_python_node(node),
                    dependencies=[DependencyInfo(
                        name=module,
                        type="external" if "." in module else "internal",
                        source="from_import"
                    )],
                    metadata={'asname': alias.asname}
                )
        
        return None
    
    def _is_method(self, node: ast.FunctionDef) -> bool:
        """Check if function is a method (inside a class)."""
        parent = getattr(node, 'parent', None)
        return parent and isinstance(parent, ast.ClassDef)
    
    def _extract_modifiers(self, node: ast.AST) -> List[str]:
        """Extract modifiers from AST node."""
        modifiers = []
        if hasattr(node, 'decorator_list') and node.decorator_list:
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Name):
                    modifiers.append(decorator.id)
        return modifiers
    
    def _get_name_from_expr(self, expr: ast.expr) -> str:
        """Extract name from expression."""
        if isinstance(expr, ast.Name):
            return expr.id
        elif isinstance(expr, ast.Attribute):
            return f"{self._get_name_from_expr(expr.value)}.{expr.attr}"
        return str(expr)
    
    def _create_ast_node_from_python_node(self, node: ast.AST) -> ASTNode:
        """Create ASTNode from Python AST node."""
        return self.create_ast_node(
            node_type=type(node).__name__,
            position={
                "start": getattr(node, 'lineno', 0),
                "end": getattr(node, 'end_lineno', 0)
            }
        )
    
    def extract_relationships(self, elements: List[CodeElement]) -> List[Relationship]:
        """Extract relationships between Python elements."""
        relationships = []
        
        for element in elements:
            if element.type == ElementType.CLASS:
                # Inheritance relationships
                bases = element.metadata.get('bases', [])
                for base in bases:
                    relationships.append(Relationship(
                        id=str(uuid.uuid4()),
                        source_id=element.id,
                        target_id=base,
                        type=RelationshipType.INHERITS,
                        strength=1.0
                    ))
            
            elif element.type == ElementType.IMPORT:
                # Import relationships
                for dep in element.dependencies:
                    relationships.append(Relationship(
                        id=str(uuid.uuid4()),
                        source_id=element.id,
                        target_id=dep.name,
                        type=RelationshipType.IMPORTS,
                        strength=1.0
                    ))
        
        return relationships


class JavaScriptParser(BaseParser):
    """Parser for JavaScript code."""
    
    def __init__(self):
        super().__init__()
        self.supported_extensions = ['.js', '.mjs']
        self.language = LanguageType.JAVASCRIPT
    
    def can_parse(self, file_path: Path) -> bool:
        return file_path.suffix in self.supported_extensions
    
    def parse_file(self, file_path: Path) -> List[CodeElement]:
        """Parse JavaScript file using regex patterns."""
        elements = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Create module element
            module_element = CodeElement(
                id=self.generate_element_id(file_path, file_path.stem, "module"),
                name=file_path.stem,
                type=ElementType.MODULE,
                language=self.language,
                file_path=file_path,
                line_number=1,
                end_line=len(content.splitlines()),
                module=file_path.stem
            )
            elements.append(module_element)
            
            # Extract classes
            class_pattern = r'class\s+(\w+)(?:\s+extends\s+(\w+))?\s*{'
            for match in re.finditer(class_pattern, content):
                class_name = match.group(1)
                extends = match.group(2)
                
                element = CodeElement(
                    id=self.generate_element_id(file_path, class_name, "class"),
                    name=class_name,
                    type=ElementType.CLASS,
                    language=self.language,
                    file_path=file_path,
                    line_number=content[:match.start()].count('\n') + 1,
                    module=file_path.stem,
                    metadata={'extends': extends} if extends else {}
                )
                elements.append(element)
            
            # Extract functions
            function_pattern = r'(?:function\s+)?(\w+)\s*\([^)]*\)\s*{'
            for match in re.finditer(function_pattern, content):
                func_name = match.group(1)
                if func_name not in ['if', 'for', 'while', 'switch']:
                    element = CodeElement(
                        id=self.generate_element_id(file_path, func_name, "function"),
                        name=func_name,
                        type=ElementType.FUNCTION,
                        language=self.language,
                        file_path=file_path,
                        line_number=content[:match.start()].count('\n') + 1,
                        module=file_path.stem
                    )
                    elements.append(element)
            
            # Extract imports
            import_pattern = r'import\s+(?:{[^}]*}|\*\s+as\s+\w+|\w+)\s+from\s+[\'"]([^\'"]+)[\'"]'
            for match in re.finditer(import_pattern, content):
                module_name = match.group(1)
                element = CodeElement(
                    id=self.generate_element_id(file_path, f"import_{module_name}", "import"),
                    name=module_name,
                    type=ElementType.IMPORT,
                    language=self.language,
                    file_path=file_path,
                    line_number=content[:match.start()].count('\n') + 1,
                    module=file_path.stem,
                    dependencies=[DependencyInfo(
                        name=module_name,
                        type="external" if module_name.startswith('.') else "internal",
                        source="import"
                    )]
                )
                elements.append(element)
            
            # Extract requires
            require_pattern = r'const\s+(\w+)\s*=\s*require\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)'
            for match in re.finditer(require_pattern, content):
                var_name = match.group(1)
                module_name = match.group(2)
                element = CodeElement(
                    id=self.generate_element_id(file_path, f"require_{var_name}", "require"),
                    name=module_name,
                    type=ElementType.REQUIRE,
                    language=self.language,
                    file_path=file_path,
                    line_number=content[:match.start()].count('\n') + 1,
                    module=file_path.stem,
                    dependencies=[DependencyInfo(
                        name=module_name,
                        type="external" if module_name.startswith('.') else "internal",
                        source="require"
                    )],
                    metadata={'variable': var_name}
                )
                elements.append(element)
                    
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
        
        return elements
    
    def extract_relationships(self, elements: List[CodeElement]) -> List[Relationship]:
        """Extract relationships between JavaScript elements."""
        relationships = []
        
        for element in elements:
            if element.type == ElementType.CLASS:
                extends = element.metadata.get('extends')
                if extends:
                    relationships.append(Relationship(
                        id=str(uuid.uuid4()),
                        source_id=element.id,
                        target_id=extends,
                        type=RelationshipType.EXTENDS,
                        strength=1.0
                    ))
            
            elif element.type in [ElementType.IMPORT, ElementType.REQUIRE]:
                for dep in element.dependencies:
                    relationships.append(Relationship(
                        id=str(uuid.uuid4()),
                        source_id=element.id,
                        target_id=dep.name,
                        type=RelationshipType.IMPORTS if element.type == ElementType.IMPORT else RelationshipType.REQUIRES,
                        strength=1.0
                    ))
        
        return relationships


class JavaParser(BaseParser):
    """Parser for Java code."""
    
    def __init__(self):
        super().__init__()
        self.supported_extensions = ['.java']
        self.language = LanguageType.JAVA
    
    def can_parse(self, file_path: Path) -> bool:
        return file_path.suffix in self.supported_extensions
    
    def parse_file(self, file_path: Path) -> List[CodeElement]:
        """Parse Java file using regex patterns."""
        elements = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Create file element
            file_element = CodeElement(
                id=self.generate_element_id(file_path, file_path.stem, "file"),
                name=file_path.stem,
                type=ElementType.FILE,
                language=self.language,
                file_path=file_path,
                line_number=1,
                end_line=len(content.splitlines()),
                module=file_path.stem
            )
            elements.append(file_element)
            
            # Extract package declaration
            package_pattern = r'package\s+([\w.]+);'
            package_match = re.search(package_pattern, content)
            if package_match:
                package_name = package_match.group(1)
                package_element = CodeElement(
                    id=self.generate_element_id(file_path, package_name, "package"),
                    name=package_name,
                    type=ElementType.PACKAGE,
                    language=self.language,
                    file_path=file_path,
                    line_number=content[:package_match.start()].count('\n') + 1,
                    module=file_path.stem
                )
                elements.append(package_element)
            
            # Extract imports
            import_pattern = r'import\s+(?:static\s+)?([\w.*]+);'
            for match in re.finditer(import_pattern, content):
                import_name = match.group(1)
                element = CodeElement(
                    id=self.generate_element_id(file_path, f"import_{import_name}", "import"),
                    name=import_name,
                    type=ElementType.IMPORT,
                    language=self.language,
                    file_path=file_path,
                    line_number=content[:match.start()].count('\n') + 1,
                    module=file_path.stem,
                    dependencies=[DependencyInfo(
                        name=import_name,
                        type="external" if not import_name.startswith('java.') else "internal",
                        source="import"
                    )]
                )
                elements.append(element)
            
            # Extract classes
            class_pattern = r'(?:public\s+)?(?:abstract\s+)?(?:final\s+)?class\s+(\w+)(?:\s+extends\s+(\w+))?(?:\s+implements\s+([\w\s,]+))?\s*{'
            for match in re.finditer(class_pattern, content):
                class_name = match.group(1)
                extends = match.group(2)
                implements = match.group(3)
                
                modifiers = []
                if 'public' in match.group(0):
                    modifiers.append('public')
                if 'abstract' in match.group(0):
                    modifiers.append('abstract')
                if 'final' in match.group(0):
                    modifiers.append('final')
                
                element = CodeElement(
                    id=self.generate_element_id(file_path, class_name, "class"),
                    name=class_name,
                    type=ElementType.CLASS,
                    language=self.language,
                    file_path=file_path,
                    line_number=content[:match.start()].count('\n') + 1,
                    module=file_path.stem,
                    visibility='public' if 'public' in modifiers else 'package-private',
                    modifiers=modifiers,
                    metadata={
                        'extends': extends,
                        'implements': [i.strip() for i in implements.split(',')] if implements else []
                    }
                )
                elements.append(element)
            
            # Extract methods
            method_pattern = r'(?:public|private|protected)?\s*(?:static\s+)?(?:final\s+)?(?:abstract\s+)?(?:<[^>]+>\s+)?(\w+)\s+(\w+)\s*\([^)]*\)\s*(?:throws\s+[\w\s,]+)?\s*{'
            for match in re.finditer(method_pattern, content):
                return_type = match.group(1)
                method_name = match.group(2)
                
                if method_name not in ['if', 'for', 'while', 'switch']:
                    element = CodeElement(
                        id=self.generate_element_id(file_path, method_name, "method"),
                        name=method_name,
                        type=ElementType.METHOD,
                        language=self.language,
                        file_path=file_path,
                        line_number=content[:match.start()].count('\n') + 1,
                        module=file_path.stem,
                        metadata={'return_type': return_type}
                    )
                    elements.append(element)
                    
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
        
        return elements
    
    def extract_relationships(self, elements: List[CodeElement]) -> List[Relationship]:
        """Extract relationships between Java elements."""
        relationships = []
        
        for element in elements:
            if element.type == ElementType.CLASS:
                extends = element.metadata.get('extends')
                if extends:
                    relationships.append(Relationship(
                        id=str(uuid.uuid4()),
                        source_id=element.id,
                        target_id=extends,
                        type=RelationshipType.EXTENDS,
                        strength=1.0
                    ))
                
                implements = element.metadata.get('implements', [])
                for interface in implements:
                    relationships.append(Relationship(
                        id=str(uuid.uuid4()),
                        source_id=element.id,
                        target_id=interface,
                        type=RelationshipType.IMPLEMENTS,
                        strength=1.0
                    ))
            
            elif element.type == ElementType.IMPORT:
                for dep in element.dependencies:
                    relationships.append(Relationship(
                        id=str(uuid.uuid4()),
                        source_id=element.id,
                        target_id=dep.name,
                        type=RelationshipType.IMPORTS,
                        strength=1.0
                    ))
        
        return relationships


class ParserRegistry:
    """Registry for managing different language parsers."""
    
    def __init__(self):
        self.parsers: Dict[str, BaseParser] = {}
        self._register_default_parsers()
    
    def _register_default_parsers(self):
        """Register default parsers."""
        self.register_parser('python', PythonParser())
        self.register_parser('javascript', JavaScriptParser())
        self.register_parser('java', JavaParser())
    
    def register_parser(self, language: str, parser: BaseParser):
        """Register a parser for a specific language."""
        self.parsers[language] = parser
    
    def get_parser(self, language: str) -> Optional[BaseParser]:
        """Get parser for a specific language."""
        return self.parsers.get(language)
    
    def get_parser_for_file(self, file_path: Path) -> Optional[BaseParser]:
        """Get the appropriate parser for a file based on its extension."""
        for parser in self.parsers.values():
            if parser.can_parse(file_path):
                return parser
        return None
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages."""
        return list(self.parsers.keys())
    
    def get_supported_extensions(self) -> List[str]:
        """Get all supported file extensions."""
        extensions = set()
        for parser in self.parsers.values():
            extensions.update(parser.supported_extensions)
        return list(extensions) 