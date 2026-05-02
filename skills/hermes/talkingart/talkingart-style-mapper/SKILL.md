---
name: talkingart-style-mapper
description: "Map era/lighting/composition keywords to concrete generation parameters"
schema_version: "1.0"
author: Lin Cun / Xi Yue (TalkingArtProject)
license: MIT
version: 2.0

template:
  role: Visual Style Mapper
  context: |
    Era definitions in prompts/style/eras/
    Lighting mood in prompts/lighting/
    Composition rules in prompts/scene/
  task: |
    Translate natural language style descriptions to concrete generation parameters.
  steps:
    - Parse input for era, lighting, composition keywords
    - Map each keyword to predefined parameter values
    - Provide 2-3 options with explanations for ambiguous terms
    - Validate against negative prompt rules
  output_format: |
    JSON with style_parameters{}, parameter_expansion[]
  mapping_rules:
    era_accuracy_tolerance: ±20%
    default_lighting_mood: natural
    color_palette_extraction: from_historical_palettes
  constraints:
    - Era mapping must respect historical accuracy ±20%
    - Lighting mood defaults to natural when unspecified

evaluation:
  success_criteria:
    - ✓ Era mappings accurate within ±20% tolerance for all test cases
    - ✓ Parameter expansion provides clear explanations for each mapping
    - ✓ Negative prompt validation prevents incompatible combinations
