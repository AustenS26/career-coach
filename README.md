# Career Coach

English | [中文](#中文)

A reference project for building a privacy-aware AI career coach that combines general career frameworks, role-specific knowledge, and user-owned context.

This repository is intentionally generic. It does not include private resumes, employer details, internal documents, conversation logs, or personal work history.

## Run The Generic App

This repository includes a runnable generic version, not only Markdown docs.

```bash
python3 server.py
```

Then open the printed local URL. The default is `http://127.0.0.1:8421`; if that port is busy, the server uses the next available port.

The app works in two modes:

- Preview mode: no API key required; it shows the workflow and context assembly behavior.
- Model mode: set `DEEPSEEK_API_KEY` or `OPENAI_API_KEY` to get real coaching responses.

## Personalization Slots

The public repository ships with safe examples. Users fill their own private context locally:

```bash
cp context/profile.example.md context/profile.local.md
cp context/domain-knowledge.md context/domain-knowledge.local.md
```

`*.local.md` files are ignored by git. This is the main extension point: the generic coach stays public, while personal profile, employer context, target role, and private notes stay local.

## What This Builds

The goal is a local-first career coaching assistant that can help with:

- Weekly career reviews
- Interview practice
- Resume and portfolio review
- Strategy document feedback
- Offer evaluation
- Role-specific learning plans

The key design idea is simple: a useful career coach is not just a chatbot over generic advice. It needs a structured context layer that explains the user's target role, operating environment, career goals, constraints, and preferred coaching style.

## Architecture

```text
career-coach/
├── README.md
├── index.html
├── server.py
├── context/
│   ├── profile.example.md
│   ├── profile.local.md           # private, ignored by git
│   ├── domain-knowledge.md
│   ├── domain-knowledge.local.md  # private, ignored by git
│   └── coaching-principles.md
├── templates/
│   ├── weekly-review.md
│   ├── mock-interview.md
│   ├── resume-review.md
│   ├── strategy-review.md
│   └── offer-evaluation.md
└── docs/
    ├── BUILDING.md
    ├── REFERENCES.md
    └── ROADMAP.md
```

## Core Components

| Component | Purpose |
|---|---|
| `context/profile.example.md` | A sanitized profile schema users can copy and fill locally |
| `context/domain-knowledge.md` | Role, industry, market, or function-specific knowledge |
| `context/coaching-principles.md` | Rules for how the coach should diagnose, challenge, and recommend |
| `templates/` | Repeatable workflows for common career scenarios |
| `index.html` | Generic front-end template for the coaching experience |
| `server.py` | Local backend that loads context, assembles prompts, and calls a model provider |

## Build Principles

1. Keep private context local unless the user explicitly chooses otherwise.
2. Separate generic framework content from personal profile content.
3. Make every workflow diagnostic before it becomes advisory.
4. Prefer one concrete next action over broad motivational advice.
5. Capture learning over time, but treat career logs as sensitive data.

## Quick Start

1. Run `python3 server.py` to open the generic app.
2. Copy `context/profile.example.md` to a private local file such as `context/profile.local.md`.
3. Fill in role, goals, constraints, target companies, and recurring challenges.
4. Optionally create `context/domain-knowledge.local.md` for role or industry-specific context.
5. Set `DEEPSEEK_API_KEY` or `OPENAI_API_KEY` for real model responses.
6. Save only sanitized learnings back into the public project.

## Privacy Boundary

Do not commit:

- Real resumes or compensation details
- Employer, manager, or teammate names
- Internal strategy docs
- Private work logs
- Interview feedback tied to identifiable companies
- API keys or model provider credentials

See [docs/BUILDING.md](docs/BUILDING.md) for the full design.

---

# 中文

一个用于构建 AI Career Coach 的参考项目。它把通用职业框架、岗位/行业知识和用户自己的上下文组合起来，同时把隐私边界放在第一位。

这个仓库刻意保持通用，不包含真实简历、雇主信息、内部文档、对话记录或个人工作经历。

## 运行通用版本

这个仓库不只是 Markdown 文档，也包含一个可运行的通用版本：

```bash
python3 server.py
```

然后打开终端里打印出的本地地址。默认是 `http://127.0.0.1:8421`；如果端口被占用，服务会自动使用下一个可用端口。

它有两种模式：

- 预览模式：不需要 API key，用于展示工作流和上下文组装方式。
- 模型模式：设置 `DEEPSEEK_API_KEY` 或 `OPENAI_API_KEY` 后，返回真实 coaching 回复。

## 个性化插槽

public 仓库只放安全示例。用户自己的信息通过本地私有文件填充：

```bash
cp context/profile.example.md context/profile.local.md
cp context/domain-knowledge.md context/domain-knowledge.local.md
```

`*.local.md` 已经被 `.gitignore` 忽略。这就是主要扩展口：通用 Career Coach 保持公开，个人画像、雇主上下文、目标岗位和私人笔记留在本地。

## 这个项目构建什么

目标是一个 local-first 的职业教练助手，支持：

- 每周职业复盘
- 面试练习
- 简历和作品集 review
- 策略文档反馈
- Offer 评估
- 针对岗位的学习计划

核心设计思路：有用的 Career Coach 不是一个泛泛而谈的聊天机器人。它需要结构化上下文，理解用户的目标岗位、工作环境、职业目标、约束条件和偏好的 coaching 风格。

## 项目结构

```text
career-coach/
├── README.md
├── index.html
├── server.py
├── context/
│   ├── profile.example.md
│   ├── profile.local.md           # private, ignored by git
│   ├── domain-knowledge.md
│   ├── domain-knowledge.local.md  # private, ignored by git
│   └── coaching-principles.md
├── templates/
│   ├── weekly-review.md
│   ├── mock-interview.md
│   ├── resume-review.md
│   ├── strategy-review.md
│   └── offer-evaluation.md
└── docs/
    ├── BUILDING.md
    ├── REFERENCES.md
    └── ROADMAP.md
```

## 核心组件

| 组件 | 用途 |
|---|---|
| `context/profile.example.md` | 可复制的脱敏用户画像 schema |
| `context/domain-knowledge.md` | 岗位、行业、市场或职能知识 |
| `context/coaching-principles.md` | 定义教练如何诊断、挑战和给建议 |
| `templates/` | 常见职业场景的可复用工作流 |
| `index.html` | 通用前端体验模板 |
| `server.py` | 本地后端，负责加载上下文、组装 prompt、调用模型 |

## 构建原则

1. 除非用户明确选择，否则私人上下文只保存在本地。
2. 把通用框架内容和个人画像内容分开。
3. 每个工作流都应该先诊断，再给建议。
4. 优先给一个具体行动，而不是宽泛鼓励。
5. 可以长期沉淀洞察，但职业记录默认属于敏感数据。

## 快速开始

1. 运行 `python3 server.py` 打开通用 app。
2. 将 `context/profile.example.md` 复制为本地私有文件，例如 `context/profile.local.md`。
3. 填入岗位、目标、约束、目标公司和反复出现的挑战。
4. 可选：创建 `context/domain-knowledge.local.md`，补充岗位或行业上下文。
5. 设置 `DEEPSEEK_API_KEY` 或 `OPENAI_API_KEY`，启用真实模型回复。
6. 只把脱敏后的学习沉淀保存回 public 项目。

## 隐私边界

不要提交：

- 真实简历或薪酬细节
- 雇主、经理、同事姓名
- 内部策略文档
- 私人工作日志
- 绑定具体公司的面试反馈
- API key 或模型供应商凭据

完整设计见 [docs/BUILDING.md](docs/BUILDING.md)。
