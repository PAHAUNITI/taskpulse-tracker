"""
Утилиты криптографической безопасности и валидации модуля аутентификации.
"""

import hashlib
import os
import re
import secrets
from typing import Tuple


def hash_password(password: str, iterations: int = 100000) -> Tuple[str, str]:
    """
    Формирует криптостойкий хэш пароля с использованием алгоритма PBKDF2-HMAC-SHA256 и случайной соли.
    
    Args:
        password: Сырой пароль пользователя.
        iterations: Число итераций хэширования.
        
    Returns:
        Кортеж (хэш_пароля_hex, соль_hex).
    """
    if len(password) < 6:
        raise ValueError("Пароль должен содержать не менее 6 символов.")
    
    salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
    return key.hex(), salt.hex()


def verify_password(password: str, password_hash_hex: str, salt_hex: str, iterations: int = 100000) -> bool:
    """
    Проверяет пароль на соответствие сохраненному хэшу с постоянным временем сравнения (anti-timing attack).
    """
    try:
        salt = bytes.fromhex(salt_hex)
        key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)
        return secrets.compare_digest(key.hex(), password_hash_hex)
    except Exception:
        return False


def validate_email_format(email: str) -> bool:
    """Проверяет корректность формата адреса электронной почты."""
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(pattern, email.strip()))
