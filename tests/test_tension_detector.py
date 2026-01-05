"""
Tests for Tension Detector module.
"""

import pytest

from src.oneirocode.tension_detector import (
    TensionDetector,
    Tension,
    TensionAnalysis
)
from src.oneirocode.ast_parser import (
    CodeStructure,
    NamingPattern,
    GuardClause,
    ErrorHandler,
    DefensivePattern
)


class TestTension:
    """Tests for Tension dataclass."""

    def test_create_tension(self):
        """Test creating a Tension instance with all required fields.

        Verifies that a Tension object can be instantiated with name, type,
        description, symbolic interpretation, severity, and locations, and
        that all fields are correctly stored.
        """
        tension = Tension(
            name="The Guardian Who Closes Their Eyes",
            tension_type="contradiction",
            description="Guards vigilantly but suppresses errors.",
            symbolic_interpretation="A profound contradiction...",
            severity=0.7,
            locations=[("test.py", 10)]
        )
        
        assert tension.name == "The Guardian Who Closes Their Eyes"
        assert tension.tension_type == "contradiction"
        assert tension.severity == 0.7
        assert len(tension.locations) == 1


class TestTensionDetector:
    """Tests for TensionDetector class."""

    def test_detect_empty_structure(self):
        """Test tension detection on an empty code structure.

        Verifies that detecting tensions on an empty CodeStructure returns
        a TensionAnalysis with no tensions and zero overall tension level.
        """
        detector = TensionDetector()
        structure = CodeStructure()
        
        analysis = detector.detect(structure)
        
        assert isinstance(analysis, TensionAnalysis)
        assert analysis.tensions == []
        assert analysis.overall_tension_level == 0.0

    def test_detect_contradiction_guard_and_suppress(self):
        """Test detection of contradiction between guards and error suppression.

        Verifies that when code has both vigilant guard clauses and error
        suppression handlers, the detector identifies the 'Guardian Who Closes
        Their Eyes' contradiction tension.
        """
        detector = TensionDetector()
        structure = CodeStructure(
            guard_clauses=[
                GuardClause("test.py", 1, "x is None", "return", "func1"),
                GuardClause("test.py", 10, "not valid", "raise", "func2"),
                GuardClause("test.py", 20, "empty", "return", "func3"),
                GuardClause("test.py", 30, "error", "raise", "func4"),
                GuardClause("test.py", 40, "invalid", "return", "func5"),
                GuardClause("test.py", 50, "missing", "raise", "func6"),
            ],
            error_handlers=[
                ErrorHandler("test.py", 5, ["Exception"], "suppress", "func1"),
                ErrorHandler("test.py", 15, ["Exception"], "suppress", "func2"),
                ErrorHandler("test.py", 25, ["Exception"], "suppress", "func3"),
                ErrorHandler("test.py", 35, ["Exception"], "suppress", "func4"),
            ],
            function_count=10
        )
        
        analysis = detector.detect(structure)
        
        # Should detect the contradiction
        contradictions = [t for t in analysis.tensions if t.tension_type == "contradiction"]
        assert len(contradictions) > 0
        
        # Should have the "Guardian Who Closes Their Eyes" tension
        guardian_tension = [t for t in contradictions if "Guardian" in t.name]
        assert len(guardian_tension) > 0

    def test_detect_contradiction_defensive_broad_catch(self):
        """Test detection of contradiction between precise checks and broad catches.

        Verifies that when code has precise defensive patterns (null checks,
        type checks) combined with broad exception catches, the detector
        identifies this as a contradiction tension.
        """
        detector = TensionDetector()
        structure = CodeStructure(
            defensive_patterns=[
                DefensivePattern("test.py", 1, "null_check", "x is None"),
                DefensivePattern("test.py", 5, "type_check", "isinstance(x, str)"),
                DefensivePattern("test.py", 10, "null_check", "y is None"),
                DefensivePattern("test.py", 15, "assertion", "assert x"),
                DefensivePattern("test.py", 20, "null_check", "z is None"),
                DefensivePattern("test.py", 25, "type_check", "isinstance(y, int)"),
                DefensivePattern("test.py", 30, "null_check", "a is None"),
                DefensivePattern("test.py", 35, "type_check", "isinstance(z, list)"),
                DefensivePattern("test.py", 40, "null_check", "b is None"),
                DefensivePattern("test.py", 45, "null_check", "c is None"),
                DefensivePattern("test.py", 50, "null_check", "d is None"),
            ],
            error_handlers=[
                ErrorHandler("test.py", 100, ["Exception"], "suppress", "func1"),
                ErrorHandler("test.py", 110, ["BaseException"], "suppress", "func2"),
                ErrorHandler("test.py", 120, ["Exception"], "handle", "func3"),
                ErrorHandler("test.py", 130, ["Exception"], "suppress", "func4"),
            ],
            function_count=10
        )
        
        analysis = detector.detect(structure)
        
        # Should detect precise imprecision contradiction
        contradictions = [t for t in analysis.tensions if t.tension_type == "contradiction"]
        assert len(contradictions) > 0

    def test_detect_abandonment_wip_indicators(self):
        """Test detection of abandonment through work-in-progress indicators.

        Verifies that naming patterns containing TODO, FIXME, temp, or hack
        keywords are detected as abandonment tensions with the 'Unfinished
        Symphony' classification.
        """
        detector = TensionDetector()
        structure = CodeStructure(
            naming_patterns=[
                NamingPattern("todo_fix_later", "function", "test.py", 1),
                NamingPattern("fixme_validation", "function", "test.py", 10),
                NamingPattern("temp_solution", "function", "test.py", 20),
                NamingPattern("hack_workaround", "function", "test.py", 30),
            ],
            function_count=10
        )
        
        analysis = detector.detect(structure)
        
        # Should detect abandonment
        abandonments = [t for t in analysis.tensions if t.tension_type == "abandonment"]
        assert len(abandonments) > 0
        
        # Should have "Unfinished Symphony" tension
        unfinished = [t for t in abandonments if "Unfinished" in t.name]
        assert len(unfinished) > 0

    def test_detect_abandonment_empty_handlers(self):
        """Test detection of abandonment through empty error handlers.

        Verifies that error handlers that suppress exceptions without proper
        handling are detected as 'Unspoken Failures' abandonment tensions.
        """
        detector = TensionDetector()
        structure = CodeStructure(
            error_handlers=[
                ErrorHandler("test.py", 1, ["Exception"], "suppress", "func1"),
                ErrorHandler("test.py", 10, ["Exception"], "suppress", "func2"),
                ErrorHandler("test.py", 20, ["Exception"], "suppress", "func3"),
            ],
            function_count=10
        )
        
        analysis = detector.detect(structure)
        
        # Should detect unspoken failures
        abandonments = [t for t in analysis.tensions if t.tension_type == "abandonment"]
        unspoken = [t for t in abandonments if "Unspoken" in t.name]
        assert len(unspoken) > 0

    def test_detect_over_engineering_fortress(self):
        """Test detection of over-engineering through excessive defensive patterns.

        Verifies that an excessive number of defensive patterns relative to
        function count is detected as a 'Fortress of Paranoia' over-engineering
        tension.
        """
        detector = TensionDetector()
        structure = CodeStructure(
            defensive_patterns=[
                DefensivePattern("test.py", i, "null_check", f"check_{i}")
                for i in range(20)
            ],
            function_count=10
        )
        
        analysis = detector.detect(structure)
        
        # Should detect fortress of paranoia
        over_eng = [t for t in analysis.tensions if t.tension_type == "over_engineering"]
        fortress = [t for t in over_eng if "Fortress" in t.name or "Paranoia" in t.name]
        assert len(fortress) > 0

    def test_detect_over_engineering_fear_failure(self):
        """Test detection of over-engineering through excessive error handlers.

        Verifies that an excessive number of error handlers relative to
        function count is detected as a 'Fear of Failure' over-engineering
        tension.
        """
        detector = TensionDetector()
        structure = CodeStructure(
            error_handlers=[
                ErrorHandler("test.py", i, ["Exception"], "handle", f"func{i}")
                for i in range(15)
            ],
            function_count=10
        )
        
        analysis = detector.detect(structure)
        
        # Should detect fear of failure
        over_eng = [t for t in analysis.tensions if t.tension_type == "over_engineering"]
        fear = [t for t in over_eng if "Fear" in t.name]
        assert len(fear) > 0

    def test_detect_over_engineering_deep_nesting(self):
        """Test detection of over-engineering through deep nesting levels.

        Verifies that code with excessive nesting depths (6+ levels) is
        detected as an 'Endless Descent' over-engineering tension.
        """
        detector = TensionDetector()
        structure = CodeStructure(
            nesting_depths=[6, 7, 8, 6, 7],
            function_count=5
        )
        
        analysis = detector.detect(structure)
        
        # Should detect endless descent
        over_eng = [t for t in analysis.tensions if t.tension_type == "over_engineering"]
        descent = [t for t in over_eng if "Descent" in t.name]
        assert len(descent) > 0

    def test_detect_under_engineering_no_error_handling(self):
        """Test detection of under-engineering through missing error handling.

        Verifies that code with many functions but no error handlers is
        detected as 'Optimistic Ignorance' under-engineering tension.
        """
        detector = TensionDetector()
        structure = CodeStructure(
            error_handlers=[],
            function_count=20
        )
        
        analysis = detector.detect(structure)
        
        # Should detect optimistic ignorance
        under_eng = [t for t in analysis.tensions if t.tension_type == "under_engineering"]
        optimistic = [t for t in under_eng if "Optimistic" in t.name]
        assert len(optimistic) > 0

    def test_detect_under_engineering_no_defensive(self):
        """Test detection of under-engineering through missing defensive patterns.

        Verifies that code with many functions but no defensive patterns
        (null checks, type checks) is detected as 'Open Door Policy'
        under-engineering tension.
        """
        detector = TensionDetector()
        structure = CodeStructure(
            defensive_patterns=[],
            function_count=20
        )
        
        analysis = detector.detect(structure)
        
        # Should detect open door policy
        under_eng = [t for t in analysis.tensions if t.tension_type == "under_engineering"]
        open_door = [t for t in under_eng if "Open Door" in t.name]
        assert len(open_door) > 0

    def test_detect_under_engineering_no_classes(self):
        """Test detection of under-engineering through lack of class structure.

        Verifies that code with many functions but no classes is detected
        as 'Flat World' under-engineering tension, indicating missing
        abstraction layers.
        """
        detector = TensionDetector()
        structure = CodeStructure(
            function_count=30,
            class_count=0
        )
        
        analysis = detector.detect(structure)
        
        # Should detect flat world
        under_eng = [t for t in analysis.tensions if t.tension_type == "under_engineering"]
        flat_world = [t for t in under_eng if "Flat" in t.name]
        assert len(flat_world) > 0

    def test_overall_tension_level(self):
        """Test that overall tension level is calculated correctly.

        Verifies that when tensions are detected, the analysis includes
        a non-zero overall tension level representing the aggregate
        severity of all detected tensions.
        """
        detector = TensionDetector()
        structure = CodeStructure(
            guard_clauses=[
                GuardClause("test.py", i, "condition", "return", f"func{i}")
                for i in range(10)
            ],
            error_handlers=[
                ErrorHandler("test.py", i, ["Exception"], "suppress", f"func{i}")
                for i in range(5)
            ],
            function_count=15
        )
        
        analysis = detector.detect(structure)
        
        # Should have non-zero tension level
        assert analysis.overall_tension_level > 0

    def test_resolution_suggestions(self):
        """Test that resolution suggestions are provided for detected tensions.

        Verifies that when tensions are detected, the analysis includes
        actionable resolution suggestions to help address the identified
        code quality issues.
        """
        detector = TensionDetector()
        structure = CodeStructure(
            guard_clauses=[
                GuardClause("test.py", i, "condition", "return", f"func{i}")
                for i in range(10)
            ],
            error_handlers=[
                ErrorHandler("test.py", i, ["Exception"], "suppress", f"func{i}")
                for i in range(5)
            ],
            function_count=15
        )
        
        analysis = detector.detect(structure)
        
        # Should have resolution suggestions if tensions exist
        if analysis.tensions:
            assert len(analysis.resolution_suggestions) > 0

    def test_primary_conflict(self):
        """Test that the primary conflict is identified from detected tensions.

        Verifies that when multiple tensions are detected, the analysis
        identifies the most significant tension as the primary conflict
        for prioritized attention.
        """
        detector = TensionDetector()
        structure = CodeStructure(
            guard_clauses=[
                GuardClause("test.py", i, "condition", "return", f"func{i}")
                for i in range(10)
            ],
            error_handlers=[
                ErrorHandler("test.py", i, ["Exception"], "suppress", f"func{i}")
                for i in range(5)
            ],
            function_count=15
        )
        
        analysis = detector.detect(structure)
        
        # Should identify primary conflict
        if analysis.tensions:
            assert analysis.primary_conflict is not None
