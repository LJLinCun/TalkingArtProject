# .github/PULL_REQUEST_TEMPLATE.md
---
# Pull Request Template for TalkingArtProject

## Description
<!-- Describe what this PR adds/changes and why. Include links to relevant issues or discussions. -->

## Checklist
- [ ] I have validated the YAML against `prompts/character/template.yaml` schema
- [ ] I've provided a use case (use_case.md) explaining how to apply this prompt
- [ ] The file includes suggested negative prompts for quality control
- [ ] I've checked that the content doesn't violate copyright or safety guidelines
- [ ] The README.md directory structure has been updated if needed

## Files Changed
<!-- List modified/added files -->

**Added:**  
`prompts/style/eras/synthwave.yaml`

**Modified:**  
`.github/PULL_REQUEST_TEMPLATE.md` (this file)

## Use Case Example
<!-- Briefly describe when/how to use this in the prompt library -->

This synthwave archetype is ideal for:
- Nighttime urban scenes with neon lights
- Character designs featuring retro-futuristic aesthetics
- Cyberpunk/noir narrative contexts

**Example Prompt:**
```
yaml
subject: "Synthwave Dancer"
type: archetype
era_style: "retro-futurism"
personality: ["nostalgic", "technologically adept"]
suggested_prompt: |
  masterpiece, best quality, niji 6,
  long pink hair with LED strip accessories,
  wearing holographic bodysuit, glowing neon boots,
  retro-future cityscape background,
  volumetric lighting, chromatic aberration
```

## Testing Results
<!-- If applicable, include test outputs or validation logs -->

YAML Validation: ✅ Passed (schema compliant)
Negative Prompt Suggestions: ✅ Included in file comments

---

**Note:** For contributors, see `docs/CONTRIBUTING.md` for detailed guidelines.
