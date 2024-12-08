import json
from typing import Any, Sequence, Optional
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from .base import ReturnMode, BaseTransformer, return_mode_schema

class WebhookAPI:
    async def get_webhooks(self, team_id: str) -> dict:
        """Get webhooks."""
        response = await self.client.get(f"{self.base_url}/team/{team_id}/webhook")
        response.raise_for_status()
        return response.json()

    async def create_webhook(self, team_id: str, endpoint: str, events: list[str], **kwargs) -> dict:
        """Create a webhook."""
        data = {
            "endpoint": endpoint,
            "events": events,
            **kwargs
        }
        response = await self.client.post(
            f"{self.base_url}/team/{team_id}/webhook",
            json=data
        )
        response.raise_for_status()
        return response.json()

class WebhookTransformer(BaseTransformer):
    @classmethod
    def get_fields(cls, mode: ReturnMode) -> list[str]:
        if mode == ReturnMode.MINIMAL:
            return ["id", "endpoint", "events"]
        elif mode == ReturnMode.IMPORTANT:
            return ["id", "endpoint", "events", "health", "secret", "status"]
        return []

WEBHOOK_TOOLS = [
    Tool(
        name="get-webhooks",
        description="Get webhooks",
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
        name="create-webhook",
        description="Create a webhook",
        inputSchema={
            "type": "object",
            "properties": {
                "team_id": {"type": "string"},
                "endpoint": {"type": "string"},
                "events": {"type": "array", "items": {"type": "string"}},
                "space_id": {"type": "string", "optional": True},
                "list_id": {"type": "string", "optional": True},
                "task_id": {"type": "string", "optional": True},
                "health_check_url": {"type": "string", "optional": True}
            },
            "required": ["team_id", "endpoint", "events"]
        }
    )
]

async def handle_get_webhooks(client, arguments: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    return_mode = ReturnMode(arguments.pop("return_mode", "minimal"))
    webhooks = await client.get_webhooks(arguments["team_id"])
    transformed_data = WebhookTransformer.transform(webhooks.get("webhooks", []), return_mode)
    return [TextContent(
        type="text",
        text=json.dumps(transformed_data, indent=2)
    )]

async def handle_create_webhook(client, arguments: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    team_id = arguments.pop("team_id")
    endpoint = arguments.pop("endpoint")
    events = arguments.pop("events")
    webhook = await client.create_webhook(team_id, endpoint, events, **arguments)
    return [TextContent(
        type="text",
        text=json.dumps(webhook, indent=2)
    )]

WEBHOOK_TOOL_HANDLERS = {
    "get-webhooks": handle_get_webhooks,
    "create-webhook": handle_create_webhook
}