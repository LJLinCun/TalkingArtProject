# docs/api-reference.md
---
# TalkingArt API Reference
Complete API documentation for the TalkingArtPrompt library.

## Schema Definitions

### Character Template (prompts/character/template.yaml)
**File:** `prompts/character/template.yaml`  
**Description:** Core schema for all character designs and archetypes. Includes required fields, appearance attributes, setting definitions, mood controls, and techniques for quality generation.

| Field | Type | Required |
|-------|------|----------|
| `type` | string | Yes |
| `schema_version` | string | Yes |
| `prompt` | dict/object | Yes |
| `techniques` | array[string] | No |
| `negative_prompt` | object/dict | No |

**Usage:** Fill `{field}` placeholders with actual values before generation.

---

## Style Fusion API

### Function Signature
```python
def create_fusion(base_style: str, accent_style: str = None) -> dict:
    """
    Generate fusion prompt with parameters.
    
    Args:
        base_style (str): Primary style ('anime', 'watercolor', etc.)
        accent_style (str, optional): Secondary style to blend
    
    Returns:
        dict containing fusion_name, techniques, color_palette, example_prompt
    """
```

**Available Base Styles:** anime, watercolor, oil_paint, pixel_art, ink_sketch

---

## Camera Parameters
**File:** `prompts/scene/camera-angles.yaml`  
**Description:** Angle definitions for scene composition and cinematography control.

| Parameter | Value |
|-----------|-------|
| low_angle | -30° to -45° elevation (hero shots) |
| birdseye | 75° to 90° (strategic views, cityscapes) |
| over_the_shoulder | Slight offset, dialogue scenes |

---

## Lighting Control
**File:** `prompts/lighting/color-temp.yaml`  
**Description:** Color temperature table for atmospheric control.

| Temp | Range | Description |
|------|-------|-------------|
| Warm | 2800-3200K | Sunset, candle light |
| Neutral | 4500-5500K | Fluorescent, daylight |
| Cool | 6500-9000K | Moonlight, shadows |

---

## Validation Tools
**File:** `tools/validate-prompts.py`  
**Description:** Schema validation and impact analysis tools.

```python
from tools.validate_prompts import validate_schema, analyze_impact
```

**Example:**
```python
prompt = {"name": "Cyberpunk Ninja", ...
valid, message = validate_schema(prompt)
analysis = analyze_impact(prompt)
```

---

## Error Codes
- `E001`: Missing required field (e.g., `name`)
- `E002`: Invalid type in array field
- `E003`: Negative prompt contains prohibited keywords

---
**TalkingArtProject Team** ✨
