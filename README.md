# MCP ClickUp Python Server

A Model Context Protocol (MCP) server implementation that provides integration between LLMs and ClickUp. It focuses on using Clickup API endpoints as MCP tools.

## Features

### Return Modes
The server implements a flexible data return system with three modes that control the level of detail in responses:

- **Minimal Mode** - Returns only essential fields (e.g., ID, name, basic status)
- **Important Mode** - Returns key business fields while excluding technical details
- **Full Mode** - Returns complete raw response from ClickUp API

#### Nested Field Handling
The server supports nested field access using dot notation:
- `status.status` - Extracts the status string from status object
- `assignees.email` - Extracts emails from assignee objects
- `tags.name` - Extracts tag names from tag objects

Example transformations:
```json
// Original ClickUp response
{
  "id": "task123",
  "name": "Example Task",
  "status": {
    "status": "in progress",
    "color": "#4169E1"
  },
  "assignees": [
    {"id": 123, "email": "user@example.com"}
  ]
}

// Minimal mode
{
  "id": "task123",
  "name": "Example Task",
  "status_status": "in progress",
  "assignees_email": ["user@example.com"]
}

### Data processing features

* **Automatic Array Handling** - Processes both single items and arrays of items
* **Recursive Processing** - Properly handles nested structures like subtasks
* **ID Preservation** - Maintains critical identifiers across all return modes
* **Type Safety** - Implements type checking and validation
* **Null Safety** - Gracefully handles missing or null fields


## Available tools

### Comments
- **get-comments** - Get comments on a task
- **create-task-comment** - Create a comment on a task

### Custom Fields
- **get-accessible-custom-fields** - Get custom fields accessible in a list
- **set-custom-field-value** - Set custom field value
- **remove-custom-field-value** - Remove custom field value

### Dependencies
- **add-task-dependency** - Add a dependency between tasks
- **remove-task-dependency** - Remove a dependency from a task
- **add-task-link** - Add a link between tasks
- **delete-task-link** - Remove a link between tasks

### Docs
- **search-docs** - Search and filter docs in workspace
- **create-doc** - Create a new doc
- **get-doc** - Get doc details
- **get-doc-pages** - Get all pages in a doc
- **create-page** - Create a new page in a doc
- **get-page** - Get page details
- **edit-page** - Edit/update a page

### Folders
- **update-folder** - Update a folder
- **get-folders** - Get all folders in a space
- **get-folder** - Get a specific folder

### Goals
- **create-goal** - Create a new goal in a team
- **get-goals** - Get goals in a team

### Lists
- **get-lists** - Get all lists in a space
- **create-folderless-list** - Create a list directly in a space without a folder

### Spaces
- **get-spaces** - Get all spaces in a team
- **create-space** - Create a new space in a team

### Tasks
- **create-task** - Create a new task in a list
- **update-task** - Update a task
- **get-task-watchers** - Get watchers of a task
- **add-task-watcher** - Add a watcher to a task
- **get-task-details** - Get detailed information about a specific task
- **get-tasks** - Get tasks from a list
- **create-task-attachment** - Create a task attachment

### Teams
- **get-teams** - Get all accessible teams/workspaces
- **create-team-group** - Create a team (user group)

### Time Tracking
- **get-time-entries** - Get time entries within a date range
- **start-time-entry** - Start time tracking for a task

### Views
- **get-view** - Get view details
- **get-view-tasks** - Get tasks from a view

### Webhooks
- **get-webhooks** - Get webhooks
- **create-webhook** - Create a webhook

---
  
## Prerequisites

- Python 3.10 or higher
- Git
- ClickUp API Token

### Installing Prerequisites

## Installation

1. Clone the repository:
```bash
git clone https://github.com/maciejr81/clickup-mcp
cd clickup-mcp
```

2. Set up the Python environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On MacOS
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install 
```bash
pip install -e .
```


## Configuration

Create a configuration file for Claude Desktop:

```json
{
  "mcpServers": {
    "clickup": {
      "command": "/path/to/your/repo/.venv/bin/python",
      "args": ["-m", "clickup.server"],
      "cwd": "/path/to/your/repo",
      "env": {
        "CLICKUP_API_TOKEN": "your token"
      }
    }
  }
}
```

Place this file at:
- macOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`


## Example prompts

Prompts similar to those will trigger the tool usage:

> List me tasks from the Clickup list `[list id]`, do it in return_mode important

Having the tasks fetched you can reference them by name going forward in the same chat.

> Get the page id from this Clickup url structure 
https://app.clickup.com/[space]/v/dc/[doc id]/[page id] and get the content from it using get-page tool

Will return the content of a Clickup document

Once the initial data is fetched (tasks from a list, links to tasks from a document) a fully natural conversation about the tasks can take place (add a comment to the task '[task name]', update the previous task, move to the task and review the action points, etc.).


## Development

### Running Tests
```bash
# Run all tests
python -m unittest discover -s tests

# Run specific test file
python -m unittest tests/test_task_transformer.py
```

## Debugging

### Debugging MCP servers

Since MCP servers run over `stdio`, debugging can be challenging. For the best debugging experience, we strongly recommend using the [MCP Inspector](https://github.com/modelcontextprotocol/inspector).

You can launch the MCP Inspector via npm with this command:

```bash
npx @modelcontextprotocol/inspector uv --directory /path/to/your server run clickup
```

Upon launching, the Inspector will display a URL that you can access in your browser to begin debugging.

Set the environment variable (`CLICKUP_API_TOKEN`) with the same token value as you added into the `claude_desktop_config.json`. The variable name can be found in the left column of the MCP Inspector.


### Claude Desktop MCP errors logs

Check the files inside when the Claude Desktop app shows MCP connection related errors after start `/Library/Logs/Claude`

## Current limitations

Requires Claude Desktop App when working with Claude.ai (doesn't work in the browser version as of Dec 8, 2024)

## License

MIT License - see LICENSE file for details.

## Acknowledgments

Inspired by https://github.com/noahvanhart/mcp-server-clickup 