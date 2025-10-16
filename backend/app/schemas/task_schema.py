"""
Task Schema for validation and serialization
"""
from marshmallow import Schema, fields, validate, validates, ValidationError


class TaskSchema(Schema):
    """
    Schema for task validation and serialization
    """
    id = fields.Int(dump_only=True)
    title = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=200, error="Title must be between 1 and 200 characters")
    )
    description = fields.Str(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    comments_count = fields.Int(dump_only=True)
    
    @validates('title')
    def validate_title(self, value):
        """
        Validate that title is not just whitespace
        
        Args:
            value: Title string to validate
            
        Raises:
            ValidationError: If title is empty or whitespace only
        """
        if not value or not value.strip():
            raise ValidationError("Title cannot be empty or whitespace only")


class TaskUpdateSchema(Schema):
    """
    Schema for updating existing tasks
    All fields are optional for partial updates
    """
    title = fields.Str(
        validate=validate.Length(min=1, max=200, error="Title must be between 1 and 200 characters")
    )
    description = fields.Str(allow_none=True)
    
    @validates('title')
    def validate_title(self, value):
        """Validate title is not whitespace only"""
        if value is not None and (not value or not value.strip()):
            raise ValidationError("Title cannot be empty or whitespace only")


# Schema instances
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
task_update_schema = TaskUpdateSchema()
