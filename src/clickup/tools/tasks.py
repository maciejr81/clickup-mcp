import json
from typing import Any, Sequence, Optional
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from .base import ReturnMode, BaseTransformer, return_mode_schema

# API client methods for tasks
class TaskAPI:
    
    async def create_task(self, list_id: str, name: str, **kwargs) -> dict:
        """Create a task."""
        data = {"name": name, **kwargs}
        response = await self.client.post(
            f"{self.base_url}/list/{list_id}/task",
            json=data
        )
        response.raise_for_status()
        return response.json()
    
    async def get_task_details(self, task_id: str, custom_task_ids: bool = False, team_id: Optional[str] = None) -> dict:
        """Get detailed information about a specific task."""
        params = {}
        if custom_task_ids:
            if not team_id:
                raise ValueError("team_id is required when using custom_task_ids")
            params["custom_task_ids"] = "true"
            params["team_id"] = team_id
            
        response = await self.client.get(
            f"{self.base_url}/task/{task_id}",
            params=params
        )
        response.raise_for_status()
        return response.json()

    async def get_tasks(self, list_id: str, **kwargs) -> list[dict]:
        """Get tasks from a list."""
        response = await self.client.get(
            f"{self.base_url}/list/{list_id}/task",
            params=kwargs
        )
        response.raise_for_status()
        return response.json()

    async def update_task(self, task_id: str, **kwargs) -> dict:
        """Update a task."""
        response = await self.client.put(
            f"{self.base_url}/task/{task_id}",
            json=kwargs
        )
        response.raise_for_status()
        return response.json()
    
    async def get_task_watchers(self, task_id: str) -> list[dict]:
        """Get task watchers."""
        response = await self.client.get(f"{self.base_url}/task/{task_id}/watching")
        response.raise_for_status()
        return response.json()["watchers"]
    
    async def add_task_watcher(self, task_id: str, watcher_id: str) -> dict:
        """Add a watcher to a task."""
        response = await self.client.post(
            f"{self.base_url}/task/{task_id}/watching",
            json={"watcher_id": watcher_id}
        )
        response.raise_for_status()
        return response.json()
    
    async def create_task_attachment(self, task_id: str, file) -> dict:
        """Create a task attachment."""
        files = {"attachment": file}
        response = await self.client.post(
            f"{self.base_url}/task/{task_id}/attachment",
            files=files
        )
        response.raise_for_status()
        return response.json()
        
# Data transformer for tasks
class TaskTransformer(BaseTransformer):
    @classmethod
    def get_fields(cls, mode: ReturnMode) -> list[str]:
        if mode == ReturnMode.MINIMAL:
            return ["id", "name", "status.status", "assignees.email"]
        elif mode == ReturnMode.IMPORTANT:
            return [
                "id", "name", "text_content", "due_date", "status.status", "priority", "assignees.email", "tags.name"
            ]
        return []  # Should never reach here due to base class handling FULL mode


# Tool definitions
TASK_TOOLS = [
    Tool(
        name="create-task",
        description="Create a new task in a list",
        inputSchema={
            "type": "object",
            "properties": {
                "list_id": {"type": "string"},
                "name": {"type": "string"},
                "markdown_description": {"type": "string", "optional": True},
                "assignees": {"type": "array", "items": {"type": "integer"}, "optional": True},
                "tags": {"type": "array", "items": {"type": "string"}, "optional": True},
                "status": {"type": "string", "optional": True},
                "priority": {"type": "integer", "optional": True},
                "due_date": {"type": "integer", "optional": True},
                "time_estimate": {"type": "integer", "optional": True},
                "notify_all": {"type": "boolean", "optional": True},
                **return_mode_schema
            },
            "required": ["list_id", "name"]
        }
    ),
    Tool(
        name="update-task",
        description="Update a task",
        inputSchema={
            "type": "object",
            "properties": {
                "task_id": {"type": "string"},
                "name": {"type": "string", "optional": True},
                "markdown_description": {"type": "string", "optional": True},
                "status": {"type": "string", "optional": True},
                "priority": {"type": "integer", "optional": True},
                "due_date": {"type": "integer", "optional": True},
                "time_estimate": {"type": "integer", "optional": True},
                "assignees": {"type": "array", "items": {"type": "integer"}, "optional": True},
                "archived": {"type": "boolean", "optional": True},
                **return_mode_schema
            },
            "required": ["task_id"]
        }
    ),
    Tool(
        name="get-task-watchers",
        description="Get watchers of a task",
        inputSchema={
            "type": "object",
            "properties": {
                "task_id": {"type": "string"},
                **return_mode_schema
            },
            "required": ["task_id"]
        }
    ),
    Tool(
        name="add-task-watcher",
        description="Add a watcher to a task",
        inputSchema={
            "type": "object",
            "properties": {
                "task_id": {"type": "string"},
                "watcher_id": {"type": "string"}
            },
            "required": ["task_id", "watcher_id"]
        }
    ),    
    Tool(
        name="get-task-details",
        description="Get detailed information about a specific task",
        inputSchema={
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "string",
                    "description": "The ID of the task"
                },
                "custom_task_ids": {
                    "type": "boolean",
                    "description": "Use custom task IDs",
                    "optional": True
                },
                "team_id": {
                    "type": "string",
                    "description": "Team ID (required for custom task IDs)",
                    "optional": True
                },
                **return_mode_schema
            },
            "required": ["task_id"]
        }
    ),
    Tool(
        name="get-tasks",
        description="Get tasks from a list",
        inputSchema={
            "type": "object",
            "properties": {
                "list_id": {"type": "string"},
                "archived": {"type": "boolean", "optional": True},
                "page": {"type": "integer", "optional": True},
                "order_by": {"type": "string", "optional": True},
                "reverse": {"type": "boolean", "optional": True},
                "subtasks": {"type": "boolean", "optional": True},
                "statuses": {"type": "array", "items": {"type": "string"}, "optional": True},
                "include_closed": {"type": "boolean", "optional": True},
                "assignees": {"type": "array", "items": {"type": "string"}, "optional": True},
                **return_mode_schema
            },
            "required": ["list_id"]
        }
    ),
    Tool(
        name="create-task-attachment",
        description="Create a task attachment",
        inputSchema={
            "type": "object",
            "properties": {
                "task_id": {"type": "string"},
                "attachment": {"type": "string", "format": "binary"}
            },
            "required": ["task_id", "attachment"]
        }
    )
]

