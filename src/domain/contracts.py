"""
Domain Data Contracts and Immutable Entities for TaskPulse.
Enforces strict immutability (frozen dataclasses) and Pure Functions (ECC Standard).
"""

from dataclasses import dataclass, replace
from enum import Enum
from typing import Optional
from datetime import datetime, timezone


class UserRole(str, Enum):
    """Роли пользователей в соответствии с RBAC-матрицей."""
    ADMINISTRATOR = "ADMINISTRATOR"
    TEAM_LEAD = "TEAM_LEAD"
    DEVELOPER = "DEVELOPER"
    OBSERVER = "OBSERVER"


class TaskPriority(str, Enum):
    """Приоритеты задач."""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class TaskStatus(str, Enum):
    """Статусы жизненного цикла задачи на Kanban-доске."""
    BACKLOG = "BACKLOG"
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    CODE_REVIEW = "CODE_REVIEW"
    DONE = "DONE"


class TaskType(str, Enum):
    """Типы задач."""
    FEATURE = "FEATURE"
    BUG = "BUG"
    REFACTOR = "REFACTOR"
    TASK = "TASK"


class SprintStatus(str, Enum):
    """Статусы итераций (спринтов)."""
    PLANNING = "PLANNING"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"


# Разрешенные переходы статусов задач
VALID_STATUS_TRANSITIONS: dict[TaskStatus, set[TaskStatus]] = {
    TaskStatus.BACKLOG: {TaskStatus.TODO},
    TaskStatus.TODO: {TaskStatus.IN_PROGRESS, TaskStatus.BACKLOG},
    TaskStatus.IN_PROGRESS: {TaskStatus.CODE_REVIEW, TaskStatus.TODO},
    TaskStatus.CODE_REVIEW: {TaskStatus.DONE, TaskStatus.IN_PROGRESS},
    TaskStatus.DONE: {TaskStatus.IN_PROGRESS},  # Reopen в случае дефекта
}


@dataclass(frozen=True)
class User:
    """Иммутабельная сущность пользователя."""
    id: str
    username: str
    full_name: str
    email: str
    role: UserRole
    weekly_capacity_hours: int = 40
    is_active: bool = True


@dataclass(frozen=True)
class Task:
    """Иммутабельная сущность задачи (тикета)."""
    id: str
    issue_key: str  # например, TP-104
    project_id: str
    title: str
    description: str
    task_type: TaskType
    priority: TaskPriority
    status: TaskStatus
    creator_id: str
    assignee_id: Optional[str] = None
    sprint_id: Optional[str] = None
    estimated_minutes: int = 0
    spent_minutes: int = 0
    remaining_minutes: int = 0
    created_at: str = ""


@dataclass(frozen=True)
class Worklog:
    """Иммутабельная запись о списании рабочего времени."""
    id: str
    task_id: str
    user_id: str
    duration_minutes: int
    comment: str
    logged_at: str


@dataclass(frozen=True)
class Sprint:
    """Иммутабельная сущность спринта."""
    id: str
    project_id: str
    name: str
    goal: str
    status: SprintStatus
    start_date: str
    end_date: str
    capacity_hours: int


# ================= Pure Immutable Functions =================

def create_task(
    id: str,
    issue_key: str,
    project_id: str,
    title: str,
    description: str,
    task_type: TaskType,
    priority: TaskPriority,
    creator_id: str,
    estimated_hours: float,
    assignee_id: Optional[str] = None,
    sprint_id: Optional[str] = None,
) -> Task:
    """Создает новую задачу с начальным статусом BACKLOG."""
    est_minutes = int(estimated_hours * 60)
    now_iso = datetime.now(timezone.utc).isoformat()
    return Task(
        id=id,
        issue_key=issue_key,
        project_id=project_id,
        title=title,
        description=description,
        task_type=task_type,
        priority=priority,
        status=TaskStatus.BACKLOG,
        creator_id=creator_id,
        assignee_id=assignee_id,
        sprint_id=sprint_id,
        estimated_minutes=est_minutes,
        spent_minutes=0,
        remaining_minutes=est_minutes,
        created_at=now_iso,
    )


def transition_task_status(task: Task, new_status: TaskStatus, actor_role: UserRole) -> Task:
    """
    Выполняет переход задачи в новый статус с валидацией RBAC и допустимых переходов.
    Возвращает НОВЫЙ экземпляр Task без мутации исходного.
    """
    if actor_role == UserRole.OBSERVER:
        raise PermissionError("Наблюдатель (Observer) не имеет прав на смену статуса задачи.")

    if task.status == new_status:
        return task

    allowed = VALID_STATUS_TRANSITIONS.get(task.status, set())
    if new_status not in allowed:
        raise ValueError(f"Недопустимый переход статуса: {task.status.value} -> {new_status.value}")

    return replace(task, status=new_status)


def log_work_time(
    task: Task,
    duration_minutes: int,
    user_id: str,
    comment: str,
    worklog_id: str
) -> tuple[Task, Worklog]:
    """
    Списывает рабочее время. Возвращает кортеж (новый Task, новый Worklog).
    Гарантирует пересчет spent_minutes и remaining_minutes.
    """
    if duration_minutes <= 0:
        raise ValueError("Длительность списания времени должна быть строго больше нуля.")

    new_spent = task.spent_minutes + duration_minutes
    new_remaining = max(0, task.remaining_minutes - duration_minutes)

    updated_task = replace(task, spent_minutes=new_spent, remaining_minutes=new_remaining)

    log = Worklog(
        id=worklog_id,
        task_id=task.id,
        user_id=user_id,
        duration_minutes=duration_minutes,
        comment=comment,
        logged_at=datetime.now(timezone.utc).isoformat(),
    )

    return updated_task, log


def assign_task(task: Task, assignee_id: Optional[str], actor_role: UserRole) -> Task:
    """Назначает исполнителя задачи с проверкой прав доступа."""
    if actor_role == UserRole.OBSERVER:
        raise PermissionError("Наблюдатель не имеет прав на назначение исполнителей.")
    return replace(task, assignee_id=assignee_id)


def is_wip_limit_exceeded(tasks_in_status: list[Task], limit: int) -> bool:
    """Проверяет соблюдение WIP-лимита для колонки доски."""
    if limit <= 0:
        return False
    return len(tasks_in_status) >= limit
