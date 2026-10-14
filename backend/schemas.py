import re

from pydantic import BaseModel, field_validator


def check_password_strength(password: str) -> None:
    errors = []

    if len(password) < 8:
        errors.append("минимум 8 символов")
    if not re.search(r"[A-Z]", password):
        errors.append("хотя бы одна заглавная буква")
    if not re.search(r"[a-z]", password):
        errors.append("хотя бы одна строчная буква")
    if not re.search(r"\d", password):
        errors.append("хотя бы одна цифра")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=]", password):
        errors.append("хотя бы один спецсимвол")

    if errors:
        raise ValueError("Пароль слишком простой. Нужно: " + ", ".join(errors))


class UserCreate(BaseModel):
    username: str
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, v):
            raise ValueError("Введите корректный email (например: name@example.com)")
        return v.lower()

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        check_password_strength(value)
        return value


class UserRead(BaseModel):
    id: int
    email: str
    is_active: bool

    class Config:
        from_attributes = True
