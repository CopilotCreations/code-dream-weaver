"""
Command Line Interface Module

Provides the CLI entrypoint for Oneirocode.
"""

import argparse
import sys
import io
from pathlib import Path

from . import __version__
from .analyzer import OneirocodeAnalyzer


def _ensure_utf8_stdout():
    """Ensure stdout uses UTF-8 encoding on Windows."""
    if sys.platform == 'win32':
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        elif hasattr(sys.stdout, 'buffer'):
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        prog='oneirocode',
        description='Oneirocode - A Dream Interpreter for Software Codebases',
        epilog='For more information, visit: https://github.com/oneirocode'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Analyze command
    analyze_parser = subparsers.add_parser(
        'analyze',
        help='Analyze a repository and generate a dream interpretation'
    )
    
    analyze_parser.add_argument(
        'repo_path',
        type=str,
        help='Path to the repository to analyze'
    )
    
    analyze_parser.add_argument(
        '-o', '--output',
        type=str,
        default=None,
        help='Output file path (default: stdout)'
    )
    
    analyze_parser.add_argument(
        '--llm',
        action='store_true',
        default=False,
        help='Enable LLM-enhanced interpretation (requires API configuration)'
    )
    
    analyze_parser.add_argument(
        '--quiet',
        action='store_true',
        default=False,
        help='Suppress progress messages'
    )
    
    return parser


def run_analyze(args: argparse.Namespace) -> int:
    """Run the analyze command."""
    repo_path = args.repo_path
    output_path = args.output
    llm_enabled = args.llm
    quiet = args.quiet
    
    # Validate repository path
    path = Path(repo_path)
    if not path.exists():
        print(f"Error: Repository path not found: {repo_path}", file=sys.stderr)
        return 1
    
    if not path.is_dir():
        print(f"Error: Path is not a directory: {repo_path}", file=sys.stderr)
        return 1
    
    # Perform analysis
    try:
        if not quiet:
            print(f"🌙 Oneirocode Dream Interpreter v{__version__}", file=sys.stderr)
            print(f"📂 Analyzing: {repo_path}", file=sys.stderr)
            print("", file=sys.stderr)
        
        analyzer = OneirocodeAnalyzer(llm_enabled=llm_enabled)
        
        if not quiet:
            print("🔍 Parsing codebase...", file=sys.stderr)
        
        report = analyzer.analyze(repo_path)
        
        if not quiet:
            structure = analyzer.get_structure()
            print(f"   Found {structure.file_count} files, {structure.function_count} functions", file=sys.stderr)
            print("🎭 Mapping symbolic archetypes...", file=sys.stderr)
            print("🔄 Detecting recurring motifs...", file=sys.stderr)
            print("⚡ Identifying tensions...", file=sys.stderr)
            print("📝 Synthesizing narrative...", file=sys.stderr)
            print("", file=sys.stderr)
            print(f"✨ Interpretation complete ({report.word_count} words)", file=sys.stderr)
            print("", file=sys.stderr)
        
        # Output the report
        if output_path:
            output_file = Path(output_path)
            output_file.write_text(report.content, encoding='utf-8')
            if not quiet:
                print(f"📄 Report saved to: {output_path}", file=sys.stderr)
        else:
            print(report.content)
        
        return 0
        
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}", file=sys.stderr)
        return 1


def main(argv: list = None) -> int:
    """Main CLI entrypoint."""
    _ensure_utf8_stdout()
    
    parser = create_parser()
    args = parser.parse_args(argv)
    
    if args.command is None:
        parser.print_help()
        return 0
    
    if args.command == 'analyze':
        return run_analyze(args)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
