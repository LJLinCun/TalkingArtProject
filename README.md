# TalkingArtProject — AI 智能体提示词工程框架

> **重要说明**: 本项目专为**AI 智能体服务**（OpenClaw、Hermes等）设计，提供模块化、可组合的提示词工程解决方案。不生产也不依赖任何视觉/视频内容生成提示词。

## 🎯 项目定位

这是一个为高级 AI 智能体构建的提示词工程框架，核心能力包括：

- **结构化提示词设计**: 基于清晰 schema 的系统化提示词组织
- **角色原型定义**: 可复用的智能体行为与交互模式
- **场景构图编排**: 多轮对话的上下文流转与控制
- **风格时代适配**: 跨时代的表达范式迁移

## 📁 项目结构

```
prompts/
├── character/
│   └── archetypes/          # 角色原型提示词库（智能体人格定义）
├── scene/
│   └── [composition/]       # 场景编排提示词（对话流转控制）
├── style/
│   ├── eras/               # 风格时代适配提示词（表达范式迁移）
│   └── lighting/           # 光影效果提示词（视觉-文本映射）
experiments/                 # 实验记录与迭代日志
examples/                    # 使用案例与测试脚本
```

## 🔧 Schema 版本控制

```yaml
schema_version: v1.0
author: LJLinCun
project_name: TalkingArtProject
framework_type: AI-Agent-Prompt-Engineering
last_updated: 2024
description: | 面向AI智能体的结构化提示词工程框架，提供模块化、可组合的
              提示词设计能力。专为高级AI系统（OpenClaw、Hermes等）的
              复杂交互场景而构建。
```

## 🚀 快速开始

### 1. 初始化项目

```bash
git clone https://github.com/LJLinCun/TalkingArtProject.git
cd TalkingArtProject
git pull origin main
```

### 2. 配置身份（首次使用）

```bash
git config --global user.name "你的名字"
git config --global user.email "你的邮箱@example.com"
```

### 3. Token 认证推送

```bash
# 方法1：使用 gh CLI（推荐）
gh auth setup-git

# 方法2：手动配置 git credential helper
git config --global credential.helper store
```

## 📝 核心能力说明

### 角色原型（Character Archetypes）
为 OpenClaw/Hermes等高级AI智能体定义自主决策机制、任务执行边界与交互协议，支持复杂场景下的多模态协同与工作流编排。

### 场景构图（Scene Composition）
设计面向Agent的多轮交互上下文流转逻辑，实现跨模态信息追踪、状态机管理与目标导向的任务达成控制。

### 风格时代适配（Style Eras）
迁移不同历史时期的表达范式与知识框架，使智能体能够跨越领域边界进行自适应响应与跨语境任务执行。

## 🔐 安全与隐私

- ✅ 本项目不包含任何视觉内容生成能力
- ✅ 所有提示词模块均为纯文本设计，无图像/视频依赖
- ✅ 符合 AI 智能体系统的纯对话型交互需求

## 📄 License

MIT 许可证 — 详见 LICENSE 文件。
