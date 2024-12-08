import json
from typing import Any, Sequence, Optional
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from .base import ReturnMode, BaseTransformer, return_mode_schema

class GoalAPI:
    async def get_goals(self, team_id: str) -> list[dict]:
        """Get goals."""
        response = await self.client.get(f"{self.base_url}/team/{team_id}/goal")
        response.raise_for_status()
        return response.json()["goals"]

    async def create_goal(self, team_id: str, name: str, **kwargs) -> dict:
        """Create a goal."""
        data = {"name": name, **kwargs}
        response = await self.client.post(
            f"{self.base_url}/team/{team_id}/goal",
            json=data
        )
        response.raise_for_status()
        return response.json()

class GoalTransformer(BaseTransformer):
    @classmethod
    def get_fields(cls, mode: ReturnMode) -> list[str]:
        if mode == ReturnMode.MINIMAL:
            return ["id", "name", "date_created"]
        elif mode == ReturnMode.IMPORTANT:
            return ["id", "name", "date_created", "owner", "color", "description", "multiple_owners", "owners"]
        return []

GOAL_TOOLS = [
    Tool(
        name="create-goal",
        description="Create a new goal in a team",
        inputSchema={
            "type": "object",
            "properties": {
                "team_id": {"type": "string"},
                "name": {"type": "string"},
                "due_date": {"type": "integer", "optional": True},
                "description": {"type": "string", "optional": True},
                "multiple_owners": {"type": "boolean", "optional": True},
                "owners": {"type": "array", "items": {"type": "integer"}, "optional": True},
                "color": {"type": "string", "optional": True}
            },
            "required": ["team_id", "name"]
        }
    ),
    Tool(
        name="get-goals",
        description="Get goals in a team",
        inputSchema={
            "type": "object",
            "properties": {
                "team_id": {"type": "string"},
                **return_mode_schema
            },
            "required": ["team_id"]
        }
    )
]

async def handle_create_goal(client, arguments: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    team_id = arguments.pop("team_id")
    name = arguments.pop("name")
    goal = await client.create_goal(team_id, name, **arguments)
    return [TextContent(
        type="text",
        text=json.dumps(goal, indent=2)
    )]

async def handle_get_goals(client, arguments: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    return_mode = ReturnMode(arguments.pop("return_mode", "minimal"))
    goals = await client.get_goals(arguments["team_id"])
    transformed_data = GoalTransformer.transform(goals, return_mode)
    return [TextContent(
        type="text",
        text=json.dumps(transformed_data, indent=2)
    )]

GOAL_TOOL_HANDLERS = {
    "create-goal": handle_create_goal,
    "get-goals": handle_get_goals
}