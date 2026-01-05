"""
Tests for AST Parser module.
"""

import ast
import pytest
import tempfile
import os
from pathlib import Path

from src.oneirocode.ast_parser import (
    ASTParser,
    ASTVisitor,
    CodeStructure,
    NamingPattern,
    GuardClause,
    ErrorHandler,
    DefensivePattern
)


class TestNamingPattern:
    """Tests for NamingPattern dataclass."""

    def test_create_naming_pattern(self):
        """Test creating a NamingPattern with all fields specified.

        Verifies that a NamingPattern can be created with name, category,
        file_path, line_number, prefix, and suffix, and that all values
        are correctly stored.
        """
        pattern = NamingPattern(
            name="validate_input",
            category="function",
            file_path="test.py",
            line_number=10,
            prefix="validate_",
            suffix=None
        )
        assert pattern.name == "validate_input"
        assert pattern.category == "function"
        assert pattern.prefix == "validate_"
        assert pattern.suffix is None

    def test_naming_pattern_without_prefix_suffix(self):
        """Test creating a NamingPattern without prefix or suffix.

        Verifies that prefix and suffix default to None when not provided.
        """
        pattern = NamingPattern(
            name="my_function",
            category="function",
            file_path="test.py",
            line_number=5
        )
        assert pattern.prefix is None
        assert pattern.suffix is None


