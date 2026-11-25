"""
Иерархия доменных исключений программной системы «TaskPulse».
"""

class DomainError(Exception):
    """Базовый класс для всех доменных исключений системы."""
    pass


class ValidationError(DomainError):
    """Ошибка валидации входных данных."""
    pass


class AuthenticationError(DomainError):
    """Ошибка аутентификации (неверный логин/пароль)."""
    pass


class PermissionDeniedError(DomainError):
    """Нарушение прав ролевой модели доступа (RBAC)."""
    pass


class WipLimitExceededError(DomainError):
    """Превышение лимита незавершенного производства (WIP-лимит)."""
    pass


class InvalidStatusTransitionError(DomainError):
    """Попытка недопустимого перехода статуса в воркфлоу задачи."""
    pass
