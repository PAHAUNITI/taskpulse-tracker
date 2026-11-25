"""
Модульные и интеграционные тесты программных модулей Дня 4 (TaskPulse).
Проверяет позитивные и негативные сценарии модулей Auth, Tasks и TimeTracking.
"""

import pytest
from src.domain.contracts import TaskPriority, TaskStatus, TaskType, UserRole
from src.domain.exceptions import (
    AuthenticationError,
    InvalidStatusTransitionError,
    PermissionDeniedError,
    ValidationError,
    WipLimitExceededError,
)
from src.modules.auth import AuthService
from src.modules.tasks import TaskService
from src.modules.time_tracking import TimeTrackingService, calculate_task_progress


def test_auth_successful_registration_and_login():
    """Проверка 1: Корректная регистрация и вход пользователя."""
    auth = AuthService()
    user = auth.register_user("u1", "ivan_dev", "ivan@taskpulse.io", "strongPass123", UserRole.DEVELOPER)
    assert user.username == "ivan_dev"
    assert user.role == UserRole.DEVELOPER

    session = auth.authenticate("ivan_dev", "strongPass123")
    assert session.token != ""
    assert session.username == "ivan_dev"


def test_auth_invalid_password_rejection():
    """Проверка 2: Отказ в авторизации при вводе неверного пароля."""
    auth = AuthService()
    auth.register_user("u1", "ivan_dev", "ivan@taskpulse.io", "strongPass123", UserRole.DEVELOPER)

    with pytest.raises(AuthenticationError, match="Неверный пароль"):
        auth.authenticate("ivan_dev", "wrongPassword")


def test_auth_invalid_email_format():
    """Проверка 3: Ошибка валидации некорректного email."""
    auth = AuthService()
    with pytest.raises(ValidationError, match="Некорректный адрес"):
        auth.register_user("u2", "user2", "invalid-email-format", "pass123")


def test_task_creation_and_lifecycle():
    """Проверка 4: Создание тикета и корректная смена статусов."""
    tasks = TaskService()
    task = tasks.create_task(
        project_id="p1",
        title="Модуль аналитики",
        description="Разработать расчет метрик",
        priority=TaskPriority.HIGH,
        task_type=TaskType.FEATURE,
        estimated_hours=4.0,
        creator_id="u1",
        actor_role=UserRole.DEVELOPER,
    )
    assert task.issue_key == "TP-101"
    assert task.status == TaskStatus.BACKLOG

    t_todo = tasks.move_task_status(task.id, TaskStatus.TODO, UserRole.DEVELOPER)
    assert t_todo.status == TaskStatus.TODO

    t_prog = tasks.move_task_status(task.id, TaskStatus.IN_PROGRESS, UserRole.DEVELOPER)
    assert t_prog.status == TaskStatus.IN_PROGRESS


def test_task_invalid_transition_rejection():
    """Проверка 5: Запрет недопустимого перехода статуса (скачок Backlog -> Done)."""
    tasks = TaskService()
    task = tasks.create_task("p1", "Задача", "", TaskPriority.LOW, TaskType.TASK, 2.0, "u1", UserRole.DEVELOPER)

    with pytest.raises(InvalidStatusTransitionError, match="Недопустимый переход"):
        tasks.move_task_status(task.id, TaskStatus.DONE, UserRole.DEVELOPER)


def test_task_wip_limit_enforcement():
    """Проверка 6: Превышение WIP-лимита блокирует добавление лишних задач в работу."""
    tasks = TaskService()
    tasks.set_wip_limit(TaskStatus.IN_PROGRESS, limit=2, actor_role=UserRole.TEAM_LEAD)

    # Создаем 3 задачи и переводим в TODO
    t1 = tasks.create_task("p1", "Задача 1", "", TaskPriority.LOW, TaskType.TASK, 1.0, "u1", UserRole.DEVELOPER)
    t2 = tasks.create_task("p1", "Задача 2", "", TaskPriority.LOW, TaskType.TASK, 1.0, "u1", UserRole.DEVELOPER)
    t3 = tasks.create_task("p1", "Задача 3", "", TaskPriority.LOW, TaskType.TASK, 1.0, "u1", UserRole.DEVELOPER)

    tasks.move_task_status(t1.id, TaskStatus.TODO, UserRole.DEVELOPER)
    tasks.move_task_status(t2.id, TaskStatus.TODO, UserRole.DEVELOPER)
    tasks.move_task_status(t3.id, TaskStatus.TODO, UserRole.DEVELOPER)

    # Первые две задачи успешно входят в работу
    tasks.move_task_status(t1.id, TaskStatus.IN_PROGRESS, UserRole.DEVELOPER)
    tasks.move_task_status(t2.id, TaskStatus.IN_PROGRESS, UserRole.DEVELOPER)

    # Третья задача превышает лимит (2) -> WipLimitExceededError
    with pytest.raises(WipLimitExceededError, match="Превышен WIP-лимит"):
        tasks.move_task_status(t3.id, TaskStatus.IN_PROGRESS, UserRole.DEVELOPER)


def test_observer_rbac_permission_denied():
    """Проверка 7: Запрет модификации данных для роли Наблюдателя (Observer)."""
    tasks = TaskService()
    with pytest.raises(PermissionDeniedError, match="Наблюдатель не имеет прав"):
        tasks.create_task("p1", "Задача", "", TaskPriority.LOW, TaskType.TASK, 1.0, "obs1", UserRole.OBSERVER)


def test_time_tracking_worklog_and_progress():
    """Проверка 8: Корректность списания времени и пересчета остатка/прогресса."""
    tasks = TaskService()
    time_svc = TimeTrackingService(tasks)

    task = tasks.create_task("p1", "Верстка", "", TaskPriority.MEDIUM, TaskType.TASK, 5.0, "u1", UserRole.DEVELOPER)
    # 5 часов = 300 минут

    wl = time_svc.log_work(task.id, duration_minutes=120, user_id="u1", comment="Сверстал шапку", actor_role=UserRole.DEVELOPER)
    assert wl.duration_minutes == 120

    updated_task = tasks.get_task(task.id)
    assert updated_task.spent_minutes == 120
    assert updated_task.remaining_minutes == 180  # 300 - 120

    progress = calculate_task_progress(updated_task.spent_minutes, updated_task.estimated_minutes)
    assert progress == 40.0  # 120 / 300 * 100%


def test_time_tracking_invalid_duration_rejection():
    """Проверка 9: Отказ при попытке списать отрицательное время."""
    tasks = TaskService()
    time_svc = TimeTrackingService(tasks)
    task = tasks.create_task("p1", "Тест", "", TaskPriority.LOW, TaskType.TASK, 1.0, "u1", UserRole.DEVELOPER)

    with pytest.raises(ValidationError, match="строго больше 0 минут"):
        time_svc.log_work(task.id, -30, "u1", "err", UserRole.DEVELOPER)
