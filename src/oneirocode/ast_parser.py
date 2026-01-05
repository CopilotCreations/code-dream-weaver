"""
AST Parser Module

Parses Python source files and extracts structural patterns for symbolic analysis.
"""

import ast
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Any, Optional


@dataclass
class NamingPattern:
    """Represents a naming pattern found in code."""
    name: str
    category: str  # 'function', 'class', 'variable', 'constant'
    file_path: str
    line_number: int
    prefix: Optional[str] = None
    suffix: Optional[str] = None


@dataclass
class GuardClause:
    """Represents a guard clause (early return/raise pattern)."""
    file_path: str
    line_number: int
    condition: str
    action: str  # 'return', 'raise', 'continue', 'break'
    function_name: str


@dataclass
class ErrorHandler:
    """Represents an error handling block."""
    file_path: str
    line_number: int
    exception_types: List[str]
    handler_action: str  # 'suppress', 'reraise', 'transform', 'log'
    function_name: str


@dataclass
class DefensivePattern:
    """Represents defensive programming patterns."""
    file_path: str
    line_number: int
    pattern_type: str  # 'null_check', 'type_check', 'bounds_check', 'assertion'
    context: str


@dataclass
class CodeStructure:
    """Aggregated structural information from a codebase."""
    naming_patterns: List[NamingPattern] = field(default_factory=list)
    guard_clauses: List[GuardClause] = field(default_factory=list)
    error_handlers: List[ErrorHandler] = field(default_factory=list)
    defensive_patterns: List[DefensivePattern] = field(default_factory=list)
    function_count: int = 0
    class_count: int = 0
    file_count: int = 0
    total_lines: int = 0
    nesting_depths: List[int] = field(default_factory=list)
    repetition_motifs: Dict[str, int] = field(default_factory=dict)


