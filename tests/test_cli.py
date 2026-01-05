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
        """Test that the parser has the correct program name.

        Verifies that the parser is configured with 'oneirocode' as the
        program name, which is used in help messages and version output.
        """
        parser = create_parser()
        
        # Version should be accessible
        assert parser.prog == 'oneirocode'

    def test_parser_has_analyze_command(self):
        """Test that the parser supports the analyze command.

        Verifies that the parser correctly parses the 'analyze' command
        and extracts the repository path argument.
        """
        parser = create_parser()
        
        # Should parse analyze command
        args = parser.parse_args(['analyze', '/test/path'])
        assert args.command == 'analyze'
        assert args.repo_path == '/test/path'

    def test_parser_analyze_output_option(self):
        """Test that the parser supports the output option for analyze command.

        Verifies that the '-o' flag correctly sets the output file path
        for the analysis results.
        """
        parser = create_parser()
        
        args = parser.parse_args(['analyze', '/test/path', '-o', 'output.md'])
        assert args.output == 'output.md'

    def test_parser_analyze_quiet_option(self):
        """Test that the parser supports the quiet option for analyze command.

        Verifies that the '--quiet' flag is correctly parsed and sets
        the quiet attribute to True.
        """
        parser = create_parser()
        
        args = parser.parse_args(['analyze', '/test/path', '--quiet'])
        assert args.quiet is True

    def test_parser_analyze_llm_option(self):
        """Test that the parser supports the LLM option for analyze command.

        Verifies that the '--llm' flag is correctly parsed and sets
        the llm attribute to True for enabling LLM-enhanced analysis.
        """
        parser = create_parser()
        
        args = parser.parse_args(['analyze', '/test/path', '--llm'])
        assert args.llm is True


class TestMain:
    """Tests for main function."""

    def test_no_command_shows_help(self, capsys):
        """Test that running with no command shows help and returns success.

        Args:
            capsys: Pytest fixture for capturing stdout/stderr.
        """
        result = main([])
        
        assert result == 0

    def test_version_flag(self):
        """Test that the version flag displays version and exits cleanly.

        Verifies that '--version' causes a SystemExit with code 0
        after displaying version information.
        """
        with pytest.raises(SystemExit) as exc_info:
            main(['--version'])
        
        assert exc_info.value.code == 0

    def test_invalid_repo_path(self):
        """Test that analyzing a nonexistent path returns an error code.

        Verifies that the CLI returns exit code 1 when given a path
        that does not exist.
        """
        result = main(['analyze', '/nonexistent/path'])
        
        assert result == 1


class TestRunAnalyze:
    """Tests for run_analyze function."""

    def test_analyze_valid_repository(self, capsys):
        """Test analyzing a valid repository with Python files.

        Args:
            capsys: Pytest fixture for capturing stdout/stderr.

        Creates a temporary directory with a test Python file and verifies
        that the analysis completes successfully with expected output.
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
''')
            
            result = main(['analyze', tmpdir, '--quiet'])
            
            assert result == 0
            
            captured = capsys.readouterr()
            assert "Oneirocode Dream Interpretation" in captured.out

    def test_analyze_with_output_file(self):
        """Test that analysis results can be written to an output file.

        Creates a temporary directory with a test file and verifies that
        the analysis output is correctly written to the specified file.
        """
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
        """Test that analyzing a nonexistent path returns an error.

        Verifies that the CLI returns exit code 1 when the specified
        repository path does not exist.
        """
        result = main(['analyze', '/nonexistent/path'])
        
        assert result == 1

    def test_analyze_file_not_directory(self):
        """Test that analyzing a file instead of a directory returns an error.

        Verifies that the CLI returns exit code 1 when given a file path
        instead of a directory path.
        """
        with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as f:
            f.write(b"def test(): pass")
            f.flush()
            
            result = main(['analyze', f.name])
            
            assert result == 1

    def test_analyze_no_python_files(self):
        """Test that analyzing a directory with no Python files returns an error.

        Creates a temporary directory with only non-Python files and verifies
        that the CLI returns exit code 1.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create non-Python file
            test_file = Path(tmpdir) / "readme.txt"
            test_file.write_text("Hello World")
            
            result = main(['analyze', tmpdir, '--quiet'])
            
            assert result == 1

    def test_analyze_progress_messages(self, capsys):
        """Test that progress messages are displayed during analysis.

        Args:
            capsys: Pytest fixture for capturing stdout/stderr.

        Verifies that progress messages are written to stderr during
        the analysis process.
        """
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
        """Test a complete analysis workflow with a realistic mini-project.

        Creates a temporary project structure with multiple Python modules
        and verifies that the full analysis produces expected output sections
        including archetypes, motifs, and psychological profile.
        """
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
        """Test analyzing the oneirocode source itself.

        Args:
            capsys: Pytest fixture for capturing stdout/stderr.

        Verifies that the CLI can successfully analyze its own source code,
        serving as both a functional test and a demonstration of capabilities.
        """
        # Get path to src/oneirocode
        import src.oneirocode
        oneirocode_path = Path(src.oneirocode.__file__).parent
        
        if oneirocode_path.exists():
            result = main(['analyze', str(oneirocode_path), '--quiet'])
            
            assert result == 0
            
            captured = capsys.readouterr()
            assert "Oneirocode Dream Interpretation" in captured.out
