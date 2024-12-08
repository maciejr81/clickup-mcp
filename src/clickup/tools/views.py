import json
from typing import Any, Sequence, Optional
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from .base import ReturnMode, BaseTransformer, return_mode_schema

class ViewAPI:
    async def get_view(self, view_id: str) -> dict:
        """Get a specific view."""
        response = await self.client.get(f"{self.base_url}/view/{view_id}")
        response.raise_for_status()
        return response.json()

    async def get_view_tasks(self, view_id: str, page: int = 0) -> dict:
        """Get tasks from a specific view."""
        response = await self.client.get(
            f"{self.base_url}/view/{view_id}/task",
            params={"page": page}
        )
        response.raise_for_status()
        return response.json()

class ViewTransformer(BaseTransformer):
    @classmethod
    def get_fields(cls, mode: ReturnMode) -> list[str]:
        if mode == ReturnMode.MINIMAL:
            return ["id", "name"]
        elif mode == ReturnMode.IMPORTANT:
            return ["id", "name", "status", "priority.priority","date_updated", "assignees.email", "tags.name"]
        return []

VIEW_TOOLS = [
    Tool(
        name="get-view",
        description="Get view details",
        inputSchema={
            "type": "object",
            "properties": {
                "view_id": {"type": "string"},
                **return_mode_schema
            },
            "required": ["view_id"]
        }
    ),
    Tool(
        name="get-view-tasks",
        description="Get tasks from a view",
        inputSchema={
            "type": "object",
            "properties": {
                "view_id": {"type": "string"},
                "page": {"type": "integer", "optional": False},
                **return_mode_schema
            },
            "required": ["view_id"]
        }
    )
]

async def handle_get_view(client, arguments: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    return_mode = ReturnMode(arguments.pop("return_mode", "minimal"))
    view = await client.get_view(arguments["view_id"])
    transformed_data = ViewTransformer.transform(view, return_mode)
    return [TextContent(
        type="text",
        text=json.dumps(transformed_data, indent=2)
    )]

async def handle_get_view_tasks(client, arguments: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    return_mode = ReturnMode(arguments.pop("return_mode", "minimal"))
    page = arguments.pop("page", 0)
    tasks = await client.get_view_tasks(arguments["view_id"], page)
    transformed_data = ViewTransformer.transform(tasks, return_mode)
    return [TextContent(
        type="text",
        text=json.dumps(transformed_data, indent=2)
    )]

VIEW_TOOL_HANDLERS = {
    "get-view": handle_get_view,
    "get-view-tasks": handle_get_view_tasks
}