class ASTVisitor(ast.NodeVisitor):
    """Custom AST visitor for extracting code patterns."""

    def __init__(self, file_path: str):
        """Initialize the AST visitor.

        Args:
            file_path: Path to the file being visited.
        """
        self.file_path = file_path
        self.naming_patterns: List[NamingPattern] = []
        self.guard_clauses: List[GuardClause] = []
        self.error_handlers: List[ErrorHandler] = []
        self.defensive_patterns: List[DefensivePattern] = []
        self.function_count = 0
        self.class_count = 0
        self.current_function: Optional[str] = None
        self.nesting_depth = 0
        self.max_nesting_depths: List[int] = []
        self.structure_signatures: List[str] = []

    def _extract_prefix_suffix(self, name: str) -> tuple:
        """Extract common prefixes and suffixes from names.

        Args:
            name: The identifier name to analyze.

        Returns:
            A tuple of (prefix, suffix) where each is either a matched
            string or None if no common prefix/suffix was found.
        """
        prefixes = ['get_', 'set_', 'is_', 'has_', 'can_', 'do_', 'make_', 
                    'create_', 'build_', 'init_', 'validate_', 'check_', 
                    'process_', 'handle_', '_']
        suffixes = ['_handler', '_manager', '_factory', '_builder', '_validator',
                    '_processor', '_helper', '_util', '_service', '_controller',
                    '_impl', '_base', '_mixin', '_error', '_exception']
        
        found_prefix = None
        found_suffix = None
        
        for prefix in prefixes:
            if name.startswith(prefix):
                found_prefix = prefix
                break
        
        for suffix in suffixes:
            if name.endswith(suffix):
                found_suffix = suffix
                break
        
        return found_prefix, found_suffix

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Visit a function definition node.

        Args:
            node: The FunctionDef AST node to process.
        """
        self.function_count += 1
        prev_function = self.current_function
        self.current_function = node.name
        
        prefix, suffix = self._extract_prefix_suffix(node.name)
        self.naming_patterns.append(NamingPattern(
            name=node.name,
            category='function',
            file_path=self.file_path,
            line_number=node.lineno,
            prefix=prefix,
            suffix=suffix
        ))
        
        # Check for guard clauses at function start
        self._check_guard_clauses(node)
        
        # Track nesting depth
        prev_depth = self.nesting_depth
        self.nesting_depth += 1
        self.max_nesting_depths.append(self._calculate_max_nesting(node))
        
        # Create structure signature for repetition detection
        sig = self._create_structure_signature(node)
        self.structure_signatures.append(sig)
        
        self.generic_visit(node)
        self.nesting_depth = prev_depth
        self.current_function = prev_function

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        """Visit an async function definition node.

        Args:
            node: The AsyncFunctionDef AST node to process.
        """
        # Treat async functions similarly
        self.visit_FunctionDef(node)  # type: ignore

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Visit a class definition node.

        Args:
            node: The ClassDef AST node to process.
        """
        self.class_count += 1
        prefix, suffix = self._extract_prefix_suffix(node.name)
        self.naming_patterns.append(NamingPattern(
            name=node.name,
            category='class',
            file_path=self.file_path,
            line_number=node.lineno,
            prefix=prefix,
            suffix=suffix
        ))
        self.generic_visit(node)

    def visit_Name(self, node: ast.Name) -> None:
        """Visit a name node to track constant naming patterns.

        Args:
            node: The Name AST node to process.
        """
        # Track variable naming patterns (constants)
        if node.id.isupper() and len(node.id) > 1:
            self.naming_patterns.append(NamingPattern(
                name=node.id,
                category='constant',
                file_path=self.file_path,
                line_number=node.lineno
            ))
        self.generic_visit(node)

    def visit_Try(self, node: ast.Try) -> None:
        """Visit a try/except block to extract error handling patterns.

        Args:
            node: The Try AST node to process.
        """
        for handler in node.handlers:
            exception_types = []
            if handler.type:
                if isinstance(handler.type, ast.Name):
                    exception_types.append(handler.type.id)
                elif isinstance(handler.type, ast.Tuple):
                    for elt in handler.type.elts:
                        if isinstance(elt, ast.Name):
                            exception_types.append(elt.id)
            else:
                exception_types.append('BaseException')
            
            handler_action = self._determine_handler_action(handler)
            
            self.error_handlers.append(ErrorHandler(
                file_path=self.file_path,
                line_number=handler.lineno,
                exception_types=exception_types,
                handler_action=handler_action,
                function_name=self.current_function or '<module>'
            ))
        
        self.generic_visit(node)

    def visit_If(self, node: ast.If) -> None:
        """Visit an if statement to check for defensive patterns.

        Args:
            node: The If AST node to process.
        """
        # Check for defensive patterns
        self._check_defensive_patterns(node)
        self.generic_visit(node)

    def visit_Assert(self, node: ast.Assert) -> None:
        """Visit an assert statement to track defensive patterns.

        Args:
            node: The Assert AST node to process.
        """
        self.defensive_patterns.append(DefensivePattern(
            file_path=self.file_path,
            line_number=node.lineno,
            pattern_type='assertion',
            context=ast.unparse(node.test) if hasattr(ast, 'unparse') else 'assertion'
        ))
        self.generic_visit(node)

    def _check_guard_clauses(self, node: ast.FunctionDef) -> None:
        """Identify guard clauses at the start of a function.

        Checks the first 3 statements of a function body for early
        return or raise patterns that serve as guard clauses.

        Args:
            node: The FunctionDef AST node to analyze.
        """
        for i, stmt in enumerate(node.body[:3]):  # Check first 3 statements
            if isinstance(stmt, ast.If):
                # Check if the if body contains early exit
                for body_stmt in stmt.body:
                    if isinstance(body_stmt, ast.Return):
                        condition = ast.unparse(stmt.test) if hasattr(ast, 'unparse') else 'condition'
                        self.guard_clauses.append(GuardClause(
                            file_path=self.file_path,
                            line_number=stmt.lineno,
                            condition=condition,
                            action='return',
                            function_name=node.name
                        ))
                    elif isinstance(body_stmt, ast.Raise):
                        condition = ast.unparse(stmt.test) if hasattr(ast, 'unparse') else 'condition'
                        self.guard_clauses.append(GuardClause(
                            file_path=self.file_path,
                            line_number=stmt.lineno,
                            condition=condition,
                            action='raise',
                            function_name=node.name
                        ))

    def _check_defensive_patterns(self, node: ast.If) -> None:
        """Identify defensive programming patterns in if statements.

        Detects null checks and type checks that indicate defensive
        programming practices.

        Args:
            node: The If AST node to analyze.
        """
        condition = node.test
        
        # Null checks: if x is None, if x is not None, if not x
        if isinstance(condition, ast.Compare):
            for op in condition.ops:
                if isinstance(op, (ast.Is, ast.IsNot)):
                    for comparator in condition.comparators:
                        if isinstance(comparator, ast.Constant) and comparator.value is None:
                            self.defensive_patterns.append(DefensivePattern(
                                file_path=self.file_path,
                                line_number=node.lineno,
                                pattern_type='null_check',
                                context=ast.unparse(condition) if hasattr(ast, 'unparse') else 'null check'
                            ))
        
        # Type checks: isinstance(x, type)
        if isinstance(condition, ast.Call):
            if isinstance(condition.func, ast.Name) and condition.func.id == 'isinstance':
                self.defensive_patterns.append(DefensivePattern(
                    file_path=self.file_path,
                    line_number=node.lineno,
                    pattern_type='type_check',
                    context=ast.unparse(condition) if hasattr(ast, 'unparse') else 'type check'
                ))

    def _determine_handler_action(self, handler: ast.ExceptHandler) -> str:
        """Determine what action an exception handler takes.

        Args:
            handler: The ExceptHandler AST node to analyze.

        Returns:
            A string describing the handler action: 'suppress', 'reraise',
            'transform', 'log', or 'handle'.
        """
        if not handler.body:
            return 'suppress'
        
        for stmt in handler.body:
            if isinstance(stmt, ast.Raise):
                if stmt.exc is None:
                    return 'reraise'
                return 'transform'
            if isinstance(stmt, ast.Expr):
                if isinstance(stmt.value, ast.Call):
                    if isinstance(stmt.value.func, ast.Attribute):
                        if stmt.value.func.attr in ('error', 'warning', 'exception', 'info', 'debug'):
                            return 'log'
        
        if len(handler.body) == 1 and isinstance(handler.body[0], ast.Pass):
            return 'suppress'
        
        return 'handle'

    def _calculate_max_nesting(self, node: ast.AST) -> int:
        """Calculate maximum nesting depth within a node.

        Args:
            node: The AST node to analyze for nesting depth.

        Returns:
            The maximum nesting depth found within the node.
        """
        max_depth = 0
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.With, ast.Try)):
                depth = self._get_node_depth(child, node)
                max_depth = max(max_depth, depth)
        
        return max_depth

    def _get_node_depth(self, target: ast.AST, root: ast.AST) -> int:
        """Get the nesting depth of a node relative to root.

        Args:
            target: The AST node to find the depth of.
            root: The root AST node to measure depth from.

        Returns:
            The nesting depth of target relative to root.
        """
        depth = 0
        for node in ast.walk(root):
            if node is target:
                return depth
            if isinstance(node, (ast.If, ast.For, ast.While, ast.With, ast.Try, 
                                 ast.FunctionDef, ast.AsyncFunctionDef)):
                depth += 1
        return depth

    def _create_structure_signature(self, node: ast.FunctionDef) -> str:
        """Create a structural signature for pattern matching.

        Generates a string signature based on function structure including
        argument count, decorators, body structure, and return presence.

        Args:
            node: The FunctionDef AST node to create a signature for.

        Returns:
            A pipe-delimited string representing the function's structure.
        """
        parts = []
        
        # Parameter count
        parts.append(f"args:{len(node.args.args)}")
        
        # Has decorators
        if node.decorator_list:
            parts.append(f"deco:{len(node.decorator_list)}")
        
        # Body structure
        body_types = []
        for stmt in node.body[:5]:  # First 5 statements
            body_types.append(type(stmt).__name__)
        parts.append(f"body:{'-'.join(body_types)}")
        
        # Has return
        has_return = any(isinstance(n, ast.Return) for n in ast.walk(node))
        parts.append(f"ret:{has_return}")
        
        return '|'.join(parts)


