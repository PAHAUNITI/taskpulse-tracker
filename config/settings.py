"""
Application Configuration Settings for TaskPulse.
Stores environment-driven configurations and defaults.
"""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    app_name: str = "TaskPulse"
    app_version: str = "1.0.0"
    environment: str = "development"
    database_url: str = "sqlite:///taskpulse.db"
    jwt_secret: str = "insecure-default-change-in-production"
    jwt_expiry_minutes: int = 1440  # 24 часа
    wip_limit_default: int = 3
    password_salt_rounds: int = 100000


def load_config() -> AppConfig:
    """Загружает конфигурацию из переменных окружения с безопасными значениями по умолчанию."""
    return AppConfig(
        app_name=os.getenv("APP_NAME", "TaskPulse"),
        app_version=os.getenv("APP_VERSION", "1.0.0"),
        environment=os.getenv("NODE_ENV", "development"),
        database_url=os.getenv("DATABASE_URL", "sqlite:///taskpulse.db"),
        jwt_secret=os.getenv("JWT_SECRET", "taskpulse-dev-secret-key-123"),
        jwt_expiry_minutes=int(os.getenv("JWT_EXPIRY_MINUTES", "1440")),
        wip_limit_default=int(os.getenv("WIP_LIMIT_DEFAULT", "3")),
    )
