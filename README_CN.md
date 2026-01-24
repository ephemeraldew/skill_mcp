# Skill MCP Server

<p align="center">
  <strong>让任何 AI Agent 瞬间成为专家 — 只需放入一个 Skill 文件夹</strong>
</p>

<p align="center">
  <a href="#特性">特性</a> •
  <a href="#快速开始">快速开始</a> •
  <a href="#工作原理">工作原理</a> •
  <a href="#创建-skill">创建 Skill</a> •
  <a href="#文档">文档</a>
</p>

---

**Skill MCP Server** 是一个 [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) 服务器，让 Claude 等 AI Agent 能够动态加载和使用模块化的 "Skills"。

可以把它理解为 **AI Agent 的插件系统** — 将 Skill 文件夹放入目录，你的 Agent 就立即获得新能力。无需编码，无需重启服务。

## 为什么选择 Skill MCP Server？

| 传统方式 | 使用 Skill MCP Server |
|---------|---------------------|
| 编写代码扩展 Agent 能力 | 只需复制一个文件夹 |
| 重启服务才能生效 | 热加载，即时可用 |
| 每个能力都要单独开发 | 社区共享，即插即用 |
| 复杂的集成工作 | 零配置 |

## 特性

- **即时扩展能力** — 放入 Skill 文件夹，立即获得新能力
- **零配置** — Skills 自动发现和加载
- **热重载** — 无需重启即可添加新 Skills
- **多语言脚本** — 支持 Python、Shell、JavaScript、TypeScript
- **安全设计** — 路径验证、沙箱化文件操作
- **资源捆绑** — Skill 可包含模板、参考文档和资源文件

## 快速开始

### 安装

```bash
# 使用 pip
pip install skill-mcp-server

# 使用 uv（推荐）
uv pip install skill-mcp-server
```

### 30 秒上手

```bash
# 1. 创建 skills 目录
mkdir skills

# 2. 下载或创建一个 skill（示例：复制 skill-creator）
cp -r examples/skill-creator skills/

# 3. 启动服务器
skill-mcp-server --skills-dir ./skills
```

搞定！你的 AI Agent 现在可以使用这个 Skill 了。

### 配置 Claude Desktop

添加到 `claude_desktop_config.json`：

```json
{
  "mcpServers": {
    "skill-server": {
      "command": "skill-mcp-server",
      "args": ["--skills-dir", "/path/to/your/skills"]
    }
  }
}
```

### 配置 Claude Code

添加到 `~/.claude.json`：

```json
{
  "mcpServers": {
    "skill-server": {
      "command": "skill-mcp-server",
      "args": [
        "--skills-dir", "/path/to/your/skills",
        "--workspace", "/path/to/workspace"
      ]
    }
  }
}
```

## 工作原理

```
┌─────────────────────────────────────────────────────────────────┐
│                        AI Agent (Claude)                         │
└─────────────────────────────────────────────────────────────────┘
                                │
                                │ MCP 协议
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Skill MCP Server                            │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐    │
│  │   skill   │  │  skill_   │  │  skill_   │  │   file_   │    │
│  │  loader   │  │ resource  │  │  script   │  │   ops     │    │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘    │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                         Skills 目录                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │ 数据分析师   │  │  文档写手    │  │  API助手    │  ...        │
│  │  SKILL.md   │  │  SKILL.md   │  │  SKILL.md   │             │
│  │  scripts/   │  │  templates/ │  │  references/│             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└─────────────────────────────────────────────────────────────────┘
```

### 可用的 MCP 工具

| 工具 | 描述 |
|------|------|
| `skill` | 加载 Skill 获取详细指导 |
| `list_skills` | 列出所有可用的 Skills |
| `skill_resource` | 读取 Skill 的资源文件 |
| `skill_script` | 执行 Skill 捆绑的脚本 |
| `file_read` | 从工作目录读取文件 |
| `file_write` | 向工作目录写入文件 |
| `file_edit` | 编辑工作目录中的现有文件 |

## 创建 Skill

Skill 就是一个包含 `SKILL.md` 文件的文件夹：

```
my-skill/
├── SKILL.md              # 必需：给 AI 的指导说明
├── scripts/              # 可选：可执行脚本
│   └── process_data.py
├── references/           # 可选：参考文档
│   └── api_docs.md
└── assets/               # 可选：模板、图片等
    └── report_template.md
```

### SKILL.md 格式

```markdown
---
name: my-skill
description: 简要描述这个 Skill 做什么以及何时使用
---

# My Skill

## 概述

解释这个 Skill 能让 AI 做什么。

## 使用方法

给 AI Agent 的分步指导说明...

## 可用资源

- `scripts/process_data.py` - 处理输入数据
- `assets/report_template.md` - 输出模板
```

### 示例：数据分析师 Skill

```markdown
---
name: data-analyst
description: 分析 CSV 数据并生成洞察报告
---

# 数据分析师

## 使用场景

当用户需要以下功能时使用此 Skill：
- 分析 CSV 或表格数据
- 生成统计摘要
- 创建数据可视化

## 工作流程

1. 使用 `file_read` 读取数据文件
2. 执行 `scripts/analyze.py` 进行统计分析
3. 使用 `assets/report_template.md` 格式化输出
4. 使用 `file_write` 写入报告
```

## 使用场景

- **数据分析** — Agent 变身数据科学家
- **文档生成** — Agent 创建专业文档
- **API 集成** — Agent 对接特定 API
- **代码审查** — Agent 遵循团队规范
- **DevOps 任务** — Agent 自动化部署流程

## 文档

- [快速入门指南](docs/getting-started.md)
- [创建 Skills](docs/creating-skills.md)
- [Skill 格式参考](docs/skill-format.md)
- [API 参考](docs/api/)

## 开发

```bash
# 克隆仓库
git clone https://github.com/your-org/skill-mcp-server.git
cd skill-mcp-server

# 安装开发依赖
uv pip install -e ".[dev]"

# 运行测试
pytest

# 运行代码检查
ruff check src/
```

## 贡献

欢迎贡献！请参阅 [CONTRIBUTING.md](CONTRIBUTING.md) 了解指南。

## 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

<p align="center">
  <sub>基于 <a href="https://modelcontextprotocol.io/">Model Context Protocol</a> 构建</sub>
</p>