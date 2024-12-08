import json
from typing import Any, Sequence, Optional
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from .base import ReturnMode, BaseTransformer, return_mode_schema

class TimeTrackingAPI:
    async def get_time_entries(self, team_id: str, **kwargs) -> list[dict]:
        """Get time entries within a date range."""
        response = await self.client.get(
            f"{self.base_url}/team/{team_id}/time_entries",
            params=kwargs
        )
        response.raise_for_status()
        return response.json()["data"]
    
    async def start_time_entry(self, task_id: str, **kwargs) -> dict:
        """Start time tracking for a task."""
        response = await self.client.post(
            f"{self.base_url}/task/{task_id}/time",
            json=kwargs
        )
        response.raise_for_status()
        return response.json()

class TimeEntryTransformer(BaseTransformer):
    @classmethod
    def get_fields(cls, mode: ReturnMode) -> list[str]:
        if mode == ReturnMode.MINIMAL:
            return ["id", "task", "wid", "user", "duration"]
        elif mode == ReturnMode.IMPORTANT:
            return ["id", "task", "wid", "user", "duration", "billable", "description", "tags"]
        return []

TIME_TRACKING_TOOLS = [
    Tool(
        name="get-time-entries",
        description="Get time entries within a date range",
        inputSchema={
            "type": "object",
            "properties": {
                "team_id": {"type": "string"},
                "start_date": {"type": "integer", "optional": True},
                "end_date": {"type": "integer", "optional": True},
                **return_mode_schema
            },
            "required": ["team_id"]
        }
    ),
    Tool(
        name="start-time-entry",
        description="Start time tracking for a task",
        inputSchema={
            "type": "object",
            "properties": {
                "task_id": {"type": "string"},
                "description": {"type": "string", "optional": True},
                "billable": {"type": "boolean", "optional": True}
            },
            "required": ["task_id"]
        }
    )
]

async def handle_get_time_entries(client, arguments: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    return_mode = ReturnMode(arguments.pop("return_mode", "minimal"))
    team_id = arguments.pop("team_id")
    entries = await client.get_time_entries(team_id, **arguments)
    transformed_data = TimeEntryTransformer.transform(entries, return_mode)
    return [TextContent(
        type="text",
        text=json.dumps(transformed_data, indent=2)
    )]

async def handle_start_time_entry(client, arguments: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    task_id = arguments.pop("task_id")
    entry = await client.start_time_entry(task_id, **arguments)
    return [TextContent(
        type="text",
        text=json.dumps(entry, indent=2)
    )]

TIME_TRACKING_TOOL_HANDLERS = {
    "get-time-entries": handle_get_time_entries,
    "start-time-entry": handle_start_time_entry
}