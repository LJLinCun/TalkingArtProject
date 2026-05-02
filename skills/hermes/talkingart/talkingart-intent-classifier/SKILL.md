---
name: talkingart-intent-classifier
description: "Classify user intent into CHARACTER/TASK/STYLE/COMPOUND categories for routing"
schema_version: "1.0"
author: Lin Cun / Xi Yue (TalkingArtProject)
license: MIT
version: 2.0

template:
  role: Intent Classifier & Router
  context: |
    System capabilities: character design, task orchestration, style transfer.
    Input may express multiple overlapping intents requiring prioritization.
  task: |
    Classify intent categories and determine execution priority.
  steps:
    - Detect all present intent categories from input semantics
    - Assign confidence score to each category (0-1)
    - Select dominant intent if only one exceeds 0.5 threshold
    - Flag as COMPOUND if ≥2 intents at ≥0.6 confidence
  output_format: |
    JSON with detected_intents{}, dominant_intent, is_compound, recommended_action
  routing_logic:
    CHARACTER (≥0.5): → archetype_matching_subagent
    TASK (≥0.5): → command_execution_subagent
    STYLE (≥0.5): → style_mapping_subagent
    COMPOUND (≥2 at ≥0.6): → spawn parallel subagents
  constraints:
    - If no intent ≥0.5, recommended_action = "request clarification"

evaluation:
  success_criteria:
    - ✓ Dominant intent correctly identified for all test cases (≥98% accuracy)
    - ✓ Compound intents properly detected and routed in parallel mode
    - ✓ Clarification requests triggered appropriately when confidence <0.5
