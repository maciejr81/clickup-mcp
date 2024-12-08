import unittest
from unittest.mock import Mock, patch
import json

from clickup.tools.tasks import TaskTransformer, handle_create_task  # Adjust imports based on your structure

class TestTaskCreation(unittest.TestCase):
    def setUp(self):
        # Sample ClickUp API response for task creation
        clickup_response_str = '''{
		  "id": "86b33a921",
		  "custom_id": null,
		  "custom_item_id": 0,
		  "name": "New Task Name",
		  "text_content": "Testing API task creation with Claude",
		  "description": "Testing API task creation with Claude",
		  "status": {
		    "id": "p2426624_L3sasdeX",
		    "status": "not started",
		    "color": "#87909e",
		    "orderindex": 0,
		    "type": "open"
		  },
		  "orderindex": "39908591.00000000000000000000000000000000",
		  "date_created": "1733500518926",
		  "date_updated": "1733500518926",
		  "date_closed": null,
		  "date_done": null,
		  "archived": false,
		  "creator": {
		    "id": 1123,
		    "username": "Test",
		    "color": "#1b5e20",
		    "email": "test@test.com,",
		    "profilePicture": "https://attachments.clickup.com/profilePictures/test.jpg"
		  },
		  "assignees": [],
		  "group_assignees": [],
		  "watchers": [],
		  "checklists": [],
		  "tags": [],
		  "parent": null,
		  "top_level_parent": null,
		  "priority": null,
		  "due_date": null,
		  "start_date": null,
		  "points": null,
		  "time_estimate": null,
		  "time_spent": 0,
		  "custom_fields": [],
		  "dependencies": [],
		  "linked_tasks": [],
		  "locations": [],
		  "team_id": "1234",
		  "url": "https://app.clickup.com/t/86b33a921",
		  "sharing": {
		    "public": false,
		    "public_share_expires_on": null,
		    "public_fields": [
		      "assignees",
		      "priority",
		      "due_date",
		      "content",
		      "comments",
		      "attachments",
		      "customFields",
		      "subtasks",
		      "tags",
		      "checklists",
		      "coverimage"
		    ],
		    "token": null,
		    "seo_optimized": false
		  },
		  "permission_level": "create",
		  "list": {
		    "id": "12312",
		    "name": "Lab Inbox",
		    "access": true
		  },
		  "project": {
		    "id": "212",
		    "name": "Lab",
		    "hidden": false,
		    "access": true
		  },
		  "folder": {
		    "id": "213123",
		    "name": "Lab",
		    "hidden": false,
		    "access": true
		  },
		  "space": {
		    "id": "2426624"
		  }
		}'''

        # Parse the JSON string into a Python dict
        self.clickup_response = json.loads(clickup_response_str)
        self.transformer = TaskTransformer()

    @patch('clickup.tools.tasks.TaskAPI')
    async def test_create_task_response_processing(self, mock_api):
        # Setup mock client and response
        mock_client = Mock()
        mock_client.create_task.return_value = self.clickup_response

        # Test arguments
        arguments = {
            "list_id": "12312",
            "name": "New Task Name",
            "text_content": "Testing API task creation with Claude",
            "return_mode": "minimal"
        }

        # Call the handler
        result = await handle_create_task(mock_client, arguments)
        
        # Extract the transformed data from the TextContent response
        transformed_data = json.loads(result[0].text)

        # Assertions for minimal mode
        self.assertEqual(transformed_data["id"], "86b33a921")  # ID should always be present
        self.assertEqual(transformed_data["name"], "New Task Name")
        self.assertEqual(transformed_data["status_status"], "not started")

        # Test important mode
        arguments["return_mode"] = "important"
        result_important = await handle_create_task(mock_client, arguments)
        transformed_data_important = json.loads(result_important[0].text)
        
        # Assertions for important mode
        self.assertEqual(transformed_data_important["id"], "86b33a921")
        self.assertEqual(transformed_data_important["text_content"], "Testing API task creation with Claude")
        
        # Test full mode
        arguments["return_mode"] = "full"
        result_full = await handle_create_task(mock_client, arguments)
        transformed_data_full = json.loads(result_full[0].text)
        
        # Full mode should return the complete response
        self.assertEqual(transformed_data_full, self.clickup_response)

    def test_direct_transformer(self):
        """Test the transformer directly with the response"""
        # Test minimal mode
        minimal_result = self.transformer.transform(self.clickup_response, mode='minimal')
        self.assertEqual(minimal_result["id"], "86b33a921")
        self.assertEqual(minimal_result["name"], "New Task Name")
        self.assertEqual(minimal_result["status_status"], "not started")

        # Test important mode
        important_result = self.transformer.transform(self.clickup_response, mode='important')
        self.assertEqual(important_result["id"], "86b33a921")
        self.assertEqual(important_result["text_content"], "Testing API task creation with Claude")
        
        # Test full mode
        full_result = self.transformer.transform(self.clickup_response, mode='full')
        self.assertEqual(full_result, self.clickup_response)

if __name__ == '__main__':
    unittest.main()