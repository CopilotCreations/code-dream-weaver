# Suggestions for Future Improvements

This document outlines potential enhancements to Oneirocode that could extend its capabilities, improve accuracy, or add new features.

## High Priority Enhancements

### 1. Multi-Language Support

**Current State:** Oneirocode only analyzes Python codebases.

**Suggestion:** Extend support to additional languages:
- JavaScript/TypeScript (using tree-sitter or babel)
- Java (using javalang or ANTLR)
- Go (using go/ast)
- Rust (using syn)

**Implementation Approach:**
```python
class LanguageParser(Protocol):
    def parse_file(self, path: Path) -> Optional[LanguageVisitor]: ...
    def get_structure(self) -> CodeStructure: ...

# Factory pattern for language-specific parsers
def get_parser(language: str) -> LanguageParser:
    parsers = {
        'python': PythonParser,
        'javascript': JavaScriptParser,
        'java': JavaParser,
    }
    return parsers[language]()
```

### 2. Temporal Analysis

**Current State:** Analysis is a snapshot in time.

**Suggestion:** Track codebase evolution over git history:
- Archetype shifts over time
- Tension accumulation patterns
- Motif emergence and decay

**Benefits:**
- See how codebase personality evolves
- Identify when tensions were introduced
- Track "personality changes" after major refactors

### 3. Team Pattern Attribution

**Current State:** Analysis treats codebase as monolithic.

**Suggestion:** Attribute patterns to git authors:
- Per-author archetype profiles
- Team psychological dynamics
- Style consistency analysis

**Privacy Considerations:**
- Make this opt-in
- Aggregate rather than individual tracking
- Focus on patterns, not judgment

## Medium Priority Enhancements

### 4. Custom Ontology Configuration

**Current State:** Archetype mappings are hardcoded.

**Suggestion:** Allow users to define custom ontologies:
```yaml
# custom-ontology.yaml
archetypes:
  security_guardian:
    description: "Protects against security vulnerabilities"
    patterns:
      prefixes: ["sanitize_", "escape_", "validate_input_"]
      suffixes: ["_sanitizer", "_validator"]
    
  performance_optimizer:
    description: "Focuses on speed and efficiency"
    patterns:
      prefixes: ["optimize_", "cache_", "batch_"]
```

**Benefits:**
- Domain-specific interpretations
- Team vocabulary alignment
- Industry-specific archetypes (security, performance, etc.)

### 5. Comparative Analysis

**Current State:** Each analysis is independent.

**Suggestion:** Add comparison mode:
```bash
oneirocode compare project1 project2 -o comparison.md
```

**Features:**
- Side-by-side archetype comparison
- Tension differential
- Motif overlap analysis
- "Personality compatibility" score

### 6. Interactive Mode

**Current State:** CLI produces static output.

**Suggestion:** Add interactive exploration:
```bash
oneirocode explore /path/to/repo
```

**Features:**
- Navigate through archetypes interactively
- Drill down into specific files
- Ask questions about patterns
- Generate focused sub-reports

### 7. Visualization Output

**Current State:** Output is Markdown only.

**Suggestion:** Add visual representations:
- Archetype radar charts
- Tension heat maps
- Motif frequency graphs
- File-level archetype coloring

**Implementation:** Generate HTML report with embedded visualizations using libraries like Plotly or D3.js.

## Lower Priority Enhancements

### 8. IDE Integration

**Suggestion:** Create extensions for popular IDEs:
- VSCode extension with inline annotations
- JetBrains plugin
- Real-time archetype indicators

**Example:**
```
// Function displays "Guardian" indicator
function validateUserInput(input) {  // 🛡️ Guardian
    if (!input) throw new Error('Invalid input');
    ...
}
```

### 9. CI/CD Integration Templates

**Suggestion:** Provide ready-to-use CI/CD templates:
- GitHub Actions workflow
- GitLab CI pipeline
- Azure Pipelines

**Use Cases:**
- Track personality over time
- Alert on significant tension increases
- Generate interpretation on release

### 10. Natural Language Queries

**Suggestion:** Allow natural language questions:
```bash
oneirocode ask "Why does this codebase seem anxious?"
oneirocode ask "What are the main sources of tension?"
```

**Implementation:** Use LLM to interpret questions and map to analysis results.

### 11. Pattern Anomaly Detection

**Suggestion:** Identify files that don't match the dominant pattern:
- Files with different "personality" than the project
- Potential integration issues
- Team style divergence

### 12. Export Formats

**Suggestion:** Support additional output formats:
- JSON (for programmatic consumption)
- HTML (for web viewing)
- PDF (for documentation)
- SARIF (for tool integration)

## Architecture Improvements

### 13. Plugin System

**Suggestion:** Create extensible plugin architecture:
```python
class OneirocodePlugin(Protocol):
    name: str
    
    def analyze(self, structure: CodeStructure) -> PluginResult: ...
    def contribute_narrative(self, result: PluginResult) -> str: ...

# Register plugins
analyzer.register_plugin(SecurityArchetypePlugin())
analyzer.register_plugin(PerformancePatternPlugin())
```

### 14. Streaming Analysis

**Suggestion:** For large repositories, stream results:
- File-by-file progress updates
- Early archetype predictions
- Incremental report building

### 15. Caching Layer

**Suggestion:** Cache parsed ASTs and intermediate results:
- Speed up re-analysis
- Enable incremental updates
- Support watch mode

## Research Directions

### 16. Correlation Studies

**Suggestion:** Research correlation between:
- Archetype profiles and bug density
- Tension levels and team satisfaction
- Motif patterns and maintainability scores

### 17. Cross-Project Patterns

**Suggestion:** Analyze patterns across many open-source projects:
- Common archetype distributions
- Framework-specific patterns
- Language-specific tendencies

### 18. Psychological Framework Extensions

**Suggestion:** Explore additional psychological frameworks:
- Enneagram-style typology
- MBTI-inspired classifications
- Attachment theory patterns

## Implementation Roadmap

### Phase 1 (Short-term)
1. Custom ontology configuration
2. JSON export format
3. Basic visualization output

### Phase 2 (Medium-term)
1. Multi-language support (JavaScript first)
2. Comparative analysis
3. CI/CD templates

### Phase 3 (Long-term)
1. IDE integrations
2. Temporal analysis
3. Plugin system

## Contributing

If you're interested in implementing any of these suggestions:

1. Open an issue to discuss the approach
2. Reference this document in your PR
3. Ensure comprehensive test coverage
4. Update documentation accordingly

We welcome contributions that align with Oneirocode's philosophy of treating code as symbolic expression.
