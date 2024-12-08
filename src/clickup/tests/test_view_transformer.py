import unittest
from unittest.mock import Mock, patch
import json

from clickup.tools.views import ViewTransformer  # Adjust the import path accordingly

class TestViewTransformer(unittest.TestCase):

    def setUp(self):
        # Sample data provided in the prompt
        self.data = {
            "tasks": [
                {
                    "id": "9hx",
                    "name": "New Task Name",
                    "status": {
                        "status": "Open",
                        "color": "#d3d3d3",
                        "orderindex": 0,
                        "type": "open"
                    },
                    "orderindex": "1.00000000000000000000000000000000",
                    "date_created": "1567780450202",
                    "date_updated": "1567780450202",
                    "date_closed": None,
                    "date_done": None,
                    "creator": {
                        "id": 183,
                        "username": "John Doe",
                        "color": "#827718",
                        "profilePicture": "https://attachments-public.clickup.com/profilePictures/183_abc.jpg"
                    },
                    "assignees": [],
                    "checklists": [],
                    "tags": [],
                    "parent": None,
                    "priority": None,
                    "due_date": None,
                    "start_date": None,
                    "points": 3,
                    "time_estimate": None,
                    "time_spent": None,
                    "custom_fields": {
                        "id": "0a52c486-5f05-403b-b4fd-c512ff05131c",
                        "name": "My Text Custom field",
                        "type": "text",
                        "type_config": {},
                        "date_created": "1622176979540",
                        "hide_from_guests": False,
                        "value": {
                            "value": "This is a string of text added to a Custom Field."
                        },
                        "required": True
                    },
                    "list": {"id": "123"},
                    "folder": {"id": "456"},
                    "space": {"id": "789"},
                    "url": "https://app.clickup.com/t/9hx"
                },
            ],
            "last_page": True
        }
        
        # Instantiate the transformer and set up the data
        self.transformer = ViewTransformer()

    @patch('clickup.tools.views.handle_get_view')  # Adjust the patch path accordingly
    def test_transform_mode_full(self, mock_handle_get_view):
        # Mock handle_get_view to return the expected data for testing
        mock_handle_get_view.return_value = json.dumps(self.data)
        
        # Test the "full" mode, pass entity data as required
        result = self.transformer.transform(self.data, mode='full')
        
        # Assertions to validate the result based on the "full" mode
        self.assertIsNotNone(result)
        # Add more assertions depending on what full mode is supposed to return
        print(result)

    @patch('clickup.tools.views.handle_get_view')
    def test_transform_mode_important(self, mock_handle_get_view):
        # Mock handle_get_view to return the expected data for testing
        mock_handle_get_view.return_value = json.dumps(self.data)
        
        # Test the "important" mode, pass entity data as required
        result = self.transformer.transform(self.data, mode='important')
        
        # Assertions to validate the result based on the "important" mode
        self.assertIsNotNone(result)
        print(result)

    @patch('clickup.tools.views.handle_get_view')
    def test_transform_mode_minimal(self, mock_handle_get_view):
        # Mock handle_get_view to return the expected data for testing
        mock_handle_get_view.return_value = json.dumps(self.data)
        
        # Test the "minimal" mode, pass entity data as required
        result = self.transformer.transform(self.data, mode='minimal')
        
        # Assertions to validate the result based on the "minimal" mode
        self.assertIsNotNone(result)
        print(result)

if __name__ == '__main__':
    unittest.main()
