# Skill MCP Server

<p align="center">
  <strong>让任何 AI Agent 瞬间掌握 Claude Skills 的"超能力"</strong>
</p>

<p align="center">
  <a href="#什么是-skill-mcp-server">介绍</a> •
  <a href="#为什么选择-skill-mcp-server">选择</a> •
  <a href="#核心特性">核心特性</a> •
  <a href="#快速开始">快速开始</a> •
  <a href="#创建-skill">创建 Skill</a> •
  <a href="#文档">文档</a>
</p>

## 什么是 Skill MCP Server？

Skill MCP Server 是一个标准的 Model Context Protocol (MCP) 服务器，它的作用很简单：把 Claude Skills 的能力桥接到任何支持 MCP 的 AI Agent 上。

<p align="center">
  <img src="docs/skll_mcp.png" alt="Skill MCP Server" style="max-width: 100%; height: auto;"/>
</p>

以前，Claude Skills 主要用在 Anthropic 的官方工具里。如果你的 AI 应用不支持 Skills，就得自己实现一套解析和执行逻辑，非常麻烦。现在有了这个项目，你只需要简单配置一下，就能让任何支持 MCP 的 Agent 直接使用标准的 Skill 文件。

## 核心概念

- **MCP (模型上下文协议)**：可以理解为 AI 界的"USB 接口"。只要你的 AI 助手支持这个接口，就能接入各种工具和服务。
- **Claude Skills**：可以理解为 AI 的"技能包"。它不只是文档，还包括操作说明（`SKILL.md`）、配套脚本（Python/JS）和参考资料。

Skill MCP Server 就是一个"转换器"，让各种 Agent 都能用上 Skill 生态，实现即插即用。

## 为什么选择 Skill MCP Server？

如果你的 Agent 还不支持 Skills，这个项目能帮你快速接入：

| 维度 | 原生支持的 Agent (如 Claude Code) | 其他 Agent (配合本项目使用) |
|------|----------------------------------|----------------------------|
| 获取门槛 | 官方深度集成，通常无法迁移 | 低门槛，通过标准 MCP 协议即可 |
| 研发负担 | 官方已完成底层开发 | 零代码，无需自行开发 Skill 解析引擎 |
| 应用灵活性 | 绑定在特定客户端 | 跨平台，自研 Agent、开源工具均可使用 |
| 功能对齐 | 完整支持脚本、资源及文件流 | 完美对齐，提供同等的动态执行与资源访问能力 |

## 核心特性

- 高度标准化：严格遵循 MCP 协议
- 通用性强：不绑定特定厂商，支持所有兼容 MCP 的 AI 客户端
- 免开发集成：帮助尚未具备 Skill 调用能力的 Agent 快速接入 Skill 生态
- 完全兼容：支持 `SKILL.md` 格式及 `scripts/`、`references/` 资源目录
- 工作空间隔离：支持指定 `--workspace`，明确约定 Skill 产出文件的存放位置
- 热重载：无需重启即可添加新 Skills
- 安全设计：路径验证、沙箱化文件操作

## 快速开始

推荐使用 `uvx` 运行，无需手动安装。

### 安装

```bash
# 使用 pip
pip install skill-mcp-server

# 使用 uv（推荐）
uv pip install skill-mcp-server
```

### 配置 MCP

将 Skill MCP Server 添加到你的 MCP 客户端配置中。所有支持 MCP 的客户端配置格式相同：

**使用 uvx（推荐，无需安装）：**

```json
{
  "mcpServers": {
    "skill-server": {
      "command": "uvx",
      "args": [
        "skill-mcp-server",
        "--skills-dir", "/path/to/your/skills",
        "--workspace", "/path/to/workspace"
      ]
    }
  }
}
```

**使用本地安装：**

```json
{
  "mcpServers": {
    "skill-server": {
      "command": "python",
      "args": [
        "-m", "skill_mcp_server",
        "--skills-dir", "/path/to/your/skills",
        "--workspace", "/path/to/workspace"
      ]
    }
  }
}
```

**配置文件位置：**
- Claude Desktop: `claude_desktop_config.json`（位置因操作系统而异）
- Claude Code: `~/.claude.json`
- 其他 MCP 客户端: 请参考客户端文档

**参数说明：**

- `--skills-dir`: 核心参数。设置为你想要让 Agent 调用的所有 Skill 文件夹的根目录。
- `--workspace`: 重要参数。指定 Skill 执行过程中产出文件（如代码、报告等）的保存位置。

## 提供的工具 (MCP Tools)

连接成功后，你的 AI Agent 可以使用以下工具：

1. `list_skills`：列出所有可用的技能
2. `skill`：加载特定技能，获取其 `SKILL.md` 中的详细指导
3. `skill_resource`：读取技能包内的参考文档或模板
4. `skill_script`：在安全环境下执行技能自带的脚本
5. `file_read`：从指定的 `workspace` 中读取文件
6. `file_write`：向指定的 `workspace` 中写入文件
7. `file_edit`：编辑 `workspace` 中的现有文件

## 如何创建一个 Skill？

一个标准的 Skill 结构如下：

```
my-skills/
└── deploy-helper/           # 技能文件夹
    ├── SKILL.md             # 核心说明文档 (必须)
    ├── scripts/             # 可执行脚本
    └── references/          # 参考资料
```

**SKILL.md 示例：**

```markdown
---
name: deploy-helper
description: 帮助用户一键部署应用到生产环境
---

# 部署助手使用说明

当用户要求部署时，请按以下步骤操作：
1. 使用 `skill_resource` 读取部署模板。
2. 修改本地配置文件。
3. 调用 `skill_script` 执行部署脚本。
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

## 使用场景

- 数据分析：让 Agent 具备数据分析能力
- 文档生成：让 Agent 创建专业文档
- API 集成：让 Agent 对接特定 API
- 代码审查：让 Agent 遵循团队规范
- DevOps 任务：让 Agent 自动化部署流程

## 文档

- [快速入门指南](docs/getting-started.md)
- [创建 Skills](docs/creating-skills.md)
- [Skill 格式参考](docs/skill-format.md)
- [发布指南](docs/publishing.md)

## 开发

```bash
# 克隆仓库
git clone https://github.com/ephemeraldew/skill_mcp.git
cd skill_mcp

# 安装开发依赖
uv pip install -e ".[dev]"

# 运行测试
pytest

# 运行代码检查
ruff check src/
```

## 贡献与反馈

欢迎提交 Pull Request 或报告 Issue！

如果这个项目对你有帮助，请给一个 Star。

## 许可证

MIT License - 详见 [LICENSE](LICENSE)

## 相关资源

- [MCP 官方文档](https://modelcontextprotocol.io/)
- [Claude Skills 官方说明](https://code.claude.com/docs/en/skills)
- [Agent Skills 开放标准](https://agentskills.io/)

---

<p align="center">
  <sub>基于 <a href="https://modelcontextprotocol.io/">Model Context Protocol</a> 构建</sub>
</p>
