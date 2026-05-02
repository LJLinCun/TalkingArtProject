# 🎯 TalkingArtProject - 核心架构与提示词工程指南
# TalkingArtProject Core Architecture & Prompt Engineering Guide

---

## 🏗️ Project Architecture (项目架构)

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  User Input Text│ →   │Keyword       │ →   │Intent        │ →   │Execute       │
│ (自然语言输入)  │     │ Expansion    │     │Understanding  │     │Command/Action│
└─────────────────┘     │ & Extraction │     └──────────────┘     └──────────────┘
                         └──────────────┘              ^               v
                                            ┌──────────────┐   ┌──────────────┐
                                            │Role/Persona  │   │Style/Visual  │
                                            │ Selection    │   │ Parameter    │
                                            └──────────────┘   │ Mapping      │
                                                                └──────────────┘
```

### Core Flow (核心流程)
1. **用户输入**: 自然语言文本（如："画一个赛博朋克风格的机械工程师在工作室"
2. **关键词扩展/提取**: 识别实体、风格、属性、场景等关键要素并补充缺失信息
3. **意图理解与解析**: 判断是角色定义、任务执行还是风格迁移
4. **智能体执行**: 结合选择的角色原型和风格参数生成最终输出

---

## 📐 Prompt Architecture by Module (按模块的提示词架构)

### Module 1: Keyword Expansion & Extraction (关键词扩展/提取)

**目标**: 从用户模糊输入中提取/补充结构化信息

```
# Role: Semantic Keyword Extractor & Expander
## Context:
- User input may be incomplete, ambiguous, or overly concise
- Need to infer missing attributes while respecting user intent
## Task:
Extract and expand keywords from natural language into structured schema
## Steps:
1. Parse input for explicit entities (subject, action, style)
2. Infer implicit attributes using archetype library as reference
3. Generate 3-5 expansion options per entity where ambiguity exists
4. Output JSON with confidence scores
## Output Format:
{
  "original_input": string,
  "extracted_entities": [
    {"type": "subject", "value": "...", "confidence": 0.X}
  ],
  "expanded_options": {
    "style": ["option1", "option2"],
    "setting": ["option1", "option2"]
  },
  "recommended_expansion": {"merged_entity": "..."}
}
## Constraints:
- Maximum expansion depth: 3 levels
- Do not invent completely unrelated concepts
- Maintain original intent fidelity (confidence ≥ 0.7)
```

### Module 2: Intent Understanding & Parsing (意图理解与解析)

**目标**: 识别用户真实意图并映射到系统能力

```
# Role: Intent Classifier & Mapper
## Context:
- System capabilities: character design, task orchestration, style transfer
- Input may mix multiple intents or be ambiguous
## Task:
Classify user intent and route to appropriate execution module
## Steps:
1. Detect primary intent category (CHARACTER / TASK / STYLE / COMPOUND)
2. Extract action verb and target object if present
3. Identify required parameters based on intent type
4. Flag missing critical information requiring clarification
## Output Format:
{
  "intent_type": enum,           # CHARACTER | TASK | STYLE | COMPOUND | CLARIFICATION_NEEDED
  "action": string,              # Extracted action verb or null
  "target": string,              # Target object/entity or null
  "required_params": list[string],
  "missing_critical_info": bool,
  "fallback_intent": string      # If primary intent unclear
}
## Constraints:
- COMPOUND intents: prioritize dominant action (e.g., "design a character IN steampunk style" → CHARACTER)
- CLARIFICATION_NEEDED only when confidence < 0.6 on all categories
```

### Module 3: Role/Persona Selection (角色原型选择)

**目标**: 从 archetype library 中匹配最佳角色原型

```
# Role: Archetype Matcher
## Context:
- Archetypes stored in prompts/character/archetypes/
- Each archetype has personality_traits, props, visual descriptors
## Task:
Match user input to most appropriate archetype(s)
## Steps:
1. Extract semantic keywords from input (e.g., "engineer", "clockwork", "brass")
2. Score each archetype by trait/keyword overlap + domain relevance
3. Select top 1-3 matches with similarity scores
4. If no strong match, recommend closest related archetype(s)
## Output Format:
{
  "matched_archetypes": [
    {
      "name": string,
      "similarity_score": float (0-1),
      "matching_keywords": list[string],
      "recommended_modifications": list[string]
    }
  ],
  "recommendation": string  # Brief explanation for user
}
## Constraints:
- Minimum similarity threshold: 0.4 to recommend
- Maximum 3 recommendations per input
```

### Module 4: Style/Visual Parameter Mapping (风格参数映射)

**目标**: 将用户描述的风格术语映射到具体生成参数

```
# Role: Visual Style Mapper
## Context:
- Era definitions in prompts/style/eras/
- Lighting mood in prompts/lighting/
- Composition rules in prompts/scene/
## Task:
Translate natural language style descriptions to concrete generation parameters
## Steps:
1. Parse input for era, lighting, composition keywords
2. Map each keyword to predefined parameter values
3. For ambiguous terms, provide 2-3 options with explanations
4. Validate against negative prompt rules
## Output Format:
{
  "style_parameters": {
    "era": {"name": string, "year_range": "X-Y AD", "key_visuals": list[string]},
    "lighting_mood": enum,           # ambient | dramatic | cinematic | natural
    "color_palette": list[hex_code],  # Dominant colors from palette def
    "composition": {"rule": string, "camera_angle": enum}
  },
  "parameter_expansion": [
    {
      "input_term": string,
      "mapped_value": string,
      "confidence": float (0-1)
    }
  ]
}
## Constraints:
- Era mapping must respect historical accuracy ±20%
- Lighting mood default to natural when unspecified
```

### Module 5: Command Execution & Generation (命令执行与生成)

**目标**: 综合所有信息执行最终生成任务

```
# Role: Integrated Generator
## Context:
- Receives expanded keywords, intent classification, matched archetype, style parameters
- Must synthesize all into coherent final output
## Task:
Execute the complete generation task with all contextual information
## Steps:
1. Validate all required parameters are present and valid
2. Assemble prompt following project template schema
3. Apply archetype personality_traits to dynamic variables
4. Inject style parameters into base_prompt appropriately
5. Run self-validation against negative prompts and constraints
6. Output final result with metadata
## Output Format:
{
  "generation_result": string,     # Final generated content (text/image prompt)
  "metadata": {
    "archetype_used": string,
    "style_era": string,
    "total_prompt_length": int,
    "confidence_score": float (0-1),
    "parameters_applied": list[string]
  }
}
## Constraints:
- Prompt length must respect model-specific limits
- Self-validation failure requires graceful fallback to default parameters
```

---

## 🎨 TalkingArtProject Template Schema (项目模板模式)

### Character Design Template (角色设计模板)
```yaml
type: character_design
schema_version: "2.0"
prompt:
  # Core Identity
  subject: "{name}, {age} years old"
  
  # Appearance Attributes
  appearance:
    hair: [color, length, style, accessories]
    eyes: [shape, color, expression, makeup]
    clothing: [era_style, modern_elements, layers, accessories]
    skin_tone: [base_color, marks, jewelry]
  
  # Setting & Atmosphere
  setting:
    environment: {type, time_of_day, weather}
    location: {landmark, urban_or_rural, specific_details}
  
  # Mood & Composition
  mood:
    atmosphere: [lighting_quality, color_palette]
    emotion: [body_language, facial_expression, props]

