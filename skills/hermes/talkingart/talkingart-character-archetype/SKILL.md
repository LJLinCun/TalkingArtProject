---
name: talkingart-character-archetype
description: "Load and match TalkingArtProject character archetype library to natural language input"
schema_version: "1.0"
author: Lin Cun / Xi Yue (TalkingArtProject)
license: MIT
version: 2.0

template:
  role: Archetype Matcher
  context: |
    Archetypes stored in prompts/character/archetypes/
    Each archetype has personality_traits, props, visual descriptors.
  task: |
    Match user input to most appropriate archetype(s) from the library.
  steps:
    - Extract semantic keywords from input (subject + style terms)
    - Score each archetype by trait/keyword overlap + domain relevance
    - Select top 1-3 matches with similarity scores ≥0.4
    - Provide gap-filling suggestions for low-similarity cases
  output_format: |
    JSON with matched_archetypes[], recommendation field
  matching_algorithm: |
    similarity = (keyword_overlap * 0.6) + (domain_relevance * 0.4)
  selection_criteria:
    min_similarity: 0.4
    max_recommendations: 3
  constraints:
    - At least one of hair_options, eye_options, or clothing_layers required

evaluation:
  success_criteria:
    - ✓ Matched archetype similarity scores ≥0.87 for obvious matches
    - ✓ Gap-filling suggestions provided when similarity <0.4
    - ✓ Maximum 3 recommendations enforced per input
