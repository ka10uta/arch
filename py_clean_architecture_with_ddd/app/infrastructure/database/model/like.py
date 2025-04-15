from tortoise import fields
from tortoise.models import Model

from .comment import Comment
from .post import Post
from .user import User


class Like(Model):
    id = fields.IntField(pk=True)
    user_id: fields.ForeignKeyRelation[User] | None = fields.ForeignKeyField(
        "models.User", related_name="user_likes", null=True,
    )
    post_id: fields.ForeignKeyRelation[Post] | None = fields.ForeignKeyField(
        "models.Post", related_name="post_likes", null=True,
    )
    comment_id: fields.ForeignKeyRelation[Comment] | None = fields.ForeignKeyField(
        "models.Comment", related_name="comment_likes", null=True,
    )
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
