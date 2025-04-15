from tortoise import fields
from tortoise.models import Model

from .user import User


class Post(Model):
    id = fields.IntField(pk=True)
    user_id: fields.ForeignKeyRelation[User] = fields.ForeignKeyField("models.User", related_name="user_posts")
    title = fields.CharField(max_length=255)
    content = fields.TextField()
    is_published = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
