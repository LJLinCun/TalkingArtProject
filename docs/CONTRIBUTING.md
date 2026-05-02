# docs/CONTRIBUTING.md
---
# Contributing to TalkingArtProject

Thank you for your interest in contributing! This guide explains how to add new prompts, improve existing ones, and participate in the project.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Adding New Prompts](#adding-new-prompts)
3. [Style Fusion Contributions](#style-fusion-contributions)
4. [Code & Tools](#code--tools)
5. [Testing Your Changes](#testing-your-changes)
6. [Pull Request Guidelines](#pull-request-guidelines)

---

## Getting Started

### Prerequisites
- Basic Python knowledge (for tools/ scripts)
- Understanding of YAML syntax
- Familiarity with prompt engineering concepts

### Local Setup
```bash
cd /home/lincun/workspace/TalkingArtProject
pip install pyyaml  # For validation tools
```

---

## Adding New Prompts

### Character Prompts (prompts/character/)

#### Template Structure
All character prompts must follow the schema defined in `template.yaml`:

```yaml
# Required fields only:
type: "archetype" or "example"
schema_version: "1.0"
name: "Short description of the archetype"
base_prompt: |
  <your prompt here>
```

#### Example Entry (prompts/character/examples/test_02.yaml)
```yaml
type: example
schema_version: "1.0"
test_case_id: TC-2026-0502-002
name: "Space Colonial Settler"
description: "A settler adapting to alien environments with terraforming technology"
personality_traits:
  - "technologically illiterate but internet-savvy"
  - "disappointed by corporate overpromises"
clothing_layers:
  - "modular environmental suit with visible cooling vents"
```

**File Naming Convention:**
- `archetypes/{name}.yaml` — For character prototypes
- `examples/test_{id}.yaml` — For testing and documentation
- `eras/{era_name}.yaml` — See style/ section below

---

## Style Fusion Contributions (prompts/style/)

### Adding New Eras/Techiques
See `fusion-params.py` for the algorithm.

**File:** `prompts/style/eras/synthwave.yaml`
```yaml
type: era_style
schema_version: "1.0"
name: "Synthwave / Retro-Futurism"
description: "80s-inspired neon aesthetic combining vintage technology with futuristic vision"
color_palette:
  primary: ["#FF6B9D", "#4A5F7C"]
  secondary: ["#FFE5D9", "#E0FFFF"]
characteristics:
  - "neon-lit urban environments"
  - "hacked digital interfaces"
  - "grainy film stock aesthetic"
suggested_keywords: [
  "synthwave",
  "retro-futurism",
  "neon-noir",
  "vaporwave"
]
negative_keywords: ["photorealistic", "3d render"]
```

**File:** `prompts/style/eras/victorian-steampunk.yaml`
```yaml
type: era_style
schema_version: "1.0"
name: "Victorian Steampunk"
description: "Industrial age meets fantasy, combining Victorian aesthetics with mechanical technology"
color_palette:
  primary: ["#5C4033", "#8B7355"]
  secondary: ["#D2691E", "#CD5C5C"]
classification: "historical-fantasy"
negative_keywords: [
  "electricity",
  "plastic",
  "modern technology"
]
suggested_combinations:
  - "airship interior with brass fittings"
  - "clockwork automatons in gas-lit workshops"
```

---

## Code & Tools (tools/)

### Adding New Validation Scripts
Scripts in `tools/` should follow these guidelines:

1. **Type hints required:** Use Python type annotations for all functions
2. **Error handling:** Wrap file operations in try-except blocks
3. **Documentation:** Include docstrings explaining inputs and outputs
4. **Testing:** Add unit tests (not included here but encouraged)

**Example script:** `tools/analyze_impact.py`
```python
import yaml
from pathlib import Path

def analyze_prompt_file(file_path: str) -> dict:
    """
    Analyze a prompt YAML file and report complexity metrics.
    
    Args:
        file_path (str): Path to the prompt YAML file
    
    Returns:
        Dictionary containing analysis results
    """
    with open(file_path) as f:
        data = yaml.safe_load(f)
    # Analysis logic here...
```

### Adding New Python Functions to fusion-params.py
New style combinations can be added by extending the `style_tokens` dictionary in `fusion-params.py`. Ensure all new styles are documented with color palettes and negative keywords.

---

## Testing Your Changes

Before submitting, test your prompts locally:

1. **Syntax Validation**
```bash
cd /home/lincun/workspace/TalkingArtProject/tools
python validate_prompts.py "prompts/character/template.yaml"  # Check schema
```

2. **Impact Analysis (Dry Run)**
```bash
# Analyze example files to check complexity scores
python ../analyze_impact.py "examples/test_01.yaml"
```

3. **Manual Testing** (if you have SDXL/Niji installed)
- Generate test outputs using your new prompts
- Verify negative keywords work correctly
- Check that color palettes render as expected

---

## Pull Request Guidelines

### Required Documentation
Every PR must include:
1. **Use Case:** A markdown file (`use_case.md`) explaining when/how to use the prompt
2. **Test Results:** Screenshots or generation parameters used for testing
3. **Negative Prompts:** Suggested keywords to avoid
4. **Schema Compliance:** Confirmation that YAML follows `template.yaml` structure

### Code Review Checklist
- [ ] File naming follows convention (see examples above)
- [ ] Comments explain design decisions
- [ ] No hardcoded strings in tools/ scripts
- [ ] Schema version incremented if breaking changes made

---

## Community & Discussion

If you have questions or want to discuss specific prompts:
1. Create an issue on GitHub with your use case
2. Join the #talking-art Discord channel (invite URL: TBD)
3. Review existing issues before creating duplicates

## License

By contributing, you agree that your contributions are licensed under the MIT License.

---
**TalkingArtProject Team** ✨
*Making prompt engineering accessible to all*
