# Oneirocode

## A Dream Interpreter for Software Codebases

> *"Code is never merely functional. Every naming choice, every structural decision, every error handled or ignored carries meaning beyond its technical purpose."*

Oneirocode is a symbolic interpretation tool that analyzes Python codebases and produces psychoanalytic-style narrative interpretations. It treats code as symbolic expression rather than engineering artifact—revealing the unconscious patterns, archetypes, and tensions that emerge from the collective act of programming.

## Features

- **Static AST Analysis**: Parses Python source files to extract naming patterns, guard clauses, error handling, and defensive programming patterns
- **Symbolic Ontology**: Maps code patterns to psychological archetypes (Guardian, Anxious Caretaker, Suppressor, etc.)
- **Motif Detection**: Identifies recurring structural and naming patterns, assigning symbolic meaning to repetition
- **Tension Detection**: Discovers contradictions (validation without consumers, abstractions without users)
- **Narrative Synthesis**: Generates prose interpretations structured as psychological profiles

## Installation

```bash
# Clone the repository
git clone https://github.com/yourorg/oneirocode.git
cd oneirocode

# Create virtual environment (Python 3.11+)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

## Quick Start

```bash
# Analyze a repository
oneirocode analyze /path/to/your/repo

# Save output to file
oneirocode analyze /path/to/your/repo -o interpretation.md

# Quiet mode (no progress messages)
oneirocode analyze /path/to/your/repo --quiet
```

Or use the run.py entry point:

```bash
python run.py analyze /path/to/your/repo
```

## Symbolic Ontology

Oneirocode maps code patterns to symbolic archetypes. The mapping is **explicit, rule-based, and deterministic**—no randomness or external APIs are required.

### Archetypes

| Archetype | Triggered By | Symbolic Meaning |
|-----------|--------------|------------------|
| **Guardian** | `validate_*` functions, guard clauses | Protective patterns, boundary enforcement |
| **Sentinel** | `check_*` functions, logging handlers | Watchfulness, monitoring awareness |
| **Gatekeeper** | `guard_*` functions, early returns | Access control, strict conditions |
| **Anxious Caretaker** | High guard ratio, `ensure_*` patterns | Worry, excessive checking |
| **Perfectionist** | `verify_*` functions, heavy validation | Demand for correctness |
| **Authoritarian Gatekeeper** | Assert statements, raise-on-failure | Intolerance of deviation |
| **Builder** | `create_*`, `build_*` functions | Generative, constructive patterns |
| **Factory** | `*_factory` classes, `make_*` functions | Systematic creation |
| **Suppressor** | Empty except blocks, `pass` handlers | Error avoidance, denial |
| **Transformer** | `process_*`, `transform_*` functions | Data metamorphosis |
| **Labyrinth Dweller** | Deep nesting (>4 levels) | Complexity embrace |
| **Minimalist** | Flat structure, short functions | Simplicity preference |
| **Ritualist** | Repeated structural patterns | Pattern devotion |

### Naming Pattern Symbolism

| Pattern | Symbolic Meaning |
|---------|------------------|
| `get_*` | Retrieval—reaching out to acquire resources |
| `set_*` | Assignment—establishing state with intention |
| `is_*` | Inquiry—seeking truth about nature |
| `has_*` | Possession—checking for containing multitudes |
| `_*` (private) | Privacy—guarding secrets from outside gaze |
| `*_handler` | Responsibility—accepting the burden of action |
| `*_manager` | Authority—claiming control |
| `*_service` | Devotion—serving and providing |

## Output Format

Oneirocode produces a Markdown essay structured as:

1. **Codebase Vital Signs**: Quantitative metrics
2. **Dominant Archetypes**: The primary symbolic figures
3. **Recurring Motifs**: Patterns that repeat with amplified significance
4. **Unresolved Tensions**: Contradictions and conflicts
5. **Psychological Profile**: Synthesized character description
6. **Closing Reflection**: Interpretive conclusion

## Example Output

```markdown
# Oneirocode Dream Interpretation

## Repository: `my-project`

### Dominant Archetypes

#### 1. The Anxious Caretaker
**Presence Strength:** [████████░░] (80%)

> The Anxious Caretaker worries endlessly, checking and rechecking. 
> This code reveals deep concern about what might go wrong.

**Evidence:**
- High guard clause ratio (0.45)
- Naming pattern with prefix 'validate_'
- Extensive input validation

### Unresolved Tensions

#### The Guardian Who Closes Their Eyes
**Type:** Contradiction
**Severity:** [██████░░░░]

The code guards vigilantly (23 guards) but also suppresses errors (8 suppressions).

> A profound contradiction: the code simultaneously demands perfection 
> at entry yet ignores failures in execution...
```

## Architecture

```
src/oneirocode/
├── __init__.py           # Package initialization
├── analyzer.py           # Main orchestrator
├── ast_parser.py         # Python AST parsing and pattern extraction
├── cli.py                # Command-line interface
├── motif_detector.py     # Recurring pattern detection
├── narrative_synthesizer.py  # Prose generation
├── symbolic_ontology.py  # Archetype mapping rules
└── tension_detector.py   # Contradiction detection
```

See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed design documentation.

## Development

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=src/oneirocode --cov-report=html

# Format code
black src tests
isort src tests

# Type checking
mypy src

# Lint
flake8 src tests
```

## LLM Integration (Optional)

Oneirocode includes an optional LLM hook for enhanced narrative generation. This is **disabled by default** and requires external API configuration:

```bash
# Enable LLM mode (requires API key)
oneirocode analyze /path/to/repo --llm
```

Configure via environment variables:
```bash
export ONEIROCODE_LLM_ENABLED=true
export OPENAI_API_KEY=your-key-here
```

## Philosophy

Oneirocode is inspired by:

- **Jungian Psychology**: Archetypes as universal patterns of human expression
- **Dream Analysis**: Treating recurring symbols as meaningful communication
- **Code as Language**: Software as a form of human expression, not just engineering

The tool does not judge code quality—it interprets code symbolism, making conscious what was unconscious in the act of creation.

## License

MIT License - See LICENSE file for details.

## Contributing

Contributions are welcome! Please read our contributing guidelines and submit pull requests.

---

*"The dreamer must interpret their own dreams."*
