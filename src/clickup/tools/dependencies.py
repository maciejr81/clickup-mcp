import json
from typing import Any, Sequence, Optional
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from .base import ReturnMode, BaseTransformer, return_mode_schema

class DependencyAPI:
    async def add_task_dependency(self, task_id: str, depends_on: str, dependency_type: str = "waiting_on") -> dict:
        """Add a dependency to a task."""
        data = {
            "depends_on": depends_on,
            "dependency_type": dependency_type
        }
        response = await self.client.post(
            f"{self.base_url}/task/{task_id}/dependency",
            json=data
        )
        response.raise_for_status()
        return response.json()

    async def remove_task_dependency(self, task_id: str, dependency_id: str) -> dict:
        """Remove a dependency from a task."""
        response = await self.client.delete(
            f"{self.base_url}/task/{task_id}/dependency/{dependency_id}"
        )
        response.raise_for_status()
        return response.json()

    async def add_task_link(self, task_id: str, links_to: str) -> dict:
        """Add a task link."""
        response = await self.client.post(
            f"{self.base_url}/task/{task_id}/link/{links_to}"
        )
        response.raise_for_status()
        return response.json()

    async def delete_task_link(self, task_id: str, links_to: str) -> dict:
        """Delete a task link."""
        response = await self.client.delete(
            f"{self.base_url}/task/{task_id}/link/{links_to}"
        )
        response.raise_for_status()
        return response.json()

DEPENDENCY_TOOLS = [
    Tool(
        name="add-task-dependency",
        description="Add a dependency between tasks",
        inputSchema={
            "type": "object",
            "properties": {
                "task_id": {"type": "string"},
                "depends_on": {"type": "string"},
                "dependency_type": {
                    "type": "string",
                    "optional": True,
                    "enum": ["waiting_on", "blocking"]
                }
            },
            "required": ["task_id", "depends_on"]
        }
    ),
    Tool(
        name="remove-task-dependency",
        description="Remove a dependency from a task",
        inputSchema={
            "type": "object",
            "properties": {
                "task_id": {"type": "string"},
                "dependency_id": {"type": "string"}
            },
            "required": ["task_id", "dependency_id"]
        }
    ),
    Tool(
        name="add-task-link",
        description="Add a link between tasks",
        inputSchema={
            "type": "object",
            "properties": {
                "task_id": {"type": "string"},
                "links_to": {"type": "string"}
            },
            "required": ["task_id", "links_to"]
        }
    ),
    Tool(
        name="delete-task-link",
        description="Remove a link between tasks",
        inputSchema={
            "type": "object",
            "properties": {
                "task_id": {"type": "string"},
                "links_to": {"type": "string"}
            },
            "required": ["task_id", "links_to"]
        }
    )
]

async def handle_add_task_dependency(client, arguments: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    result = await client.add_task_dependency(
        task_id=arguments["task_id"],
        depends_on=arguments["depends_on"],
        dependency_type=arguments.get("dependency_type", "waiting_on")
    )
    return [TextContent(
        type="text",
        text=json.dumps(result, indent=2)
    )]

async def handle_remove_task_dependency(client, arguments: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    result = await client.remove_task_dependency(
        task_id=arguments["task_id"],
        dependency_id=arguments["dependency_id"]
    )
    return [TextContent(
        type="text",
        text=json.dumps(result, indent=2)
    )]

async def handle_add_task_link(client, arguments: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    result = await client.add_task_link(
        task_id=arguments["task_id"],
        links_to=arguments["links_to"]
    )
    return [TextContent(
        type="text",
        text=json.dumps(result, indent=2)
    )]

async def handle_delete_task_link(client, arguments: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    result = await client.delete_task_link(
        task_id=arguments["task_id"],
        links_to=arguments["links_to"]
    )
    return [TextContent(
        type="text",
        text=json.dumps(result, indent=2)
    )]

DEPENDENCY_TOOL_HANDLERS = {
    "add-task-dependency": handle_add_task_dependency,
    "remove-task-dependency": handle_remove_task_dependency,
    "add-task-link": handle_add_task_link,
    "delete-task-link": handle_delete_task_link
}