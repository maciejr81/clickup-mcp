import json
from typing import Any, Sequence, Optional
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from .base import ReturnMode, BaseTransformer, return_mode_schema

class ListAPI:
    async def get_lists(self, space_id: str) -> list[dict]:
        """Get lists in a space."""
        response = await self.client.get(f"{self.base_url}/space/{space_id}/list")
        response.raise_for_status()
        return response.json()["lists"]
    
    async def create_folderless_list(self, space_id: str, name: str, **kwargs) -> dict:
        """Create a list directly in a space."""
        data = {"name": name, **kwargs}
        response = await self.client.post(
            f"{self.base_url}/space/{space_id}/list",
            json=data
        )
        response.raise_for_status()
        return response.json()

class ListTransformer(BaseTransformer):
    @classmethod
    def get_fields(cls, mode: ReturnMode) -> list[str]:
        if mode == ReturnMode.MINIMAL:
            return ["id", "name"]
        elif mode == ReturnMode.IMPORTANT:
            return ["id", "name", "text_content", "due_date", "status.status", "priority", "assignees.email", "task.name"]
        return []

LIST_TOOLS = [
    Tool(
        name="get-lists",
        description="Get all lists in a space",
        inputSchema={
            "type": "object",
            "properties": {
                "space_id": {"type": "string"},
                **return_mode_schema
            },
            "required": ["space_id"]
        }
    ),
    Tool(
        name="create-folderless-list",
        description="Create a list directly in a space without a folder",
        inputSchema={
            "type": "object",
            "properties": {
                "space_id": {"type": "string"},
                "name": {"type": "string"},
                "content": {"type": "string", "optional": True},
                "due_date": {"type": "integer", "optional": True},
                "priority": {"type": "integer", "optional": True},
                "assignee": {"type": "integer", "optional": True},
                "status": {"type": "string", "optional": True}
            },
            "required": ["space_id", "name"]
        }
    )
]

async def handle_get_lists(client, arguments: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    return_mode = ReturnMode(arguments.pop("return_mode", "minimal"))
    lists = await client.get_lists(arguments["space_id"])
    transformed_data = ListTransformer.transform(lists, return_mode)
    return [TextContent(
        type="text",
        text=json.dumps(transformed_data, indent=2)
    )]

async def handle_create_folderless_list(client, arguments: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    space_id = arguments.pop("space_id")
    name = arguments.pop("name")
    list_data = await client.create_folderless_list(space_id, name, **arguments)
    return [TextContent(
        type="text",
        text=json.dumps(list_data, indent=2)  # Always return full data for create operations
    )]

LIST_TOOL_HANDLERS = {
    "get-lists": handle_get_lists,
    "create-folderless-list": handle_create_folderless_list
}