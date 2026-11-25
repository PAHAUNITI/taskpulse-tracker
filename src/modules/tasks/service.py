"""
Сервис управления задачами (Task & Kanban Engine).
"""

from typing import Dict, List, Optional
from src.domain.contracts import (
    Task,
    TaskPriority,
    TaskStatus,
    TaskType,
    UserRole,
    VALID_STATUS_TRANSITIONS,
    create_task as create_domain_task,
)
from src.domain.exceptions import (
    InvalidStatusTransitionError,
    PermissionDeniedError,
    ValidationError,
    WipLimitExceededError,
)
from .validation import validate_task_input


class TaskService:
    """Сервис управления жизненным циклом задач и канбан-доски."""

    def __init__(self):
        self._tasks: Dict[str, Task] = {}
        self._task_counter: int = 100
        self._wip_limits: Dict[TaskStatus, int] = {
            TaskStatus.IN_PROGRESS: 3,
            TaskStatus.CODE_REVIEW: 2,
        }

    def set_wip_limit(self, status: TaskStatus, limit: int, actor_role: UserRole) -> None:
        """Устанавливает лимит незавершенного производства (только Тимлид)."""
        if actor_role != UserRole.TEAM_LEAD and actor_role != UserRole.ADMINISTRATOR:
            raise PermissionDeniedError("Установка WIP-лимитов разрешена только Тимлиду.")
        if limit < 0:
            raise ValidationError("WIP-лимит не может быть отрицательным.")
        self._wip_limits[status] = limit

    def create_task(
        self,
        project_id: str,
        title: str,
        description: str,
        priority: TaskPriority,
        task_type: TaskType,
        estimated_hours: float,
        creator_id: str,
        actor_role: UserRole
    ) -> Task:
        """Создает задачу в бэклоге с автогенерацией уникального ключа TP-XXX."""
        if actor_role == UserRole.OBSERVER:
            raise PermissionDeniedError("Наблюдатель не имеет прав на создание задач.")

        validate_task_input(title, estimated_hours)

        self._task_counter += 1
        issue_key = f"TP-{self._task_counter}"
        task_id = f"task_{self._task_counter}"

        task = create_domain_task(
            id=task_id,
            issue_key=issue_key,
            project_id=project_id,
            title=title.strip(),
            description=description,
            task_type=task_type,
            priority=priority,
            creator_id=creator_id,
            estimated_hours=estimated_hours,
        )
        self._tasks[task_id] = task
        return task

    def get_task(self, task_id: str) -> Task:
        """Возвращает задачу по ID."""
        task = self._tasks.get(task_id)
        if not task:
            raise ValidationError(f"Задача с идентификатором '{task_id}' не найдена.")
        return task

    def get_tasks_by_status(self, status: TaskStatus) -> List[Task]:
        """Возвращает список задач в определенном статусе."""
        return [t for t in self._tasks.values() if t.status == status]

    def move_task_status(self, task_id: str, new_status: TaskStatus, actor_role: UserRole) -> Task:
        """Перемещает карточку задачи с проверкой допустимых переходов и WIP-лимитов."""
        if actor_role == UserRole.OBSERVER:
            raise PermissionDeniedError("Наблюдатель не имеет прав на смену статуса задачи.")

        task = self.get_task(task_id)
        if task.status == new_status:
            return task

        allowed = VALID_STATUS_TRANSITIONS.get(task.status, set())
        if new_status not in allowed:
            raise InvalidStatusTransitionError(
                f"Недопустимый переход из '{task.status.value}' в '{new_status.value}'."
            )

        # Проверка WIP-лимита
        limit = self._wip_limits.get(new_status, 0)
        if limit > 0:
            current_count = len(self.get_tasks_by_status(new_status))
            if current_count >= limit:
                raise WipLimitExceededError(
                    f"Превышен WIP-лимит для колонки '{new_status.value}' (лимит: {limit}, текущих задач: {current_count})."
                )

        from dataclasses import replace
        updated = replace(task, status=new_status)
        self._tasks[task_id] = updated
        return updated

    def assign_task(self, task_id: str, assignee_id: Optional[str], actor_role: UserRole) -> Task:
        """Назначает исполнителя задачи."""
        if actor_role == UserRole.OBSERVER:
            raise PermissionDeniedError("Наблюдатель не имеет прав на назначение исполнителя.")
        task = self.get_task(task_id)
        from dataclasses import replace
        updated = replace(task, assignee_id=assignee_id)
        self._tasks[task_id] = updated
        return updated
