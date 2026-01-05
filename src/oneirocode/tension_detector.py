"""
Tension Detector Module

Identifies contradictions and unresolved tensions in code structure.
These tensions represent the psychic conflicts within the codebase.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Set, Tuple, Optional
from collections import defaultdict

from .ast_parser import CodeStructure, NamingPattern, GuardClause, ErrorHandler, DefensivePattern


@dataclass
class Tension:
    """Represents a detected tension or contradiction."""
    name: str
    tension_type: str  # 'contradiction', 'abandonment', 'over_engineering', 'under_engineering'
    description: str
    symbolic_interpretation: str
    severity: float  # 0.0 to 1.0
    locations: List[Tuple[str, int]]


@dataclass
class TensionAnalysis:
    """Complete tension analysis results."""
    tensions: List[Tension] = field(default_factory=list)
    overall_tension_level: float = 0.0
    primary_conflict: Optional[str] = None
    resolution_suggestions: List[str] = field(default_factory=list)


class TensionDetector:
    """
    Detects contradictions and unresolved tensions in code.
    
    Like dreams that reveal inner conflicts, code often contains
    contradictory impulses: validation without consumers, abstractions
    without implementations, guards without purposes.
    """

    def __init__(self):
        """Initialize the TensionDetector with an empty analysis."""
        self.analysis = TensionAnalysis()

    def detect(self, structure: CodeStructure) -> TensionAnalysis:
        """Perform complete tension detection on code structure.

        Analyzes the code structure to identify contradictions, abandonments,
        over-engineering, and under-engineering patterns.

        Args:
            structure: The parsed code structure containing functions, classes,
                error handlers, and defensive patterns to analyze.

        Returns:
            A TensionAnalysis object containing detected tensions sorted by
            severity, overall tension level, primary conflict, and resolution
            suggestions.
        """
        self.analysis = TensionAnalysis()
        
        # Detect various types of tensions
        contradictions = self._detect_contradictions(structure)
        abandonments = self._detect_abandonments(structure)
        over_engineering = self._detect_over_engineering(structure)
        under_engineering = self._detect_under_engineering(structure)
        
        # Combine all tensions
        all_tensions = contradictions + abandonments + over_engineering + under_engineering
        
        # Sort by severity
        all_tensions.sort(key=lambda t: t.severity, reverse=True)
        
        self.analysis.tensions = all_tensions
        
        # Calculate overall tension level
        if all_tensions:
            self.analysis.overall_tension_level = sum(t.severity for t in all_tensions) / len(all_tensions)
            self.analysis.primary_conflict = all_tensions[0].name if all_tensions else None
        
        # Generate resolution suggestions
        self._generate_resolution_suggestions()
        
        return self.analysis

    def _detect_contradictions(self, structure: CodeStructure) -> List[Tension]:
        """Detect contradictory patterns in code.

        Identifies tensions where the code exhibits opposing behaviors, such as
        heavy validation combined with error suppression, or defensive patterns
        paired with broad exception catching.

        Args:
            structure: The parsed code structure to analyze for contradictions.

        Returns:
            A list of Tension objects representing detected contradictions,
            each with symbolic interpretation and severity score.
        """
        tensions = []
        
        # Contradiction: Heavy validation but also heavy error suppression
        if structure.guard_clauses and structure.error_handlers:
            guard_count = len(structure.guard_clauses)
            suppress_count = sum(1 for h in structure.error_handlers if h.handler_action == 'suppress')
            
            if guard_count > 5 and suppress_count > 3:
                # Both guarding heavily AND suppressing errors
                severity = min(1.0, (guard_count + suppress_count) / 20)
                tensions.append(Tension(
                    name="The Guardian Who Closes Their Eyes",
                    tension_type='contradiction',
                    description=f"The code guards vigilantly ({guard_count} guards) but also suppresses errors ({suppress_count} suppressions).",
                    symbolic_interpretation="A profound contradiction: the code simultaneously demands perfection at entry yet ignores failures in execution. Like a parent who sets strict rules but looks away when they're broken. This suggests conflicting intentions—a desire for control wrestling with avoidance of consequences.",
                    severity=severity,
                    locations=[(g.file_path, g.line_number) for g in structure.guard_clauses[:3]]
                ))
        
        # Contradiction: Defensive patterns but broad exception catching
        if structure.defensive_patterns and structure.error_handlers:
            defensive_count = len(structure.defensive_patterns)
            broad_catches = [h for h in structure.error_handlers 
                           if 'Exception' in h.exception_types or 'BaseException' in h.exception_types]
            
            if defensive_count > 10 and len(broad_catches) > 3:
                severity = min(1.0, (defensive_count + len(broad_catches)) / 25)
                tensions.append(Tension(
                    name="The Precise Imprecision",
                    tension_type='contradiction',
                    description=f"Detailed defensive checks ({defensive_count}) coexist with broad exception catches ({len(broad_catches)}).",
                    symbolic_interpretation="The code is meticulous about input validation yet cavalier about error handling. It's like carefully checking IDs at the door but not noticing when the building catches fire. This reveals split consciousness—detail-oriented in one realm, negligent in another.",
                    severity=severity,
                    locations=[(p.file_path, p.line_number) for p in structure.defensive_patterns[:3]]
                ))
        
        # Contradiction: Many functions but few classes (or vice versa)
        if structure.function_count > 0 and structure.class_count > 0:
            ratio = structure.function_count / structure.class_count
            
            if ratio > 20:
                # Many functions per class - potentially god classes
                tensions.append(Tension(
                    name="The Overburdened Classes",
                    tension_type='contradiction',
                    description=f"Very high function-to-class ratio ({ratio:.1f}:1).",
                    symbolic_interpretation="Classes exist but carry immense burden, hosting many functions. The code believes in structure but concentrates power. Like organizations with hollow hierarchies—the form of delegation without its substance.",
                    severity=min(1.0, ratio / 50),
                    locations=[]
                ))
        
        return tensions

    def _detect_abandonments(self, structure: CodeStructure) -> List[Tension]:
        """Detect patterns suggesting abandoned or incomplete work.

        Identifies work-in-progress indicators in naming conventions (TODO, FIXME,
        HACK, etc.) and empty exception handlers that suggest unfinished intentions.

        Args:
            structure: The parsed code structure to analyze for abandonment patterns.

        Returns:
            A list of Tension objects representing detected abandonments,
            each with symbolic interpretation and severity score.
        """
        tensions = []
        
        # Look for naming patterns that suggest work in progress
        wip_indicators = ['todo', 'fixme', 'hack', 'temp', 'tmp', 'test_', 'debug']
        wip_patterns = []
        
        for pattern in structure.naming_patterns:
            name_lower = pattern.name.lower()
            if any(indicator in name_lower for indicator in wip_indicators):
                wip_patterns.append(pattern)
        
        if len(wip_patterns) >= 3:
            tensions.append(Tension(
                name="The Unfinished Symphony",
                tension_type='abandonment',
                description=f"Found {len(wip_patterns)} work-in-progress indicators in naming.",
                symbolic_interpretation="The code carries the marks of intention never fulfilled. TODOs and FIXMEs litter the landscape like abandoned construction sites. These are promises made to oneself and left unkept—a backlog of the soul.",
                severity=min(1.0, len(wip_patterns) / 10),
                locations=[(p.file_path, p.line_number) for p in wip_patterns[:5]]
            ))
        
        # Check for empty or near-empty error handlers (pass statements)
        empty_handlers = [h for h in structure.error_handlers if h.handler_action == 'suppress']
        
        if len(empty_handlers) >= 3:
            tensions.append(Tension(
                name="The Unspoken Failures",
                tension_type='abandonment',
                description=f"Found {len(empty_handlers)} empty or suppressing exception handlers.",
                symbolic_interpretation="Errors are caught but not addressed—acknowledged but not processed. Like receiving bad news and immediately forgetting it. The code knows things go wrong but refuses to speak of them.",
                severity=min(1.0, len(empty_handlers) / 8),
                locations=[(h.file_path, h.line_number) for h in empty_handlers[:5]]
            ))
        
        return tensions

    def _detect_over_engineering(self, structure: CodeStructure) -> List[Tension]:
        """Detect patterns suggesting over-engineering.

        Identifies excessive defensive patterns, overwhelming error handling,
        and deep nesting that indicate paranoid or overly complex code design.

        Args:
            structure: The parsed code structure to analyze for over-engineering.

        Returns:
            A list of Tension objects representing detected over-engineering
            patterns, each with symbolic interpretation and severity score.
        """
        tensions = []
        
        # Check for excessive defensive patterns relative to code size
        if structure.function_count > 0:
            defensive_ratio = len(structure.defensive_patterns) / structure.function_count
            
            if defensive_ratio > 1.0:
                tensions.append(Tension(
                    name="The Fortress of Paranoia",
                    tension_type='over_engineering',
                    description=f"Defensive pattern ratio of {defensive_ratio:.2f} per function.",
                    symbolic_interpretation="Every function bristles with defensive checks, more armor than action. The code trusts nothing, expecting attack from all sides. This hyper-vigilance suggests past trauma—perhaps production incidents or unreliable collaborators—now encoded into permanent wariness.",
                    severity=min(1.0, defensive_ratio / 2),
                    locations=[(p.file_path, p.line_number) for p in structure.defensive_patterns[:5]]
                ))
        
        # Check for excessive error handling
        if structure.function_count > 0:
            error_ratio = len(structure.error_handlers) / structure.function_count
            
            if error_ratio > 0.8:
                tensions.append(Tension(
                    name="The Fear of Failure",
                    tension_type='over_engineering',
                    description=f"Nearly every function wrapped in try-except ({error_ratio:.2f} ratio).",
                    symbolic_interpretation="The code cannot take a step without preparing for failure. This excessive caution suggests deep anxiety about consequences. Like someone who checks the stove five times before leaving—the behavior of a codebase that has been burned.",
                    severity=min(1.0, error_ratio),
                    locations=[(e.file_path, e.line_number) for e in structure.error_handlers[:5]]
                ))
        
        # Check for excessive nesting depth
        if structure.nesting_depths:
            deep_nesting = [d for d in structure.nesting_depths if d > 5]
            if len(deep_nesting) > 3:
                tensions.append(Tension(
                    name="The Endless Descent",
                    tension_type='over_engineering',
                    description=f"Found {len(deep_nesting)} instances of very deep nesting (>5 levels).",
                    symbolic_interpretation="The code burrows ever deeper, creating labyrinths of logic. Each condition spawns another, each loop contains more loops. This is the architecture of a mind that cannot simplify—that adds rather than abstracts.",
                    severity=min(1.0, len(deep_nesting) / 10),
                    locations=[]
                ))
        
        return tensions

    def _detect_under_engineering(self, structure: CodeStructure) -> List[Tension]:
        """Detect patterns suggesting under-engineering.

        Identifies lack of error handling, missing defensive patterns, and
        absence of structural organization that indicate insufficient care.

        Args:
            structure: The parsed code structure to analyze for under-engineering.

        Returns:
            A list of Tension objects representing detected under-engineering
            patterns, each with symbolic interpretation and severity score.
        """
        tensions = []
        
        # Check for lack of error handling
        if structure.function_count > 10 and len(structure.error_handlers) < 2:
            tensions.append(Tension(
                name="The Optimistic Ignorance",
                tension_type='under_engineering',
                description=f"{structure.function_count} functions but only {len(structure.error_handlers)} error handlers.",
                symbolic_interpretation="The code proceeds with unwavering optimism, barely acknowledging that things might go wrong. This isn't confidence—it's denial. Like walking a tightrope without a net, the code assumes perpetual success.",
                severity=0.6,
                locations=[]
            ))
        
        # Check for lack of defensive patterns
        if structure.function_count > 10 and len(structure.defensive_patterns) < 3:
            tensions.append(Tension(
                name="The Open Door Policy",
                tension_type='under_engineering',
                description=f"{structure.function_count} functions but only {len(structure.defensive_patterns)} defensive patterns.",
                symbolic_interpretation="The code accepts whatever it receives without question. No guards stand at the gates, no checks verify the visitors. This radical trust might be enlightened—or dangerously naive.",
                severity=0.5,
                locations=[]
            ))
        
        # Check for lack of structure (no classes in a large codebase)
        if structure.function_count > 20 and structure.class_count == 0:
            tensions.append(Tension(
                name="The Flat World",
                tension_type='under_engineering',
                description=f"{structure.function_count} functions but no classes.",
                symbolic_interpretation="The code spreads flat across the landscape, refusing hierarchy. While there's beauty in simplicity, this lack of structure in a larger codebase suggests resistance to organization—a preference for independence over community.",
                severity=0.4,
                locations=[]
            ))
        
        return tensions

    def _generate_resolution_suggestions(self):
        """Generate symbolic suggestions for resolving tensions.

        Creates human-readable suggestions for addressing each detected tension
        based on its type, storing up to 5 suggestions in the analysis results.
        """
        suggestions = []
        
        for tension in self.analysis.tensions:
            if tension.tension_type == 'contradiction':
                suggestions.append(
                    f"The '{tension.name}' calls for integration—reconciling opposing impulses into coherent intention."
                )
            elif tension.tension_type == 'abandonment':
                suggestions.append(
                    f"The '{tension.name}' whispers of unfinished business—commitments waiting to be honored or consciously released."
                )
            elif tension.tension_type == 'over_engineering':
                suggestions.append(
                    f"The '{tension.name}' suggests learning to trust—releasing some armor, allowing vulnerability."
                )
            elif tension.tension_type == 'under_engineering':
                suggestions.append(
                    f"The '{tension.name}' invites greater care—building structures to support future growth."
                )
        
        self.analysis.resolution_suggestions = suggestions[:5]  # Top 5 suggestions
