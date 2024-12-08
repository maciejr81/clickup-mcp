import os
import httpx
from dotenv import load_dotenv
from typing import Optional

from ..tools.tasks import TaskAPI
from ..tools.lists import ListAPI
from ..tools.spaces import SpaceAPI
from ..tools.comments import CommentAPI
from ..tools.teams import TeamAPI
from ..tools.time_tracking import TimeTrackingAPI
from ..tools.webhooks import WebhookAPI
from ..tools.goals import GoalAPI
from ..tools.views import ViewAPI
from ..tools.custom_fields import CustomFieldAPI
from ..tools.folders import FolderAPI
from ..tools.dependencies import DependencyAPI
from ..tools.docs import DocAPI

class ClickUpClient(
    TaskAPI,
    ListAPI, 
    SpaceAPI,
    CommentAPI,
    TeamAPI,
    TimeTrackingAPI,
    WebhookAPI,
    GoalAPI,
    ViewAPI,
    CustomFieldAPI,
    FolderAPI,
    DependencyAPI,
    DocAPI
):
    """ClickUp API client that combines all entity-specific APIs."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.clickup.com/api/v2"  # For v2 endpoints
        self.base_url_v3 = "https://api.clickup.com/api/v3"  # For v3 endpoints
        self.headers = {
            "Authorization": api_key,
            "Content-Type": "application/json"
        }
        self._setup_client()
    
    @classmethod
    async def create(cls) -> 'ClickUpClient':
        """Factory method for creating client instance."""
        load_dotenv()
        api_key = os.getenv("CLICKUP_API_TOKEN")
        if not api_key:
            raise ValueError("CLICKUP_API_TOKEN environment variable not set")
        return cls(api_key)
    
    def _setup_client(self):
        """Setup the HTTP client with proper timeout and retry settings."""
        timeout = httpx.Timeout(30.0, connect=10.0)
        limits = httpx.Limits(max_keepalive_connections=5, max_connections=10)
        self.client = httpx.AsyncClient(
            headers=self.headers,
            timeout=timeout,
            limits=limits
        )

    async def __aenter__(self) -> 'ClickUpClient':
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.client.aclose()