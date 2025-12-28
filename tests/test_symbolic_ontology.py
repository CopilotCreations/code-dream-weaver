"""
Tests for Symbolic Ontology module.
"""

import pytest

from src.oneirocode.symbolic_ontology import (
    SymbolicOntology,
    Archetype,
    ArchetypeMatch,
    SymbolicProfile,
    get_archetype_description
)
from src.oneirocode.ast_parser import (
    CodeStructure,
    NamingPattern,
    GuardClause,
    ErrorHandler,
    DefensivePattern
)


class TestArchetype:
    """Tests for Archetype enum."""

    def test_archetype_values(self):
        assert Archetype.GUARDIAN.value == "guardian"
        assert Archetype.ANXIOUS_CARETAKER.value == "anxious_caretaker"
        assert Archetype.SUPPRESSOR.value == "suppressor"
        assert Archetype.BUILDER.value == "builder"

    def test_all_archetypes_have_descriptions(self):
        for archetype in Archetype:
            description = get_archetype_description(archetype)
            assert description is not None
            assert len(description) > 0


class TestSymbolicOntology:
    """Tests for SymbolicOntology class."""

    def test_analyze_empty_structure(self):
        ontology = SymbolicOntology()
        structure = CodeStructure()
        
        profile = ontology.analyze(structure)
        
        assert isinstance(profile, SymbolicProfile)
        assert profile.dominant_archetypes == []
        assert profile.secondary_archetypes == []

    def test_analyze_naming_patterns_guardian(self):
        ontology = SymbolicOntology()
        structure = CodeStructure(
            naming_patterns=[
                NamingPattern("validate_user", "function", "test.py", 1, prefix="validate_"),
                NamingPattern("validate_input", "function", "test.py", 5, prefix="validate_"),
                NamingPattern("validate_data", "function", "test.py", 10, prefix="validate_"),
            ],
            function_count=3
        )
        
        profile = ontology.analyze(structure)
        
        # Guardian should be detected due to validate_ prefix
        archetype_names = [a.archetype for a in profile.dominant_archetypes]
        assert Archetype.GUARDIAN in archetype_names

    def test_analyze_naming_patterns_builder(self):
        ontology = SymbolicOntology()
        structure = CodeStructure(
            naming_patterns=[
                NamingPattern("create_user", "function", "test.py", 1, prefix="create_"),
                NamingPattern("build_config", "function", "test.py", 5, prefix="build_"),
                NamingPattern("make_request", "function", "test.py", 10, prefix="make_"),
            ],
            function_count=3
        )
        
        profile = ontology.analyze(structure)
        
        # Builder/Factory archetypes should be detected
        archetype_names = [a.archetype for a in profile.dominant_archetypes + profile.secondary_archetypes]
        assert Archetype.BUILDER in archetype_names or Archetype.FACTORY in archetype_names

    def test_analyze_suffix_patterns(self):
        ontology = SymbolicOntology()
        structure = CodeStructure(
            naming_patterns=[
                NamingPattern("UserHandler", "class", "test.py", 1, suffix="_handler"),
                NamingPattern("DataHandler", "class", "test.py", 10, suffix="_handler"),
                NamingPattern("RequestHandler", "class", "test.py", 20, suffix="_handler"),
            ],
            function_count=0,
            class_count=3
        )
        
        profile = ontology.analyze(structure)
        
        # Helper archetype should be detected due to _handler suffix
        archetype_names = [a.archetype for a in profile.dominant_archetypes + profile.secondary_archetypes]
        assert Archetype.HELPER in archetype_names

    def test_analyze_guard_clauses_high_ratio(self):
        ontology = SymbolicOntology()
        structure = CodeStructure(
            guard_clauses=[
                GuardClause("test.py", 1, "x is None", "return", "func1"),
                GuardClause("test.py", 10, "not valid", "raise", "func2"),
                GuardClause("test.py", 20, "len(x) == 0", "return", "func3"),
                GuardClause("test.py", 30, "error", "raise", "func4"),
                GuardClause("test.py", 40, "invalid", "return", "func5"),
            ],
            function_count=10  # 50% guard ratio
        )
        
        profile = ontology.analyze(structure)
        
        # Anxious caretaker or gatekeeper should be detected
        archetype_names = [a.archetype for a in profile.dominant_archetypes + profile.secondary_archetypes]
        assert Archetype.ANXIOUS_CARETAKER in archetype_names or Archetype.GATEKEEPER in archetype_names

    def test_analyze_error_suppression(self):
        ontology = SymbolicOntology()
        structure = CodeStructure(
            error_handlers=[
                ErrorHandler("test.py", 1, ["Exception"], "suppress", "func1"),
                ErrorHandler("test.py", 10, ["Exception"], "suppress", "func2"),
                ErrorHandler("test.py", 20, ["Exception"], "suppress", "func3"),
                ErrorHandler("test.py", 30, ["Exception"], "suppress", "func4"),
                ErrorHandler("test.py", 40, ["Exception"], "suppress", "func5"),
            ],
            function_count=10
        )
        
        profile = ontology.analyze(structure)
        
        # Suppressor archetype should be detected
        archetype_names = [a.archetype for a in profile.dominant_archetypes + profile.secondary_archetypes]
        assert Archetype.SUPPRESSOR in archetype_names or Archetype.DENIER in archetype_names

    def test_analyze_deep_nesting(self):
        ontology = SymbolicOntology()
        structure = CodeStructure(
            nesting_depths=[5, 6, 7, 5, 6],  # Average > 4
            function_count=5
        )
        
        profile = ontology.analyze(structure)
        
        # Labyrinth dweller should be detected
        archetype_names = [a.archetype for a in profile.dominant_archetypes + profile.secondary_archetypes]
        assert Archetype.LABYRINTH_DWELLER in archetype_names

    def test_analyze_flat_structure(self):
        ontology = SymbolicOntology()
        structure = CodeStructure(
            nesting_depths=[1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1],  # Average < 2
            function_count=12
        )
        
        profile = ontology.analyze(structure)
        
        # Minimalist should be detected
        archetype_names = [a.archetype for a in profile.dominant_archetypes + profile.secondary_archetypes]
        assert Archetype.MINIMALIST in archetype_names

    def test_behavioral_traits_error_avoidant(self):
        ontology = SymbolicOntology()
        structure = CodeStructure(
            error_handlers=[
                ErrorHandler("test.py", 1, ["Exception"], "suppress", "func1"),
                ErrorHandler("test.py", 10, ["Exception"], "suppress", "func2"),
                ErrorHandler("test.py", 20, ["Exception"], "suppress", "func3"),
                ErrorHandler("test.py", 30, ["Exception"], "handle", "func4"),
            ],
            function_count=10
        )
        
        profile = ontology.analyze(structure)
        
        # Should have error-avoidant trait
        assert "Error-avoidant" in profile.behavioral_traits

    def test_behavioral_traits_hyper_vigilant(self):
        ontology = SymbolicOntology()
        structure = CodeStructure(
            defensive_patterns=[
                DefensivePattern("test.py", 1, "null_check", "x is None"),
                DefensivePattern("test.py", 5, "type_check", "isinstance(x, str)"),
                DefensivePattern("test.py", 10, "null_check", "y is None"),
                DefensivePattern("test.py", 15, "assertion", "assert x"),
                DefensivePattern("test.py", 20, "null_check", "z is None"),
                DefensivePattern("test.py", 25, "type_check", "isinstance(y, int)"),
            ],
            function_count=10
        )
        
        profile = ontology.analyze(structure)
        
        # Should have hyper-vigilant trait
        assert "Hyper-vigilant" in profile.behavioral_traits


class TestArchetypeMatch:
    """Tests for ArchetypeMatch dataclass."""

    def test_create_archetype_match(self):
        match = ArchetypeMatch(
            archetype=Archetype.GUARDIAN,
            strength=0.8,
            evidence=["High validation ratio"],
            locations=[("test.py", 10)]
        )
        
        assert match.archetype == Archetype.GUARDIAN
        assert match.strength == 0.8
        assert len(match.evidence) == 1
        assert len(match.locations) == 1


class TestGetArchetypeDescription:
    """Tests for get_archetype_description function."""

    def test_guardian_description(self):
        desc = get_archetype_description(Archetype.GUARDIAN)
        assert "Guardian" in desc
        assert "protective" in desc.lower() or "threshold" in desc.lower()

    def test_suppressor_description(self):
        desc = get_archetype_description(Archetype.SUPPRESSOR)
        assert "Suppressor" in desc
        assert "error" in desc.lower() or "silence" in desc.lower()

    def test_builder_description(self):
        desc = get_archetype_description(Archetype.BUILDER)
        assert "Builder" in desc
        assert "create" in desc.lower() or "structure" in desc.lower()
