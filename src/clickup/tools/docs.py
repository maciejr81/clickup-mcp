import json
from typing import Any, Sequence, Optional
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from .base import ReturnMode, BaseTransformer, return_mode_schema

class DocAPI:
    async def search_docs(self, workspace_id: str, **kwargs) -> dict:
        """Search docs in workspace."""
        response = await self.client.get(
            f"{self.base_url_v3}/workspaces/{workspace_id}/docs",
            params=kwargs
        )
        response.raise_for_status()
        return response.json()
    
    async def create_doc(self, workspace_id: str, name: str, parent: dict, visibility: str, create_page: bool = True) -> dict:
        """Create a new doc."""
        data = {
            "name": name,
            "parent": parent,
            "visibility": visibility,
            "create_page": create_page
        }
        response = await self.client.post(
            f"{self.base_url_v3}/workspaces/{workspace_id}/docs",
            json=data
        )
        response.raise_for_status()
        return response.json()
    
    async def get_doc(self, workspace_id: str, doc_id: str) -> dict:
        """Get doc details."""
        response = await self.client.get(
            f"{self.base_url_v3}/workspaces/{workspace_id}/docs/{doc_id}"
        )
        response.raise_for_status()
        return response.json()
    
    async def get_doc_page_listing(self, workspace_id: str, doc_id: str, max_page_depth: int = -1) -> dict:
        """Get page listing for a doc."""
        params = {"max_page_depth": max_page_depth}
        response = await self.client.get(
            f"{self.base_url_v3}/workspaces/{workspace_id}/docs/{doc_id}/pageListing",
            params=params
        )
        response.raise_for_status()
        return response.json()
    
    async def get_doc_pages(self, workspace_id: str, doc_id: str, max_page_depth: int = -1, 
                           content_format: str = "text/md") -> dict:
        """Get all pages in a doc."""
        params = {
            "max_page_depth": max_page_depth,
            "content_format": content_format
        }
        response = await self.client.get(
            f"{self.base_url_v3}/workspaces/{workspace_id}/docs/{doc_id}/pages",
            params=params
        )
        response.raise_for_status()
        return response.json()
    
    async def create_page(self, workspace_id: str, doc_id: str, name: str, content: str, 
                         parent_page_id: Optional[str] = None, sub_title: Optional[str] = None,
                         content_format: str = "text/md") -> dict:
        """Create a new page in a doc."""
        data = {
            "name": name,
            "content": content,
            "parent_page_id": parent_page_id,
            "sub_title": sub_title,
            "content_format": content_format
        }
        response = await self.client.post(
            f"{self.base_url_v3}/workspaces/{workspace_id}/docs/{doc_id}/pages",
            json=data
        )
        response.raise_for_status()
        return response.json()
    
    async def get_page(self, workspace_id: str, doc_id: str, page_id: str,
                      content_format: str = "text/md") -> dict:
        """Get page details."""
        params = {"content_format": content_format}
        response = await self.client.get(
            f"{self.base_url_v3}/workspaces/{workspace_id}/docs/{doc_id}/pages/{page_id}",
            params=params
        )
        response.raise_for_status()
        return response.json()
    
    async def edit_page(self, workspace_id: str, doc_id: str, page_id: str,
                       name: str, content: str, sub_title: str,
                       content_edit_mode: str = "replace",
                       content_format: str = "text/md") -> dict:
        """Edit a page in a doc."""
        data = {
            "name": name,
            "content": content,
            "sub_title": sub_title,
            "content_edit_mode": content_edit_mode,
            "content_format": content_format
        }
        response = await self.client.put(
            f"{self.base_url_v3}/workspaces/{workspace_id}/docs/{doc_id}/pages/{page_id}",
            json=data
        )
        response.raise_for_status()
        return response.json()

class DocTransformer(BaseTransformer):
    @classmethod
    def get_fields(cls, mode: ReturnMode) -> list[str]:
        if mode == ReturnMode.MINIMAL:
            return ["id", "name", "visibility", "status"]
        elif mode == ReturnMode.IMPORTANT:
            return ["id", "name", "visibility", "status", "creator", "date_created", "parent", "sharing"]
        return []

