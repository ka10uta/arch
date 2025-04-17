from app.domain.exceptions import InvalidValueObjectError


class InvalidEmailError(InvalidValueObjectError):
    """メールアドレスの形式が無効な場合の例外"""

    def __init__(self, email: str) -> None:
        super().__init__(f"Invalid email format: {email}")


class InvalidUserNameError(InvalidValueObjectError):
    """ユーザー名が無効な場合の例外"""

    def __init__(self, name: str) -> None:
        super().__init__(f"Invalid username: {name}")
