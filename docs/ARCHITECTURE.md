# Oneirocode Architecture

## Overview

Oneirocode is designed as a modular pipeline that transforms source code into symbolic narrative interpretation. The architecture follows a clear data flow pattern with well-defined boundaries between components.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CLI Interface                                │
│                        (cli.py)                                      │
└─────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      OneirocodeAnalyzer                              │
│                       (analyzer.py)                                  │
│                                                                      │
│  Orchestrates the complete analysis pipeline:                        │
│  1. Parse → 2. Symbolize → 3. Detect Motifs → 4. Detect Tensions    │
│  5. Synthesize Narrative                                             │
└─────────────────────────────────────────────────────────────────────┘
                                   │
         ┌─────────────────────────┼─────────────────────────┐
         │                         │                         │
         ▼                         ▼                         ▼
┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
│   ASTParser     │   │SymbolicOntology │   │  MotifDetector  │
│ (ast_parser.py) │   │(symbolic_       │   │(motif_          │
│                 │   │ ontology.py)    │   │ detector.py)    │
│ Extracts:       │   │                 │   │                 │
│ - Naming        │   │ Maps patterns   │   │ Finds recurring │
│ - Guards        │   │ to archetypes   │   │ patterns        │
│ - Errors        │   │                 │   │                 │
│ - Defensive     │   │                 │   │                 │
└─────────────────┘   └─────────────────┘   └─────────────────┘
         │                         │                         │
         └─────────────────────────┼─────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      TensionDetector                                 │
│                   (tension_detector.py)                              │
│                                                                      │
│  Identifies contradictions and conflicts in the code structure       │
└─────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    NarrativeSynthesizer                              │
│                 (narrative_synthesizer.py)                           │
│                                                                      │
│  Generates prose interpretation from all analysis results            │
└─────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
                         Markdown Report
```

## Component Details

### 1. AST Parser (`ast_parser.py`)

The foundation of the analysis pipeline. Uses Python's built-in `ast` module to parse source files.

**Responsibilities:**
- Traverse repository and find Python files
- Parse each file into an Abstract Syntax Tree
- Extract structural patterns:
  - **Naming Patterns**: Function/class names with prefixes/suffixes
  - **Guard Clauses**: Early return/raise patterns at function start
  - **Error Handlers**: Try/except blocks and their behavior
  - **Defensive Patterns**: Null checks, type checks, assertions

**Key Classes:**
- `ASTVisitor`: Custom `ast.NodeVisitor` that extracts patterns
- `ASTParser`: Orchestrates file parsing across repository
- `CodeStructure`: Data class holding all extracted patterns

**Data Flow:**
```
Python Files → AST Trees → Pattern Extraction → CodeStructure
```

### 2. Symbolic Ontology (`symbolic_ontology.py`)

The interpretive core that maps code patterns to psychological archetypes.

**Responsibilities:**
- Define the archetype taxonomy (23 archetypes)
- Map naming patterns to archetypes via prefix/suffix rules
- Analyze guard clause density for anxiety indicators
- Evaluate error handling for coping strategies
- Calculate archetype strength scores

**Key Classes:**
- `Archetype`: Enum defining all symbolic archetypes
- `SymbolicOntology`: Rule engine for archetype mapping
- `SymbolicProfile`: Result containing dominant/secondary archetypes

**Mapping Rules:**
```python
NAMING_ARCHETYPES = {
    'validate_': Archetype.GUARDIAN,
    'check_': Archetype.SENTINEL,
    '_handler': Archetype.HELPER,
    '_factory': Archetype.FACTORY,
    ...
}
```

**Design Principle:** All mappings are explicit and deterministic. No machine learning, no probabilistic inference.

### 3. Motif Detector (`motif_detector.py`)

Identifies patterns that recur across the codebase, treating repetition as meaningful.

**Responsibilities:**
- Count naming pattern occurrences
- Detect structural repetition (similar function signatures)
- Identify behavioral patterns (error handling styles)
- Analyze code rhythm (function sizes, class ratios)

**Key Classes:**
- `Motif`: Represents a detected pattern with symbolic meaning
- `MotifDetector`: Pattern counting and interpretation
- `MotifAnalysis`: Collection of detected motifs

**Motif Types:**
1. **Naming Motifs**: Recurring prefixes/suffixes
2. **Structural Motifs**: Repeated code shapes
3. **Behavioral Motifs**: Consistent error handling
4. **Rhythmic Motifs**: Code organization patterns

### 4. Tension Detector (`tension_detector.py`)

Identifies contradictions and unresolved conflicts in code structure.

**Responsibilities:**
- Detect contradictory patterns (guarding + suppressing)
- Find abandonment indicators (TODOs, incomplete handlers)
- Identify over-engineering symptoms
- Identify under-engineering symptoms

**Key Classes:**
- `Tension`: Represents a detected conflict
- `TensionDetector`: Conflict identification logic
- `TensionAnalysis`: Collection with severity assessment

**Tension Types:**
1. **Contradiction**: Opposing patterns coexisting
2. **Abandonment**: Incomplete or deferred work
3. **Over-engineering**: Excessive complexity/defense
4. **Under-engineering**: Missing appropriate structure

### 5. Narrative Synthesizer (`narrative_synthesizer.py`)

Generates the final prose interpretation from all analysis results.

**Responsibilities:**
- Structure the report into sections
- Generate prose descriptions of archetypes
- Interpret motifs in symbolic language
- Describe tensions as psychological conflicts
- Create cohesive psychological profile

**Key Classes:**
- `NarrativeSynthesizer`: Prose generation engine
- `InterpretationReport`: Final output with metadata

**Report Structure:**
1. Header with vital signs
2. Introduction
3. Dominant Archetypes
4. Recurring Motifs
5. Unresolved Tensions
6. Psychological Profile
7. Closing Reflection

### 6. CLI Interface (`cli.py`)

User-facing command-line interface.

**Commands:**
- `oneirocode analyze <repo_path>`: Main analysis command

**Options:**
- `-o, --output`: Output file path
- `--llm`: Enable LLM enhancement (disabled by default)
- `--quiet`: Suppress progress messages

## Data Structures

### Core Data Classes

```python
@dataclass
class CodeStructure:
    naming_patterns: List[NamingPattern]
    guard_clauses: List[GuardClause]
    error_handlers: List[ErrorHandler]
    defensive_patterns: List[DefensivePattern]
    function_count: int
    class_count: int
    file_count: int
    total_lines: int
    nesting_depths: List[int]
    repetition_motifs: Dict[str, int]