class PageTransformer(BaseTransformer):
    @classmethod
    def get_fields(cls, mode: ReturnMode) -> list[str]:
        if mode == ReturnMode.MINIMAL:
            return ["id", "name", "content"]
        elif mode == ReturnMode.IMPORTANT:
            return ["id", "name", "content", "sub_title", "parent_page_id", "date_created", "date_updated"]
        return []

DOC_TOOLS = [
    Tool(
        name="search-docs",
        description="Search and filter docs in workspace",
        inputSchema={
            "type": "object",
            "properties": {
                "workspace_id": {"type": "string"},
                "id": {"type": "string", "optional": True},
                "creator": {"type": "number", "optional": True},
                "deleted": {"type": "boolean", "optional": True},
                "archived": {"type": "boolean", "optional": True},
                "parent_id": {"type": "string", "optional": True},
                "parent_type": {"type": "string", "optional": True},
                "limit": {"type": "number", "minimum": 10, "maximum": 100, "optional": True},
                "next_cursor": {"type": "string", "optional": True},
                **return_mode_schema
            },
            "required": ["workspace_id"]
        }
    ),
    Tool(
        name="create-doc",
        description="Create a new doc",
        inputSchema={
            "type": "object",
            "properties": {
                "workspace_id": {"type": "string"},
                "name": {"type": "string"},
                "parent": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "type": {"type": "number"}
                    },
                    "required": ["id", "type"]
                },
                "visibility": {"type": "string"},
                "create_page": {"type": "boolean", "optional": True},
                **return_mode_schema
            },
            "required": ["workspace_id", "name", "parent", "visibility"]
        }
    ),
    Tool(
        name="get-doc",
        description="Get doc details",
        inputSchema={
            "type": "object",
            "properties": {
                "workspace_id": {"type": "string"},
                "doc_id": {"type": "string"},
                **return_mode_schema
            },
            "required": ["workspace_id", "doc_id"]
        }
    ),
    Tool(
        name="get-doc-pages",
        description="Get all pages in a doc",
        inputSchema={
            "type": "object",
            "properties": {
                "workspace_id": {"type": "string"},
                "doc_id": {"type": "string"},
                "max_page_depth": {"type": "number", "optional": True},
                "content_format": {"type": "string", "optional": True},
                **return_mode_schema
            },
            "required": ["workspace_id", "doc_id"]
        }
    ),
    Tool(
        name="create-page",
        description="Create a new page in a doc",
        inputSchema={
            "type": "object",
            "properties": {
                "workspace_id": {"type": "string"},
                "doc_id": {"type": "string"},
                "name": {"type": "string"},
                "content": {"type": "string"},
                "parent_page_id": {"type": "string", "optional": True},
                "sub_title": {"type": "string", "optional": True},
                "content_format": {"type": "string", "optional": True},
                **return_mode_schema
            },
            "required": ["workspace_id", "doc_id", "name", "content"]
        }
    ),
    Tool(
        name="get-page",
        description="Get page details",
        inputSchema={
            "type": "object",
            "properties": {
                "workspace_id": {"type": "string"},
                "doc_id": {"type": "string"},
                "page_id": {"type": "string"},
                "content_format": {"type": "string", "optional": True},
                **return_mode_schema
            },
            "required": ["workspace_id", "doc_id", "page_id"]
        }
    ),
    Tool(
        name="edit-page",
        description="Edit/update a page",
        inputSchema={
            "type": "object",
            "properties": {
                "workspace_id": {"type": "string"},
                "doc_id": {"type": "string"},
                "page_id": {"type": "string"},
                "name": {"type": "string"},
                "content": {"type": "string"},
                "sub_title": {"type": "string"},
                "content_edit_mode": {"type": "string", "optional": True},
                "content_format": {"type": "string", "optional": True},
                **return_mode_schema
            },
            "required": ["workspace_id", "doc_id", "page_id", "name", "content", "sub_title"]
        }
    )
]

