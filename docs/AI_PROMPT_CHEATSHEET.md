# 🎯 AI Agent Prompt Engineering Cheatsheet
# AI 智能体提示词工程速查手册

---

## ⚡ Quick Reference (快速参考)

### Core Formula (核心公式)
```
Good Prompt = Clear Role + Rich Context + Structured Steps + Format Spec + Constraints
```

| Element | Minimum Requirement | Best Practice |
|---------|---------------------|---------------|
| **Role** | 1-2 sentence defining expertise | Include archetype + communication style |
| **Context** | Immediate goal only | Layer: Primary → Secondary → Environmental |
| **Task** | Clear verb phrase | Numbered steps with decision points |
| **Format** | JSON/Markdown spec | Schema validation where possible |
| **Constraints** | 2-3 key limits | Length, tone, boundaries, safety |

---

## 📐 Standard Structure (标准结构)

```
# Role: [定义]
## Context:
- Goal: ...
- Audience: ...
- Domain: ...
## Task:
1. Step 1
2. Step 2
3. Step 3
## Output Format:
```json
{ "key": "value" }
```
## Constraints:
- Max X words, tone Y, avoid Z
```

---

## 🎨 Role Archetypes (角色原型)

| Type | Prompt Pattern | Example |
|------|---------------|----------|
| **Expert** | "You are an expert in... Answer directly with evidence." |
| **Consultant** | "Act as a consultant. Ask clarifying questions first, then provide structured recommendations." |
| **Collaborator** | "We're brainstorming. Suggest X ideas, build on mine, don't judge prematurely." |
| **Critic** | "Review this code/prompt critically. Point out flaws before praising strengths." |

---

## 🔧 Task Patterns (任务模式)

### Chain-of-Thought
```markdown
Step 1: Analyze input for key elements
Step 2: Derive implications from each element
Step 3: Synthesize into actionable output
```

### ReAct (Reason + Act)
```markdown
Think → [observation]
Observe → [result]
Repeat until task complete
```

---

## 📊 Output Formats (输出格式速查)

| Format | Use Case | Validation |
|--------|----------|------------|
| **Markdown** | Human-readable docs | None needed |
| **JSON/JSONL** | API responses | JSON Schema validation |
| **CSV/TSV** | Data export | Header row + type inference |
| **Code Block** | Code snippets | Syntax highlighting enabled |

---

## 🚫 Anti-Patterns (反模式速查)

❌ "Help me with this" → ✅ "Guide the user through X process in 3 steps"

❌ "Don't be too long" → ✅ "Maximum 300 words, use bullet points"

❌ "Return results" → ✅ "Output JSON with keys: result, status, reasoning"

---

## 📚 TalkingArtProject Patterns (项目特定模式)

### Character Archetype Template
```yaml
type: archetype_library
archetype:
  name: string                     # e.g., "Clockwork Engineer"
  base_prompt: |
    masterpiece, best quality,
    {dynamic_variables}, in {setting}
  personality_traits:               # Required!
    - "obsessive about precision"
    - "believes machines have souls"
```

### Task Orchestration Template
```yaml
type: task_orchestrator
task:
  name: string
  goal: string
  steps:
    - step_number: 1
      action: "Validate user input"
      decision_points: ["Is input complete? → YES/NO"]
```

---

## ✅ Pre-Prompt Checklist (发布前检查清单)

- [ ] Role clearly defined with archetype?
- [ ] Context has at least primary + one secondary layer?
- [ ] Steps numbered and sequential?
- [ ] Output format explicitly specified?
- [ ] At least 2 constraints included (length, tone, or boundaries)?
- [ ] Few-shot examples provided for complex tasks?

---

**Version:** v1.0 | **Owner:** Lin Cun / 希悦
**Last Updated:** 2025-May-02