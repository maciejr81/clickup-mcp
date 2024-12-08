import json
from typing import Any, Sequence, Optional
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from .base import ReturnMode, BaseTransformer, return_mode_schema

class TeamAPI:
    async def get_teams(self) -> list[dict]:
        """Get all accessible teams/workspaces."""
        response = await self.client.get(f"{self.base_url}/team")
        response.raise_for_status()
        return response.json()["teams"]

    async def create_team_group(self, team_id: str, name: str, member_ids: list[int]) -> dict:
        """Create a team (user group)."""
        data = {
            "name": name,
            "member_ids": member_ids
        }
        response = await self.client.post(
            f"{self.base_url}/team/{team_id}/group",
            json=data
        )
        response.raise_for_status()
        return response.json()

class TeamTransformer(BaseTransformer):
    @classmethod
    def get_fields(cls, mode: ReturnMode) -> list[str]:
        if mode == ReturnMode.MINIMAL:
            return ["id", "name"]
        elif mode == ReturnMode.IMPORTANT:
            return ["id", "name", "color", "avatar", "members"]
        return []

TEAM_TOOLS = [
    Tool(
        name="get-teams",
        description="Get all accessible teams/workspaces",
        inputSchema={
            "type": "object",
            "properties": {
                **return_mode_schema
            }
        }
    ),
    Tool(
        name="create-team-group",
        description="Create a team (user group)",
        inputSchema={
            "type": "object",
            "properties": {
                "team_id": {"type": "string"},
                "name": {"type": "string"},
                "member_ids": {"type": "array", "items": {"type": "integer"}}
            },
            "required": ["team_id", "name", "member_ids"]
        }
    )
]

async def handle_get_teams(client, arguments: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    return_mode = ReturnMode(arguments.pop("return_mode", "minimal"))
    teams = await client.get_teams()
    transformed_data = TeamTransformer.transform(teams, return_mode)
    return [TextContent(
        type="text",
        text=json.dumps(transformed_data, indent=2)
    )]

async def handle_create_team_group(client, arguments: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    team_id = arguments.pop("team_id")
    name = arguments.pop("name")
    member_ids = arguments.pop("member_ids")
    team = await client.create_team_group(team_id, name, member_ids)
    return [TextContent(
        type="text",
        text=json.dumps(team, indent=2)  # Full response for creation
    )]

TEAM_TOOL_HANDLERS = {
    "get-teams": handle_get_teams,
    "create-team-group": handle_create_team_group
}