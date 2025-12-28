"""
Tests for Motif Detector module.
"""

import pytest

from src.oneirocode.motif_detector import (
    MotifDetector,
    Motif,
    MotifAnalysis
)
from src.oneirocode.ast_parser import (
    CodeStructure,
    NamingPattern,
    GuardClause,
    ErrorHandler,
    DefensivePattern
)


class TestMotif:
    """Tests for Motif dataclass."""

    def test_create_motif(self):
        motif = Motif(
            name="The Retrieval Pattern",
            pattern_type="naming",
            occurrences=10,
            symbolic_meaning="A reaching out to acquire resources.",
            examples=[("test.py", 1), ("test.py", 10)],
            intensity=0.5
        )
        
        assert motif.name == "The Retrieval Pattern"
        assert motif.pattern_type == "naming"
        assert motif.occurrences == 10
        assert motif.intensity == 0.5
        assert len(motif.examples) == 2


class TestMotifDetector:
    """Tests for MotifDetector class."""

    def test_detect_empty_structure(self):
        detector = MotifDetector()
        structure = CodeStructure()
        
        analysis = detector.detect(structure)
        
        assert isinstance(analysis, MotifAnalysis)
        assert analysis.motifs == []

    def test_detect_naming_motifs_prefix(self):
        detector = MotifDetector()
        structure = CodeStructure(
            naming_patterns=[
                NamingPattern("get_user", "function", "test.py", 1, prefix="get_"),
                NamingPattern("get_config", "function", "test.py", 10, prefix="get_"),
                NamingPattern("get_data", "function", "test.py", 20, prefix="get_"),
                NamingPattern("get_settings", "function", "test.py", 30, prefix="get_"),
            ],
            function_count=4
        )
        
        analysis = detector.detect(structure)
        
        # Should detect get_ pattern as motif
        naming_motifs = [m for m in analysis.motifs if m.pattern_type == "naming"]
        assert len(naming_motifs) > 0
        
        # Check that get_ pattern is detected
        get_motifs = [m for m in naming_motifs if "Retrieval" in m.name]
        assert len(get_motifs) > 0

    def test_detect_naming_motifs_suffix(self):
        detector = MotifDetector()
        structure = CodeStructure(
            naming_patterns=[
                NamingPattern("UserHandler", "class", "test.py", 1, suffix="_handler"),
                NamingPattern("DataHandler", "class", "test.py", 10, suffix="_handler"),
                NamingPattern("RequestHandler", "class", "test.py", 20, suffix="_handler"),
                NamingPattern("EventHandler", "class", "test.py", 30, suffix="_handler"),
            ],
            function_count=0,
            class_count=4
        )
        
        analysis = detector.detect(structure)
        
        # Should detect _handler pattern as motif
        naming_motifs = [m for m in analysis.motifs if m.pattern_type == "naming"]
        assert len(naming_motifs) > 0

    def test_detect_structural_guard_heavy(self):
        detector = MotifDetector()
        structure = CodeStructure(
            guard_clauses=[
                GuardClause("test.py", 1, "x is None", "return", "func1"),
                GuardClause("test.py", 10, "not valid", "raise", "func2"),
                GuardClause("test.py", 20, "empty", "return", "func3"),
                GuardClause("test.py", 30, "error", "raise", "func4"),
            ],
            function_count=10
        )
        
        analysis = detector.detect(structure)
        
        # Should detect fortress/guard pattern
        structural_motifs = [m for m in analysis.motifs if m.pattern_type == "structural"]
        assert len(structural_motifs) > 0

    def test_detect_structural_try_heavy(self):
        detector = MotifDetector()
        structure = CodeStructure(
            error_handlers=[
                ErrorHandler("test.py", 1, ["Exception"], "handle", "func1"),
                ErrorHandler("test.py", 10, ["ValueError"], "handle", "func2"),
                ErrorHandler("test.py", 20, ["RuntimeError"], "handle", "func3"),
                ErrorHandler("test.py", 30, ["Exception"], "handle", "func4"),
            ],
            function_count=10
        )
        
        analysis = detector.detect(structure)
        
        # Should detect anxiety pattern
        structural_motifs = [m for m in analysis.motifs if m.pattern_type == "structural"]
        assert len(structural_motifs) > 0

    def test_detect_behavioral_silencing(self):
        detector = MotifDetector()
        structure = CodeStructure(
            error_handlers=[
                ErrorHandler("test.py", 1, ["Exception"], "suppress", "func1"),
                ErrorHandler("test.py", 10, ["Exception"], "suppress", "func2"),
                ErrorHandler("test.py", 20, ["Exception"], "suppress", "func3"),
            ],
            function_count=10
        )
        
        analysis = detector.detect(structure)
        
        # Should detect silencing behavioral pattern
        behavioral_motifs = [m for m in analysis.motifs if m.pattern_type == "behavioral"]
        silencing_motifs = [m for m in behavioral_motifs if "Silencing" in m.name]
        assert len(silencing_motifs) > 0

    def test_detect_behavioral_null_watch(self):
        detector = MotifDetector()
        structure = CodeStructure(
            defensive_patterns=[
                DefensivePattern("test.py", 1, "null_check", "x is None"),
                DefensivePattern("test.py", 10, "null_check", "y is None"),
                DefensivePattern("test.py", 20, "null_check", "z is None"),
                DefensivePattern("test.py", 30, "null_check", "data is None"),
            ],
            function_count=10
        )
        
        analysis = detector.detect(structure)
        
        # Should detect void watch pattern
        behavioral_motifs = [m for m in analysis.motifs if m.pattern_type == "behavioral"]
        void_watch = [m for m in behavioral_motifs if "Void Watch" in m.name]
        assert len(void_watch) > 0

    def test_detect_rhythmic_patterns(self):
        detector = MotifDetector()
        structure = CodeStructure(
            function_count=50,
            class_count=5,
            total_lines=1000
        )
        
        analysis = detector.detect(structure)
        
        # Should have rhythm signature
        assert analysis.rhythm_signature != ""
        
        # Should detect rhythmic motif
        rhythmic_motifs = [m for m in analysis.motifs if m.pattern_type == "rhythmic"]
        assert len(rhythmic_motifs) > 0

    def test_detect_repetition_motif(self):
        detector = MotifDetector()
        structure = CodeStructure(
            repetition_motifs={
                "args:2|body:If-Return|ret:True": 5,
                "args:1|body:Return|ret:True": 4,
                "args:0|body:Assign-Return|ret:True": 3,
            },
            function_count=20
        )
        
        analysis = detector.detect(structure)
        
        # Should detect ritual of repetition
        structural_motifs = [m for m in analysis.motifs if m.pattern_type == "structural"]
        repetition_motifs = [m for m in structural_motifs if "Repetition" in m.name]
        assert len(repetition_motifs) > 0

    def test_pattern_diversity(self):
        detector = MotifDetector()
        structure = CodeStructure(
            naming_patterns=[
                NamingPattern("get_data", "function", "test.py", 1, prefix="get_"),
                NamingPattern("get_user", "function", "test.py", 10, prefix="get_"),
                NamingPattern("get_config", "function", "test.py", 20, prefix="get_"),
            ],
            guard_clauses=[
                GuardClause("test.py", 1, "x is None", "return", "func1"),
                GuardClause("test.py", 10, "not valid", "raise", "func2"),
                GuardClause("test.py", 20, "empty", "return", "func3"),
                GuardClause("test.py", 30, "error", "raise", "func4"),
            ],
            error_handlers=[
                ErrorHandler("test.py", 1, ["Exception"], "suppress", "func1"),
                ErrorHandler("test.py", 10, ["Exception"], "suppress", "func2"),
                ErrorHandler("test.py", 20, ["Exception"], "suppress", "func3"),
            ],
            function_count=20,
            class_count=2,
            total_lines=500
        )
        
        analysis = detector.detect(structure)
        
        # Should have multiple pattern types
        pattern_types = set(m.pattern_type for m in analysis.motifs)
        assert len(pattern_types) >= 2

    def test_dominant_pattern(self):
        detector = MotifDetector()
        structure = CodeStructure(
            naming_patterns=[
                NamingPattern("validate_user", "function", "test.py", 1, prefix="validate_"),
                NamingPattern("validate_input", "function", "test.py", 10, prefix="validate_"),
                NamingPattern("validate_data", "function", "test.py", 20, prefix="validate_"),
                NamingPattern("validate_config", "function", "test.py", 30, prefix="validate_"),
                NamingPattern("validate_request", "function", "test.py", 40, prefix="validate_"),
            ],
            function_count=5
        )
        
        analysis = detector.detect(structure)
        
        # Should have a dominant pattern
        assert analysis.dominant_pattern is not None
