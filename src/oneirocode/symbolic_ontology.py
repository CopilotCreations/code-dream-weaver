"""
Symbolic Ontology Module

Defines the mapping between code patterns and symbolic archetypes.
This is the core interpretive framework of Oneirocode.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Set, Tuple
from enum import Enum

from .ast_parser import CodeStructure, NamingPattern, GuardClause, ErrorHandler, DefensivePattern


class Archetype(Enum):
    """Symbolic archetypes representing psychological patterns in code."""
    
    # Guardian archetypes - protective patterns
    GUARDIAN = "guardian"
    SENTINEL = "sentinel"
    GATEKEEPER = "gatekeeper"
    
    # Control archetypes - authority patterns
    AUTHORITARIAN_GATEKEEPER = "authoritarian_gatekeeper"
    CONTROLLER = "controller"
    ORCHESTRATOR = "orchestrator"
    
    # Caretaker archetypes - nurturing/anxiety patterns
    ANXIOUS_CARETAKER = "anxious_caretaker"
    PERFECTIONIST = "perfectionist"
    OVERPROTECTIVE_PARENT = "overprotective_parent"
    
    # Creator archetypes - generative patterns
    BUILDER = "builder"
    FACTORY = "factory"
    ARCHITECT = "architect"
    
    # Servant archetypes - utility patterns
    HELPER = "helper"
    SERVANT = "servant"
    MESSENGER = "messenger"
    
    # Shadow archetypes - problematic patterns
    SUPPRESSOR = "suppressor"
    DENIER = "denier"
    ABANDONER = "abandoner"
    
    # Transformation archetypes
    TRANSFORMER = "transformer"
    ALCHEMIST = "alchemist"
    
    # Structural archetypes
    LABYRINTH_DWELLER = "labyrinth_dweller"
    MINIMALIST = "minimalist"
    RITUALIST = "ritualist"


@dataclass
class ArchetypeMatch:
    """Represents a detected archetype with supporting evidence."""
    archetype: Archetype
    strength: float  # 0.0 to 1.0
    evidence: List[str]
    locations: List[Tuple[str, int]]  # (file_path, line_number)


@dataclass 
class SymbolicProfile:
    """Complete symbolic profile of a codebase."""
    dominant_archetypes: List[ArchetypeMatch] = field(default_factory=list)
    secondary_archetypes: List[ArchetypeMatch] = field(default_factory=list)
    naming_themes: Dict[str, int] = field(default_factory=dict)
    behavioral_traits: List[str] = field(default_factory=list)


class SymbolicOntology:
    """
    Maps code patterns to symbolic archetypes using deterministic rules.
    
    The ontology treats code as psychological expression:
    - Naming patterns reveal self-perception and role-definition
    - Guard clauses indicate boundary-setting and trust levels
    - Error handling exposes anxiety management strategies
    - Defensive patterns show relationship with uncertainty
    """

    # Naming pattern to archetype mappings
    NAMING_ARCHETYPES = {
        # Prefixes
        'validate_': Archetype.GUARDIAN,
        'check_': Archetype.SENTINEL,
        'guard_': Archetype.GATEKEEPER,
        'ensure_': Archetype.ANXIOUS_CARETAKER,
        'verify_': Archetype.PERFECTIONIST,
        'assert_': Archetype.AUTHORITARIAN_GATEKEEPER,
        'create_': Archetype.BUILDER,
        'build_': Archetype.ARCHITECT,
        'make_': Archetype.FACTORY,
        'get_': Archetype.SERVANT,
        'fetch_': Archetype.MESSENGER,
        'handle_': Archetype.HELPER,
        'process_': Archetype.TRANSFORMER,
        'transform_': Archetype.ALCHEMIST,
        'convert_': Archetype.ALCHEMIST,
        
        # Suffixes
        '_handler': Archetype.HELPER,
        '_manager': Archetype.CONTROLLER,
        '_controller': Archetype.ORCHESTRATOR,
        '_factory': Archetype.FACTORY,
        '_builder': Archetype.BUILDER,
        '_validator': Archetype.GUARDIAN,
        '_guard': Archetype.GATEKEEPER,
        '_service': Archetype.SERVANT,
        '_helper': Archetype.HELPER,
        '_util': Archetype.HELPER,
        '_processor': Archetype.TRANSFORMER,
    }

    # Error handling behavior to archetype mappings
    ERROR_ARCHETYPES = {
        'suppress': Archetype.SUPPRESSOR,
        'reraise': Archetype.MESSENGER,
        'transform': Archetype.TRANSFORMER,
        'log': Archetype.SENTINEL,
        'handle': Archetype.HELPER,
    }

    # Threshold constants for classification
    GUARD_CLAUSE_ANXIETY_THRESHOLD = 0.3  # Ratio of functions with guards
    DEFENSIVE_PATTERN_PARANOIA_THRESHOLD = 0.5  # Ratio of defensive patterns
    ERROR_SUPPRESSION_DENIAL_THRESHOLD = 0.4  # Ratio of suppressed errors
    NESTING_LABYRINTH_THRESHOLD = 4  # Average nesting depth

    def __init__(self):
        self.profile = SymbolicProfile()

    def analyze(self, structure: CodeStructure) -> SymbolicProfile:
        """Perform complete symbolic analysis of code structure."""
        self.profile = SymbolicProfile()
        
        archetype_scores: Dict[Archetype, Tuple[float, List[str], List[Tuple[str, int]]]] = {}
        
        # Analyze naming patterns
        self._analyze_naming_patterns(structure, archetype_scores)
        
        # Analyze guard clauses
        self._analyze_guard_clauses(structure, archetype_scores)
        
        # Analyze error handling
        self._analyze_error_handlers(structure, archetype_scores)
        
        # Analyze defensive patterns
        self._analyze_defensive_patterns(structure, archetype_scores)
        
        # Analyze structural complexity
        self._analyze_structural_complexity(structure, archetype_scores)
        
        # Convert scores to matches and sort
        all_matches = []
        for archetype, (score, evidence, locations) in archetype_scores.items():
            if score > 0:
                normalized_score = min(1.0, score)
                all_matches.append(ArchetypeMatch(
                    archetype=archetype,
                    strength=normalized_score,
                    evidence=evidence,
                    locations=locations[:10]  # Limit locations
                ))
        
        all_matches.sort(key=lambda x: x.strength, reverse=True)
        
        # Split into dominant (top 3) and secondary
        self.profile.dominant_archetypes = all_matches[:3]
        self.profile.secondary_archetypes = all_matches[3:8]
        
        # Extract naming themes
        self._extract_naming_themes(structure)
        
        # Determine behavioral traits
        self._determine_behavioral_traits(structure)
        
        return self.profile

    def _add_archetype_score(
        self,
        scores: Dict[Archetype, Tuple[float, List[str], List[Tuple[str, int]]]],
        archetype: Archetype,
        delta: float,
        evidence: str,
        location: Tuple[str, int] = None
    ):
        """Add score to an archetype with evidence."""
        if archetype not in scores:
            scores[archetype] = (0.0, [], [])
        
        current_score, current_evidence, current_locations = scores[archetype]
        new_evidence = current_evidence + [evidence] if evidence not in current_evidence else current_evidence
        new_locations = current_locations + ([location] if location else [])
        scores[archetype] = (current_score + delta, new_evidence, new_locations)

    def _analyze_naming_patterns(
        self, 
        structure: CodeStructure,
        scores: Dict[Archetype, Tuple[float, List[str], List[Tuple[str, int]]]]
    ):
        """Analyze naming patterns for archetypal significance."""
        for pattern in structure.naming_patterns:
            # Check prefixes
            if pattern.prefix and pattern.prefix in self.NAMING_ARCHETYPES:
                archetype = self.NAMING_ARCHETYPES[pattern.prefix]
                self._add_archetype_score(
                    scores, archetype, 0.1,
                    f"Naming pattern with prefix '{pattern.prefix}'",
                    (pattern.file_path, pattern.line_number)
                )
            
            # Check suffixes
            if pattern.suffix and pattern.suffix in self.NAMING_ARCHETYPES:
                archetype = self.NAMING_ARCHETYPES[pattern.suffix]
                self._add_archetype_score(
                    scores, archetype, 0.1,
                    f"Naming pattern with suffix '{pattern.suffix}'",
                    (pattern.file_path, pattern.line_number)
                )
            
            # Track naming themes
            if pattern.prefix:
                self.profile.naming_themes[pattern.prefix] = \
                    self.profile.naming_themes.get(pattern.prefix, 0) + 1
            if pattern.suffix:
                self.profile.naming_themes[pattern.suffix] = \
                    self.profile.naming_themes.get(pattern.suffix, 0) + 1

    def _analyze_guard_clauses(
        self,
        structure: CodeStructure,
        scores: Dict[Archetype, Tuple[float, List[str], List[Tuple[str, int]]]]
    ):
        """Analyze guard clauses for boundary-setting patterns."""
        if structure.function_count == 0:
            return
        
        guard_ratio = len(structure.guard_clauses) / max(structure.function_count, 1)
        
        # High guard clause ratio indicates anxious caretaker
        if guard_ratio > self.GUARD_CLAUSE_ANXIETY_THRESHOLD:
            self._add_archetype_score(
                scores, Archetype.ANXIOUS_CARETAKER, 0.3,
                f"High guard clause ratio ({guard_ratio:.2f})"
            )
            self._add_archetype_score(
                scores, Archetype.GATEKEEPER, 0.2,
                "Extensive boundary checking"
            )
        
        # Analyze specific guard patterns
        raise_guards = [g for g in structure.guard_clauses if g.action == 'raise']
        return_guards = [g for g in structure.guard_clauses if g.action == 'return']
        
        if len(raise_guards) > len(return_guards):
            self._add_archetype_score(
                scores, Archetype.AUTHORITARIAN_GATEKEEPER, 0.2,
                "Prefers raising exceptions over silent returns"
            )
        elif len(return_guards) > len(raise_guards):
            self._add_archetype_score(
                scores, Archetype.HELPER, 0.2,
                "Prefers graceful degradation"
            )
        
        for guard in structure.guard_clauses:
            self._add_archetype_score(
                scores, Archetype.GUARDIAN, 0.05,
                f"Guard clause in {guard.function_name}",
                (guard.file_path, guard.line_number)
            )

    def _analyze_error_handlers(
        self,
        structure: CodeStructure,
        scores: Dict[Archetype, Tuple[float, List[str], List[Tuple[str, int]]]]
    ):
        """Analyze error handling for anxiety management patterns."""
        if not structure.error_handlers:
            return
        
        action_counts = {}
        for handler in structure.error_handlers:
            action_counts[handler.handler_action] = action_counts.get(handler.handler_action, 0) + 1
        
        total_handlers = len(structure.error_handlers)
        
        # Suppression indicates denial
        suppress_ratio = action_counts.get('suppress', 0) / total_handlers
        if suppress_ratio > self.ERROR_SUPPRESSION_DENIAL_THRESHOLD:
            self._add_archetype_score(
                scores, Archetype.SUPPRESSOR, 0.4,
                f"High error suppression ratio ({suppress_ratio:.2f})"
            )
            self._add_archetype_score(
                scores, Archetype.DENIER, 0.3,
                "Pattern of ignoring errors"
            )
        
        # Broad exception catches indicate over-protection
        broad_catches = [h for h in structure.error_handlers 
                        if 'Exception' in h.exception_types or 'BaseException' in h.exception_types]
        if len(broad_catches) > total_handlers * 0.5:
            self._add_archetype_score(
                scores, Archetype.OVERPROTECTIVE_PARENT, 0.3,
                "Frequent broad exception catching"
            )
        
        # Map actions to archetypes
        for action, count in action_counts.items():
            if action in self.ERROR_ARCHETYPES:
                archetype = self.ERROR_ARCHETYPES[action]
                self._add_archetype_score(
                    scores, archetype, count * 0.05,
                    f"Error handling pattern: {action}"
                )

    def _analyze_defensive_patterns(
        self,
        structure: CodeStructure,
        scores: Dict[Archetype, Tuple[float, List[str], List[Tuple[str, int]]]]
    ):
        """Analyze defensive patterns for trust/paranoia levels."""
        if structure.function_count == 0:
            return
        
        defensive_ratio = len(structure.defensive_patterns) / max(structure.function_count, 1)
        
        if defensive_ratio > self.DEFENSIVE_PATTERN_PARANOIA_THRESHOLD:
            self._add_archetype_score(
                scores, Archetype.ANXIOUS_CARETAKER, 0.3,
                f"High defensive pattern density ({defensive_ratio:.2f})"
            )
            self._add_archetype_score(
                scores, Archetype.PERFECTIONIST, 0.2,
                "Extensive input validation"
            )
        
        # Analyze pattern types
        pattern_types = {}
        for pattern in structure.defensive_patterns:
            pattern_types[pattern.pattern_type] = pattern_types.get(pattern.pattern_type, 0) + 1
        
        if pattern_types.get('assertion', 0) > 5:
            self._add_archetype_score(
                scores, Archetype.AUTHORITARIAN_GATEKEEPER, 0.2,
                "Heavy use of assertions"
            )
        
        if pattern_types.get('null_check', 0) > 10:
            self._add_archetype_score(
                scores, Archetype.SENTINEL, 0.2,
                "Vigilant null checking"
            )

    def _analyze_structural_complexity(
        self,
        structure: CodeStructure,
        scores: Dict[Archetype, Tuple[float, List[str], List[Tuple[str, int]]]]
    ):
        """Analyze structural complexity for maze/simplicity patterns."""
        if structure.nesting_depths:
            avg_nesting = sum(structure.nesting_depths) / len(structure.nesting_depths)
            max_nesting = max(structure.nesting_depths) if structure.nesting_depths else 0
            
            if avg_nesting > self.NESTING_LABYRINTH_THRESHOLD:
                self._add_archetype_score(
                    scores, Archetype.LABYRINTH_DWELLER, 0.4,
                    f"High average nesting depth ({avg_nesting:.2f})"
                )
            
            if max_nesting > 6:
                self._add_archetype_score(
                    scores, Archetype.LABYRINTH_DWELLER, 0.2,
                    f"Very deep nesting detected (depth {max_nesting})"
                )
            
            if avg_nesting < 2 and structure.function_count > 10:
                self._add_archetype_score(
                    scores, Archetype.MINIMALIST, 0.3,
                    "Flat, simple structure"
                )
        
        # Analyze repetition motifs for ritualistic behavior
        if structure.repetition_motifs:
            repeated_patterns = [sig for sig, count in structure.repetition_motifs.items() if count > 3]
            if len(repeated_patterns) > 5:
                self._add_archetype_score(
                    scores, Archetype.RITUALIST, 0.3,
                    f"Many repeated structural patterns ({len(repeated_patterns)})"
                )

    def _extract_naming_themes(self, structure: CodeStructure):
        """Extract dominant naming themes from patterns."""
        theme_counts: Dict[str, int] = {}
        
        for pattern in structure.naming_patterns:
            if pattern.prefix:
                theme_counts[pattern.prefix] = theme_counts.get(pattern.prefix, 0) + 1
            if pattern.suffix:
                theme_counts[pattern.suffix] = theme_counts.get(pattern.suffix, 0) + 1
        
        # Keep top themes
        sorted_themes = sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)
        self.profile.naming_themes = dict(sorted_themes[:10])

    def _determine_behavioral_traits(self, structure: CodeStructure):
        """Determine high-level behavioral traits."""
        traits = []
        
        # Error handling behavior
        if structure.error_handlers:
            suppress_count = sum(1 for h in structure.error_handlers if h.handler_action == 'suppress')
            if suppress_count > len(structure.error_handlers) * 0.3:
                traits.append("Error-avoidant")
            elif suppress_count < len(structure.error_handlers) * 0.1:
                traits.append("Error-confronting")
        
        # Defensive posture
        if structure.function_count > 0:
            defensive_ratio = len(structure.defensive_patterns) / structure.function_count
            if defensive_ratio > 0.5:
                traits.append("Hyper-vigilant")
            elif defensive_ratio < 0.1:
                traits.append("Trusting")
        
        # Guard clause behavior
        if structure.function_count > 0:
            guard_ratio = len(structure.guard_clauses) / structure.function_count
            if guard_ratio > 0.4:
                traits.append("Boundary-focused")
            elif guard_ratio < 0.1:
                traits.append("Permissive")
        
        # Structural traits
        if structure.nesting_depths:
            avg_nesting = sum(structure.nesting_depths) / len(structure.nesting_depths)
            if avg_nesting > 3:
                traits.append("Complexity-embracing")
            elif avg_nesting < 1.5:
                traits.append("Simplicity-seeking")
        
        self.profile.behavioral_traits = traits


def get_archetype_description(archetype: Archetype) -> str:
    """Get a symbolic description for an archetype."""
    descriptions = {
        Archetype.GUARDIAN: "The Guardian stands at the threshold, ensuring only the worthy may pass. This code expresses a protective instinct, validating and verifying before proceeding.",
        
        Archetype.SENTINEL: "The Sentinel watches ever-vigilant, logging and monitoring all that transpires. This code maintains awareness, recording the flow of data and events.",
        
        Archetype.GATEKEEPER: "The Gatekeeper controls access with strict conditions. This code establishes clear boundaries, turning away that which does not meet its criteria.",
        
        Archetype.AUTHORITARIAN_GATEKEEPER: "The Authoritarian Gatekeeper rules with an iron fist, raising exceptions without mercy. This code tolerates no deviation from its expectations.",
        
        Archetype.CONTROLLER: "The Controller seeks to manage and direct all aspects of the system. This code expresses a need for order and coordination.",
        
        Archetype.ORCHESTRATOR: "The Orchestrator conducts the symphony of components, ensuring harmony. This code coordinates complex interactions with careful timing.",
        
        Archetype.ANXIOUS_CARETAKER: "The Anxious Caretaker worries endlessly, checking and rechecking. This code reveals deep concern about what might go wrong.",
        
        Archetype.PERFECTIONIST: "The Perfectionist accepts nothing less than flawless input. This code strives for correctness through exhaustive validation.",
        
        Archetype.OVERPROTECTIVE_PARENT: "The Overprotective Parent shields from all harm, catching every exception. This code wraps everything in safety, perhaps too much.",
        
        Archetype.BUILDER: "The Builder creates new structures with purpose. This code is generative, bringing new entities into existence.",
        
        Archetype.FACTORY: "The Factory produces instances according to established patterns. This code embodies creation through standardized processes.",
        
        Archetype.ARCHITECT: "The Architect designs grand structures with vision. This code establishes foundations and frameworks for others to build upon.",
        
        Archetype.HELPER: "The Helper serves without ego, providing utility to others. This code exists to support and assist, asking nothing in return.",
        
        Archetype.SERVANT: "The Servant responds to requests with diligence. This code fetches and retrieves, mediating between systems.",
        
        Archetype.MESSENGER: "The Messenger carries information between realms. This code transmits and propagates, ensuring signals reach their destination.",
        
        Archetype.SUPPRESSOR: "The Suppressor silences errors, burying them in darkness. This code hides problems rather than confronting them.",
        
        Archetype.DENIER: "The Denier refuses to acknowledge what has occurred. This code pretends exceptions never happened.",
        
        Archetype.ABANDONER: "The Abandoner leaves tasks unfinished, paths unexplored. This code starts journeys it does not complete.",
        
        Archetype.TRANSFORMER: "The Transformer changes one form into another. This code is alchemical, transmuting data through its processes.",
        
        Archetype.ALCHEMIST: "The Alchemist works mysterious conversions. This code transforms the base into something precious.",
        
        Archetype.LABYRINTH_DWELLER: "The Labyrinth Dweller thrives in complexity, creating nested passages. This code embraces deep structures that challenge navigation.",
        
        Archetype.MINIMALIST: "The Minimalist achieves with economy, using only what is needed. This code expresses elegance through simplicity.",
        
        Archetype.RITUALIST: "The Ritualist repeats patterns with devotion. This code follows established ceremonies, finding meaning in repetition.",
    }
    return descriptions.get(archetype, "An undefined archetype awaiting interpretation.")
