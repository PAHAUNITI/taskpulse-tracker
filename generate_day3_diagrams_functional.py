"""
Генератор функциональных диаграмм IDEF0 и DFD для Дня 3 практики (TaskPulse).
7. IDEF0 A-0 (Контекстная)
8. IDEF0 A0 (Декомпозиция)
9. DFD Level 0 (Общая)
10. DFD Level 1 (Декомпозиция процесса 3.0)
"""

import os
from PIL import Image, ImageDraw, ImageFont

def get_fonts():
    try:
        font_title = ImageFont.truetype("arialbd.ttf", 26)
        font_sub = ImageFont.truetype("arialbd.ttf", 18)
        font_box = ImageFont.truetype("arialbd.ttf", 14)
        font_text = ImageFont.truetype("arial.ttf", 12)
        font_text_bold = ImageFont.truetype("arialbd.ttf", 12)
        font_mono = ImageFont.truetype("consola.ttf", 11)
        font_rel = ImageFont.truetype("ariali.ttf", 11)
    except Exception:
        font_title = ImageFont.load_default()
        font_sub = font_title
        font_box = font_title
        font_text = font_title
        font_text_bold = font_title
        font_mono = font_title
        font_rel = font_title
    return font_title, font_sub, font_box, font_text, font_text_bold, font_mono, font_rel


def draw_arrow(draw, x1, y1, x2, y2, color="#0F172A", width=2, arrow_len=10):
    import math
    draw.line([x1, y1, x2, y2], fill=color, width=width)
    angle = math.atan2(y2 - y1, x2 - x1)
    p1 = (x2 - arrow_len * math.cos(angle - math.pi / 6), y2 - arrow_len * math.sin(angle - math.pi / 6))
    p2 = (x2 - arrow_len * math.cos(angle + math.pi / 6), y2 - arrow_len * math.sin(angle + math.pi / 6))
    draw.polygon([ (x2, y2), p1, p2 ], fill=color)


