"""
Main Analyzer Module

Coordinates all analysis components to produce complete codebase interpretations.
"""

from pathlib import Path
from typing import Optional

from .ast_parser import ASTParser, CodeStructure
from .symbolic_ontology import SymbolicOntology, SymbolicProfile
from .motif_detector import MotifDetector, MotifAnalysis
from .tension_detector import TensionDetector, TensionAnalysis
from .narrative_synthesizer import NarrativeSynthesizer, InterpretationReport


class OneirocodeAnalyzer:
    """
    Main analyzer that coordinates all interpretation components.
    
    This is the central orchestrator of the dream interpretation process,
    bringing together AST parsing, symbolic mapping, motif detection,
    tension analysis, and narrative synthesis.
    """

    def __init__(self, llm_enabled: bool = False):
        """
        Initialize the analyzer.
        
        Args:
            llm_enabled: Whether to enable LLM-enhanced interpretation.
                        Disabled by default; requires external API configuration.
        """
        self.llm_enabled = llm_enabled
        
        # Initialize all components
        self.parser = ASTParser()
        self.ontology = SymbolicOntology()
        self.motif_detector = MotifDetector()
        self.tension_detector = TensionDetector()
        self.synthesizer = NarrativeSynthesizer()
        
        # Analysis results
        self.structure: Optional[CodeStructure] = None
        self.profile: Optional[SymbolicProfile] = None
        self.motifs: Optional[MotifAnalysis] = None
        self.tensions: Optional[TensionAnalysis] = None

    def analyze(self, repo_path: str) -> InterpretationReport:
        """
        Perform complete analysis of a repository.
        
        Args:
            repo_path: Path to the repository to analyze.
            
        Returns:
            InterpretationReport containing the complete narrative interpretation.
            
        Raises:
            FileNotFoundError: If the repository path does not exist.
            ValueError: If no Python files are found in the repository.
        """
        path = Path(repo_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Repository path not found: {repo_path}")
        
        # Step 1: Parse the codebase
        self.structure = self.parser.parse_repository(repo_path)
        
        if self.structure.file_count == 0:
            raise ValueError(f"No Python files found in repository: {repo_path}")
        
        # Step 2: Perform symbolic analysis
        self.profile = self.ontology.analyze(self.structure)
        
        # Step 3: Detect motifs
        self.motifs = self.motif_detector.detect(self.structure)
        
        # Step 4: Detect tensions
        self.tensions = self.tension_detector.detect(self.structure)
        
        # Step 5: Synthesize narrative
        report = self.synthesizer.synthesize(
            repo_path=repo_path,
            structure=self.structure,
            profile=self.profile,
            motifs=self.motifs,
            tensions=self.tensions
        )
        
        return report

    def get_structure(self) -> Optional[CodeStructure]:
        """Get the parsed code structure from the last analysis."""
        return self.structure

    def get_profile(self) -> Optional[SymbolicProfile]:
        """Get the symbolic profile from the last analysis."""
        return self.profile

    def get_motifs(self) -> Optional[MotifAnalysis]:
        """Get the motif analysis from the last analysis."""
        return self.motifs

    def get_tensions(self) -> Optional[TensionAnalysis]:
        """Get the tension analysis from the last analysis."""
        return self.tensions


def analyze_repository(repo_path: str, llm_enabled: bool = False) -> InterpretationReport:
    """
    Convenience function to analyze a repository.
    
    Args:
        repo_path: Path to the repository to analyze.
        llm_enabled: Whether to enable LLM-enhanced interpretation.
        
    Returns:
        InterpretationReport containing the complete narrative interpretation.
    """
    analyzer = OneirocodeAnalyzer(llm_enabled=llm_enabled)
    return analyzer.analyze(repo_path)
