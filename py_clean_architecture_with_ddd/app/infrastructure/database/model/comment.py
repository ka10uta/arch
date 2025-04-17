from tortoise import fields
from tortoise.models import Model

from .post import PostModel
from .user import UserModel


class CommentModel(Model):
    id = fields.IntField(pk=True)
    post_id: fields.ForeignKeyRelation[PostModel] = fields.ForeignKeyField("models.PostModel", related_name="post_comments")
    user_id: fields.ForeignKeyRelation[UserModel] = fields.ForeignKeyField("models.UserModel", related_name="user_comments")
    parent_comment_id: fields.ForeignKeyRelation["CommentModel"] | None = fields.ForeignKeyField(
        "models.CommentModel", related_name="comments", null=True,
    )
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "comments"
