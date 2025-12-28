"""
Tests for CLI module.
"""

import pytest
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

from src.oneirocode.cli import main, create_parser, run_analyze
from src.oneirocode import __version__


class TestCreateParser:
    """Tests for create_parser function."""

    def test_parser_has_version(self):
        parser = create_parser()
        
        # Version should be accessible
        assert parser.prog == 'oneirocode'

    def test_parser_has_analyze_command(self):
        parser = create_parser()
        
        # Should parse analyze command
        args = parser.parse_args(['analyze', '/test/path'])
        assert args.command == 'analyze'
        assert args.repo_path == '/test/path'

    def test_parser_analyze_output_option(self):
        parser = create_parser()
        
        args = parser.parse_args(['analyze', '/test/path', '-o', 'output.md'])
        assert args.output == 'output.md'

    def test_parser_analyze_quiet_option(self):
        parser = create_parser()
        
        args = parser.parse_args(['analyze', '/test/path', '--quiet'])
        assert args.quiet is True

    def test_parser_analyze_llm_option(self):
        parser = create_parser()
        
        args = parser.parse_args(['analyze', '/test/path', '--llm'])
        assert args.llm is True


class TestMain:
    """Tests for main function."""

    def test_no_command_shows_help(self, capsys):
        result = main([])
        
        assert result == 0

    def test_version_flag(self):
        with pytest.raises(SystemExit) as exc_info:
            main(['--version'])
        
        assert exc_info.value.code == 0

    def test_invalid_repo_path(self):
        result = main(['analyze', '/nonexistent/path'])
        
        assert result == 1


class TestRunAnalyze:
    """Tests for run_analyze function."""

    def test_analyze_valid_repository(self, capsys):
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
''')
            
            result = main(['analyze', tmpdir, '--quiet'])
            
            assert result == 0
            
            captured = capsys.readouterr()
            assert "Oneirocode Dream Interpretation" in captured.out

    def test_analyze_with_output_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test file
            test_file = Path(tmpdir) / "test.py"
            test_file.write_text("def hello(): pass")
            
            output_file = Path(tmpdir) / "output.md"
            
            result = main(['analyze', tmpdir, '-o', str(output_file), '--quiet'])
            
            assert result == 0
            assert output_file.exists()
            
            content = output_file.read_text()
            assert "Oneirocode Dream Interpretation" in content

    def test_analyze_nonexistent_path(self):
        result = main(['analyze', '/nonexistent/path'])
        
        assert result == 1

    def test_analyze_file_not_directory(self):
        with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as f:
            f.write(b"def test(): pass")
            f.flush()
            
            result = main(['analyze', f.name])
            
            assert result == 1

    def test_analyze_no_python_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create non-Python file
            test_file = Path(tmpdir) / "readme.txt"
            test_file.write_text("Hello World")
            
            result = main(['analyze', tmpdir, '--quiet'])
            
            assert result == 1

    def test_analyze_progress_messages(self, capsys):
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / "test.py"
            test_file.write_text("def hello(): pass")
            
            result = main(['analyze', tmpdir])
            
            assert result == 0
            
            captured = capsys.readouterr()
            # Progress messages go to stderr
            assert "Parsing codebase" in captured.err
            assert "Interpretation complete" in captured.err


class TestCLIIntegration:
    """Integration tests for CLI."""

    def test_full_analysis_workflow(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a realistic mini-project
            src_dir = Path(tmpdir) / "src"
            src_dir.mkdir()
            
            # Main module
            main_file = src_dir / "main.py"
            main_file.write_text('''
def validate_config(config):
    """Validate configuration."""
    if config is None:
        raise ValueError("Config required")
    if not isinstance(config, dict):
        raise TypeError("Config must be dict")
    return config

def process_request(request):
    """Process incoming request."""
    try:
        validated = validate_config(request)
        return handle_request(validated)
    except Exception as e:
        pass  # Suppress for now

class RequestHandler:
    """Handles requests."""
    
    def handle(self, request):
        if request is None:
            return None
        return self._process(request)
    
    def _process(self, request):
        return request
''')
            
            # Utils module
            utils_file = src_dir / "utils.py"
            utils_file.write_text('''
def get_config():
    """Get configuration."""
    return {}

def get_logger():
    """Get logger instance."""
    return None

def create_session():
    """Create new session."""
    return {}

MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30
''')
            
            output_file = Path(tmpdir) / "interpretation.md"
            
            result = main(['analyze', tmpdir, '-o', str(output_file), '--quiet'])
            
            assert result == 0
            assert output_file.exists()
            
            content = output_file.read_text()
            
            # Check for expected content
            assert "Oneirocode Dream Interpretation" in content
            assert "Dominant Archetypes" in content
            assert "Recurring Motifs" in content
            assert "Psychological Profile" in content

    def test_self_analysis(self, capsys):
        """Test analyzing the oneirocode source itself."""
        # Get path to src/oneirocode
        import src.oneirocode
        oneirocode_path = Path(src.oneirocode.__file__).parent
        
        if oneirocode_path.exists():
            result = main(['analyze', str(oneirocode_path), '--quiet'])
            
            assert result == 0
            
            captured = capsys.readouterr()
            assert "Oneirocode Dream Interpretation" in captured.out