@dataclass
class SymbolicProfile:
    dominant_archetypes: List[ArchetypeMatch]
    secondary_archetypes: List[ArchetypeMatch]
    naming_themes: Dict[str, int]
    behavioral_traits: List[str]

@dataclass
class MotifAnalysis:
    motifs: List[Motif]
    rhythm_signature: str
    dominant_pattern: Optional[str]
    pattern_diversity: float

@dataclass
class TensionAnalysis:
    tensions: List[Tension]
    overall_tension_level: float
    primary_conflict: Optional[str]
    resolution_suggestions: List[str]
```

## Design Decisions

### 1. Standard Library Only (Core)

The core analysis uses only Python's standard library (`ast`, `dataclasses`, `pathlib`). This ensures:
- No dependency conflicts
- Fast installation
- Broad compatibility

### 2. Deterministic Output

All pattern-to-archetype mappings are explicit rules, not ML models:
- Reproducible results
- Explainable interpretations
- No API dependencies

### 3. Separation of Analysis and Synthesis

Analysis (pattern extraction) is kept separate from synthesis (narrative generation):
- Testable components
- Swappable narrative styles
- Clear responsibilities

### 4. Optional LLM Hook

LLM integration is isolated and disabled by default:
- Core functionality works offline
- Enhanced mode available when configured
- Clean separation of concerns

## Extension Points

### Adding New Archetypes

1. Add to `Archetype` enum in `symbolic_ontology.py`
2. Add mapping rules in `NAMING_ARCHETYPES`
3. Add description in `get_archetype_description()`

### Adding New Motif Types

1. Create detection method in `MotifDetector`
2. Add to `NAMING_SYMBOLISM` or `STRUCTURAL_SYMBOLISM`
3. Include in `detect()` method

### Adding New Tension Types

1. Create detection method in `TensionDetector`
2. Add symbolic interpretation
3. Include in `detect()` method

### Custom Narrative Styles

1. Subclass `NarrativeSynthesizer`
2. Override section generation methods
3. Use in `OneirocodeAnalyzer`

## Performance Considerations

- **File Filtering**: Excludes venv, __pycache__, etc.
- **Lazy Parsing**: Files parsed on-demand
- **Bounded Collections**: Pattern lists capped for memory
- **No External I/O**: Core analysis is CPU-bound

## Testing Strategy

- **Unit Tests**: Each component tested in isolation
- **Integration Tests**: Full pipeline tests
- **Fixture Repository**: Test fixtures with known patterns
- **Coverage Target**: 75%+ line coverage
