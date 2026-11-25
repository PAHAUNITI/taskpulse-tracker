"""
Точка входа и демонстрационный запуск программных модулей «TaskPulse».
Демонстрирует сквозное взаимодействие модулей Auth, Tasks и TimeTracking.
"""

from src.domain.contracts import TaskPriority, TaskStatus, TaskType, UserRole
from src.modules.auth import AuthService
from src.modules.tasks import TaskService
from src.modules.time_tracking import TimeTrackingService, calculate_task_progress


def run_demo():
    print("=" * 70)
    print("🚀 Запуск демонстрационной среды программных модулей «TaskPulse»")
    print("=" * 70)

    # 1. Инициализация сервисов
    auth_service = AuthService()
    task_service = TaskService()
    time_service = TimeTrackingService(task_service)

    # 2. Модуль 1: Регистрация и аутентификация
    print("\n[1] Модуль аутентификации (Auth Module):")
    dev_user = auth_service.register_user(
        user_id="usr_dev_1",
        username="pavel_dev",
        email="pavel@taskpulse.io",
        password="securePassword123!",
        role=UserRole.DEVELOPER
    )
    print(f"  ✓ Зарегистрирован пользователь: {dev_user.username} (Роль: {dev_user.role.value})")

    session = auth_service.authenticate("pavel_dev", "securePassword123!")
    print(f"  ✓ Успешная авторизация! Выдан сессионный токен: {session.token[:12]}...")

    # 3. Модуль 2: Управление задачами (Task & Kanban Module)
    print("\n[2] Модуль управления задачами (Task & Kanban Module):")
    task = task_service.create_task(
        project_id="proj_alpha",
        title="Разработка JWT провайдера и middleware безопасности",
        description="Реализовать валидацию HttpOnly куки и проверку RBAC",
        priority=TaskPriority.HIGH,
        task_type=TaskType.FEATURE,
        estimated_hours=6.0,
        creator_id=dev_user.id,
        actor_role=dev_user.role
    )
    print(f"  ✓ Создана задача [{task.issue_key}]: \"{task.title}\"")
    print(f"    Статус: {task.status.value} | Оценка: {task.estimated_minutes // 60} ч ({task.estimated_minutes} мин)")

    # Перевод задачи: BACKLOG -> TODO -> IN_PROGRESS
    t_todo = task_service.move_task_status(task.id, TaskStatus.TODO, dev_user.role)
    t_in_prog = task_service.move_task_status(task.id, TaskStatus.IN_PROGRESS, dev_user.role)
    print(f"  ✓ Задача переведена по воркфлоу: {task.status.value} -> {t_todo.status.value} -> {t_in_prog.status.value}")

    # 4. Модуль 3: Учет трудозатрат (Time Tracking Module)
    print("\n[3] Модуль учета времени (Time Tracking Module):")
    worklog = time_service.log_work(
        task_id=task.id,
        duration_minutes=150,  # 2.5 часа
        user_id=dev_user.id,
        comment="Реализовано хэширование паролей и проверка подписи токена",
        actor_role=dev_user.role
    )
    print(f"  ✓ Зафиксировано списание времени: {worklog.duration_minutes} мин ({worklog.duration_minutes / 60} ч)")
    print(f"    Комментарий: \"{worklog.comment}\"")

    updated_task = task_service.get_task(task.id)
    progress = calculate_task_progress(updated_task.spent_minutes, updated_task.estimated_minutes)
    print(f"\n📊 Итоговые метрики задачи [{updated_task.issue_key}]:")
    print(f"  • Списано времени: {updated_task.spent_minutes} мин ({updated_task.spent_minutes / 60} ч)")
    print(f"  • Осталось трудоемкости: {updated_task.remaining_minutes} мин ({updated_task.remaining_minutes / 60} ч)")
    print(f"  • Прогресс выполнения: {progress}%")

    print("\n" + "=" * 70)
    print("✅ Все программные модули функционируют штатно и согласованы!")
    print("=" * 70)


if __name__ == "__main__":
    run_demo()
