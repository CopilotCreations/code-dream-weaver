"""
Motif Detector Module

Identifies recurring structural and naming patterns across a codebase,
assigning symbolic meaning to repetition and rhythm.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Set, Tuple, Optional
from collections import Counter

from .ast_parser import CodeStructure, NamingPattern


@dataclass
class Motif:
    """Represents a detected recurring pattern."""
    name: str
    pattern_type: str  # 'structural', 'naming', 'behavioral', 'rhythmic'
    occurrences: int
    symbolic_meaning: str
    examples: List[Tuple[str, int]]  # (file_path, line_number)
    intensity: float  # 0.0 to 1.0, based on frequency


@dataclass
class MotifAnalysis:
    """Complete motif analysis results."""
    motifs: List[Motif] = field(default_factory=list)
    rhythm_signature: str = ""
    dominant_pattern: Optional[str] = None
    pattern_diversity: float = 0.0


class MotifDetector:
    """
    Detects and interprets recurring patterns in code.
    
    In dream analysis, recurring symbols carry amplified meaning.
    Similarly, recurring code patterns reveal the unconscious 
    habits and beliefs of the codebase's creators.
    """

    # Symbolic meanings for naming patterns
    NAMING_SYMBOLISM = {
        # Prefixes
        'get_': ("Retrieval", "A reaching out to acquire, to bring back what is needed. The code seeks external resources."),
        'set_': ("Assignment", "An act of establishment, placing value with intention. The code asserts state."),
        'is_': ("Inquiry", "A question about identity, seeking truth about nature. The code probes existence."),
        'has_': ("Possession", "A check for ownership, for containing multitudes. The code asks about abundance."),
        'can_': ("Capability", "A question of potential, of what might be. The code explores possibility."),
        'do_': ("Action", "A call to motion, to making things happen. The code commands change."),
        'make_': ("Creation", "The primal act of bringing forth. The code generates new existence."),
        'create_': ("Genesis", "Deliberate creation, the beginning of something new. The code initiates."),
        'build_': ("Construction", "Piece by piece assembly with purpose. The code erects structures."),
        'init_': ("Awakening", "The first breath, the initialization of being. The code brings to consciousness."),
        'validate_': ("Judgment", "The testing of worth, the examination of validity. The code pronounces verdict."),
        'check_': ("Vigilance", "The watchful eye, ever-scanning for truth. The code maintains awareness."),
        'process_': ("Transformation", "The journey through change. The code shepherds data through metamorphosis."),
        'handle_': ("Stewardship", "The careful management of responsibility. The code accepts duty."),
        '_': ("Privacy", "The hidden, the internal, the protected from outside gaze. The code guards secrets."),
        
        # Suffixes
        '_handler': ("Responsibility", "One who handles, who takes charge. This pattern accepts the burden of action."),
        '_manager': ("Authority", "One who manages, who directs. This pattern claims control."),
        '_factory': ("Production", "A place of making, of systematic creation. This pattern produces."),
        '_builder': ("Craftsmanship", "One who builds with care and intention. This pattern constructs."),
        '_validator': ("Judgment", "One who validates, who determines worth. This pattern evaluates."),
        '_processor': ("Alchemy", "One who transforms through process. This pattern transmutes."),
        '_helper': ("Service", "One who assists, who supports. This pattern aids."),
        '_util': ("Utility", "The practical, the useful. This pattern serves function."),
        '_service': ("Devotion", "One who serves, who provides. This pattern fulfills requests."),
        '_controller': ("Direction", "One who controls, who guides. This pattern steers."),
        '_impl': ("Manifestation", "The implementation, the concrete reality. This pattern realizes."),
        '_base': ("Foundation", "The base upon which others stand. This pattern supports."),
        '_mixin': ("Blending", "That which blends into others. This pattern shares essence."),
        '_error': ("Failure", "The acknowledgment of what went wrong. This pattern names problems."),
        '_exception': ("Interruption", "The breaking of normal flow. This pattern signals disruption."),
    }

    # Structural pattern symbolism
    STRUCTURAL_SYMBOLISM = {
        'guard_heavy': ("Fortress", "The code has built walls, checking repeatedly before allowing passage."),
        'try_heavy': ("Anxiety", "The code wraps itself in try blocks, anticipating failure at every turn."),
        'nested_deep': ("Labyrinth", "The code burrows deep, creating passages within passages."),
        'flat_simple': ("Prairie", "The code spreads flat and open, simple to traverse."),
        'function_many': ("Fragmentation", "The code is divided into many small pieces, each with singular purpose."),
        'function_few': ("Monolith", "The code concentrates power in few large functions."),
        'class_heavy': ("Society", "The code organizes into classes, creating hierarchies and relationships."),
        'class_sparse': ("Individualism", "The code favors functions over classes, preferring action to structure."),
    }

    def __init__(self):
        self.analysis = MotifAnalysis()

    def detect(self, structure: CodeStructure) -> MotifAnalysis:
        """Perform complete motif detection on code structure."""
        self.analysis = MotifAnalysis()
        
        # Detect naming motifs
        naming_motifs = self._detect_naming_motifs(structure)
        
        # Detect structural motifs
        structural_motifs = self._detect_structural_motifs(structure)
        
        # Detect behavioral motifs
        behavioral_motifs = self._detect_behavioral_motifs(structure)
        
        # Detect rhythmic patterns
        rhythmic_motifs, rhythm_sig = self._detect_rhythmic_patterns(structure)
        
        # Combine all motifs
        all_motifs = naming_motifs + structural_motifs + behavioral_motifs + rhythmic_motifs
        
        # Sort by intensity
        all_motifs.sort(key=lambda m: m.intensity, reverse=True)
        
        self.analysis.motifs = all_motifs
        self.analysis.rhythm_signature = rhythm_sig
        
        # Determine dominant pattern
        if all_motifs:
            self.analysis.dominant_pattern = all_motifs[0].name
        
        # Calculate diversity
        pattern_types = set(m.pattern_type for m in all_motifs)
        self.analysis.pattern_diversity = len(pattern_types) / 4.0  # 4 possible types
        
        return self.analysis

    def _detect_naming_motifs(self, structure: CodeStructure) -> List[Motif]:
        """Detect recurring naming patterns."""
        motifs = []
        
        # Count prefix occurrences
        prefix_counts: Dict[str, List[NamingPattern]] = {}
        suffix_counts: Dict[str, List[NamingPattern]] = {}
        
        for pattern in structure.naming_patterns:
            if pattern.prefix:
                if pattern.prefix not in prefix_counts:
                    prefix_counts[pattern.prefix] = []
                prefix_counts[pattern.prefix].append(pattern)
            
            if pattern.suffix:
                if pattern.suffix not in suffix_counts:
                    suffix_counts[pattern.suffix] = []
                suffix_counts[pattern.suffix].append(pattern)
        
        # Create motifs for significant patterns (3+ occurrences)
        for prefix, patterns in prefix_counts.items():
            if len(patterns) >= 3:
                name, meaning = self.NAMING_SYMBOLISM.get(
                    prefix, 
                    (prefix.strip('_').capitalize(), f"A recurring invocation of '{prefix}'")
                )
                
                intensity = min(1.0, len(patterns) / 20.0)
                
                motifs.append(Motif(
                    name=f"The {name} Pattern",
                    pattern_type='naming',
                    occurrences=len(patterns),
                    symbolic_meaning=meaning,
                    examples=[(p.file_path, p.line_number) for p in patterns[:5]],
                    intensity=intensity
                ))
        
        for suffix, patterns in suffix_counts.items():
            if len(patterns) >= 3:
                name, meaning = self.NAMING_SYMBOLISM.get(
                    suffix,
                    (suffix.strip('_').capitalize(), f"A recurring manifestation of '{suffix}'")
                )
                
                intensity = min(1.0, len(patterns) / 20.0)
                
                motifs.append(Motif(
                    name=f"The {name} Pattern",
                    pattern_type='naming',
                    occurrences=len(patterns),
                    symbolic_meaning=meaning,
                    examples=[(p.file_path, p.line_number) for p in patterns[:5]],
                    intensity=intensity
                ))
        
        return motifs

    def _detect_structural_motifs(self, structure: CodeStructure) -> List[Motif]:
        """Detect recurring structural patterns."""
        motifs = []
        
        # Analyze repetition motifs
        significant_repetitions = [
            (sig, count) for sig, count in structure.repetition_motifs.items()
            if count >= 3
        ]
        
        if significant_repetitions:
            total_repetitions = sum(count for _, count in significant_repetitions)
            motifs.append(Motif(
                name="The Ritual of Repetition",
                pattern_type='structural',
                occurrences=total_repetitions,
                symbolic_meaning="The code returns to familiar forms, finding comfort in known structures. Like a dreamer revisiting the same landscape, these patterns reveal unconscious preferences.",
                examples=[],
                intensity=min(1.0, len(significant_repetitions) / 10.0)
            ))
        
        # Check for guard-heavy pattern
        if structure.function_count > 0:
            guard_ratio = len(structure.guard_clauses) / structure.function_count
            if guard_ratio > 0.3:
                name, meaning = self.STRUCTURAL_SYMBOLISM['guard_heavy']
                motifs.append(Motif(
                    name=f"The {name}",
                    pattern_type='structural',
                    occurrences=len(structure.guard_clauses),
                    symbolic_meaning=meaning,
                    examples=[(g.file_path, g.line_number) for g in structure.guard_clauses[:5]],
                    intensity=min(1.0, guard_ratio * 2)
                ))
        
        # Check for try-heavy pattern
        if structure.function_count > 0:
            try_ratio = len(structure.error_handlers) / structure.function_count
            if try_ratio > 0.3:
                name, meaning = self.STRUCTURAL_SYMBOLISM['try_heavy']
                motifs.append(Motif(
                    name=f"The {name}",
                    pattern_type='structural',
                    occurrences=len(structure.error_handlers),
                    symbolic_meaning=meaning,
                    examples=[(e.file_path, e.line_number) for e in structure.error_handlers[:5]],
                    intensity=min(1.0, try_ratio * 2)
                ))
        
        # Check nesting depth patterns
        if structure.nesting_depths:
            avg_depth = sum(structure.nesting_depths) / len(structure.nesting_depths)
            if avg_depth > 3:
                name, meaning = self.STRUCTURAL_SYMBOLISM['nested_deep']
                motifs.append(Motif(
                    name=f"The {name}",
                    pattern_type='structural',
                    occurrences=len([d for d in structure.nesting_depths if d > 3]),
                    symbolic_meaning=meaning,
                    examples=[],
                    intensity=min(1.0, avg_depth / 5)
                ))
            elif avg_depth < 2 and structure.function_count > 5:
                name, meaning = self.STRUCTURAL_SYMBOLISM['flat_simple']
                motifs.append(Motif(
                    name=f"The {name}",
                    pattern_type='structural',
                    occurrences=structure.function_count,
                    symbolic_meaning=meaning,
                    examples=[],
                    intensity=0.5
                ))
        
        return motifs

    def _detect_behavioral_motifs(self, structure: CodeStructure) -> List[Motif]:
        """Detect recurring behavioral patterns."""
        motifs = []
        
        # Error handling behavior patterns
        if structure.error_handlers:
            action_counts = Counter(h.handler_action for h in structure.error_handlers)
            
            dominant_action = action_counts.most_common(1)[0] if action_counts else None
            if dominant_action and dominant_action[1] >= 3:
                action, count = dominant_action
                
                action_meanings = {
                    'suppress': ("The Silencing", "Errors are caught and silenced, their voices muffled. The code prefers peace to truth."),
                    'reraise': ("The Amplification", "Errors are caught and thrown again, their message preserved. The code believes in transparency."),
                    'transform': ("The Translation", "Errors are caught and transformed, their meaning reinterpreted. The code shapes the narrative."),
                    'log': ("The Recording", "Errors are caught and documented, their occurrence noted. The code maintains the record."),
                    'handle': ("The Resolution", "Errors are caught and addressed, their challenge met. The code takes responsibility."),
                }
                
                name, meaning = action_meanings.get(action, (action.capitalize(), f"A pattern of {action}"))
                
                motifs.append(Motif(
                    name=name,
                    pattern_type='behavioral',
                    occurrences=count,
                    symbolic_meaning=meaning,
                    examples=[(h.file_path, h.line_number) for h in structure.error_handlers 
                             if h.handler_action == action][:5],
                    intensity=min(1.0, count / 10)
                ))
        
        # Defensive pattern behavior
        if structure.defensive_patterns:
            pattern_counts = Counter(p.pattern_type for p in structure.defensive_patterns)
            
            for pattern_type, count in pattern_counts.most_common():
                if count >= 3:
                    pattern_meanings = {
                        'null_check': ("The Void Watch", "The code vigilantly guards against nothingness, checking for None at every turn."),
                        'type_check': ("The Identity Verification", "The code demands proof of type, questioning the nature of all that enters."),
                        'bounds_check': ("The Boundary Patrol", "The code watches the edges, ensuring nothing exceeds its proper limits."),
                        'assertion': ("The Truth Demand", "The code asserts what must be true, crashing if reality disagrees."),
                    }
                    
                    name, meaning = pattern_meanings.get(
                        pattern_type, 
                        (pattern_type.replace('_', ' ').title(), f"A pattern of {pattern_type}")
                    )
                    
                    motifs.append(Motif(
                        name=name,
                        pattern_type='behavioral',
                        occurrences=count,
                        symbolic_meaning=meaning,
                        examples=[(p.file_path, p.line_number) for p in structure.defensive_patterns
                                 if p.pattern_type == pattern_type][:5],
                        intensity=min(1.0, count / 15)
                    ))
        
        return motifs

    def _detect_rhythmic_patterns(self, structure: CodeStructure) -> Tuple[List[Motif], str]:
        """Detect rhythmic patterns in code organization."""
        motifs = []
        rhythm_parts = []
        
        # Analyze function-to-class ratio
        if structure.class_count > 0:
            func_class_ratio = structure.function_count / structure.class_count
            if func_class_ratio > 10:
                rhythm_parts.append("function-heavy")
            elif func_class_ratio < 3:
                rhythm_parts.append("class-heavy")
            else:
                rhythm_parts.append("balanced")
        else:
            rhythm_parts.append("procedural")
        
        # Analyze lines-to-function ratio (average function size)
        if structure.function_count > 0:
            avg_function_size = structure.total_lines / structure.function_count
            if avg_function_size > 50:
                rhythm_parts.append("long-form")
            elif avg_function_size < 15:
                rhythm_parts.append("short-form")
            else:
                rhythm_parts.append("medium-form")
        
        # Create rhythm signature
        rhythm_signature = "-".join(rhythm_parts)
        
        # Create rhythm motif
        rhythm_meanings = {
            "function-heavy-short-form": "The code moves in quick, staccato bursts—many small functions, each a brief note in a rapid melody.",
            "function-heavy-long-form": "The code flows in long procedural movements, each function a complete movement unto itself.",
            "class-heavy-short-form": "The code organizes into many small classes with brief methods, a society of specialists.",
            "class-heavy-long-form": "The code builds large, comprehensive classes, each a world unto itself.",
            "balanced-medium-form": "The code strikes a balance, mixing classes and functions in measured proportion.",
            "procedural-short-form": "The code tells its story through many brief functions, eschewing class structure entirely.",
            "procedural-long-form": "The code moves in long procedural waves, each function a substantial narrative.",
        }
        
        meaning = rhythm_meanings.get(
            rhythm_signature,
            f"The code follows a {rhythm_signature} rhythm, its own unique meter."
        )
        
        if structure.function_count > 0:
            motifs.append(Motif(
                name="The Rhythm of Structure",
                pattern_type='rhythmic',
                occurrences=structure.function_count + structure.class_count,
                symbolic_meaning=meaning,
                examples=[],
                intensity=0.6
            ))
        
        return motifs, rhythm_signature