techniques:
  - "masterpiece"
  - "best quality"
  - "highly detailed"
negative_prompt: ["lowres", "bad anatomy", ...]
examples: {basic_portrait, cyberpunk_ninja}
```

---

## 🔄 End-to-End Example (端到端示例)

**用户输入**: "画一个蒸汽朋克风格的老工匠在工作室"

### Step 1: Keyword Expansion & Extraction
```json
{
  "extracted_entities": [
    {"type": "style", "value": "steampunk", "confidence": 0.95},
    {"type": "subject", "value": "old craftsman/workshop owner", "confidence": 0.7}
  ],
  "expanded_options": {
    "age_range": ["45-65", "30-50"],
    "workshop_type": ["clockmaking", "watch repair", "general crafting"]
  }
}
```

### Step 2: Intent Understanding
```json
{
  "intent_type": "CHARACTER",
  "action": "design/illustrate",
  "target": "character in steampunk style",
  "required_params": ["era", "clothing", "props", "setting"],
  "missing_critical_info": false
}
```

### Step 3: Archetype Matching
```json
{
  "matched_archetypes": [
    {
      "name": "Clockwork Engineer",
      "similarity_score": 0.87,
      "matching_keywords": ["craftsman", "clockwork", "steam"],
      "recommended_modifications": ["emphasize age signs: gray hair, weathered face"]
    }
  ],
  "recommendation": "Clockwork Engineer archetype matches well - emphasizes precision and mechanical passion"
}
```

### Step 4: Style Parameter Mapping
```json
{
  "style_parameters": {
    "era": {"name": "Victorian Era", "year_range": "1837-1901 AD", "key_visuals": ["brass", "cogwheels", "steam pipes"]},
    "lighting_mood": "dramatic",
    "color_palette": ["#C4A56E", "#2D3E4B", "#8B0000", "#F4C430"],
    "composition": {"rule": "Rule of Thirds", "camera_angle": "medium shot, eye level"}
  }
}
```

### Step 5: Final Generation
```json
{
  "generation_result": "masterpiece, best quality, highly detailed,
    1boy, age 50-60, weathered face with gray hair tied back,
    wearing layered leather apron over Victorian shirt with brass buttons,
    holding precision calipers and brass pocket watch,
    cluttered workshop background: brass instruments, blueprints, scattered gears,
    dramatic lighting from single window, volumetric dust motes,
    focused expression, slight smile showing craftsmanship pride",
  "metadata": {
    "archetype_used": "Clockwork Engineer",
    "style_era": "Victorian Steampunk",
    "total_prompt_length": 387,
    "confidence_score": 0.92,
    "parameters_applied": ["era: Victorian", "lighting: dramatic", "archetype: Clockwork Engineer"]
  }
}
```

---

## ✅ Implementation Checklist (实施检查清单)

### Phase 1: Core Infrastructure (核心基础设施)
- [ ] Keyword expansion module with archetype library as knowledge base
- [ ] Intent classification system (CHARACTER / TASK / STYLE / COMPOUND)
- [ ] Base prompt templates for each intent type

### Phase 2: Enhancement Layer (增强层)
- [ ] Archetype matching algorithm with similarity scoring
- [ ] Style-to-parameter mapping engine
- [ ] Few-shot examples database per archetype

### Phase 3: Integration & Polish (集成与优化)
- [ ] End-to-end pipeline testing with diverse inputs
- [ ] Self-validation against negative prompts and constraints
- [ ] Error handling and graceful degradation

---

**Version:** v1.0 | **Owner:** Lin Cun / 希悦
**Last Updated:** 2025-May-02