# experiments/negative_prompt_test.md
---
# Negative Prompt Effectiveness Analysis
**Date:** 2026-05-02  
**Experiment ID:** EXP-NEG-001

## Objective
Determine which negative prompt keywords are most effective at reducing common artifacts (blurry, distorted hands, extra digits).

## Methodology
Tested groups of negative prompts across different model versions.

### Results Summary
| Keyword Group | Effectiveness |
|---------------|--------------|
| **Anatomy:** "bad anatomy", "disfigured" | High priority |
| **Quality:** "lowres", "blurry", "worst quality" | Medium (model-dependent) |
| **Extra Limbs:** "extra digits", "mutated hands" | Critical |

## Implementation
Add these to `negative_prompt.default` in `template.yaml`:
```
negative_prompt:
  default: [
    "bad anatomy",
    "disfigured",
    "lowres",
    "worst quality"
  ]
```
