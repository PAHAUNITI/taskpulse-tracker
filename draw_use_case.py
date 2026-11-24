import os
from PIL import Image, ImageDraw, ImageFont

def draw_uml_use_case(output_path):
    width, height = 1800, 1250
    img = Image.new("RGB", (width, height), "#F8FAFC") # Slate 50 background
    draw = ImageDraw.Draw(img)

    # Попытка загрузить системные шрифты
    try:
        font_title = ImageFont.truetype("arialbd.ttf", 26)
        font_sub = ImageFont.truetype("arialbd.ttf", 18)
        font_actor = ImageFont.truetype("arialbd.ttf", 15)
        font_uc = ImageFont.truetype("arial.ttf", 14)
        font_uc_bold = ImageFont.truetype("arialbd.ttf", 14)
        font_rel = ImageFont.truetype("ariali.ttf", 12)
    except Exception:
        font_title = ImageFont.load_default()
        font_sub = font_title
        font_actor = font_title
        font_uc = font_title
        font_uc_bold = font_title
        font_rel = font_title

    # 1. Заголовок диаграммы
    draw.text((width // 2, 35), "UML Диаграмма вариантов использования (Use Case Diagram)", fill="#0F172A", font=font_title, anchor="mm")
    draw.text((width // 2, 70), "Программный комплекс «TaskPulse» (DevFlow Tracker) — Спецификация взаимодействия", fill="#475569", font=font_sub, anchor="mm")

    # 2. Граница системы (System Boundary)
    sys_x1, sys_y1, sys_x2, sys_y2 = 340, 110, 1460, 1200
    draw.rectangle([sys_x1, sys_y1, sys_x2, sys_y2], fill="#FFFFFF", outline="#0EA5E9", width=3)
    draw.rectangle([sys_x1, sys_y1, sys_x1 + 380, sys_y1 + 36], fill="#0EA5E9", outline="#0EA5E9")
    draw.text((sys_x1 + 190, sys_y1 + 18), "Система «TaskPulse» (Scope Boundary)", fill="#FFFFFF", font=font_sub, anchor="mm")

    # 3. Акторы (Actors)
    actors = [
        {"id": "admin", "name": "Администратор\nсистемы", "x": 160, "y": 250, "color": "#E11D48"},
        {"id": "lead", "name": "Тимлид /\nМенеджер", "x": 160, "y": 550, "color": "#2563EB"},
        {"id": "dev", "name": "Разработчик /\nИсполнитель", "x": 160, "y": 920, "color": "#059669"},
        {"id": "obs", "name": "Наблюдатель /\nКуратор", "x": 1640, "y": 420, "color": "#7C3AED"},
        {"id": "git", "name": "Git-сервер\n(GitHub/GitLab)", "x": 1640, "y": 880, "color": "#475569", "is_sys": True},
    ]

    def draw_actor(x, y, name, color, is_sys=False):
        if is_sys:
            # Прямоугольник для внешней системы
            draw.rectangle([x - 55, y - 45, x + 55, y + 25], fill="#F1F5F9", outline=color, width=2)
            draw.text((x, y - 10), "«external»\nGit Server", fill=color, font=font_actor, anchor="mm", align="center")
            draw.text((x, y + 45), name, fill="#0F172A", font=font_actor, anchor="mm", align="center")
        else:
            # Пиктограмма стикмена
            head_r = 18
            draw.ellipse([x - head_r, y - 55, x + head_r, y - 55 + head_r * 2], outline=color, fill="#FFFFFF", width=3)
            # Тело
            draw.line([x, y - 55 + head_r * 2, x, y + 10], fill=color, width=3)
            # Руки
            draw.line([x - 28, y - 10, x + 28, y - 10], fill=color, width=3)
            # Ноги
            draw.line([x, y + 10, x - 22, y + 45], fill=color, width=3)
            draw.line([x, y + 10, x + 22, y + 45], fill=color, width=3)
            draw.text((x, y + 68), name, fill="#0F172A", font=font_actor, anchor="mm", align="center")

    for act in actors:
        draw_actor(act["x"], act["y"], act["name"], act["color"], act.get("is_sys", False))

    # 4. Варианты использования (Use Cases)
    use_cases = {
        "uc_auth": {"name": "Авторизоваться\nв системе (RBAC)", "x": 900, "y": 180, "w": 220, "h": 65, "bg": "#F0FDF4", "border": "#16A34A"},
        "uc_users": {"name": "Управлять учетными\nзаписями и проектами", "x": 620, "y": 250, "w": 230, "h": 65, "bg": "#FFF1F2", "border": "#E11D48"},
        
        "uc_create_task": {"name": "Создать задачу\nв бэклоге проекта", "x": 600, "y": 420, "w": 220, "h": 65, "bg": "#EFF6FF", "border": "#2563EB"},
        "uc_edit_task": {"name": "Редактировать атрибуты\nи Markdown задачи", "x": 600, "y": 530, "w": 220, "h": 65, "bg": "#EFF6FF", "border": "#2563EB"},
        "uc_assign": {"name": "Назначить исполнителя\nна задачу", "x": 600, "y": 640, "w": 220, "h": 65, "bg": "#EFF6FF", "border": "#2563EB"},

        "uc_move_card": {"name": "Переместить карточку\nна Kanban-доске", "x": 600, "y": 780, "w": 220, "h": 65, "bg": "#F0FDF4", "border": "#16A34A"},
        "uc_wip": {"name": "Проверить соблюдение\nWIP-лимитов", "x": 920, "y": 780, "w": 210, "h": 60, "bg": "#FEF3C7", "border": "#D97706"},
        "uc_time": {"name": "Списать фактически\nзатраченное время", "x": 600, "y": 910, "w": 220, "h": 65, "bg": "#F0FDF4", "border": "#16A34A"},

        "uc_sprint_plan": {"name": "Сформировать и\nзапустить спринт", "x": 920, "y": 420, "w": 210, "h": 65, "bg": "#EFF6FF", "border": "#2563EB"},
        "uc_sprint_close": {"name": "Завершить спринт\nи закрыть скоуп", "x": 920, "y": 530, "w": 210, "h": 65, "bg": "#EFF6FF", "border": "#2563EB"},

        "uc_git": {"name": "Привязать Git-коммиты\nи ветки по Webhook", "x": 1220, "y": 880, "w": 230, "h": 65, "bg": "#F8FAFC", "border": "#475569"},
        
        "uc_burndown": {"name": "Просмотреть Burndown\nи табель Timesheet", "x": 1220, "y": 420, "w": 230, "h": 65, "bg": "#FAF5FF", "border": "#7C3AED"},
        "uc_comment": {"name": "Оставить рецензию /\nкомментарий к задаче", "x": 1220, "y": 550, "w": 230, "h": 65, "bg": "#FAF5FF", "border": "#7C3AED"},
        "uc_export": {"name": "Экспортировать отчет\nпо спринту (CSV/PDF)", "x": 1220, "y": 680, "w": 230, "h": 65, "bg": "#FAF5FF", "border": "#7C3AED"},
    }

    # Отрисовка эллипсов Use Case
    for uc_id, uc in use_cases.items():
        x, y, w, h = uc["x"], uc["y"], uc["w"], uc["h"]
        box = [x - w // 2, y - h // 2, x + w // 2, y + h // 2]
        draw.ellipse(box, fill=uc["bg"], outline=uc["border"], width=2)
        draw.text((x, y), uc["name"], fill="#0F172A", font=font_uc, anchor="mm", align="center")

    # 5. Линии связей Актор -> Вариант использования
    def link_actor_uc(act_id, uc_id, color="#94A3B8"):
        act = next(a for a in actors if a["id"] == act_id)
        uc = use_cases[uc_id]
        ax, ay = act["x"], act["y"]
        ux, uy = uc["x"], uc["y"]
        # Коррекция точек соединения
        if ax < ux:
            start_x = ax + 35 if not act.get("is_sys") else ax + 60
            end_x = ux - uc["w"] // 2
        else:
            start_x = ax - 35 if not act.get("is_sys") else ax - 60
            end_x = ux + uc["w"] // 2
        draw.line([start_x, ay, end_x, uy], fill=color, width=2)

    # Связи Администратора
    link_actor_uc("admin", "uc_users", "#E11D48")
    link_actor_uc("admin", "uc_auth", "#E11D48")

    # Связи Тимлида
    link_actor_uc("lead", "uc_create_task", "#2563EB")
    link_actor_uc("lead", "uc_edit_task", "#2563EB")
    link_actor_uc("lead", "uc_assign", "#2563EB")
    link_actor_uc("lead", "uc_sprint_plan", "#2563EB")
    link_actor_uc("lead", "uc_sprint_close", "#2563EB")
    link_actor_uc("lead", "uc_move_card", "#2563EB")
    link_actor_uc("lead", "uc_burndown", "#2563EB")

    # Связи Разработчика
    link_actor_uc("dev", "uc_create_task", "#059669")
    link_actor_uc("dev", "uc_move_card", "#059669")
    link_actor_uc("dev", "uc_time", "#059669")
    link_actor_uc("dev", "uc_edit_task", "#059669")

    # Связи Наблюдателя
    link_actor_uc("obs", "uc_burndown", "#7C3AED")
    link_actor_uc("obs", "uc_comment", "#7C3AED")
    link_actor_uc("obs", "uc_export", "#7C3AED")

    # Связи Git-сервера
    link_actor_uc("git", "uc_git", "#475569")

    # 6. Отношения <<include>> и <<extend>> (пунктирные линии)
    def draw_dashed_arrow(x1, y1, x2, y2, label="", color="#475569"):
        # Рисование пунктирной линии
        import math
        dist = math.hypot(x2 - x1, y2 - y1)
        if dist == 0:
            return
        dashes = int(dist // 10)
        dx = (x2 - x1) / dist
        dy = (y2 - y1) / dist
        for i in range(dashes):
            if i % 2 == 0:
                sx = x1 + dx * i * 10
                sy = y1 + dy * i * 10
                ex = x1 + dx * min((i + 1) * 10, dist)
                ey = y1 + dy * min((i + 1) * 10, dist)
                draw.line([sx, sy, ex, ey], fill=color, width=2)
        
        # Стрелка на конце
        arrow_len = 10
        angle = math.atan2(y2 - y1, x2 - x1)
        p1 = (x2 - arrow_len * math.cos(angle - math.pi / 6), y2 - arrow_len * math.sin(angle - math.pi / 6))
        p2 = (x2 - arrow_len * math.cos(angle + math.pi / 6), y2 - arrow_len * math.sin(angle + math.pi / 6))
        draw.line([x2, y2, p1[0], p1[1]], fill=color, width=2)
        draw.line([x2, y2, p2[0], p2[1]], fill=color, width=2)

        # Текст метки отношения
        if label:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2 - 12
            draw.text((mx, my), label, fill=color, font=font_rel, anchor="mm")

    # <<extend>>: uc_wip -> uc_move_card (проверка WIP-лимита расширяет перемещение карточки)
    draw_dashed_arrow(use_cases["uc_wip"]["x"] - use_cases["uc_wip"]["w"] // 2, use_cases["uc_wip"]["y"],
                      use_cases["uc_move_card"]["x"] + use_cases["uc_move_card"]["w"] // 2, use_cases["uc_move_card"]["y"],
                      label="«extend»", color="#D97706")

    # <<include>>: uc_move_card -> uc_auth (перемещение требует авторизации)
    draw_dashed_arrow(use_cases["uc_move_card"]["x"] + 60, use_cases["uc_move_card"]["y"] - 30,
                      use_cases["uc_auth"]["x"] - 50, use_cases["uc_auth"]["y"] + 30,
                      label="«include»", color="#2563EB")

    # <<include>>: uc_time -> uc_auth (списание времени требует авторизации)
    draw_dashed_arrow(use_cases["uc_time"]["x"] + 80, use_cases["uc_time"]["y"] - 30,
                      use_cases["uc_auth"]["x"] - 80, use_cases["uc_auth"]["y"] + 30,
                      label="«include»", color="#16A34A")

    # Легенда диаграммы
    leg_x, leg_y = sys_x1 + 20, sys_y2 - 70
    draw.rectangle([leg_x, leg_y, leg_x + 620, leg_y + 55], fill="#F8FAFC", outline="#CBD5E1")
    draw.text((leg_x + 10, leg_y + 12), "Легенда связей:", fill="#0F172A", font=font_uc_bold)
    draw.line([leg_x + 130, leg_y + 18, leg_x + 190, leg_y + 18], fill="#2563EB", width=2)
    draw.text((leg_x + 200, leg_y + 12), "Ассоциация", fill="#475569", font=font_uc)
    
    # Пунктир include
    draw.line([leg_x + 300, leg_y + 18, leg_x + 350, leg_y + 18], fill="#2563EB", width=2)
    draw.text((leg_x + 360, leg_y + 12), "«include» (Обязательное включение)", fill="#2563EB", font=font_rel)
    
    draw.line([leg_x + 300, leg_y + 38, leg_x + 350, leg_y + 38], fill="#D97706", width=2)
    draw.text((leg_x + 360, leg_y + 32), "«extend» (Условное расширение)", fill="#D97706", font=font_rel)

    # Сохраняем диаграмму
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG", dpi=(300, 300))
    print(f"UML Use Case diagram successfully created: {output_path}")

if __name__ == "__main__":
    out = r"C:\Users\paha2\.gemini\antigravity\scratch\taskpulse-tracker\docs\use-case-diagram.png"
    draw_uml_use_case(out)
