# AI Agent Prompt Engineering Best Practices
# AI 智能体提示词工程最佳实践指南

---

## 📋 Table of Contents (目录)
- [1. Core Principles](#core-principles) - 核心原则
- [2. Standard Structure Template](#standard-structure-template) - 标准结构模板
- [3. Role Definition Framework](#role-definition-framework) - 角色定义框架
- [4. Context Structuring](#context-structuring) - 上下文构建
- [5. Task Decomposition](#task-decomposition) - 任务分解
- [6. Output Format Specification](#output-format-specification) - 输出格式规范
- [7. Constraints & Boundaries](#constraints-boundaries) - 约束与边界
- [8. Examples & Few-Shot Learning](#examples-few-shot-learning) - 示例与少样本学习
- [9. TalkingArtProject Integration](#talkingartproject-integration) - TalkingArtProject 集成指南

---

## 1. Core Principles (核心原则)

### 1.1 Four Pillars of Effective Agent Prompts
**有效智能体提示词的四大支柱：**

| 支柱 | 说明 | 示例 |
|------|------|------|
| **Clarity (明确性)** | 目标、角色、任务必须清晰无歧义 | "你是一个 AI 提示词工程师，负责设计多轮对话系统" |
| **Context (上下文)** | 提供足够的背景信息让智能体理解场景 | "用户是初学 Python 的开发者，需要耐心指导" |
| **Constraints (约束)** | 定义边界、限制条件和失败条件 | "不超过 300 字，使用中文输出，避免技术术语" |
| **Format (格式)** | 指定结构化输出格式便于解析 | "以 JSON 数组返回，每个元素包含 role, content, action" |

### 1.2 Anti-Patterns to Avoid (应避免的反模式)
- ❌ **Ambiguous Goals** - "帮助这个用户" → ✅ "引导用户完成首次代码提交流程"
- ❌ **Vague Constraints** - "不要太长" → ✅ "不超过 300 字，分三点输出"
- ❌ **Unstructured Output** - "返回结果" → ✅ "以 JSON 格式返回：{result, status}"
- ❌ **Over-constraining** - 过度限制导致创造性下降
- ❌ **Context Bloat** - 无关背景信息增加理解负担

---

## 2. Standard Structure Template (标准结构模板)

### 2.1 Base Template (基础模板)

```markdown
# Role: [角色定义]
## Context: [背景上下文]
## Task: [明确任务]
## Steps: [执行步骤]
## Output Format: [输出格式]
## Constraints: [约束条件]
```

### 2.2 Detailed Example (详细示例)

```markdown
# Role: AI Prompt Engineering Assistant
## Context:
- User is designing a multi-turn dialogue system for customer service
- Target audience: business analysts with limited technical knowledge
- Domain: e-commerce platform optimization
## Task:
Design prompts that enable the agent to analyze conversation logs and extract key insights
## Steps:
1. Parse user's intent from conversation context
2. Identify sentiment and urgency level (low/medium/high)
3. Extract 3-5 actionable recommendations
4. Format output for business stakeholder review
## Output Format:
JSON array with objects containing: {intent, sentiment, recommendations[], summary}
## Constraints:
- Maximum 300 words per response
- Use plain language, avoid jargon without explanation
- Prioritize empathy and solution-oriented tone
- Do not provide technical implementation details unless explicitly requested
```

---

## 3. Role Definition Framework (角色定义框架)

### 3.1 Role Components (角色组成要素)

```yaml
role_definition:
  name: "[角色名称]"
  archetype: "[原型类型，如：expert, consultant, collaborator, critic]"
  expertise: "[专业领域]"
  communication_style: "[沟通风格]"
  tone: "[语气特征]"
  boundaries: "[能力边界]"
```

### 3.2 Archetype Library (原型库参考)

| 原型 | 适用场景 | 关键特征 |
|------|----------|----------|
| **Expert** | 技术咨询、知识解答 | 权威、直接、基于证据 |
| **Consultant** | 业务分析、方案设计 | 结构化、引导式、结果导向 |
| **Collaborator** | 创意生成、头脑风暴 | 开放、探索性、鼓励发散 |
| **Critic** | 代码审查、提示词优化 | 严谨、批判性、改进导向 |
| **Narrator** | 故事创作、内容生成 | 沉浸感、一致性、情感共鸣 |

---

## 4. Context Structuring (上下文构建)

### 4.1 Information Layers (信息分层)

```markdown
# Primary Context (核心上下文 - 必须)
- User's immediate goal: [当前目标]
- Domain knowledge required: [所需领域知识]

# Secondary Context (次要上下文 - 条件性)
- Background information: [背景信息]
- Assumptions made: [隐含假设]

# Environmental Context (环境上下文 - 可选)
- System constraints: [系统限制]
- Tool capabilities: [工具能力]
```

### 4.2 Context Injection Patterns (上下文注入模式)

| 模式 | 适用场景 | 示例 |
|------|----------|------|
| **Chain-of-Thought** | 复杂推理任务 | "首先分析...然后推导...最后总结..." |
| **ReAct (Reason+Act)** | 需要工具调用 | "思考→行动→观察→再行动"循环 |
| **Tree-of-Thoughts** | 多路径探索 | 评估多个解决方案后选择最优 |
| **Self-Consistency** | 提高准确性 | 生成多种答案，投票选最一致 |

---

## 5. Task Decomposition (任务分解)

### 5.1 Granularity Guidelines (粒度指导原则)

| 任务复杂度 | 建议步骤数 | 每步深度 |
|-----------|----------|----------|
| 简单查询 | 1-2 步 | 直接响应 |
| 中等任务 | 3-5 步 | 包含子决策点 |
| 复杂工作流 | 6+ 步 | 需要状态管理 |

### 5.2 Decomposition Framework (分解框架)

```markdown
## Task: [总体目标]

### Step 1: [初始化]
- Action: 验证输入完整性
- Decision Point: 是否缺信息？→ YES/NO → 请求补充或继续

### Step 2: [分析阶段]
- Sub-step 2.1: Parse 关键要素
- Sub-step 2.2: Identify 约束条件
- Output to next step: 结构化数据对象

### Step 3: [执行/生成]
- Algorithm selection: [算法选择逻辑]
- Parameters: [参数配置规则]

### Step 4: [验证]
- Self-check checklist:
  - ✓ Does output meet format requirements?
  - ✓ Are all constraints satisfied?
  - ✓ Is reasoning transparent where needed?
```

---

## 6. Output Format Specification (输出格式规范)

### 6.1 Format Types (格式类型)

#### Text Formats:
- **Markdown** - 人类可读，结构化文档
- **JSON/JSONL** - 机器解析，API 响应
- **CSV/TSV** - 表格数据导出
- **Code Block** - 代码片段输出

#### Structured Templates:
```yaml
template_type: structured_response
schema_version: "2.0"
fields:
  - name: result
    type: string
    required: true
  - name: metadata
    type: object
    properties:
      timestamp: number
      confidence: number (0-1)
      reasoning: array[string]
```

### 6.2 Format Enforcement Strategies (格式强制策略)

| 策略 | 说明 | 适用场景 |
|------|------|----------|
| **Schema Validation** | JSON Schema/Pydantic | API 集成、数据管道 |
| **Regex Patterns** | 正则表达式验证 | 特定格式要求 |
| **Template Variables** | Jinja2/Mustache 模板 | 动态内容生成 |
| **Multi-format Fallback** | 主格式失败时降级 | 兼容性需求 |

---

## 7. Constraints & Boundaries (约束与边界)

### 7.1 Constraint Categories (约束分类)

```markdown
# Length Constraints
- Word count: [数字]
- Character limit: [数字]
- Section limits: {intro: X, body: Y, conclusion: Z}

# Content Boundaries
- Do NOT include: [禁止内容列表]
- Must include: [必含要素]
- Tone guidelines: [语气要求]

# Safety & Ethics
- PII handling: 不输出个人隐私数据
- Bias mitigation: 避免歧视性语言
- Fallback behavior: "我不知道"而非幻觉 |

# Performance Constraints
- Response latency target: < X ms
- Token budget per turn: ≤ Y tokens
- Memory footprint: 控制在 Z MB 以内 |
```

### 7.2 Boundary Testing (边界测试)

| 边界类型 | 测试场景 | 预期行为 |
|---------|----------|----------|
| **Out-of-Distribution** | 输入完全无关的内容 | 礼貌拒绝，提供相关帮助 |
| **Adversarial Input** | 试图绕过约束的指令 | 坚持边界，解释限制原因 |
| **Ambiguous Edge Cases** | 模糊不清的请求 | 请求澄清或给出最合理的解读 |

---

## 8. Examples & Few-Shot Learning (示例与少样本学习)

### 8.1 Example Structure (示例结构)

```markdown
## Task Description:
[任务说明]

## Input Format:
```
{
  "user_query": "...",
  "context": "..."
}
```

## Few-Shot Examples:

### Example 1
**Input:**
```json
{"user_query": "解释什么是深度学习", "context": "用户是初学者"}
```

**Output:**
```markdown
深度学习是一种模拟人脑神经网络结构的人工智能技术...
```

### Example 2:
**Input:**
```json
{"user_query": "计算斐波那契数列第 10 项", "context": "编程问题"}
```

**Output:**
```markdown
使用递归或迭代方法...结果为 55
```

## Evaluation Criteria:
- [✓] Accuracy
- [✓] Completeness
- [✓] Relevance to context
- [✓] Format compliance
```

### 8.2 Example Design Principles (示例设计原则)

1. **Variety** - 覆盖不同输入类型和难度级别
2. **Representativeness** - 反映真实使用场景
3. **Progressive Complexity** - 从简单到复杂递进
4. **Edge Cases Included** - 包含边界情况示例

---

## 9. TalkingArtProject Integration (TalkingArtProject 集成指南)

### 9.1 Project-Specific Patterns (项目特定模式)

```yaml
# TalkingArtProject 提示词架构标准:
talking_art_architecture:
  version: "2.0"
  core_components:
    - component: character_definition
      format: YAML archetype library + Markdown base_prompt
      validation: personality_consistency, trait_coherence
    
    - component: task_orchestration
      format: Task definition with step decomposition
      validation: workflow_completeness, state_management
    
    - component: style_transfer
      format: Era/lighting/style parameter mapping
      validation: cross_domain_coherence
```

### 9.2 Integration Checklist (集成检查清单)

- [ ] **Character Archetypes** - 符合 YAML schema 规范，包含完整的 personality_traits 和 props
- [ ] **Task Prompts** - 使用标准结构模板，包含 Steps、Output Format、Constraints
- [ ] **Style Definitions** - 遵循 era/lighting/style 映射规则
- [ ] **Examples Included** - 每个复杂任务提供至少 2 个 few-shot examples
- [ ] **Validation Tests** - 关键提示词有对应的 test cases

### 9.3 Continuous Improvement Workflow (持续改进工作流)

```mermaid
graph LR
    A[New Prompt Draft] --> B{Self-Check}
    B -->|Passes| C[Add to Library]
    B -->|Fails| D[Refine]
    C --> E[Run Evaluation Suite]
    E --> F{Score Threshold Met?}
    F -->|Yes| G[Maintain)
    F -->|No| D
    D --> H[Version Control Update]
```

### 9.4 Recommended Tooling (推荐工具)

| 工具 | 用途 | 命令 |
|------|------|------|
| **pygount** | 代码/提示词体积分析 | `pygount .` |
| **pytest + fixtures** | 提示词验证测试 | `pytest prompts/ --verbose` |
| **lm-eval-harness** | 提示词质量评估 | `lm_eval --model local ...` |
| **W&B** | 实验追踪与版本管理 | `wandb login && wandb init` |

---

## 📚 References & Further Reading (参考资料)

### Core Frameworks:
1. **Chain-of-Thought Prompting** - Wei et al., 2022
2. **ReAct: Reasoning + Acting** - Yao et al., 2023
3. **Self-Consistency** - Wang et al., 2023
4. **Tree of Thoughts** - Yao et al., 2023
5. **Constitutional AI** - Bai et al., 2022

### Best Practice Guides:
- [Prompt Engineering Guide](https://github.com/danielmiessler/awesome-prompts)
- [Analog Prompt Engineering](https://www.analogpromptengineering.com/)
- [Advanced Prompt Engineering](https://pypi.org/project/prompts/)

---

## 🔄 Version History (版本历史)

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0 | 2024-01-15 | Initial creation, core framework established |
| v1.1 | 2024-03-20 | Added TalkingArtProject integration section |
| v2.0 | Current | Enhanced structure, comprehensive examples added |

---

**Document Owner:** Lin Cun (希悦) / LJLinCun  
**Last Updated:** 2025-May-02  
**License:** MIT - Feel free to fork and adapt for your projects