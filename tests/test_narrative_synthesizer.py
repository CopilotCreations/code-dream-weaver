"""
Tests for Narrative Synthesizer module.
"""

import pytest

from src.oneirocode.narrative_synthesizer import (
    NarrativeSynthesizer,
    InterpretationReport
)
from src.oneirocode.ast_parser import CodeStructure
from src.oneirocode.symbolic_ontology import (
    SymbolicProfile,
    ArchetypeMatch,
    Archetype
)
from src.oneirocode.motif_detector import MotifAnalysis, Motif
from src.oneirocode.tension_detector import TensionAnalysis, Tension


class TestInterpretationReport:
    """Tests for InterpretationReport dataclass."""

    def test_create_report(self):
        report = InterpretationReport(
            title="Test Report",
            generated_at="2024-01-01T00:00:00",
            content="# Test Content",
            word_count=2
        )
        
        assert report.title == "Test Report"
        assert report.word_count == 2


class TestNarrativeSynthesizer:
    """Tests for NarrativeSynthesizer class."""

    def test_synthesize_empty_analysis(self):
        synthesizer = NarrativeSynthesizer()
        
        structure = CodeStructure()
        profile = SymbolicProfile()
        motifs = MotifAnalysis()
        tensions = TensionAnalysis()
        
        report = synthesizer.synthesize(
            repo_path="/test/repo",
            structure=structure,
            profile=profile,
            motifs=motifs,
            tensions=tensions
        )
        
        assert isinstance(report, InterpretationReport)
        assert report.title == "Dream Interpretation: /test/repo"
        assert report.word_count > 0

    def test_report_contains_header(self):
        synthesizer = NarrativeSynthesizer()
        
        structure = CodeStructure(
            file_count=10,
            total_lines=1000,
            function_count=50,
            class_count=5
        )
        profile = SymbolicProfile()
        motifs = MotifAnalysis()
        tensions = TensionAnalysis()
        
        report = synthesizer.synthesize(
            repo_path="/test/repo",
            structure=structure,
            profile=profile,
            motifs=motifs,
            tensions=tensions
        )
        
        # Should contain header with metrics
        assert "Oneirocode Dream Interpretation" in report.content
        assert "Files Analyzed" in report.content
        assert "10" in report.content
        assert "1,000" in report.content

    def test_report_contains_archetypes(self):
        synthesizer = NarrativeSynthesizer()
        
        structure = CodeStructure(function_count=10)
        profile = SymbolicProfile(
            dominant_archetypes=[
                ArchetypeMatch(
                    archetype=Archetype.GUARDIAN,
                    strength=0.8,
                    evidence=["High validation ratio"],
                    locations=[("test.py", 10)]
                )
            ]
        )
        motifs = MotifAnalysis()
        tensions = TensionAnalysis()
        
        report = synthesizer.synthesize(
            repo_path="/test/repo",
            structure=structure,
            profile=profile,
            motifs=motifs,
            tensions=tensions
        )
        
        # Should contain archetype section
        assert "Dominant Archetypes" in report.content
        assert "Guardian" in report.content
        assert "80%" in report.content

    def test_report_contains_motifs(self):
        synthesizer = NarrativeSynthesizer()
        
        structure = CodeStructure(function_count=10)
        profile = SymbolicProfile()
        motifs = MotifAnalysis(
            motifs=[
                Motif(
                    name="The Retrieval Pattern",
                    pattern_type="naming",
                    occurrences=10,
                    symbolic_meaning="Reaching out to acquire resources.",
                    examples=[("test.py", 1)],
                    intensity=0.7
                )
            ],
            rhythm_signature="function-heavy-short-form"
        )
        tensions = TensionAnalysis()
        
        report = synthesizer.synthesize(
            repo_path="/test/repo",
            structure=structure,
            profile=profile,
            motifs=motifs,
            tensions=tensions
        )
        
        # Should contain motif section
        assert "Recurring Motifs" in report.content
        assert "Retrieval Pattern" in report.content

    def test_report_contains_tensions(self):
        synthesizer = NarrativeSynthesizer()
        
        structure = CodeStructure(function_count=10)
        profile = SymbolicProfile()
        motifs = MotifAnalysis()
        tensions = TensionAnalysis(
            tensions=[
                Tension(
                    name="The Guardian Who Closes Their Eyes",
                    tension_type="contradiction",
                    description="Guards vigilantly but suppresses errors.",
                    symbolic_interpretation="A profound contradiction...",
                    severity=0.7,
                    locations=[("test.py", 10)]
                )
            ],
            overall_tension_level=0.7
        )
        
        report = synthesizer.synthesize(
            repo_path="/test/repo",
            structure=structure,
            profile=profile,
            motifs=motifs,
            tensions=tensions
        )
        
        # Should contain tension section
        assert "Unresolved Tensions" in report.content
        assert "Guardian Who Closes Their Eyes" in report.content
        assert "contradiction" in report.content.lower()

    def test_report_contains_psychological_profile(self):
        synthesizer = NarrativeSynthesizer()
        
        structure = CodeStructure(
            function_count=10,
            nesting_depths=[2, 2, 3, 2, 2]
        )
        profile = SymbolicProfile(
            behavioral_traits=["Boundary-focused", "Error-confronting"]
        )
        motifs = MotifAnalysis()
        tensions = TensionAnalysis()
        
        report = synthesizer.synthesize(
            repo_path="/test/repo",
            structure=structure,
            profile=profile,
            motifs=motifs,
            tensions=tensions
        )
        
        # Should contain psychological profile section
        assert "Psychological Profile" in report.content

    def test_report_contains_closing(self):
        synthesizer = NarrativeSynthesizer()
        
        structure = CodeStructure(function_count=10)
        profile = SymbolicProfile()
        motifs = MotifAnalysis()
        tensions = TensionAnalysis()
        
        report = synthesizer.synthesize(
            repo_path="/test/repo",
            structure=structure,
            profile=profile,
            motifs=motifs,
            tensions=tensions
        )
        
        # Should contain closing section
        assert "Closing Reflection" in report.content
        assert "dreamer" in report.content.lower()

    def test_report_contains_resolution_suggestions(self):
        synthesizer = NarrativeSynthesizer()
        
        structure = CodeStructure(function_count=10)
        profile = SymbolicProfile()
        motifs = MotifAnalysis()
        tensions = TensionAnalysis(
            tensions=[
                Tension(
                    name="Test Tension",
                    tension_type="contradiction",
                    description="Test description",
                    symbolic_interpretation="Test interpretation",
                    severity=0.5,
                    locations=[]
                )
            ],
            resolution_suggestions=[
                "The 'Test Tension' calls for integration."
            ]
        )
        
        report = synthesizer.synthesize(
            repo_path="/test/repo",
            structure=structure,
            profile=profile,
            motifs=motifs,
            tensions=tensions
        )
        
        # Should contain resolution suggestions
        assert "Paths Forward" in report.content

    def test_strength_bar_creation(self):
        synthesizer = NarrativeSynthesizer()
        
        bar_full = synthesizer._create_strength_bar(1.0)
        bar_half = synthesizer._create_strength_bar(0.5)
        bar_empty = synthesizer._create_strength_bar(0.0)
        
        assert "█" in bar_full
        assert "░" in bar_empty
        assert bar_half.count("█") == 5
        assert bar_half.count("░") == 5

    def test_word_count_accuracy(self):
        synthesizer = NarrativeSynthesizer()
        
        structure = CodeStructure(function_count=10)
        profile = SymbolicProfile()
        motifs = MotifAnalysis()
        tensions = TensionAnalysis()
        
        report = synthesizer.synthesize(
            repo_path="/test/repo",
            structure=structure,
            profile=profile,
            motifs=motifs,
            tensions=tensions
        )
        
        # Word count should be reasonable
        assert report.word_count > 100
        assert report.word_count == len(report.content.split())
