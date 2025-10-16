"""
Comment Schema for validation and serialization
Uses Marshmallow for data validation
"""
from marshmallow import Schema, fields, validate, validates, ValidationError


class CommentSchema(Schema):
    """
    Schema for comment validation and serialization
    """
    id = fields.Int(dump_only=True)
    task_id = fields.Int(required=True, validate=validate.Range(min=1))
    content = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=2000, error="Content must be between 1 and 2000 characters")
    )
    author = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100, error="Author name must be between 1 and 100 characters")
    )
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    @validates('content')
    def validate_content(self, value):
        """
        Validate that content is not just whitespace
        
        Args:
            value: Content string to validate
            
        Raises:
            ValidationError: If content is empty or whitespace only
        """
        if not value or not value.strip():
            raise ValidationError("Content cannot be empty or whitespace only")
    
    @validates('author')
    def validate_author(self, value):
        """
        Validate that author is not just whitespace
        
        Args:
            value: Author string to validate
            
        Raises:
            ValidationError: If author is empty or whitespace only
        """
        if not value or not value.strip():
            raise ValidationError("Author cannot be empty or whitespace only")


class CommentUpdateSchema(Schema):
    """
    Schema for updating existing comments
    All fields are optional for partial updates
    """
    content = fields.Str(
        validate=validate.Length(min=1, max=2000, error="Content must be between 1 and 2000 characters")
    )
    author = fields.Str(
        validate=validate.Length(min=1, max=100, error="Author name must be between 1 and 100 characters")
    )
    
    @validates('content')
    def validate_content(self, value):
        """Validate content is not whitespace only"""
        if value is not None and (not value or not value.strip()):
            raise ValidationError("Content cannot be empty or whitespace only")
    
    @validates('author')
    def validate_author(self, value):
        """Validate author is not whitespace only"""
        if value is not None and (not value or not value.strip()):
            raise ValidationError("Author cannot be empty or whitespace only")


# Schema instances
comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)
comment_update_schema = CommentUpdateSchema()
