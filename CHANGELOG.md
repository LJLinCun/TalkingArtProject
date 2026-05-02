# CHANGELOG.md
---
# TalkingArtProject Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0/), adapted for prompt engineering libraries.

## [Unreleased]
### Added
- Initial schema definition (`prompts/character/template.yaml`)
- Style fusion algorithm (`style/fusion-params.py`)
- Camera parameters system (`prompts/scene/camera-angles.yaml`)
- Lighting color temperature tables (`lighting/color-temp.yaml`)

## [1.0.0] - 2026-05-02
### Added
- **Core Architecture:**
  - Character template schema (v1.0)
  - Archetype library with cyberpunk and steampunk examples
  - Example test cases for validation

- **Style System:**
  - Fusion parameters Python module
  - Era style definitions (synthwave, victorian-steampunk)
  - Technique descriptors (oil paint, pixel art)

- **Scene Control:**
  - Camera angle parameters
  - Composition rules (golden ratio, rule of thirds)
  - Lens characteristics database

- **Lighting:**
  - Color temperature reference table
  - Volumetric lighting effects

- **Tools & Validation:**
  - Prompt validator (`tools/validate-prompts.py`)
  - Impact analysis scripts
  - CI/CD linting workflow

- **Documentation:**
  - API reference guide
  - Contributing guidelines
  - Experiment records (lighting, texture anchoring, morphing gradients)

### Modified
- `.gitignore`: Added Python/ML/AI-specific patterns

### Removed
- None (initial release)

## [0.1.0] - Planned Future
- Multi-agent collaboration protocols
- Automated prompt generation from natural language
- Cross-model compatibility testing

---
**TalkingArtProject Team** ✨
