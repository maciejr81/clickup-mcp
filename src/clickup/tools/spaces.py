import json
from typing import Any, Sequence, Optional
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from .base import ReturnMode, BaseTransformer, return_mode_schema

class SpaceAPI:
    async def get_spaces(self, team_id: str) -> list[dict]:
        """Get spaces in a team."""
        response = await self.client.get(f"{self.base_url}/team/{team_id}/space")
        response.raise_for_status()
        return response.json()["spaces"]
    
    async def create_space(self, team_id: str, name: str, **kwargs) -> dict:
        """Create a space."""
        data = {"name": name, **kwargs}
        response = await self.client.post(
            f"{self.base_url}/team/{team_id}/space",
            json=data
        )
        response.raise_for_status()
        return response.json()

class SpaceTransformer(BaseTransformer):
    @classmethod
    def get_fields(cls, mode: ReturnMode) -> list[str]:
        if mode == ReturnMode.MINIMAL:
            return ["id", "name"]
        elif mode == ReturnMode.IMPORTANT:
            return ["id", "name", "features", "statuses", "multiple_assignees"]
        return []

SPACE_TOOLS = [
    Tool(
        name="get-spaces",
        description="Get all spaces in a team",
        inputSchema={
            "type": "object",
            "properties": {
                "team_id": {"type": "string"},
                **return_mode_schema
            },
            "required": ["team_id"]
        }
    ),
    Tool(
        name="create-space",
        description="Create a new space in a team",
        inputSchema={
            "type": "object",
            "properties": {
                "team_id": {"type": "string"},
                "name": {"type": "string"},
                "multiple_assignees": {"type": "boolean", "optional": True},
                "features": {"type": "object", "optional": True}
            },
            "required": ["team_id", "name"]
        }
    )
]

async def handle_get_spaces(client, arguments: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    return_mode = ReturnMode(arguments.pop("return_mode", "minimal"))
    spaces = await client.get_spaces(arguments["team_id"])
    transformed_data = SpaceTransformer.transform(spaces, return_mode)
    return [TextContent(
        type="text",
        text=json.dumps(transformed_data, indent=2)
    )]

async def handle_create_space(client, arguments: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    team_id = arguments.pop("team_id")
    name = arguments.pop("name")
    space = await client.create_space(team_id, name, **arguments)
    return [TextContent(
        type="text",
        text=json.dumps(space, indent=2)
    )]

SPACE_TOOL_HANDLERS = {
    "get-spaces": handle_get_spaces,
    "create-space": handle_create_space
}