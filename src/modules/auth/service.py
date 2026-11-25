"""
Сервис аутентификации и авторизации пользователей (RBAC).
"""

from dataclasses import dataclass
from typing import Dict, Optional, Set
import secrets
from src.domain.contracts import User, UserRole
from src.domain.exceptions import AuthenticationError, PermissionDeniedError, ValidationError
from .security import hash_password, verify_password, validate_email_format


@dataclass(frozen=True)
class UserCredentials:
    id: str
    username: str
    email: str
    password_hash: str
    salt: str
    role: UserRole


@dataclass(frozen=True)
class AuthSession:
    token: str
    user_id: str
    username: str
    role: UserRole


class AuthService:
    """Сервис управления пользователями и сессиями аутентификации."""

    def __init__(self):
        # Хранилище учетных записей в памяти (иммутабельный доступ)
        self._users: Dict[str, UserCredentials] = {}
        self._sessions: Dict[str, AuthSession] = {}

    def register_user(
        self,
        user_id: str,
        username: str,
        email: str,
        password: str,
        role: UserRole = UserRole.DEVELOPER
    ) -> User:
        """Регистрирует нового пользователя с хэшированием пароля."""
        if not username or len(username.strip()) < 3:
            raise ValidationError("Имя пользователя должно содержать не менее 3 символов.")

        if not validate_email_format(email):
            raise ValidationError(f"Некорректный адрес электронной почты: {email}")

        if username in self._users:
            raise ValidationError(f"Пользователь с именем '{username}' уже существует.")

        pwd_hash, salt = hash_password(password)

        creds = UserCredentials(
            id=user_id,
            username=username,
            email=email,
            password_hash=pwd_hash,
            salt=salt,
            role=role,
        )
        self._users[username] = creds

        return User(
            id=user_id,
            username=username,
            full_name=username.capitalize(),
            email=email,
            role=role,
        )

    def authenticate(self, username: str, password: str) -> AuthSession:
        """Проверяет учетные данные и генерирует сессионный токен."""
        creds = self._users.get(username)
        if not creds:
            raise AuthenticationError("Пользователь с указанным логином не найден.")

        if not verify_password(password, creds.password_hash, creds.salt):
            raise AuthenticationError("Неверный пароль пользователя.")

        token = secrets.token_hex(24)
        session = AuthSession(
            token=token,
            user_id=creds.id,
            username=creds.username,
            role=creds.role,
        )
        self._sessions[token] = session
        return session

    def verify_role_access(self, role: UserRole, allowed_roles: Set[UserRole]) -> None:
        """Проверяет соответствие роли запрашиваемому уровню доступа."""
        if role not in allowed_roles:
            raise PermissionDeniedError(
                f"Доступ запрещен для роли {role.value}. Требуется одна из: {[r.value for r in allowed_roles]}"
            )
