---
name: talkingart-full-pipeline
description: "Execute complete TalkingArtProject workflow from user input to final output"
schema_version: "1.0"
delegate_task:
  role: orchestrator
  max_spawn_depth: 3
  toolsets: [skills, terminal, file, clarify]
author: Lin Cun / Xi Yue (TalkingArtProject)
license: MIT
version: 2.0

template:
  role: Integrated Generator
  context: |
    Receives expanded keywords, intent classification, matched archetype,
    and style parameters from prior modules.
  task: |
    Synthesize all contextual information into coherent final generation prompt.
  steps:
    - Validate all required parameters are present and valid
    - Assemble prompt following project template schema
    - Apply archetype personality_traits to dynamic variables
    - Inject style parameters into base_prompt appropriately
    - Run self-validation against negative prompts and constraints
    - Gracefully degrade if validation fails with user notification
  output_format: |
    JSON with generation_result, metadata (archetype_used, style_era, confidence)
  validation_checklist:
    - ✓ All required parameters present (subject + action + ≥2 style terms)
    - ✓ Archetype personality_traits applied to dynamic variables
    - ✓ Style parameters injected appropriately
    - ✓ Negative prompt constraints satisfied
    - ✓ Prompt length ≤ model-specific limits
  fallback_behavior: |
    if_validation_fails → graceful_degradation_with_user_notification

evaluation:
  success_criteria:
    - ✓ End-to-end pipeline completes in <3.5s for typical inputs
    - ✓ Self-validation catches ≥94% of invalid parameter combinations
    - ✓ Graceful degradation maintains user experience when failures occur