# Tool handlers
async def handle_search_docs(client, arguments: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    return_mode = ReturnMode(arguments.pop("return_mode", "minimal"))
    workspace_id = arguments.pop("workspace_id")
    docs = await client.search_docs(workspace_id, **arguments)
    transformed_data = DocTransformer.transform(docs, return_mode)
    return [TextContent(
        type="text",
        text=json.dumps(transformed_data, indent=2)
    )]

async def handle_create_doc(client, arguments: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    return_mode = ReturnMode(arguments.pop("return_mode", "minimal"))
    workspace_id = arguments.pop("workspace_id")
    name = arguments.pop("name")
    parent = arguments.pop("parent")
    visibility = arguments.pop("visibility")
    create_page = arguments.pop("create_page", True)
    
    doc = await client.create_doc(workspace_id, name, parent, visibility, create_page)
    transformed_data = DocTransformer.transform(doc, return_mode)
    return [TextContent(
        type="text",
        text=json.dumps(transformed_data, indent=2)
    )]

async def handle_get_doc(client, arguments: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    return_mode = ReturnMode(arguments.pop("return_mode", "minimal"))
    doc = await client.get_doc(arguments["workspace_id"], arguments["doc_id"])
    transformed_data = DocTransformer.transform(doc, return_mode)
    return [TextContent(
        type="text",
        text=json.dumps(transformed_data, indent=2)
    )]

async def handle_get_doc_pages(client, arguments: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    return_mode = ReturnMode(arguments.pop("return_mode", "minimal"))
    pages = await client.get_doc_pages(
        arguments["workspace_id"],
        arguments["doc_id"],
        arguments.get("max_page_depth", -1),
        arguments.get("content_format", "text/md")
    )
    transformed_data = PageTransformer.transform(pages, return_mode)
    return [TextContent(
        type="text",
        text=json.dumps(transformed_data, indent=2)
    )]

async def handle_create_page(client, arguments: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    return_mode = ReturnMode(arguments.pop("return_mode", "minimal"))
    page = await client.create_page(
        arguments["workspace_id"],
        arguments["doc_id"],
        arguments["name"],
        arguments["content"],
        arguments.get("parent_page_id"),
        arguments.get("sub_title"),
        arguments.get("content_format", "text/md")
    )
    transformed_data = PageTransformer.transform(page, return_mode)
    return [TextContent(
        type="text",
        text=json.dumps(transformed_data, indent=2)
    )]

async def handle_get_page(client, arguments: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    return_mode = ReturnMode(arguments.pop("return_mode", "minimal"))
    page = await client.get_page(
        arguments["workspace_id"],
        arguments["doc_id"],
        arguments["page_id"],
        arguments.get("content_format", "text/md")
    )
    transformed_data = PageTransformer.transform(page, return_mode)
    return [TextContent(
        type="text",
        text=json.dumps(transformed_data, indent=2)
    )]

async def handle_edit_page(client, arguments: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    return_mode = ReturnMode(arguments.pop("return_mode", "minimal"))
    page = await client.edit_page(
        arguments["workspace_id"],
        arguments["doc_id"],
        arguments["page_id"],
        arguments["name"],
        arguments["content"],
        arguments["sub_title"],
        arguments.get("content_edit_mode", "replace"),
        arguments.get("content_format", "text/md")
    )
    transformed_data = PageTransformer.transform(page, return_mode)
    return [TextContent(
        type="text",
        text=json.dumps(transformed_data, indent=2)
    )]

DOC_TOOL_HANDLERS = {
    "search-docs": handle_search_docs,
    "create-doc": handle_create_doc,
    "get-doc": handle_get_doc,
    "get-doc-pages": handle_get_doc_pages,
    "create-page": handle_create_page,
    "get-page": handle_get_page,
    "edit-page": handle_edit_page
}