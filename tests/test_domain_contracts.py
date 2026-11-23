import pytest
from dataclasses import FrozenInstanceError
from src.domain.contracts import (
    UserRole,
    TaskPriority,
    TaskStatus,
    TaskType,
    create_task,
    transition_task_status,
    log_work_time,
    assign_task,
    is_wip_limit_exceeded,
)


def test_immutability_frozen_task():
    """Проверка строгой иммутабельности: прямая мутация объекта должна вызывать FrozenInstanceError."""
    task = create_task(
        id="t-1",
        issue_key="TP-101",
        project_id="p-1",
        title="Тестовая задача",
        description="Описание",
        task_type=TaskType.FEATURE,
        priority=TaskPriority.HIGH,
        creator_id="u-1",
        estimated_hours=4.0,
    )
    with pytest.raises(FrozenInstanceError):
        task.title = "Измененное название"  # type: ignore


def test_create_task_initial_state():
    """Проверка корректности начального состояния новой задачи."""
    task = create_task(
        id="t-1",
        issue_key="TP-101",
        project_id="p-1",
        title="Авторизация",
        description="JWT Auth",
        task_type=TaskType.FEATURE,
        priority=TaskPriority.CRITICAL,
        creator_id="u-lead",
        estimated_hours=5.0,
    )
    assert task.status == TaskStatus.BACKLOG
    assert task.estimated_minutes == 300
    assert task.spent_minutes == 0
    assert task.remaining_minutes == 300
    assert task.created_at != ""


def test_valid_status_transitions():
    """Проверка стандартного жизненного цикла задачи на доске."""
    task = create_task(
        id="t-1",
        issue_key="TP-101",
        project_id="p-1",
        title="Тест",
        description="Описание",
        task_type=TaskType.TASK,
        priority=TaskPriority.MEDIUM,
        creator_id="u-1",
        estimated_hours=2.0,
    )
    # BACKLOG -> TODO
    t_todo = transition_task_status(task, TaskStatus.TODO, UserRole.DEVELOPER)
    assert t_todo.status == TaskStatus.TODO
    assert task.status == TaskStatus.BACKLOG  # исходный неизменен!

    # TODO -> IN_PROGRESS
    t_prog = transition_task_status(t_todo, TaskStatus.IN_PROGRESS, UserRole.DEVELOPER)
    assert t_prog.status == TaskStatus.IN_PROGRESS

    # IN_PROGRESS -> CODE_REVIEW
    t_rev = transition_task_status(t_prog, TaskStatus.CODE_REVIEW, UserRole.DEVELOPER)
    assert t_rev.status == TaskStatus.CODE_REVIEW

    # CODE_REVIEW -> DONE
    t_done = transition_task_status(t_rev, TaskStatus.DONE, UserRole.TEAM_LEAD)
    assert t_done.status == TaskStatus.DONE


def test_invalid_status_transition_raises_error():
    """Попытка перепрыгнуть статус (Backlog -> Done) вызывает ValueError."""
    task = create_task(
        id="t-1",
        issue_key="TP-101",
        project_id="p-1",
        title="Тест",
        description="",
        task_type=TaskType.BUG,
        priority=TaskPriority.LOW,
        creator_id="u-1",
        estimated_hours=1.0,
    )
    with pytest.raises(ValueError, match="Недопустимый переход статуса"):
        transition_task_status(task, TaskStatus.DONE, UserRole.DEVELOPER)


def test_observer_forbidden_status_transition():
    """Наблюдатель (Observer) не имеет права менять статус задачи."""
    task = create_task(
        id="t-1",
        issue_key="TP-101",
        project_id="p-1",
        title="Тест",
        description="",
        task_type=TaskType.TASK,
        priority=TaskPriority.LOW,
        creator_id="u-1",
        estimated_hours=1.0,
    )
    with pytest.raises(PermissionError, match="Наблюдатель"):
        transition_task_status(task, TaskStatus.TODO, UserRole.OBSERVER)


def test_log_work_time_calculation():
    """Проверка математики списания времени и создания записи аудита."""
    task = create_task(
        id="t-1",
        issue_key="TP-101",
        project_id="p-1",
        title="Разработка API",
        description="",
        task_type=TaskType.FEATURE,
        priority=TaskPriority.HIGH,
        creator_id="u-1",
        estimated_hours=6.0,  # 360 мин
    )
    updated_task, worklog = log_work_time(
        task=task,
        duration_minutes=150,  # 2.5 часа
        user_id="u-dev",
        comment="Написаны контроллеры",
        worklog_id="wl-1",
    )
    assert updated_task.spent_minutes == 150
    assert updated_task.remaining_minutes == 210  # 360 - 150
    assert task.spent_minutes == 0  # Исходный объект остался чистым
    assert worklog.duration_minutes == 150
    assert worklog.task_id == "t-1"


def test_log_work_time_invalid_duration():
    """Списание нулевого или отрицательного времени запрещено."""
    task = create_task("t-1", "TP-1", "p-1", "T", "", TaskType.TASK, TaskPriority.LOW, "u-1", 1.0)
    with pytest.raises(ValueError, match="больше нуля"):
        log_work_time(task, 0, "u-1", "zero", "wl-0")
    with pytest.raises(ValueError, match="больше нуля"):
        log_work_time(task, -10, "u-1", "negative", "wl-neg")


def test_assign_task_rbac():
    """Назначение исполнителя с проверкой прав доступа."""
    task = create_task("t-1", "TP-1", "p-1", "T", "", TaskType.TASK, TaskPriority.LOW, "u-1", 1.0)
    # Наблюдатель не может назначать
    with pytest.raises(PermissionError, match="Наблюдатель"):
        assign_task(task, "u-dev", UserRole.OBSERVER)

    # Тимлид может назначать
    assigned = assign_task(task, "u-dev", UserRole.TEAM_LEAD)
    assert assigned.assignee_id == "u-dev"
    assert task.assignee_id is None  # Исходный объект не мутирован


def test_wip_limit_detection():
    """Проверка детектора превышения лимита незавершенного производства."""
    t1 = create_task("t-1", "TP-1", "p-1", "T1", "", TaskType.TASK, TaskPriority.LOW, "u-1", 1.0)
    t2 = create_task("t-2", "TP-2", "p-1", "T2", "", TaskType.TASK, TaskPriority.LOW, "u-1", 1.0)
    tasks = [t1, t2]

    assert is_wip_limit_exceeded(tasks, limit=2) is True
    assert is_wip_limit_exceeded(tasks, limit=3) is False
    assert is_wip_limit_exceeded(tasks, limit=0) is False
