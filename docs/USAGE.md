# Oneirocode Usage Guide

## Installation

### Prerequisites

- Python 3.11 or higher
- pip package manager

### Quick Install

```bash
# Clone the repository
git clone https://github.com/yourorg/oneirocode.git
cd oneirocode

# Create and activate virtual environment
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install package in development mode
pip install -e .
```

## Basic Usage

### Analyzing a Repository

The primary command is `analyze`, which takes a path to a Python repository:

```bash
oneirocode analyze /path/to/your/project
```

This will:
1. Scan all Python files in the repository
2. Extract naming patterns, guard clauses, and error handlers
3. Map patterns to symbolic archetypes
4. Detect recurring motifs
5. Identify unresolved tensions
6. Generate a Markdown interpretation

### Output Options

#### Print to Console (Default)

```bash
oneirocode analyze /path/to/project
```

#### Save to File

```bash
oneirocode analyze /path/to/project -o interpretation.md
```

#### Quiet Mode

Suppress progress messages (useful for scripting):

```bash
oneirocode analyze /path/to/project --quiet > interpretation.md
```

### Using run.py

Alternatively, use the entry point directly:

```bash
python run.py analyze /path/to/project
```

## Command Reference

### `oneirocode analyze`

Analyze a repository and generate a dream interpretation.

```
Usage: oneirocode analyze [OPTIONS] REPO_PATH

Arguments:
  REPO_PATH        Path to the repository to analyze

Options:
  -o, --output     Output file path (default: stdout)
  --llm            Enable LLM-enhanced interpretation
  --quiet          Suppress progress messages
  -h, --help       Show help message
```

### `oneirocode --version`

Display version information:

```bash
oneirocode --version
```

### `oneirocode --help`

Display help information:

```bash
oneirocode --help
```

## Understanding the Output

### Report Structure

The generated Markdown report contains the following sections:

#### 1. Codebase Vital Signs

Quantitative metrics about the analyzed codebase:

```markdown
| Metric | Value |
|--------|-------|
| Files Analyzed | 42 |
| Total Lines | 12,345 |
| Functions | 234 |
| Classes | 45 |
| Guard Clauses | 78 |
| Error Handlers | 56 |
| Defensive Patterns | 89 |
```

#### 2. Dominant Archetypes

The primary symbolic figures detected in the code, with:
- Archetype name and description
- Presence strength (0-100%)
- Evidence supporting the classification

```markdown
### 1. The Guardian
**Presence Strength:** [████████░░] (80%)

> The Guardian stands at the threshold, ensuring only the worthy may pass.

**Evidence:**
- High guard clause ratio (0.45)
- Naming pattern with prefix 'validate_'
```

#### 3. Recurring Motifs

Patterns that appear repeatedly, organized by type:
- Naming Motifs (prefix/suffix patterns)
- Structural Motifs (code shapes)
- Behavioral Motifs (error handling)
- Rhythmic Motifs (organization patterns)

#### 4. Unresolved Tensions

Contradictions and conflicts detected in the codebase:
- Tension name and type
- Severity level
- Description and symbolic interpretation

#### 5. Psychological Profile

A synthesized character description including:
- Overall traits
- Boundary orientation
- Failure relationship
- Naming psychology
- Complexity relationship

#### 6. Closing Reflection

Interpretive conclusion with optional resolution suggestions.

## Interpreting Archetypes

### Protective Archetypes

| Archetype | Indicators | Meaning |
|-----------|------------|---------|
| Guardian | `validate_*` functions | Protective boundary enforcement |
| Sentinel | `check_*`, logging | Watchful monitoring |
| Gatekeeper | Guard clauses, early returns | Strict access control |

### Anxiety Archetypes

| Archetype | Indicators | Meaning |
|-----------|------------|---------|
| Anxious Caretaker | High guard ratio | Excessive worry |
| Perfectionist | `verify_*`, heavy validation | Demand for correctness |
| Overprotective Parent | Broad exception catching | Excessive shielding |

### Shadow Archetypes

| Archetype | Indicators | Meaning |
|-----------|------------|---------|
| Suppressor | Empty except blocks | Error avoidance |
| Denier | `pass` in handlers | Refusal to acknowledge |
| Abandoner | TODOs, incomplete code | Unfinished work |

### Creator Archetypes

| Archetype | Indicators | Meaning |
|-----------|------------|---------|
| Builder | `create_*`, `build_*` | Constructive patterns |
| Factory | `*_factory`, `make_*` | Systematic creation |
| Architect | Framework patterns | Foundational design |

## Advanced Usage

### Programmatic Access

Use Oneirocode as a library in your Python code:

```python
from src.oneirocode.analyzer import OneirocodeAnalyzer

# Create analyzer
analyzer = OneirocodeAnalyzer()

# Analyze repository
report = analyzer.analyze("/path/to/repo")

# Access the report
print(report.content)
print(f"Word count: {report.word_count}")

# Access intermediate results
structure = analyzer.get_structure()
profile = analyzer.get_profile()
motifs = analyzer.get_motifs()
tensions = analyzer.get_tensions()
```

### Accessing Individual Components

```python
from src.oneirocode.ast_parser import ASTParser
from src.oneirocode.symbolic_ontology import SymbolicOntology
from src.oneirocode.motif_detector import MotifDetector
from src.oneirocode.tension_detector import TensionDetector

# Parse repository
parser = ASTParser()
structure = parser.parse_repository("/path/to/repo")

print(f"Functions: {structure.function_count}")
print(f"Guard clauses: {len(structure.guard_clauses)}")

# Analyze symbolically
ontology = SymbolicOntology()
profile = ontology.analyze(structure)

for archetype in profile.dominant_archetypes:
    print(f"{archetype.archetype.value}: {archetype.strength:.0%}")
```

### LLM Enhancement (Optional)

Enable LLM-enhanced interpretation:

```bash
# Set environment variables
export ONEIROCODE_LLM_ENABLED=true
export OPENAI_API_KEY=your-key-here

# Run with LLM flag
oneirocode analyze /path/to/project --llm
```

Note: LLM integration requires additional dependencies:
```bash
pip install openai
```

## Troubleshooting

### No Python Files Found

```
Error: No Python files found in repository: /path/to/repo
```

**Solution:** Ensure the path contains `.py` files and is not filtered by exclusion patterns (venv, __pycache__, etc.)

### Syntax Errors

Files with syntax errors are skipped. Check for:
- Incomplete Python files
- Python 2 syntax in a Python 3 environment

### Permission Errors

Ensure read access to all files in the repository.

### Large Repositories

For very large repositories, analysis may take time. Use `--quiet` to reduce output overhead.

## Tips for Best Results

1. **Analyze complete projects**: Partial codebases may not reveal full patterns

2. **Compare across projects**: Run on multiple repos to see different profiles

3. **Focus on dominant archetypes**: Secondary archetypes provide nuance

4. **Pay attention to tensions**: These often reveal the most interesting insights

5. **Read the evidence**: The evidence list shows exactly what triggered each classification

## Example Workflow

```bash
# 1. Analyze your project
oneirocode analyze . -o my-interpretation.md

# 2. View the report
cat my-interpretation.md

# 3. Compare with another project
oneirocode analyze ../other-project -o other-interpretation.md

# 4. Run in CI/CD for tracking over time
oneirocode analyze . --quiet > interpretations/$(date +%Y%m%d).md
```