class TestASTVisitor:
    """Tests for ASTVisitor class."""

    def test_extract_function_names(self):
        """Test extraction of function names from code.

        Verifies that ASTVisitor correctly identifies and counts function
        definitions, storing their names in naming_patterns.
        """
        code = '''
def validate_input(x):
    pass

def get_data():
    pass

def process_request():
    pass
'''
        tree = ast.parse(code)
        visitor = ASTVisitor("test.py")
        visitor.visit(tree)
        
        assert visitor.function_count == 3
        names = [p.name for p in visitor.naming_patterns]
        assert "validate_input" in names
        assert "get_data" in names
        assert "process_request" in names

    def test_extract_prefix(self):
        """Test extraction of naming prefixes from function names.

        Verifies that ASTVisitor correctly identifies common prefixes
        like 'validate_', 'check_', and 'get_' in function names.
        """
        code = '''
def validate_user():
    pass

def check_permissions():
    pass

def get_config():
    pass
'''
        tree = ast.parse(code)
        visitor = ASTVisitor("test.py")
        visitor.visit(tree)
        
        prefixes = [p.prefix for p in visitor.naming_patterns if p.prefix]
        assert "validate_" in prefixes
        assert "check_" in prefixes
        assert "get_" in prefixes

    def test_extract_suffix(self):
        """Test extraction of naming suffixes from class names.

        Verifies that ASTVisitor correctly identifies common suffixes
        like '_handler', '_manager', and '_factory' in class names.
        """
        code = '''
class User_handler:
    pass

class Data_manager:
    pass

class Request_factory:
    pass
'''
        tree = ast.parse(code)
        visitor = ASTVisitor("test.py")
        visitor.visit(tree)
        
        assert visitor.class_count == 3
        suffixes = [p.suffix for p in visitor.naming_patterns if p.suffix]
        assert "_handler" in suffixes
        assert "_manager" in suffixes
        assert "_factory" in suffixes

    def test_detect_guard_clause_return(self):
        """Test detection of guard clauses with early return.

        Verifies that ASTVisitor identifies guard clauses that use
        early return statements to handle edge cases.
        """
        code = '''
def process(data):
    if data is None:
        return None
    return data.process()
'''
        tree = ast.parse(code)
        visitor = ASTVisitor("test.py")
        visitor.visit(tree)
        
        assert len(visitor.guard_clauses) == 1
        guard = visitor.guard_clauses[0]
        assert guard.action == "return"
        assert guard.function_name == "process"

    def test_detect_guard_clause_raise(self):
        """Test detection of guard clauses with exception raising.

        Verifies that ASTVisitor identifies guard clauses that raise
        exceptions for invalid input conditions.
        """
        code = '''
def validate(value):
    if not value:
        raise ValueError("Value required")
    return value
'''
        tree = ast.parse(code)
        visitor = ASTVisitor("test.py")
        visitor.visit(tree)
        
        assert len(visitor.guard_clauses) == 1
        guard = visitor.guard_clauses[0]
        assert guard.action == "raise"
        assert guard.function_name == "validate"

    def test_detect_error_handler_suppress(self):
        """Test detection of error handlers that suppress exceptions.

        Verifies that ASTVisitor identifies try-except blocks where
        exceptions are caught and silently ignored with 'pass'.
        """
        code = '''
def risky_operation():
    try:
        do_something()
    except Exception:
        pass
'''
        tree = ast.parse(code)
        visitor = ASTVisitor("test.py")
        visitor.visit(tree)
        
        assert len(visitor.error_handlers) == 1
        handler = visitor.error_handlers[0]
        assert handler.handler_action == "suppress"
        assert "Exception" in handler.exception_types

    def test_detect_error_handler_reraise(self):
        """Test detection of error handlers that re-raise exceptions.

        Verifies that ASTVisitor identifies try-except blocks where
        exceptions are caught and re-raised using bare 'raise'.
        """
        code = '''
def operation():
    try:
        do_something()
    except ValueError:
        raise
'''
        tree = ast.parse(code)
        visitor = ASTVisitor("test.py")
        visitor.visit(tree)
        
        assert len(visitor.error_handlers) == 1
        handler = visitor.error_handlers[0]
        assert handler.handler_action == "reraise"
        assert "ValueError" in handler.exception_types

    def test_detect_error_handler_transform(self):
        """Test detection of error handlers that transform exceptions.

        Verifies that ASTVisitor identifies try-except blocks where
        exceptions are caught and wrapped in a different exception type.
        """
        code = '''
def operation():
    try:
        do_something()
    except ValueError as e:
        raise RuntimeError("Wrapped") from e
'''
        tree = ast.parse(code)
        visitor = ASTVisitor("test.py")
        visitor.visit(tree)
        
        assert len(visitor.error_handlers) == 1
        handler = visitor.error_handlers[0]
        assert handler.handler_action == "transform"

    def test_detect_defensive_null_check(self):
        """Test detection of defensive null check patterns.

        Verifies that ASTVisitor identifies 'if x is None' patterns
        used for defensive programming against null values.
        """
        code = '''
def process(data):
    if data is None:
        return
    data.process()
'''
        tree = ast.parse(code)
        visitor = ASTVisitor("test.py")
        visitor.visit(tree)
        
        null_checks = [p for p in visitor.defensive_patterns if p.pattern_type == "null_check"]
        assert len(null_checks) == 1

    def test_detect_defensive_type_check(self):
        """Test detection of defensive type check patterns.

        Verifies that ASTVisitor identifies isinstance() calls used
        for runtime type checking.
        """
        code = '''
def process(data):
    if isinstance(data, str):
        return data.upper()
    return str(data)
'''
        tree = ast.parse(code)
        visitor = ASTVisitor("test.py")
        visitor.visit(tree)
        
        type_checks = [p for p in visitor.defensive_patterns if p.pattern_type == "type_check"]
        assert len(type_checks) == 1

    def test_detect_assertion(self):
        """Test detection of assertion statements.

        Verifies that ASTVisitor identifies assert statements used
        as defensive programming patterns.
        """
        code = '''
def process(value):
    assert value > 0, "Value must be positive"
    return value * 2
'''
        tree = ast.parse(code)
        visitor = ASTVisitor("test.py")
        visitor.visit(tree)
        
        assertions = [p for p in visitor.defensive_patterns if p.pattern_type == "assertion"]
        assert len(assertions) == 1

    def test_detect_constants(self):
        """Test detection of constant definitions.

        Verifies that ASTVisitor identifies module-level UPPER_CASE
        variable assignments as constants.
        """
        code = '''
MAX_SIZE = 100
DEFAULT_TIMEOUT = 30
API_KEY = "secret"
'''
        tree = ast.parse(code)
        visitor = ASTVisitor("test.py")
        visitor.visit(tree)
        
        constants = [p for p in visitor.naming_patterns if p.category == "constant"]
        constant_names = [c.name for c in constants]
        assert "MAX_SIZE" in constant_names
        assert "DEFAULT_TIMEOUT" in constant_names
        assert "API_KEY" in constant_names


