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
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create invalid Python file
            test_file = Path(tmpdir) / "invalid.py"
            test_file.write_text("def broken(")
            
            parser = ASTParser()
            visitor = parser.parse_file(test_file)
            
            # Should return None for unparseable files
            assert visitor is None

    def test_parse_repository(self):
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
        parser = ASTParser()
        
        with pytest.raises(FileNotFoundError):
            parser.parse_repository("/nonexistent/path")


class TestCodeStructure:
    """Tests for CodeStructure dataclass."""

    def test_default_values(self):
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
