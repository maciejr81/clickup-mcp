import json
from typing import Any, Sequence, Optional
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from .base import ReturnMode, BaseTransformer, return_mode_schema

class CommentAPI:
    async def get_comments(self, task_id: str) -> list[dict]:
        """Get comments for a task."""
        response = await self.client.get(f"{self.base_url}/task/{task_id}/comment")
        response.raise_for_status()
        return response.json()["comments"]
    
    async def create_task_comment(self, task_id: str, comment_text: str, **kwargs) -> dict:
        """Create a comment on a task."""
        data = {"comment_text": comment_text, **kwargs}
        response = await self.client.post(
            f"{self.base_url}/task/{task_id}/comment",
            json=data
        )
        response.raise_for_status()
        return response.json()

class CommentTransformer(BaseTransformer):
    @classmethod
    def get_fields(cls, mode: ReturnMode) -> list[str]:
        if mode == ReturnMode.MINIMAL:
            return ["id", "comment_text", "user.email"]
        elif mode == ReturnMode.IMPORTANT:
            return ["id", "comment_text", "user.email","date"]
        return []

COMMENT_TOOLS = [
    Tool(
        name="get-comments",
        description="Get comments on a task",
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
        name="create-task-comment",
        description="Create a comment on a task",
        inputSchema={
            "type": "object",
            "properties": {
                "task_id": {"type": "string"},
                "comment_text": {"type": "string"},
                "assignee": {"type": "integer", "optional": True},
                "notify_all": {"type": "boolean", "optional": True}
            },
            "required": ["task_id", "comment_text"]
        }
    )
]

async def handle_get_comments(client, arguments: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    return_mode = ReturnMode(arguments.pop("return_mode", "minimal"))
    comments = await client.get_comments(arguments["task_id"])
    transformed_data = CommentTransformer.transform(comments, return_mode)
    return [TextContent(
        type="text",
        text=json.dumps(transformed_data, indent=2)
    )]

async def handle_create_task_comment(client, arguments: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    task_id = arguments.pop("task_id")
    comment_text = arguments.pop("comment_text")
    comment = await client.create_task_comment(task_id, comment_text, **arguments)
    return [TextContent(
        type="text",
        text=json.dumps(comment, indent=2)
    )]

COMMENT_TOOL_HANDLERS = {
    "get-comments": handle_get_comments,
    "create-task-comment": handle_create_task_comment
}
