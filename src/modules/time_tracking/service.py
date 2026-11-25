"""
Сервис учета трудозатрат и регистрации рабочего времени (Time Tracking & Worklog Service).
"""

from typing import Dict, List
import uuid
from src.domain.contracts import UserRole, Worklog
from src.domain.exceptions import PermissionDeniedError, ValidationError
from src.modules.tasks.service import TaskService


class TimeTrackingService:
    """Сервис регистрации списания времени по задачам."""

    def __init__(self, task_service: TaskService):
        self._task_service = task_service
        self._worklogs: Dict[str, Worklog] = {}

    def log_work(
        self,
        task_id: str,
        duration_minutes: int,
        user_id: str,
        comment: str,
        actor_role: UserRole
    ) -> Worklog:
        """
        Регистрирует затраченное рабочее время и обновляет счетчики задачи.
        """
        if actor_role == UserRole.OBSERVER:
            raise PermissionDeniedError("Наблюдатель не имеет прав на списание рабочего времени.")

        if duration_minutes <= 0:
            raise ValidationError("Длительность списания должна быть строго больше 0 минут.")

        if duration_minutes > 1440:  # максимум 24 часа за одно списание
            raise ValidationError("Нельзя списать более 24 часов за одну запись.")

        # Получаем задачу и пересчитываем агрегаты
        task = self._task_service.get_task(task_id)

        from src.domain.contracts import log_work_time
        worklog_id = f"wl_{uuid.uuid4().hex[:8]}"

        updated_task, worklog = log_work_time(
            task=task,
            duration_minutes=duration_minutes,
            user_id=user_id,
            comment=comment.strip() if comment else "Без комментария",
            worklog_id=worklog_id,
        )

        # Сохраняем обновленную задачу в TaskService
        self._task_service._tasks[task_id] = updated_task
        self._worklogs[worklog_id] = worklog

        return worklog

    def get_worklogs_by_task(self, task_id: str) -> List[Worklog]:
        """Возвращает все списания времени по конкретной задаче."""
        return [w for w in self._worklogs.values() if w.task_id == task_id]

    def get_worklogs_by_user(self, user_id: str) -> List[Worklog]:
        """Возвращает все списания времени конкретного сотрудника."""
        return [w for w in self._worklogs.values() if w.user_id == user_id]
