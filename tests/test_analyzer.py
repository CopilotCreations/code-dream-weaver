"""
Tests for Analyzer module.
"""

import pytest
import tempfile
from pathlib import Path

from src.oneirocode.analyzer import (
    OneirocodeAnalyzer,
    analyze_repository
)
from src.oneirocode.narrative_synthesizer import InterpretationReport


class TestOneirocodeAnalyzer:
    """Tests for OneirocodeAnalyzer class."""

    def test_init_default(self):
        analyzer = OneirocodeAnalyzer()
        
        assert analyzer.llm_enabled is False
        assert analyzer.structure is None
        assert analyzer.profile is None
        assert analyzer.motifs is None
        assert analyzer.tensions is None

    def test_init_with_llm(self):
        analyzer = OneirocodeAnalyzer(llm_enabled=True)
        
        assert analyzer.llm_enabled is True

    def test_analyze_valid_repository(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test file
            test_file = Path(tmpdir) / "test.py"
            test_file.write_text('''
def validate_input(x):
    if x is None:
        return None
    return x

def process_data(data):
    try:
        return data.process()
    except Exception:
        pass

class DataHandler:
    pass
''')
            
            analyzer = OneirocodeAnalyzer()
            report = analyzer.analyze(tmpdir)
            
            assert isinstance(report, InterpretationReport)
            assert report.word_count > 0
            assert "Oneirocode" in report.content

    def test_analyze_stores_results(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.py"
            test_file.write_text("def hello(): pass")
            
            analyzer = OneirocodeAnalyzer()
            analyzer.analyze(tmpdir)
            
            assert analyzer.structure is not None
            assert analyzer.profile is not None
            assert analyzer.motifs is not None
            assert analyzer.tensions is not None

    def test_analyze_nonexistent_path(self):
        analyzer = OneirocodeAnalyzer()
        
        with pytest.raises(FileNotFoundError):
            analyzer.analyze("/nonexistent/path")

    def test_analyze_empty_repository(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            analyzer = OneirocodeAnalyzer()
            
            with pytest.raises(ValueError) as exc_info:
                analyzer.analyze(tmpdir)
            
            assert "No Python files found" in str(exc_info.value)

    def test_get_structure(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.py"
            test_file.write_text("def hello(): pass")
            
            analyzer = OneirocodeAnalyzer()
            analyzer.analyze(tmpdir)
            
            structure = analyzer.get_structure()
            assert structure is not None
            assert structure.function_count == 1

    def test_get_profile(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.py"
            test_file.write_text("def validate_user(): pass")
            
            analyzer = OneirocodeAnalyzer()
            analyzer.analyze(tmpdir)
            
            profile = analyzer.get_profile()
            assert profile is not None

    def test_get_motifs(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.py"
            test_file.write_text('''
def get_user(): pass
def get_config(): pass
def get_data(): pass
''')
            
            analyzer = OneirocodeAnalyzer()
            analyzer.analyze(tmpdir)
            
            motifs = analyzer.get_motifs()
            assert motifs is not None

    def test_get_tensions(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.py"
            test_file.write_text('''
def validate(x):
    if x is None:
        raise ValueError()
    try:
        process(x)
    except:
        pass
''')
            
            analyzer = OneirocodeAnalyzer()
            analyzer.analyze(tmpdir)
            
            tensions = analyzer.get_tensions()
            assert tensions is not None


class TestAnalyzeRepository:
    """Tests for analyze_repository convenience function."""

    def test_analyze_repository_function(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.py"
            test_file.write_text("def hello(): pass")
            
            report = analyze_repository(tmpdir)
            
            assert isinstance(report, InterpretationReport)
            assert report.word_count > 0

    def test_analyze_repository_with_llm(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.py"
            test_file.write_text("def hello(): pass")
            
            # Should not raise even with llm_enabled (just ignored without config)
            report = analyze_repository(tmpdir, llm_enabled=True)
            
            assert isinstance(report, InterpretationReport)


class TestAnalyzerIntegration:
    """Integration tests for analyzer."""

    def test_complex_codebase_analysis(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a more complex project structure
            src_dir = Path(tmpdir) / "src"
            src_dir.mkdir()
            
            # Main module with various patterns
            main_file = src_dir / "main.py"
            main_file.write_text('''
"""Main module with various patterns."""

MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30

def validate_input(data):
    """Validate input data."""
    if data is None:
        raise ValueError("Data required")
    if not isinstance(data, dict):
        raise TypeError("Data must be dict")
    return data

def check_permissions(user):
    """Check user permissions."""
    if user is None:
        return False
    return user.has_permission

def process_request(request):
    """Process incoming request."""
    try:
        validated = validate_input(request)
        return _handle_request(validated)
    except ValueError as e:
        raise
    except Exception:
        pass

def _handle_request(data):
    """Internal request handler."""
    return data

class RequestHandler:
    """Handles HTTP requests."""
    
    def handle(self, request):
        if request is None:
            return None
        return self._process(request)
    
    def _process(self, request):
        return request

class DataManager:
    """Manages data operations."""
    
    def get_data(self, key):
        assert key is not None
        return {}
    
    def set_data(self, key, value):
        if key is None:
            raise ValueError("Key required")
        return True
''')
            
            # Utils module
            utils_file = src_dir / "utils.py"
            utils_file.write_text('''
"""Utility functions."""

def get_config():
    """Get configuration."""
    return {}

def get_logger():
    """Get logger instance."""
    return None

def create_session():
    """Create new session."""
    return {}

def build_response(data):
    """Build response object."""
    return {"data": data}

class ConfigFactory:
    """Creates configuration objects."""
    
    def create(self, name):
        return {}
''')
            
            analyzer = OneirocodeAnalyzer()
            report = analyzer.analyze(tmpdir)
            
            # Verify report structure
            assert "Oneirocode Dream Interpretation" in report.content
            assert "Dominant Archetypes" in report.content
            assert "Recurring Motifs" in report.content
            assert "Unresolved Tensions" in report.content
            assert "Psychological Profile" in report.content
            
            # Verify analysis captured patterns
            structure = analyzer.get_structure()
            assert structure.function_count > 5
            assert structure.class_count >= 2
            assert len(structure.guard_clauses) > 0
            
            profile = analyzer.get_profile()
            assert len(profile.dominant_archetypes) > 0 or len(profile.secondary_archetypes) > 0
