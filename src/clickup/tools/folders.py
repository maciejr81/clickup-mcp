import json
from typing import Any, Sequence, Optional
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from .base import ReturnMode, BaseTransformer, return_mode_schema

class FolderAPI:
    async def update_folder(self, folder_id: str, **kwargs) -> dict:
        """Update a folder."""
        response = await self.client.put(
            f"{self.base_url}/folder/{folder_id}",
            json=kwargs
        )
        response.raise_for_status()
        return response.json()

    async def get_folders(self, space_id: str) -> list[dict]:
        """Get all folders in a space."""
        response = await self.client.get(f"{self.base_url}/space/{space_id}/folder")
        response.raise_for_status()
        return response.json()["folders"]

    async def get_folder(self, folder_id: str) -> dict:
        """Get a specific folder."""
        response = await self.client.get(f"{self.base_url}/folder/{folder_id}")
        response.raise_for_status()
        return response.json()

class FolderTransformer(BaseTransformer):
    @classmethod
    def get_fields(cls, mode: ReturnMode) -> list[str]:
        if mode == ReturnMode.MINIMAL:
            return ["id", "name"]
        elif mode == ReturnMode.IMPORTANT:
            return ["id", "name", "statuses", "hidden", "space", "task_count", "archived"]
        return []

FOLDER_TOOLS = [
    Tool(
        name="update-folder",
        description="Update a folder",
        inputSchema={
            "type": "object",
            "properties": {
                "folder_id": {"type": "string"},
                "name": {"type": "string"},
                **return_mode_schema
            },
            "required": ["folder_id", "name"]
        }
    ),
    Tool(
        name="get-folders",
        description="Get all folders in a space",
        inputSchema={
            "type": "object",
            "properties": {
                "space_id": {"type": "string"},
                **return_mode_schema
            },
            "required": ["space_id"]
        }
    ),
    Tool(
        name="get-folder",
        description="Get a specific folder",
        inputSchema={
            "type": "object",
            "properties": {
                "folder_id": {"type": "string"},
                **return_mode_schema
            },
            "required": ["folder_id"]
        }
    )
]

async def handle_update_folder(client, arguments: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    folder_id = arguments.pop("folder_id")
    return_mode = ReturnMode(arguments.pop("return_mode", "minimal"))
    folder = await client.update_folder(folder_id, **arguments)
    transformed_data = FolderTransformer.transform(folder, return_mode)
    return [TextContent(
        type="text",
        text=json.dumps(transformed_data, indent=2)
    )]

async def handle_get_folders(client, arguments: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    return_mode = ReturnMode(arguments.pop("return_mode", "minimal"))
    folders = await client.get_folders(arguments["space_id"])
    transformed_data = FolderTransformer.transform(folders, return_mode)
    return [TextContent(
        type="text",
        text=json.dumps(transformed_data, indent=2)
    )]

async def handle_get_folder(client, arguments: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    return_mode = ReturnMode(arguments.pop("return_mode", "minimal"))
    folder = await client.get_folder(arguments["folder_id"])
    transformed_data = FolderTransformer.transform(folder, return_mode)
    return [TextContent(
        type="text",
        text=json.dumps(transformed_data, indent=2)
    )]

FOLDER_TOOL_HANDLERS = {
    "update-folder": handle_update_folder,
    "get-folders": handle_get_folders,
    "get-folder": handle_get_folder
}