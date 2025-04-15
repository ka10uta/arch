from tortoise import fields
from tortoise.models import Model

from .post import Post
from .user import User


class Comment(Model):
    id = fields.IntField(pk=True)
    post_id: fields.ForeignKeyRelation[Post] = fields.ForeignKeyField("models.Post", related_name="post_comments")
    user_id: fields.ForeignKeyRelation[User] = fields.ForeignKeyField("models.User", related_name="user_comments")
    parent_comment_id: fields.ForeignKeyRelation["Comment"] | None = fields.ForeignKeyField(
        "models.Comment", related_name="comments", null=True,
    )
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
