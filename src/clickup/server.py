import asyncio
import logging
from typing import Any, Sequence, Optional
from mcp.server import Server
from mcp.types import TextContent, ImageContent, EmbeddedResource, Tool
from mcp.server.stdio import stdio_server
from .tools import get_all_tools, get_tool_handler
from .api import ClickUpClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("clickup-server")

class ClickUpServer:
    def __init__(self):
        self.client = None
        self.app = Server("clickup-server")
        self.setup_handlers()

    def setup_handlers(self):
        @self.app.list_tools()
        async def list_tools() -> list[Tool]:
            return get_all_tools()

        @self.app.call_tool() 
        async def call_tool(name: str, arguments: Any) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
            handler = get_tool_handler(name)
            if not handler:
                raise ValueError(f"Unknown tool: {name}")
            return await handler(self.client, arguments)

    async def initialize(self):
        """Initialize the ClickUp client."""
        self.client = await ClickUpClient.create()

    async def run(self):
        """Run the server."""
        await self.initialize()
        async with stdio_server() as (read_stream, write_stream):
            await self.app.run(
                read_stream,
                write_stream,
                self.app.create_initialization_options()
            )

async def main():
    """Main entry point."""
    server = ClickUpServer()
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())