import json
from typing import Any, Sequence, Optional
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from .base import ReturnMode, BaseTransformer, return_mode_schema

class CustomFieldAPI:
    async def get_accessible_custom_fields(self, list_id: str) -> list[dict]:
        """Get custom fields accessible in a list."""
        response = await self.client.get(f"{self.base_url}/list/{list_id}/field")
        response.raise_for_status()
        return response.json()["fields"]

    async def set_custom_field_value(self, task_id: str, field_id: str, value: Any) -> dict:
        """Set custom field value."""
        response = await self.client.post(
            f"{self.base_url}/task/{task_id}/field/{field_id}",
            json={"value": value}
        )
        response.raise_for_status()
        return response.json()

    async def remove_custom_field_value(self, task_id: str, field_id: str) -> dict:
        """Remove custom field value."""
        response = await self.client.delete(
            f"{self.base_url}/task/{task_id}/field/{field_id}"
        )
        response.raise_for_status()
        return response.json()

class CustomFieldTransformer(BaseTransformer):
    @classmethod
    def get_fields(cls, mode: ReturnMode) -> list[str]:
        if mode == ReturnMode.MINIMAL:
            return ["id", "name", "type"]
        elif mode == ReturnMode.IMPORTANT:
            return ["id", "name", "type", "type_config", "date_created", "hide_from_guests"]
        return []

CUSTOM_FIELD_TOOLS = [
    Tool(
        name="get-accessible-custom-fields",
        description="Get custom fields accessible in a list",
        inputSchema={
            "type": "object",
            "properties": {
                "list_id": {"type": "string"},
                **return_mode_schema
            },
            "required": ["list_id"]
        }
    ),
    Tool(
        name="set-custom-field-value",
        description="Set custom field value",
        inputSchema={
            "type": "object",
            "properties": {
                "task_id": {"type": "string"},
                "field_id": {"type": "string"},
                "value": {"type": "string"}
            },
            "required": ["task_id", "field_id", "value"]
        }
    ),
    Tool(
        name="remove-custom-field-value",
        description="Remove custom field value",
        inputSchema={
            "type": "object",
            "properties": {
                "task_id": {"type": "string"},
                "field_id": {"type": "string"}
            },
            "required": ["task_id", "field_id"]
        }
    )
]

async def handle_get_accessible_custom_fields(client, arguments: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    return_mode = ReturnMode(arguments.pop("return_mode", "minimal"))
    fields = await client.get_accessible_custom_fields(arguments["list_id"])
    transformed_data = CustomFieldTransformer.transform(fields, return_mode)
    return [TextContent(
        type="text",
        text=json.dumps(transformed_data, indent=2)
    )]

async def handle_set_custom_field_value(client, arguments: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    result = await client.set_custom_field_value(
        task_id=arguments["task_id"],
        field_id=arguments["field_id"],
        value=arguments["value"]
    )
    return [TextContent(
        type="text",
        text=json.dumps(result, indent=2)
    )]

async def handle_remove_custom_field_value(client, arguments: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    result = await client.remove_custom_field_value(
        task_id=arguments["task_id"],
        field_id=arguments["field_id"]
    )
    return [TextContent(
        type="text",
        text=json.dumps(result, indent=2)
    )]

CUSTOM_FIELD_TOOL_HANDLERS = {
    "get-accessible-custom-fields": handle_get_accessible_custom_fields,
    "set-custom-field-value": handle_set_custom_field_value,
    "remove-custom-field-value": handle_remove_custom_field_value
}