# Tool handlers
async def handle_create_task(client, arguments: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    return_mode = ReturnMode(arguments.pop("return_mode", "minimal"))
    list_id = arguments.pop("list_id")
    name = arguments.pop("name")
    task = await client.create_task(list_id, name, **arguments)
    transformed_data = TaskTransformer.transform(task, return_mode)
    return [TextContent(
        type="text",
        text=json.dumps(transformed_data, indent=2)
    )]

async def handle_get_task_details(client, arguments: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    return_mode = ReturnMode(arguments.pop("return_mode", "minimal"))
    task = await client.get_task_details(
        task_id=arguments["task_id"],
        custom_task_ids=arguments.get("custom_task_ids", False),
        team_id=arguments.get("team_id")
    )
    transformed_data = TaskTransformer.transform(task, return_mode)
    return [TextContent(
        type="text",
        text=json.dumps(transformed_data, indent=2)
    )]

async def handle_get_tasks(client, arguments: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    return_mode = ReturnMode(arguments.pop("return_mode", "minimal"))
    tasks = await client.get_tasks(
        list_id=arguments["list_id"],
        **{k: v for k, v in arguments.items() if k != "list_id"}
    )
    transformed_data = TaskTransformer.transform(tasks, return_mode)
    return [TextContent(
        type="text",
        text=json.dumps(transformed_data, indent=2)
    )]
    
async def handle_update_task(client, arguments: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    task_id = arguments.pop("task_id")
    return_mode = ReturnMode(arguments.pop("return_mode", "minimal"))
    task = await client.update_task(task_id, **arguments)
    transformed_data = TaskTransformer.transform(task, return_mode)
    return [TextContent(
        type="text",
        text=json.dumps(transformed_data, indent=2)
    )]

async def handle_get_task_watchers(client, arguments: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    return_mode = ReturnMode(arguments.pop("return_mode", "minimal"))
    watchers = await client.get_task_watchers(arguments["task_id"])
    transformed_data = TaskTransformer.transform(watchers, return_mode)
    return [TextContent(
        type="text",
        text=json.dumps(transformed_data, indent=2)
    )]

async def handle_add_task_watcher(client, arguments: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    result = await client.add_task_watcher(
        task_id=arguments["task_id"],
        watcher_id=arguments["watcher_id"]
    )
    return [TextContent(
        type="text",
        text=json.dumps(result, indent=2)
    )]

async def handle_create_task_attachment(client, arguments: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    attachment = await client.create_task_attachment(
        task_id=arguments["task_id"],
        file=arguments["attachment"]
    )
    return [TextContent(
        type="text",
        text=json.dumps(attachment, indent=2)
    )]

# Tool registry
TASK_TOOL_HANDLERS = {
    "get-task-details": handle_get_task_details,
    "get-tasks": handle_get_tasks,
    "update-task": handle_update_task,
    "get-task-watchers": handle_get_task_watchers,
    "add-task-watcher": handle_add_task_watcher,
    "create-task-attachment": handle_create_task_attachment,
    "create-task": handle_create_task
}