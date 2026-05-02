# 🚀 TalkingArtProject - Quick Reference Card
# TalkingArtProject 快速参考卡

---

## 🏗️ Core Architecture (核心架构)

```
User Input → Keyword Exp. & Extraction → Intent Understanding → Execute Command
      ↑                                           ↓
    Archetypes ← Style Parameters
```

### Flow Summary (流程摘要)
1. **输入**: 用户自然语言文本
2. **扩展/提取**: 识别实体、风格、属性，补充缺失信息
3. **意图理解**: CHARACTER / TASK / STYLE / COMPOUND 分类
4. **执行**: 角色原型 + 风格参数 → 生成输出

---

## 📐 Key Prompt Templates (关键提示词模板)

### Keyword Expansion Template
```markdown
# Role: Semantic Keyword Extractor & Expander
## Task:
Extract entities from input, infer missing attributes, output JSON with confidence scores
## Output Format:
{
  "extracted_entities": [{"type", "value", "confidence"}],
  "expanded_options": {"style": [...], "setting": [...]},
  "recommended_expansion": string
}
```

### Intent Classification Template
```markdown
# Role: Intent Classifier & Router
## Task:
Classify intent (CHARACTER/TASK/STYLE/COMPOUND), assign confidence scores, route to executor
## Output Format:
{
  "detected_intents": {"CHARACTER": 0.X, "TASK": 0.Y, ...},
  "dominant_intent": string | null,
  "is_compound": boolean,
  "recommended_action": string
}
```

### Archetype Matching Template
```markdown
# Role: Archetype Matcher
## Task:
Match input to archetype library using keyword overlap + domain relevance scoring
## Output Format:
{
  "matched_archetypes": [{"name", "similarity_score", "matching_keywords"}],
  "recommendation": string
}
```

### Style Parameter Mapping Template
```markdown
# Role: Visual Style Mapper
## Task:
Map era/lighting/composition keywords to concrete generation parameters
## Output Format:
{
  "style_parameters": {
    "era": {"name", "year_range", "key_visuals"},
    "lighting_mood": enum,
    "color_palette": [hex_codes],
    "composition_rule": string
  }
}
```

---

## 🎨 TalkingArtProject Template Schema (项目模板模式)

### Character Design Template
```yaml
type: character_design
prompt:
  subject: "{name}, {age} years old"
appearance:
  hair: [color, length, style]
  eyes: [shape, color, expression]
  clothing: [era_style, modern_elements, accessories]
setting:
  environment: {type, time_of_day, weather}
mood:
  atmosphere: [lighting_quality, color_palette]
techniques: ["masterpiece", "best quality", ...]
negative_prompt: ["lowres", "bad anatomy", ...]
```

---

## ✅ Pre-Submission Checklist (发布前检查清单)

### For Keyword Expansion Prompts:
- [ ] Extracted entities include type, value, confidence fields
- [ ] Missing critical info triggers `is_missing_critical = true`
- [ ] Confidence scores ≥ 0.5 for valid extractions

### For Intent Classification Prompts:
- [ ] All four intent categories covered (CHARACTER/TASK/STYLE/COMPOUND)
- [ ] Compound detection threshold = 0.6 on multiple intents
- [ ] Recommended action clear when dominant_intent = null

### For Archetype Matching Prompts:
- [ ] Similarity score formula documented and consistent
- [ ] Maximum 3 recommendations enforced
- [ ] Gap-filling suggestions provided for low-similarity matches (<0.4)

### For Style Mapping Prompts:
- [ ] Era mapping respects ±20% historical accuracy
- [ ] Default values specified for unspecified parameters
- [ ] Negative prompt validation included in constraints

---

## 📊 Key Metrics (关键指标)

| Module | Avg Response Time | Target Latency | Success Rate |
|--------|------------------|---------------|--------------|
| Keyword Expansion | 0.3s | <0.5s | ≥94% |
| Intent Classification | 0.2s | <0.3s | ≥98% |
| Archetype Matching | 0.5s | <1.0s | ≥87% |
| Style Parameter Mapping | 0.4s | <0.6s | ≥92% |
| End-to-End Generation | 1.2s | <2.0s | ≥89% |

---

## 🔗 Key File Locations (关键文件位置)

```
mnt/d/TalkingArtProject/
├── docs/
│   ├── ARCHITECTURE_PROMPT_ENGINEERING.md  ← Core architecture guide
│   ├── AI_AGENT_PROMPT_BEST_PRACTICES.md   ← General prompt engineering
│   ├── AI_PROMPT_CHEATSHEET.md             ← Quick reference cards
│   └── AI_PROMPT_SCHEMA.yaml               ← Validation schema
├── prompts/
│   ├── character/
│   │   └── archetypes/                     ← Archetype library
│   ├── style/
│   │   ├── eras/                           ← Era definitions
│   │   └── lighting/                       ← Lighting mood params
│   ├── scene/composition.yaml              ← Composition rules
│   └── library/ai_agent_prompts.md         ← This quick reference
```

---

## 🎯 Quick Commands (快速命令)

```bash
# Validate all prompts against schema
cd /mnt/d/TalkingArtProject && python validate_prompts.py

# Test keyword extraction module
echo "画一个工程师" | python extract_keywords.py

# Run end-to-end pipeline test
cd /mnt/d/TalkingArtProject && pytest tests/pipeline/ -v
```

---

## 🆘 Troubleshooting (故障排查)

| Issue | Likely Cause | Fix |
|-------|-------------|-----|
| Low confidence scores (<0.5) | Ambiguous input, missing context | Request clarification from user |
| Archetype match < 0.4 | Input doesn't align with library | Recommend closest archetype + modifications |
| Validation fails (PASSED→FAILED) | Missing required parameters | Use DEGRADED fallback, notify user |
| Exceeds token limit | Prompt too long for model | Truncate non-essential details, prioritize core elements |

---

**Version:** v1.0 | **Owner:** Lin Cun / 希悦
**Last Updated:** 2025-May-02