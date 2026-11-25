"""
Валидаторы входных данных для сущности Task.
"""

from src.domain.exceptions import ValidationError


def validate_task_input(title: str, estimated_hours: float) -> None:
    """Проверяет корректность названия и оценки трудоемкости задачи."""
    if not title or len(title.strip()) < 3:
        raise ValidationError("Название задачи должно содержать минимум 3 символа.")
    
    if len(title.strip()) > 200:
        raise ValidationError("Название задачи не должно превышать 200 символов.")

    if estimated_hours <= 0:
        raise ValidationError("Оценка трудоемкости задачи должна быть строго больше нуля.")

    if estimated_hours > 1000:
        raise ValidationError("Слишком большая оценка трудоемкости (максимум 1000 часов).")
