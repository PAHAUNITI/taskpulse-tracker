"""
Аналитические утилиты для расчета трудозатрат и метрик прогресса.
"""

from typing import List
from src.domain.contracts import Worklog


def calculate_task_progress(spent_minutes: int, estimated_minutes: int) -> float:
    """
    Рассчитывает процент выработки задачи.
    
    Returns:
        Процент выполнения от 0.0 до 100.0 (с округлением до 1 знака).
    """
    if estimated_minutes <= 0:
        return 0.0
    progress = (spent_minutes / estimated_minutes) * 100.0
    return round(min(100.0, max(0.0, progress)), 1)


def calculate_user_total_hours(worklogs: List[Worklog], user_id: str) -> float:
    """Суммирует все списанные часы указанного пользователя."""
    total_minutes = sum(w.duration_minutes for w in worklogs if w.user_id == user_id)
    return round(total_minutes / 60.0, 2)
