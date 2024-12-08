from enum import Enum
from typing import Any, Dict, TypeVar, Generic, Union, Type

T = TypeVar('T')

class ReturnMode(Enum):
    MINIMAL = "minimal"  # Current behavior
    IMPORTANT = "important"  # Additional important fields
    FULL = "full"  # Raw API response
    
    @classmethod
    def from_str(cls, mode: str):
        try:
            return cls[mode.upper()]
        except KeyError:
            raise ValueError(f"Invalid mode: {mode}")

class BaseTransformer:
    @classmethod
    def transform(cls, entity, mode: ReturnMode):
        """Transform method that works with both class and instance method get_fields implementations."""
        if isinstance(mode, str):
            mode = ReturnMode.from_str(mode)
            
        if mode == ReturnMode.FULL:
            return entity

        # Handle different response structures
        if isinstance(entity, dict):
            # Check if this is a wrapper containing a tasks array
            if "tasks" in entity and isinstance(entity["tasks"], list):
                return [cls._transform_single_entity(task, mode) for task in entity["tasks"]]
            # Single task/entity case
            return cls._transform_single_entity(entity, mode)
        # Direct array case
        elif isinstance(entity, list):
            return [cls._transform_single_entity(item, mode) for item in entity]
            
        return cls._transform_single_entity(entity, mode)

    @classmethod
    def _transform_single_entity(cls, entity, mode: ReturnMode):
        """Transform a single entity based on the mode."""
        if not isinstance(entity, dict):
            return entity

        if isinstance(cls, type):
            fields = cls.get_fields(mode)
        else:
            fields = cls.get_fields(self, mode)
            
        transformed_entity = {}

        for field in fields:
            if '.' in field:
                # Handle nested field (e.g., "status.status")
                parent_key, child_key = field.split('.', 1)
                parent_value = entity.get(parent_key)
                
                if isinstance(parent_value, list):
                    # Handle array of objects (e.g., assignees array)
                    values = [
                        item.get(child_key) 
                        for item in parent_value 
                        if isinstance(item, dict)
                    ]
                    transformed_entity[f"{parent_key}_{child_key}"] = values if values else None
                elif isinstance(parent_value, dict):
                    # Handle nested object (e.g., status object)
                    transformed_entity[f"{parent_key}_{child_key}"] = parent_value.get(child_key)
                else:
                    transformed_entity[f"{parent_key}_{child_key}"] = None
            else:
                transformed_entity[field] = entity.get(field)

        return transformed_entity
                
# Schema parts that are commonly used across tools
return_mode_schema = {
    "return_mode": {
        "type": "string",
        "enum": ["minimal", "important", "full"],
        "description": "Control amount of data returned",
        "optional": True
    }
}