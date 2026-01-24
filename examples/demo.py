#!/usr/bin/env python3
"""
Simple interactive MCP client using OpenAI SDK
Connects to skill-mcp-server via stdio protocol
"""

import asyncio
import json
from pathlib import Path
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import AsyncOpenAI


class InteractiveMCPClient:
    """Interactive MCP client with OpenAI integration"""

    def __init__(self, openai_client: AsyncOpenAI, mcp_session: ClientSession):
        self.openai_client = openai_client
        self.mcp_session = mcp_session
        self.tools = []
        self.conversation_history = []

    async def initialize(self):
        """Initialize MCP connection and load available tools"""
        print("🔧 Initializing MCP client...")

        # List available tools from MCP server
        response = await self.mcp_session.list_tools()

        # Convert MCP tools to OpenAI function format
        self.tools = []
        for tool in response.tools:
            openai_tool = {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description or "",
                    "parameters": tool.inputSchema
                    if tool.inputSchema
                    else {"type": "object", "properties": {}},
                },
            }
            self.tools.append(openai_tool)

        print(f"✅ Loaded {len(self.tools)} tools from MCP server")
        if self.tools:
            print("\n📋 Available tools:")
            for tool in self.tools:
                print(f"  - {tool['function']['name']}: {tool['function']['description']}")
        print()

    async def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> Any:
        """Call MCP tool and return result"""
        print(f"🔨 Calling tool: {tool_name}")
        print(f"   Arguments: {json.dumps(arguments, indent=2)}")

        try:
            result = await self.mcp_session.call_tool(tool_name, arguments)
            print(f"✅ Tool result: {result.content[0].text if result.content else 'No result'}\n")
            return result.content[0].text if result.content else "Tool executed successfully"
        except Exception as e:
            error_msg = f"Error calling tool: {str(e)}"
            print(f"❌ {error_msg}\n")
            return error_msg

    async def chat(self, user_message: str) -> str:
        """Send message and handle tool calls"""
        # Add user message to history
        self.conversation_history.append({"role": "user", "content": user_message})

        while True:
            # Call OpenAI API
            response = await self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=self.conversation_history,
                tools=self.tools if self.tools else None,
            )

            message = response.choices[0].message

            # Check if model wants to call tools
            if message.tool_calls:
                # Add assistant message to history
                self.conversation_history.append(
                    {
                        "role": "assistant",
                        "content": message.content,
                        "tool_calls": [
                            {
                                "id": tc.id,
                                "type": "function",
                                "function": {
                                    "name": tc.function.name,
                                    "arguments": tc.function.arguments,
                                },
                            }
                            for tc in message.tool_calls
                        ],
                    }
                )

                # Execute each tool call
                for tool_call in message.tool_calls:
                    tool_name = tool_call.function.name
                    arguments = json.loads(tool_call.function.arguments)

                    # Call the MCP tool
                    result = await self.call_tool(tool_name, arguments)

                    # Add tool result to history
                    self.conversation_history.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": str(result),
                        }
                    )

                # Continue the loop to get final response
                continue
            else:
                # No more tool calls, return final response
                assistant_message = message.content or "I don't have a response."
                self.conversation_history.append(
                    {"role": "assistant", "content": assistant_message}
                )
                return assistant_message

    async def run_interactive(self):
        """Run interactive chat loop"""
        await self.initialize()

        print("💬 Interactive MCP Client")
        print("=" * 50)
        print("Type your message and press Enter")
        print("Type 'quit' or 'exit' to stop")
        print("Type 'clear' to clear conversation history")
        print("=" * 50)
        print()

        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ["quit", "exit"]:
                    print("\n👋 Goodbye!")
                    break

                if user_input.lower() == "clear":
                    self.conversation_history = []
                    print("🗑️  Conversation history cleared\n")
                    continue

                # Get AI response
                print()
                response = await self.chat(user_input)
                print(f"Assistant: {response}")
                print()

            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}\n")


async def main():
    """Main entry point"""
    # Get project root directory
    project_root = Path(__file__).parent.parent

    # Configure OpenAI client (using your custom endpoint)
    openai_client = AsyncOpenAI(
        base_url="<your_base_url>",
        api_key="<your_api_key>",
    )

    # Configure MCP server parameters (using stdio)
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

    # Connect to MCP server via stdio
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize session
            await session.initialize()

            # Create and run interactive client
            client = InteractiveMCPClient(openai_client, session)
            await client.run_interactive()


if __name__ == "__main__":
    asyncio.run(main())
