# Skill MCP Server Examples

## Interactive MCP Client Demo

A simple interactive command-line MCP client (`demo.py`) that demonstrates how to:
- Connect to skill-mcp-server via stdio protocol
- Use OpenAI SDK for chat completions
- Automatically handle tool calls from MCP server
- Maintain conversation history

### Installation

1. Install the skill-mcp-server package:
```bash
cd /path/to/skill_mcp
pip install -e .
```

2. Install example dependencies:
```bash
cd examples
pip install -r requirements.txt
```

### Configuration

Edit `demo.py` to configure your OpenAI API settings:

```python
openai_client = AsyncOpenAI(
    base_url="https://api.openai.com/v1",  # Your OpenAI endpoint
    api_key="your-api-key-here",           # Your API key
)
```

The MCP server configuration is automatically loaded from:
- **Skills directory**: `examples/skills/`
- **Workspace**: `workspace/`

### ❗️ Core Params
```python
from mcp import StdioServerParameters
...

    server_params = StdioServerParameters(
        command="python",
        args=[
            "-m",
            "skill_mcp_server",
            "--skills-dir",
            str(project_root / "examples" / "skills"),
            "--workspace",
            str(project_root / "workspace"),
        ],
    )
```

### Running the Demo

```bash
cd examples
python demo.py
```

### Usage

Once started, you'll see an interactive prompt:

```
🔧 Initializing MCP client...
✅ Loaded 2 tools from MCP server

📋 Available tools:
  - greeter_greet: Greet a person by name
  - greeter_farewell: Say goodbye to a person

💬 Interactive MCP Client
==================================================
Type your message and press Enter
Type 'quit' or 'exit' to stop
Type 'clear' to clear conversation history
==================================================

You:
```

### Example Interactions

**List available skills:**
```
You: What skills do you have?
Assistant: I have access to greeting tools that can greet and say farewell to people.
```

**Use a tool:**
```
You: Greet Alice
🔨 Calling tool: greeter_greet
   Arguments: {
     "name": "Alice"
   }
✅ Tool result: Hello, Alice! Welcome!
