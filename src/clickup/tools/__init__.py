from typing import Callable, Dict, List, Any, Optional
from mcp.types import Tool

from .tasks import TASK_TOOLS, TASK_TOOL_HANDLERS
from .lists import LIST_TOOLS, LIST_TOOL_HANDLERS
from .spaces import SPACE_TOOLS, SPACE_TOOL_HANDLERS
from .teams import TEAM_TOOLS, TEAM_TOOL_HANDLERS
from .comments import COMMENT_TOOLS, COMMENT_TOOL_HANDLERS
from .time_tracking import TIME_TRACKING_TOOLS, TIME_TRACKING_TOOL_HANDLERS
from .webhooks import WEBHOOK_TOOLS, WEBHOOK_TOOL_HANDLERS
from .goals import GOAL_TOOLS, GOAL_TOOL_HANDLERS
from .views import VIEW_TOOLS, VIEW_TOOL_HANDLERS
from .custom_fields import CUSTOM_FIELD_TOOLS, CUSTOM_FIELD_TOOL_HANDLERS
from .folders import FOLDER_TOOLS, FOLDER_TOOL_HANDLERS
from .dependencies import DEPENDENCY_TOOLS, DEPENDENCY_TOOL_HANDLERS
from .docs import DOC_TOOLS, DOC_TOOL_HANDLERS

def get_all_tools() -> List[Tool]:
    """Get all available tools."""
    return [
        *TASK_TOOLS,
        *LIST_TOOLS,
        *SPACE_TOOLS,
        *TEAM_TOOLS,
        *COMMENT_TOOLS,
        *TIME_TRACKING_TOOLS,
        *WEBHOOK_TOOLS,
        *GOAL_TOOLS,
        *VIEW_TOOLS,
        *CUSTOM_FIELD_TOOLS,
        *FOLDER_TOOLS,
        *DEPENDENCY_TOOLS,
        *DOC_TOOLS
    ]

def get_tool_handler(name: str) -> Optional[Callable]:
    """Get handler for specific tool."""
    handlers = {
        **TASK_TOOL_HANDLERS,
        **LIST_TOOL_HANDLERS,
        **SPACE_TOOL_HANDLERS,
        **TEAM_TOOL_HANDLERS,
        **COMMENT_TOOL_HANDLERS,
        **TIME_TRACKING_TOOL_HANDLERS,
        **WEBHOOK_TOOL_HANDLERS,
        **GOAL_TOOL_HANDLERS,
        **VIEW_TOOL_HANDLERS,
        **CUSTOM_FIELD_TOOL_HANDLERS,
        **FOLDER_TOOL_HANDLERS,
        **DEPENDENCY_TOOL_HANDLERS,
        **DOC_TOOL_HANDLERS
    }
    return handlers.get(name)