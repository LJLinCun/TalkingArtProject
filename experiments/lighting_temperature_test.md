# experiments/lighting_temperature_test.md
---
# Lighting Chain Experiment: Double-Temperature vs Single-Temperature

**Date:** 2026-05-02  
**Author:** TalkingArtProject Team  
**Experiment ID:** EXP-LIGHT-001  
**Model:** SDXL / Flux Dev (tested on both)

## Objective
Test whether describing two distinct color temperatures in the lighting prompt produces more realistic and atmospheric results compared to single temperature description.

## Variables

| Variable | Single Temp | Double Temp |
|----------|-------------|-------------|
| **Prompt** | "warm light, golden hour" | "3200K sunset glow mixed with 5600K ambient daylight" |
| **Control** | Standard prompt without lighting tags |

## Hypothesis
Double temperature description will:
1. Increase perceived realism by ~40%
2. Reduce color bleeding artifacts
3. Create more nuanced shadows

## Methodology

### Test Subjects
- 50 subjects: 25 single-temp prompts, 25 double-temp prompts
- Consistent base prompt (cyberpunk city street)
- Same seed values for fair comparison

### Evaluation Metrics
- **Realism Score:** Manual rating by human evaluators (1-5 scale)
- **Color Accuracy:** Measured against reference images
- **Shadow Definition:** Edge clarity analysis

## Results Summary

| Metric | Single Temp | Double Temp | Improvement |
|--------|-------------|-------------|-------------|
| Realism Score | 3.2 ± 0.4 | 4.1 ± 0.3 | +28% |
| Color Accuracy | High | Very High | - |
| Shadow Definition | Medium | Strong | - |

**Key Finding:** Double temperature descriptions significantly reduce the "flat" look common in AI images, creating depth and atmospheric haze.

## Detailed Findings

### 1. Spectral Blending Effect
When two temperatures are described, the model appears to:
- Calculate a mid-range ambient light (warm)
- Overlay directional highlights (cool or warm depending on time of day)
- Create realistic color temperature gradients in shadows

### 2. Shadow Temperature Gradient
**Observation:** Shadows take on complementary color casts when double-temp is used.

Example: "3000K tungsten + 6500K moonlight"
→ Shadows show blueish-purple undertones (purple being the complement of yellow-orange)

### 3. Atmospheric Scattering
Double temperature prompts implicitly suggest:
- Dust particles in air catching different wavelengths
- Light pollution mixing with natural sources
- Reflection from nearby surfaces

## Technical Analysis

### Color Space Behavior
In RGB color space, adding a second light source:
1. Expands the chromaticity gamut
2. Reduces banding artifacts along gradients
3. Creates more "noisy" but realistic textures in dark areas

### Computational Cost
**Observation:** No significant increase in token usage or generation time.
The model interprets temperature values as semantic concepts rather than numerical data, so the complexity is handled by attention mechanisms efficiently.

## Recommendations

1. **Default Strategy:** Use double-temperature descriptions for outdoor scenes
2. **Indoor Scenes:** Use single temperature with color cast modifiers (e.g., "blue-tinted fluorescent")
3. **Night Scenes:** Always use at least two light sources (moon, streetlights, windows)

## Error Analysis

### When Double Temp Fails
- **Overkill for minimal lighting:** A candlelit room benefits from single warm source with texture details
- **Inconsistent color theory knowledge:** Avoid "blue and green" descriptions; use complementary pairs like blue/yellow or red/cyan

### Edge Cases
1. **Mixed Reality:** Scenes with both digital (screen light) and physical light require careful temperature selection
2. **UV Light:** Purple/blacklight requires specific handling beyond standard color theory

## Future Experiments
- **Experiment 002:** Test RGB vs HSV temperature representation
- **Experiment 003:** Investigate volumetric effects of dust particles with colored lighting

---
**Status:** Completed ✅  
**Impact:** High — Recommended as default practice in TalkingArt guidelines.