class ASTParser:
    """Main parser for analyzing Python codebases."""

    def __init__(self):
        """Initialize the AST parser with an empty code structure."""
        self.structure = CodeStructure()

    def parse_file(self, file_path: Path) -> Optional[ASTVisitor]:
        """Parse a single Python file.

        Args:
            file_path: Path to the Python file to parse.

        Returns:
            An ASTVisitor containing extracted patterns, or None if the
            file could not be parsed due to syntax or encoding errors.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content, filename=str(file_path))
            visitor = ASTVisitor(str(file_path))
            visitor.visit(tree)
            
            return visitor
        except (SyntaxError, UnicodeDecodeError) as e:
            # Skip files that can't be parsed
            return None

    def parse_repository(self, repo_path: str) -> CodeStructure:
        """Parse all Python files in a repository.

        Recursively finds and parses all Python files, excluding common
        non-source directories like venv, node_modules, __pycache__, etc.

        Args:
            repo_path: Path to the repository root directory.

        Returns:
            A CodeStructure containing aggregated patterns from all files.

        Raises:
            FileNotFoundError: If the repository path does not exist.
        """
        repo = Path(repo_path)
        
        if not repo.exists():
            raise FileNotFoundError(f"Repository path not found: {repo_path}")
        
        python_files = list(repo.rglob("*.py"))
        
        # Filter out common non-source directories
        excluded_dirs = {'venv', '.venv', 'env', '.env', 'node_modules', 
                        '__pycache__', '.git', '.tox', 'dist', 'build', 
                        'egg-info', '.eggs'}
        
        filtered_files = []
        for f in python_files:
            parts = set(f.parts)
            if not parts.intersection(excluded_dirs):
                filtered_files.append(f)
        
        self.structure = CodeStructure()
        all_signatures: List[str] = []
        
        for file_path in filtered_files:
            visitor = self.parse_file(file_path)
            if visitor:
                self.structure.naming_patterns.extend(visitor.naming_patterns)
                self.structure.guard_clauses.extend(visitor.guard_clauses)
                self.structure.error_handlers.extend(visitor.error_handlers)
                self.structure.defensive_patterns.extend(visitor.defensive_patterns)
                self.structure.function_count += visitor.function_count
                self.structure.class_count += visitor.class_count
                self.structure.nesting_depths.extend(visitor.max_nesting_depths)
                all_signatures.extend(visitor.structure_signatures)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        self.structure.total_lines += len(f.readlines())
                except:
                    pass
        
        self.structure.file_count = len(filtered_files)
        
        # Calculate repetition motifs
        for sig in all_signatures:
            self.structure.repetition_motifs[sig] = self.structure.repetition_motifs.get(sig, 0) + 1
        
        return self.structure
