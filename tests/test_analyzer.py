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
        """Test that OneirocodeAnalyzer initializes with correct defaults.

        Verifies that llm_enabled is False and all analysis results are None
        before any analysis is performed.
        """
        analyzer = OneirocodeAnalyzer()
        
        assert analyzer.llm_enabled is False
        assert analyzer.structure is None
        assert analyzer.profile is None
        assert analyzer.motifs is None
        assert analyzer.tensions is None

    def test_init_with_llm(self):
        """Test that OneirocodeAnalyzer correctly sets llm_enabled flag.

        Verifies that llm_enabled is True when passed to constructor.
        """
        analyzer = OneirocodeAnalyzer(llm_enabled=True)
        
        assert analyzer.llm_enabled is True

    def test_analyze_valid_repository(self):
        """Test analyzing a valid repository with Python files.

        Creates a temporary directory with Python code containing various
        patterns and verifies the analyzer produces a valid InterpretationReport.
        """
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
        """Test that analyze stores results in analyzer attributes.

        Verifies that structure, profile, motifs, and tensions are populated
        after analysis completes.
        """
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
        """Test that analyzing a nonexistent path raises FileNotFoundError.

        Verifies proper error handling when given an invalid repository path.
        """
        analyzer = OneirocodeAnalyzer()
        
        with pytest.raises(FileNotFoundError):
            analyzer.analyze("/nonexistent/path")

    def test_analyze_empty_repository(self):
        """Test that analyzing an empty repository raises ValueError.

        Verifies that a ValueError is raised with appropriate message when
        the repository contains no Python files.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            analyzer = OneirocodeAnalyzer()
            
            with pytest.raises(ValueError) as exc_info:
                analyzer.analyze(tmpdir)
            
            assert "No Python files found" in str(exc_info.value)

    def test_get_structure(self):
        """Test that get_structure returns parsed code structure.

        Verifies that after analysis, get_structure returns a valid structure
        object with correct function count.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.py"
            test_file.write_text("def hello(): pass")
            
            analyzer = OneirocodeAnalyzer()
            analyzer.analyze(tmpdir)
            
            structure = analyzer.get_structure()
            assert structure is not None
            assert structure.function_count == 1

    def test_get_profile(self):
        """Test that get_profile returns symbolic profile.

        Verifies that after analysis, get_profile returns a valid profile
        object based on the analyzed code.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.py"
            test_file.write_text("def validate_user(): pass")
            
            analyzer = OneirocodeAnalyzer()
            analyzer.analyze(tmpdir)
            
            profile = analyzer.get_profile()
            assert profile is not None

    def test_get_motifs(self):
        """Test that get_motifs returns detected recurring patterns.

        Verifies that after analysis, get_motifs returns detected motifs
        from code with repetitive naming patterns.
        """
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
        """Test that get_tensions returns detected code tensions.

        Verifies that after analysis, get_tensions returns detected tensions
        from code with error handling patterns.
        """
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
        """Test the analyze_repository convenience function.

        Verifies that the function creates an analyzer, performs analysis,
        and returns a valid InterpretationReport.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.py"
            test_file.write_text("def hello(): pass")
            
            report = analyze_repository(tmpdir)
            
            assert isinstance(report, InterpretationReport)
            assert report.word_count > 0

    def test_analyze_repository_with_llm(self):
        """Test analyze_repository with LLM enabled.

        Verifies that the function works with llm_enabled=True and gracefully
        handles the case where LLM config is not available.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.py"
            test_file.write_text("def hello(): pass")
            
            # Should not raise even with llm_enabled (just ignored without config)
            report = analyze_repository(tmpdir, llm_enabled=True)
            
            assert isinstance(report, InterpretationReport)


class TestAnalyzerIntegration:
    """Integration tests for analyzer."""

    def test_complex_codebase_analysis(self):
        """Test analyzer with a complex multi-file codebase.

        Creates a realistic project structure with multiple modules,
        classes, and various code patterns to verify comprehensive analysis.
        """
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
