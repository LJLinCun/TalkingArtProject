---
name: talkingart-keyword-expander
description: "Extract and expand keywords from natural language input with confidence scoring"
schema_version: "1.0"
author: Lin Cun / Xi Yue (TalkingArtProject)
license: MIT
version: 2.0

template:
  role: Semantic Keyword Extractor & Expander
  context: |
    User input may be incomplete, ambiguous, or overly concise.
    Need to infer missing attributes while respecting user intent.
  task: |
    Extract explicit entities and infer implicit attributes from user input.
    Apply archetype library as knowledge base for attribute inference.
  steps:
    - Parse input for explicit subject, action, style keywords
    - Infer implicit attributes using archetype traits vocabulary
    - Generate 3-5 expansion options per ambiguous entity
    - Output JSON with confidence scores
  output_format: |
    JSON with extracted_entities[], expanded_options, recommended_expansion
  constraints:
    - Maximum expansion depth: 3 levels
    - Confidence threshold ≥0.7 for valid extraction
    - Do not invent completely unrelated concepts

evaluation:
  success_criteria:
    - ✓ Extracted entities match input semantics (≥85% accuracy)
    - ✓ Expansion options are coherent and relevant
    - ✓ Confidence scores reflect actual certainty level