class TestASTParser:
    """Tests for ASTParser class."""

    def test_parse_single_file(self):
        """Test parsing a single Python file.

        Creates a temporary file with a function containing a guard clause
        and verifies that ASTParser correctly parses and extracts the
        function and guard clause information.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test file
            test_file = Path(tmpdir) / "test.py"
            test_file.write_text('''
def validate_input(x):
    if x is None:
        return None
    return x
''')
            
            parser = ASTParser()
            visitor = parser.parse_file(test_file)
            
            assert visitor is not None
            assert visitor.function_count == 1
            assert len(visitor.guard_clauses) == 1

    def test_parse_invalid_file(self):
        """Test parsing an invalid Python file.

        Verifies that ASTParser returns None when attempting to parse
        a file with syntax errors instead of raising an exception.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create invalid Python file
            test_file = Path(tmpdir) / "invalid.py"
            test_file.write_text("def broken(")
            
            parser = ASTParser()
            visitor = parser.parse_file(test_file)
            
            # Should return None for unparseable files
            assert visitor is None

    def test_parse_repository(self):
        """Test parsing an entire repository.

        Creates a temporary directory with multiple Python files and verifies
        that ASTParser correctly aggregates statistics across all files,
        including function counts, class counts, guard clauses, and error handlers.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test files
            file1 = Path(tmpdir) / "module1.py"
            file1.write_text('''
def validate_user(user):
    if user is None:
        raise ValueError("User required")
    return user

class UserHandler:
    pass
''')
            
            file2 = Path(tmpdir) / "module2.py"
            file2.write_text('''
def process_data(data):
    try:
        return data.process()
    except Exception:
        pass

def get_config():
    return {}
''')
            
            parser = ASTParser()
            structure = parser.parse_repository(tmpdir)
            
            assert structure.file_count == 2
            assert structure.function_count == 3
            assert structure.class_count == 1
            assert len(structure.guard_clauses) == 1
            assert len(structure.error_handlers) == 1

    def test_excludes_venv_directories(self):
        """Test that virtual environment directories are excluded from parsing.

        Verifies that ASTParser skips files in 'venv' directories while
        still parsing files in other directories like 'src'.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test file in venv (should be excluded)
            venv_dir = Path(tmpdir) / "venv" / "lib"
            venv_dir.mkdir(parents=True)
            venv_file = venv_dir / "excluded.py"
            venv_file.write_text("def excluded(): pass")
            
            # Create test file in src (should be included)
            src_dir = Path(tmpdir) / "src"
            src_dir.mkdir()
            src_file = src_dir / "included.py"
            src_file.write_text("def included(): pass")
            
            parser = ASTParser()
            structure = parser.parse_repository(tmpdir)
            
            assert structure.file_count == 1
            assert structure.function_count == 1

    def test_nonexistent_repository(self):
        """Test parsing a nonexistent repository path.

        Verifies that ASTParser raises FileNotFoundError when given
        a path that does not exist.
        """
        parser = ASTParser()
        
        with pytest.raises(FileNotFoundError):
            parser.parse_repository("/nonexistent/path")


class TestCodeStructure:
    """Tests for CodeStructure dataclass."""

    def test_default_values(self):
        """Test CodeStructure default values.

        Verifies that a newly created CodeStructure instance has all
        fields initialized to their expected default values (empty lists,
        zero counts, empty dicts).
        """
        structure = CodeStructure()
        
        assert structure.naming_patterns == []
        assert structure.guard_clauses == []
        assert structure.error_handlers == []
        assert structure.defensive_patterns == []
        assert structure.function_count == 0
        assert structure.class_count == 0
        assert structure.file_count == 0
        assert structure.total_lines == 0
        assert structure.nesting_depths == []
        assert structure.repetition_motifs == {}
