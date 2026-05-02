# style/fusion-params.py — 智能体能力范式迁移引擎
---
# Agent Capability Paradigm Shift Engine - Cross-Domain Expression Framework
schema_version: "1.0"
author: TalkingArtProject
framework_type: AI-Agent-Prompt-Engineering

# Algorithm Definitions (Python functions)
def create_capability_shift(base_domain: str, target_domain: str = None) -> dict:
    """
    创建跨领域能力迁移提示词。
    
    Args:
        base_domain: 原始智能体能力域（如 '数据分析', '代码生成', '任务规划'）
        target_domain: 目标能力域（用于跨范式适配与表达框架转换）
    
    Returns:
        Dictionary containing:
            - shift_name: 迁移后的能力名称
            - adaptation_techniques: 适配方法列表
            - expression_framework: 表达框架建议
            - example_prompt: 生成的提示词模板
    """
    
    # 智能体能力领域数据库（按范式分类）
    domain_paradigms = {
        '数据分析': {
            'methods': ['统计推断', '模式识别', '异常检测'],
            'frameworks': ['量化分析', '概率建模']
        },
        '代码生成': {
            'methods': ['语法归纳', '重构推理', '类型推断'],
            'frameworks': ['形式化验证', '抽象解释']
        },
        '任务规划': {
            'methods': ['子任务分解', '约束调度', '资源分配'],
            'frameworks': ['时序逻辑', '优化理论']
        },
        '对话理解': {
            'methods': ['意图识别', '槽位填充', '多轮上下文追踪'],
            'frameworks': ['语义解析', '指代消解']
        }
    }
    
    base = domain_paradigms.get(base_domain.lower()) or {'methods': [base_domain], 'frameworks': []}
    target = domain_paradigms.get(target_domain) if target_domain else {}
    
    # 生成迁移适配方法
    primary_methods = base['methods']
    secondary_methods = target['methods'][:2] if target else []
    combined_methods = list(set(primary_methods + secondary_methods))
    
    return {
        'shift_name': f"{base_domain.capitalize()} → {target_domain or '跨范式'}迁移",
        'adaptation_techniques': combined_methods,
        'expression_frameworks': base['frameworks'] if target else [f"基于{base_domain}的框架适配"]
    }

# 能力表达框架生成器（简化版本）
def create_expression_template(base: str, target: str = None) -> str:
    """生成跨领域能力表达的提示词模板。"""
    base_templates = {
        '数据分析': ['统计推断', '模式识别'],
        '代码生成': ['语法归纳', '重构推理'],
        '任务规划': ['子任务分解', '约束调度']
    }
    
    primary = base_templates.get(base.lower(), [base])
    secondary = target_templates[target.lower()] if target else []
    
    return f"智能体能力迁移：{primary[0]} → {secondary[0] if secondary else '跨范式适配'}"

# 使用示例:
if __name__ == "__main__":
    # 数据分析 → 代码生成 范式迁移
    result = create_capability_shift('数据分析', '代码生成')
    print(f"能力迁移：{result['shift_name']}")
    print(f"适配方法：{result['adaptation_techniques']}")
    print(f"表达框架：{result['expression_frameworks']}")