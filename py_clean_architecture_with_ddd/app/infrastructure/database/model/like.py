from tortoise import fields
from tortoise.models import Model

from .comment import CommentModel
from .post import PostModel
from .user import UserModel


class LikeModel(Model):
    id = fields.IntField(pk=True)
    user_id: fields.ForeignKeyRelation[UserModel] | None = fields.ForeignKeyField(
        "models.UserModel", related_name="user_likes", null=True,
    )
    post_id: fields.ForeignKeyRelation[PostModel] | None = fields.ForeignKeyField(
        "models.PostModel", related_name="post_likes", null=True,
    )
    comment_id: fields.ForeignKeyRelation[CommentModel] | None = fields.ForeignKeyField(
        "models.CommentModel", related_name="comment_likes", null=True,
    )
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "likes"
