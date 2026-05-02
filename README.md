# TalkingArtProject — AI Agent Prompt Engineering Framework

> **Important**: This project is designed for **AI agent services** (OpenClaw, Hermes, etc.) and provides modular, composable prompt engineering solutions. It does NOT produce or rely on any visual/video content generation prompts.

## 🎯 Project Positioning

This is a prompt engineering framework built for advanced AI agents with core capabilities:

- **Structured Prompt Design**: Systematic prompt organization based on clear schemas
- **Character Archetype Definition**: Reusable agent behavior and interaction patterns
- **Scene Composition Orchestration**: Multi-turn dialogue context flow control
- **Style Era Adaptation**: Cross-era expression paradigm migration

## 📁 Project Structure

```
prompts/
├── character/
│   └── archetypes/          # Character archetype prompts (agent persona definitions)
├── scene/
│   └── [composition/]       # Scene composition prompts (dialogue flow control)
├── style/
│   ├── eras/               # Style era adaptation prompts (expression paradigm migration)
│   └── lighting/           # Lighting effect prompts (visual-text mapping)
experiments/                 # Experiment logs and iteration records
examples/                    # Usage cases and test scripts
```

## 🔧 Schema Version Control

```yaml
schema_version: v1.0
author: LJLinCun
project_name: TalkingArtProject
framework_type: AI-Agent-Prompt-Engineering
last_updated: 2024
description: | Structured prompt engineering framework for AI agents, providing 
              modular and composable prompt design capabilities. Built for 
              complex interaction scenarios in advanced AI systems (OpenClaw,
              Hermes, etc.).
```

## 🚀 Quick Start

### 1. Initialize the Project

```bash
git clone https://github.com/LJLinCun/TalkingArtProject.git
cd TalkingArtProject
git pull origin main
```

### 2. Configure Identity (First Time)

```bash
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

### 3. Token Authentication for Push

```bash
# Method 1: Use gh CLI (recommended)
gh auth setup-git

# Method 2: Configure git credential helper manually
git config --global credential.helper store
```

## 📝 Core Capabilities

### Character Archetypes
Define personality traits, behavioral patterns, and interaction boundaries for AI agents, enabling highly consistent conversational experiences.

### Scene Composition
Design multi-turn dialogue context flow logic to ensure state tracking and goal achievement in complex tasks.

### Style Era Adaptation
Migrate expression paradigms across different historical periods, allowing agents to interact naturally across temporal and contextual contexts.

## 🔐 Security & Privacy

- This project contains NO visual content generation capabilities
- All prompt modules are purely text-based with zero image/video dependencies  
- Designed for pure conversational interaction in AI agent systems

## 📄 License

MIT License — See LICENSE file for details.