def draw_idef0_a_minus_0(output_path):
    w, h = 1800, 1100
    img = Image.new("RGB", (w, h), "#F8FAFC")
    draw = ImageDraw.Draw(img)
    f_title, f_sub, f_box, f_text, f_bold, f_mono, f_rel = get_fonts()

    draw.text((w // 2, 35), "Функциональное моделирование IDEF0 — Диаграмма A-0", fill="#0F172A", font=f_title, anchor="mm")
    draw.text((w // 2, 70), "Контекстная диаграмма функционирования программной системы «TaskPulse» (DevFlow Tracker)", fill="#475569", font=f_sub, anchor="mm")

    # Центральный блок А0
    bx, by, bw, bh = 650, 400, 500, 280
    draw.rectangle([bx, by, bx + bw, by + bh], fill="#FFFFFF", outline="#0284C7", width=3)
    draw.rectangle([bx + bw - 60, by + bh - 35, bx + bw, by + bh], fill="#0284C7")
    draw.text((bx + bw - 30, by + bh - 18), "A-0", fill="#FFFFFF", font=f_bold, anchor="mm")

    draw.text((bx + bw // 2, by + bh // 2), 
              "Управление задачами, спринтами и\nучетом рабочего времени в процессе\nкомандной разработки ПО TaskPulse", 
              fill="#0F172A", font=f_title, anchor="mm", align="center")

    # ВХОДЫ (Inputs) - Слева
    draw_arrow(draw, 100, 460, bx, 460, color="#2563EB", width=3)
    draw.text((360, 440), "Технические требования к ПО\nи описания дефектов (баг-репорты)", fill="#1E3A8A", font=f_bold, anchor="mm", align="center")

    draw_arrow(draw, 100, 550, bx, 550, color="#2563EB", width=3)
    draw.text((360, 530), "События коммитов и веток Git\n(Входящие Webhook пейлоады)", fill="#1E3A8A", font=f_bold, anchor="mm", align="center")

    draw_arrow(draw, 100, 620, bx, 620, color="#2563EB", width=3)
    draw.text((360, 605), "Данные отработанных часов разработчиков", fill="#1E3A8A", font=f_bold, anchor="mm")

    # УПРАВЛЕНИЕ (Controls) - Сверху
    draw_arrow(draw, 780, 140, 780, by, color="#B45309", width=3)
    draw.text((780, 220), "Регламент Agile (Scrum / Kanban),\nWIP-лимиты и цели спринта (Sprint Goal)", fill="#B45309", font=f_bold, anchor="mm", align="center")

    draw_arrow(draw, 1020, 140, 1020, by, color="#B45309", width=3)
    draw.text((1020, 260), "Техническое задание практики,\nтребования безопасности (RBAC, 152-ФЗ)", fill="#B45309", font=f_bold, anchor="mm", align="center")

    # МЕХАНИЗМЫ (Mechanisms) - Снизу
    draw_arrow(draw, 780, 960, 780, by + bh, color="#15803D", width=3)
    draw.text((780, 840), "Участники команды (Тимлид,\nРазработчик, Куратор / Преподаватель)", fill="#15803D", font=f_bold, anchor="mm", align="center")

    draw_arrow(draw, 1020, 960, 1020, by + bh, color="#15803D", width=3)
    draw.text((1020, 880), "Серверная инфраструктура Docker,\nСУБД PostgreSQL 16, браузеры", fill="#15803D", font=f_bold, anchor="mm", align="center")

    # ВЫХОДЫ (Outputs) - Справа
    draw_arrow(draw, bx + bw, 460, 1700, 460, color="#7C3AED", width=3)
    draw.text((1420, 440), "Готовое протестированное ПО и\nзакрытые тикеты спринта (Done)", fill="#5B21B6", font=f_bold, anchor="mm", align="center")

    draw_arrow(draw, bx + bw, 550, 1700, 550, color="#7C3AED", width=3)
    draw.text((1420, 530), "Аналитические Burndown-графики,\nсводные табели Timesheets и метрики", fill="#5B21B6", font=f_bold, anchor="mm", align="center")

    draw_arrow(draw, bx + bw, 620, 1700, 620, color="#7C3AED", width=3)
    draw.text((1420, 605), "Аудиторский журнал связок «Задача-Код»", fill="#5B21B6", font=f_bold, anchor="mm")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG", dpi=(300, 300))
    print(f"IDEF0 A-0 saved: {output_path}")


def draw_idef0_a0(output_path):
    w, h = 1800, 1200
    img = Image.new("RGB", (w, h), "#F8FAFC")
    draw = ImageDraw.Draw(img)
    f_title, f_sub, f_box, f_text, f_bold, f_mono, f_rel = get_fonts()

    draw.text((w // 2, 35), "Функциональное моделирование IDEF0 — Диаграмма декомпозиции A0", fill="#0F172A", font=f_title, anchor="mm")
    draw.text((w // 2, 70), "Декомпозиция системы «TaskPulse» на базовые функциональные подсистемы", fill="#475569", font=f_sub, anchor="mm")

    blocks = [
        {"id": "A1", "name": "Управление бэклогом\nи декомпозиция\nтребований", "x": 160, "y": 200, "w": 300, "h": 140},
        {"id": "A2", "name": "Формирование и\nбалансировка спринтов\n(Capacity Planning)", "x": 560, "y": 420, "w": 320, "h": 140},
        {"id": "A3", "name": "Интерактивный трекинг\nзадач и списание\nрабочего времени", "x": 980, "y": 640, "w": 320, "h": 140},
        {"id": "A4", "name": "Формирование аналитики\nи отчетов итерации\n(Burndown / Timesheet)", "x": 1400, "y": 860, "w": 320, "h": 140},
    ]

    for b in blocks:
        bx, by, bw, bh = b["x"], b["y"], b["w"], b["h"]
        draw.rectangle([bx, by, bx + bw, by + bh], fill="#FFFFFF", outline="#0284C7", width=2)
        draw.rectangle([bx + bw - 45, by + bh - 28, bx + bw, by + bh], fill="#0284C7")
        draw.text((bx + bw - 22, by + bh - 14), b["id"], fill="#FFFFFF", font=f_bold, anchor="mm")
        draw.text((bx + bw // 2, by + bh // 2 - 8), b["name"], fill="#0F172A", font=f_box, anchor="mm", align="center")

    # Межблочные потоки
    # Вход в А1 -> Оцененный бэклог -> Вход в А2
    draw_arrow(draw, 50, 270, 160, 270, color="#2563EB", width=2)
    draw.text((105, 250), "Требования к ПО", fill="#1E3A8A", font=f_mono, anchor="mm")

    draw_arrow(draw, 460, 270, 510, 270, color="#2563EB", width=2)
    draw.line([510, 270, 510, 490], fill="#2563EB", width=2)
    draw_arrow(draw, 510, 490, 560, 490, color="#2563EB", width=2)
    draw.text((485, 360), "Оцененные тикеты бэклога", fill="#1E3A8A", font=f_mono)

    # А2 (Активный спринт) -> Вход в А3
    draw_arrow(draw, 880, 490, 930, 490, color="#2563EB", width=2)
    draw.line([930, 490, 930, 710], fill="#2563EB", width=2)
    draw_arrow(draw, 930, 710, 980, 710, color="#2563EB", width=2)
    draw.text((905, 580), "Скоуп активного спринта", fill="#1E3A8A", font=f_mono)

    # Вход коммитов и списаний в А3
    draw_arrow(draw, 800, 750, 980, 750, color="#2563EB", width=2)
    draw.text((890, 730), "Git-вебхуки и Worklogs", fill="#1E3A8A", font=f_mono, anchor="mm")

    # А3 (Журнал трудозатрат и закрытые тикеты) -> Вход в А4
    draw_arrow(draw, 1300, 710, 1350, 710, color="#2563EB", width=2)
    draw.line([1350, 710, 1350, 930], fill="#2563EB", width=2)
    draw_arrow(draw, 1350, 930, 1400, 930, color="#2563EB", width=2)
    draw.text((1325, 800), "История переходов и списаний", fill="#1E3A8A", font=f_mono)

    # Выходы А4
    draw_arrow(draw, 1720, 930, 1780, 930, color="#7C3AED", width=2)
    draw.text((1750, 910), "Burndown & Timesheet", fill="#5B21B6", font=f_bold, anchor="mm")

    # Управляющие стрелки сверху (Controls)
    draw_arrow(draw, 310, 110, 310, 200, color="#B45309", width=2)
    draw.text((310, 150), "ТЗ и критерии DoD", fill="#B45309", font=f_mono, anchor="mm")

    draw_arrow(draw, 720, 110, 720, 420, color="#B45309", width=2)
    draw.text((720, 270), "Agile Scrum регламент\nи емкость команды", fill="#B45309", font=f_mono, anchor="mm", align="center")

    draw_arrow(draw, 1140, 110, 1140, 640, color="#B45309", width=2)
    draw.text((1140, 380), "WIP-лимиты колонок", fill="#B45309", font=f_mono, anchor="mm")

    # Механизмы снизу (Mechanisms)
    draw_arrow(draw, 310, 1150, 310, 340, color="#15803D", width=2)
    draw.text((310, 800), "Тимлид / Разработчик", fill="#15803D", font=f_mono, anchor="mm")

    draw_arrow(draw, 1140, 1150, 1140, 780, color="#15803D", width=2)
    draw.text((1140, 970), "Браузер, Webhook API,\nБД PostgreSQL 16", fill="#15803D", font=f_mono, anchor="mm", align="center")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG", dpi=(300, 300))
    print(f"IDEF0 A0 saved: {output_path}")


def draw_dfd_level_0(output_path):
    w, h = 1800, 1100
    img = Image.new("RGB", (w, h), "#F8FAFC")
    draw = ImageDraw.Draw(img)
    f_title, f_sub, f_box, f_text, f_bold, f_mono, f_rel = get_fonts()

    draw.text((w // 2, 35), "Диаграмма потоков данных DFD — Уровень 0 (General / Context)", fill="#0F172A", font=f_title, anchor="mm")
    draw.text((w // 2, 70), "Глобальная схема движения информационных потоков и накопителей данных «TaskPulse»", fill="#475569", font=f_sub, anchor="mm")

    # Внешние сущности (Прямоугольники с двойной рамкой)
    def draw_ext_entity(x, y, ew, eh, name):
        draw.rectangle([x, y, x + ew, y + eh], fill="#F1F5F9", outline="#0F172A", width=2)
        draw.rectangle([x + 4, y + 4, x + ew - 4, y + eh - 4], outline="#0F172A", width=1)
        draw.text((x + ew // 2, y + eh // 2), name, fill="#0F172A", font=f_bold, anchor="mm", align="center")

    draw_ext_entity(80, 240, 240, 110, "Пользователь\n(Тимлид / Разработчик)")
    draw_ext_entity(80, 680, 240, 110, "Внешний Git-сервер\n(GitHub / GitLab)")
    draw_ext_entity(1480, 240, 240, 110, "Наблюдатель /\nКуратор практики")

    # Основные процессы (Округлые прямоугольники)
    def draw_process(pid, name, x, y, pw=280, ph=110):
        draw.rounded_rectangle([x, y, x + pw, y + ph], radius=20, fill="#FFFFFF", outline="#0284C7", width=2)
        draw.line([x, y + 32, x + pw, y + 32], fill="#0284C7", width=1)
        draw.text((x + pw // 2, y + 16), f"Процесс {pid}", fill="#0284C7", font=f_bold, anchor="mm")
        draw.text((x + pw // 2, y + 70), name, fill="#0F172A", font=f_text, anchor="mm", align="center")

    draw_process("1.0", "Аутентификация и\nсессионный контроль RBAC", 480, 150)
    draw_process("2.0", "Управление бэклогом\nи спринтами проектов", 480, 360)
    draw_process("3.0", "Интерактивный Kanban\nи учет трудозатрат (Time)", 480, 580)
    draw_process("4.0", "Парсинг и привязка\nGit-вебхуков", 480, 800)
    draw_process("5.0", "Генерация отчетов и\nметрик (Burndown)", 1050, 420)

    # Хранилища данных (Data Stores: параллельные линии)
    def draw_data_store(did, name, x, y, sw=260, sh=70):
        draw.rectangle([x, y, x + sw, y + sh], fill="#FFFFFF", outline="#CBD5E1")
        draw.line([x, y, x + sw, y], fill="#0F172A", width=3)
        draw.line([x, y + sh, x + sw, y + sh], fill="#0F172A", width=3)
        draw.line([x + 50, y, x + 50, y + sh], fill="#CBD5E1", width=1)
        draw.text((x + 25, y + sh // 2), did, fill="#0F172A", font=f_bold, anchor="mm")
        draw.text((x + 155, y + sh // 2), name, fill="#0F172A", font=f_bold, anchor="mm")

    draw_data_store("D1", "БД Пользователей и Ролей", 1050, 170)
    draw_data_store("D2", "БД Задач и Спринтов", 1050, 600)
    draw_data_store("D3", "Журнал Worklogs и Git Events", 1050, 800)

    # Потоки данных (Data Flows)
    # Пользователь -> 1.0 (Учетные данные)
    draw_arrow(draw, 320, 270, 480, 200, color="#2563EB", width=2)
    draw.text((390, 215), "Логин / пароль", fill="#1E3A8A", font=f_mono)

    # 1.0 <-> D1
    draw_arrow(draw, 760, 205, 1050, 205, color="#0F172A", width=2)
    draw.text((905, 185), "Проверка учетной записи", fill="#0F172A", font=f_mono, anchor="mm")

    # Пользователь -> 2.0 (Параметры тикетов)
    draw_arrow(draw, 320, 310, 480, 410, color="#2563EB", width=2)
    draw.text((390, 345), "Данные тикета / спринта", fill="#1E3A8A", font=f_mono)

    # 2.0 -> D2
    draw_arrow(draw, 760, 415, 1050, 620, color="#0F172A", width=2)
    draw.text((880, 490), "Сохранение задачи", fill="#0F172A", font=f_mono)

    # Пользователь -> 3.0 (Смена статуса, списание времени)
    draw_arrow(draw, 320, 340, 480, 630, color="#2563EB", width=2)
    draw.text((360, 500), "Drag-and-Drop / Часы", fill="#1E3A8A", font=f_mono)

    # 3.0 -> D2 & D3
    draw_arrow(draw, 760, 635, 1050, 635, color="#0F172A", width=2)
    draw.text((905, 615), "Обновление статуса", fill="#0F172A", font=f_mono, anchor="mm")

    draw_arrow(draw, 760, 655, 1050, 820, color="#0F172A", width=2)
    draw.text((880, 750), "Запись Worklog", fill="#0F172A", font=f_mono)

    # Git Server -> 4.0
    draw_arrow(draw, 320, 735, 480, 850, color="#475569", width=2)
    draw.text((390, 775), "HTTP POST Webhook JSON", fill="#475569", font=f_mono)

    # 4.0 -> D3
    draw_arrow(draw, 760, 855, 1050, 855, color="#0F172A", width=2)
    draw.text((905, 875), "Git Commit & Branch", fill="#0F172A", font=f_mono, anchor="mm")

    # D2 & D3 -> 5.0 (Аналитика)
    draw_arrow(draw, 1180, 600, 1180, 530, color="#7C3AED", width=2)
    draw_arrow(draw, 1220, 800, 1220, 530, color="#7C3AED", width=2)
    draw.text((1250, 560), "Агрегированные данные", fill="#7C3AED", font=f_mono)

    # 5.0 -> Наблюдатель
    draw_arrow(draw, 1330, 475, 1480, 320, color="#7C3AED", width=2)
    draw.text((1440, 420), "Сводка спринта, Burndown", fill="#5B21B6", font=f_bold, anchor="mm")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG", dpi=(300, 300))
    print(f"DFD Level 0 saved: {output_path}")


def draw_dfd_level_1(output_path):
    w, h = 1800, 1100
    img = Image.new("RGB", (w, h), "#F8FAFC")
    draw = ImageDraw.Draw(img)
    f_title, f_sub, f_box, f_text, f_bold, f_mono, f_rel = get_fonts()

    draw.text((w // 2, 35), "Диаграмма потоков данных DFD — Уровень 1 (Декомпозиция процесса 3.0)", fill="#0F172A", font=f_title, anchor="mm")
    draw.text((w // 2, 70), "Детализация процесса «3.0 Учет трудозатрат и переходы состояний на Kanban-доске»", fill="#475569", font=f_sub, anchor="mm")

    # Внешние сущности
    def draw_ext_entity(x, y, ew, eh, name):
        draw.rectangle([x, y, x + ew, y + eh], fill="#F1F5F9", outline="#0F172A", width=2)
        draw.rectangle([x + 4, y + 4, x + ew - 4, y + eh - 4], outline="#0F172A", width=1)
        draw.text((x + ew // 2, y + eh // 2), name, fill="#0F172A", font=f_bold, anchor="mm", align="center")

    draw_ext_entity(80, 420, 220, 110, "Разработчик /\nИсполнитель")
    draw_ext_entity(1500, 780, 220, 110, "Тимлид /\nАналитик")

    # Подпроцессы
    def draw_sub_process(pid, name, x, y, pw=280, ph=110):
        draw.rounded_rectangle([x, y, x + pw, y + ph], radius=20, fill="#FFFFFF", outline="#059669", width=2)
        draw.line([x, y + 32, x + pw, y + 32], fill="#059669", width=1)
        draw.text((x + pw // 2, y + 16), f"Процесс {pid}", fill="#059669", font=f_bold, anchor="mm")
        draw.text((x + pw // 2, y + 70), name, fill="#0F172A", font=f_text, anchor="mm", align="center")

    draw_sub_process("3.1", "Проверка прав доступа\nи контроль WIP-лимита", 440, 240)
    draw_sub_process("3.2", "Фиксация перемещения\nкарточки в БД", 440, 480)
    draw_sub_process("3.3", "Валидация и регистрация\nсписания часов (Worklog)", 440, 720)
    draw_sub_process("3.4", "Пересчет остаточной\nтрудоемкости (remaining)", 980, 720)

    # Хранилища данных
    def draw_data_store(did, name, x, y, sw=260, sh=70):
        draw.rectangle([x, y, x + sw, y + sh], fill="#FFFFFF", outline="#CBD5E1")
        draw.line([x, y, x + sw, y], fill="#0F172A", width=3)
        draw.line([x, y + sh, x + sw, y + sh], fill="#0F172A", width=3)
        draw.line([x + 50, y, x + 50, y + sh], fill="#CBD5E1", width=1)
        draw.text((x + 25, y + sh // 2), did, fill="#0F172A", font=f_bold, anchor="mm")
        draw.text((x + 155, y + sh // 2), name, fill="#0F172A", font=f_bold, anchor="mm")

    draw_data_store("D2", "БД Задач (Состояния)", 980, 480)
    draw_data_store("D3", "Журнал списаний Worklogs", 980, 920)

    # Потоки данных
    # Разработчик -> 3.1
    draw_arrow(draw, 300, 440, 440, 295, color="#059669", width=2)
    draw.text((345, 340), "Запрос смены статуса (Drag)", fill="#059669", font=f_mono)

    # 3.1 -> 3.2 (Разрешенный переход)
    draw_arrow(draw, 580, 350, 580, 480, color="#0F172A", width=2)
    draw.text((680, 415), "Статус валиден [wip_ok]", fill="#0F172A", font=f_mono, anchor="mm")

    # 3.2 -> D2
    draw_arrow(draw, 720, 535, 980, 535, color="#0F172A", width=2)
    draw.text((850, 515), "Обновление task.status", fill="#0F172A", font=f_mono, anchor="mm")

    # Разработчик -> 3.3 (Списание времени)
    draw_arrow(draw, 300, 490, 440, 775, color="#059669", width=2)
    draw.text((345, 660), "Длительность (мин) и коммент", fill="#059669", font=f_mono)

    # 3.3 -> D3
    draw_arrow(draw, 580, 830, 580, 955, color="#0F172A", width=2)
    draw_arrow(draw, 580, 955, 980, 955, color="#0F172A", width=2)
    draw.text((780, 935), "Запись нового Worklog", fill="#0F172A", font=f_mono, anchor="mm")

    # 3.3 -> 3.4
    draw_arrow(draw, 720, 775, 980, 775, color="#0F172A", width=2)
    draw.text((850, 755), "Списанные минуты", fill="#0F172A", font=f_mono, anchor="mm")

    # 3.4 -> D2
    draw_arrow(draw, 1110, 720, 1110, 550, color="#0F172A", width=2)
    draw.text((1230, 635), "Коррекция remaining_minutes", fill="#0F172A", font=f_mono, anchor="mm")

    # 3.4 -> Тимлид (Уведомление о прогрессе)
    draw_arrow(draw, 1260, 775, 1500, 835, color="#7C3AED", width=2)
    draw.text((1380, 785), "Сводные часы задачи", fill="#5B21B6", font=f_mono, anchor="mm")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG", dpi=(300, 300))
    print(f"DFD Level 1 saved: {output_path}")


if __name__ == "__main__":
    base = r"C:\Users\paha2\.gemini\antigravity\scratch\taskpulse-tracker\docs\diagrams"
    draw_idef0_a_minus_0(os.path.join(base, "idef0-a-0.png"))
    draw_idef0_a0(os.path.join(base, "idef0-a0.png"))
    draw_dfd_level_0(os.path.join(base, "dfd-level-0.png"))
    draw_dfd_level_1(os.path.join(base, "dfd-level-1.png"))
