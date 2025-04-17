from tortoise import fields
from tortoise.models import Model


class UserModel(Model):
    id = fields.CharField(pk=True, max_length=36)  # UUIDを文字列として保存
    name = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "users"

    def __str__(self) -> str:
        return f"{self.name} <{self.email}>"
