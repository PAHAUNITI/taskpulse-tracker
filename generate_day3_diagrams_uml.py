"""
Генератор UML диаграмм для Дня 3 практики (TaskPulse).
1. Class Diagram
2. Component Diagram
3. Deployment Diagram
4. Activity Diagram
5. State Machine Diagram
6. Communication Diagram
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


def draw_class_diagram(output_path):
    w, h = 1900, 1250
    img = Image.new("RGB", (w, h), "#F8FAFC")
    draw = ImageDraw.Draw(img)
    f_title, f_sub, f_box, f_text, f_bold, f_mono, f_rel = get_fonts()

    draw.text((w // 2, 35), "UML Диаграмма классов (Class Diagram)", fill="#0F172A", font=f_title, anchor="mm")
    draw.text((w // 2, 70), "Программная система «TaskPulse» — Статическая модель объектной структуры", fill="#475569", font=f_sub, anchor="mm")

    classes = [
        {
            "name": "User", "stereo": "«entity»", "x": 100, "y": 140, "w": 280, "h": 260,
            "attrs": ["- id: UUID", "- username: String", "- email: String", "- passwordHash: String", "- role: UserRole", "- weeklyCapacity: Int"],
            "methods": ["+ authenticate(pwd): Bool", "+ updateProfile(data): Void", "+ getAssignedTasks(): Task[*]"]
        },
        {
            "name": "Project", "stereo": "«aggregate root»", "x": 480, "y": 140, "w": 300, "h": 240,
            "attrs": ["- id: UUID", "- name: String", "- key: String [TP]", "- ownerId: UUID", "- createdAt: DateTime"],
            "methods": ["+ createSprint(goal): Sprint", "+ addTask(task): Task", "+ getBacklog(): Task[*]"]
        },
        {
            "name": "Sprint", "stereo": "«entity»", "x": 900, "y": 140, "w": 290, "h": 260,
            "attrs": ["- id: UUID", "- projectId: UUID", "- name: String", "- goal: String", "- status: SprintStatus", "- startDate: Date", "- endDate: Date"],
            "methods": ["+ startSprint(): Void", "+ finishSprint(): Void", "+ calculateBurndown(): Chart"]
        },
        {
            "name": "Task", "stereo": "«entity»", "x": 480, "y": 500, "w": 320, "h": 320,
            "attrs": ["- id: UUID", "- issueKey: String", "- projectId: UUID", "- title: String", "- description: Markdown", "- status: TaskStatus", "- priority: Priority", "- estimatedMin: Int", "- spentMin: Int", "- remainingMin: Int"],
            "methods": ["+ transitionStatus(status): Task", "+ logWork(min, comment): Worklog", "+ assignTo(userId): Void", "+ linkGitCommit(sha): Void"]
        },
        {
            "name": "Worklog", "stereo": "«entity»", "x": 100, "y": 540, "w": 280, "h": 230,
            "attrs": ["- id: UUID", "- taskId: UUID", "- userId: UUID", "- durationMin: Int", "- comment: String", "- loggedAt: DateTime"],
            "methods": ["+ getAuthor(): User", "+ validateDuration(): Bool"]
        },
        {
            "name": "GitCommit", "stereo": "«value object»", "x": 900, "y": 540, "w": 290, "h": 230,
            "attrs": ["- sha: String [40]", "- taskId: UUID", "- branch: String", "- message: String", "- authorName: String", "- commitUrl: URL"],
            "methods": ["+ extractIssueKey(): String", "+ isClosingDirective(): Bool"]
        },
        {
            "name": "KanbanBoard", "stereo": "«boundary / service»", "x": 1300, "y": 320, "w": 320, "h": 260,
            "attrs": ["- projectId: UUID", "- wipLimits: Map<Status, Int>", "- columns: List<Column>"],
            "methods": ["+ moveCard(taskId, status): Bool", "+ checkWipLimit(status): Bool", "+ renderBoard(): HTML"]
        }
    ]

    for c in classes:
        x, y, cw, ch = c["x"], c["y"], c["w"], c["h"]
        draw.rectangle([x, y, x + cw, y + ch], fill="#FFFFFF", outline="#0284C7", width=2)
        draw.rectangle([x, y, x + cw, y + 42], fill="#0284C7", outline="#0284C7")
        draw.text((x + cw // 2, y + 12), c["stereo"], fill="#BAE6FD", font=f_rel, anchor="mm")
        draw.text((x + cw // 2, y + 28), c["name"], fill="#FFFFFF", font=f_box, anchor="mm")

        # Атрибуты
        ay = y + 48
        for attr in c["attrs"]:
            draw.text((x + 8, ay), attr, fill="#1E293B", font=f_mono)
            ay += 18

        draw.line([x, ay + 4, x + cw, ay + 4], fill="#CBD5E1", width=1)
        my = ay + 10
        for method in c["methods"]:
            draw.text((x + 8, my), method, fill="#0369A1", font=f_mono)
            my += 18

    # Связи:
    # 1. Project *-- Task (Композиция: Project содержит Task)
    draw.line([630, 380, 630, 500], fill="#0F172A", width=2)
    draw.polygon([(630, 380), (624, 395), (630, 410), (636, 395)], fill="#0F172A") # закрашенный ромб
    draw.text((645, 415), "1", fill="#0F172A", font=f_bold)
    draw.text((645, 480), "0..*", fill="#0F172A", font=f_bold)

    # 2. Project o-- Sprint (Агрегация: Sprint входит в Project)
    draw.line([780, 240, 900, 240], fill="#0F172A", width=2)
    draw.polygon([(780, 240), (795, 234), (810, 240), (795, 246)], fill="#FFFFFF", outline="#0F172A") # пустой ромб
    draw.text((818, 222), "1", fill="#0F172A", font=f_bold)
    draw.text((880, 222), "0..*", fill="#0F172A", font=f_bold)

    # 3. Task *-- Worklog (Композиция: Task содержит Worklogs)
    draw.line([480, 650, 380, 650], fill="#0F172A", width=2)
    draw.polygon([(480, 650), (465, 644), (450, 650), (465, 656)], fill="#0F172A")
    draw.text((440, 632), "1", fill="#0F172A", font=f_bold)
    draw.text((395, 632), "0..*", fill="#0F172A", font=f_bold)

    # 4. Task -- GitCommit (Ассоциация 1 к 0..*)
    draw.line([800, 650, 900, 650], fill="#0F172A", width=2)
    draw.text((815, 632), "1", fill="#0F172A", font=f_bold)
    draw.text((880, 632), "0..*", fill="#0F172A", font=f_bold)

    # 5. User -- Task (Ассоциация Assignee / Reporter)
    draw.line([240, 400, 240, 480, 480, 540], fill="#64748B", width=2)
    draw.text((250, 415), "1", fill="#64748B", font=f_bold)
    draw.text((435, 520), "0..*", fill="#64748B", font=f_bold)
    draw.text((310, 490), "«assigned to»", fill="#64748B", font=f_rel)

    # 6. Sprint o-- Task (Агрегация: задачи включены в спринт)
    draw.line([1040, 400, 1040, 480, 780, 520], fill="#0F172A", width=2)
    draw.polygon([(1040, 400), (1034, 415), (1040, 430), (1046, 415)], fill="#FFFFFF", outline="#0F172A")
    draw.text((1015, 435), "0..1", fill="#0F172A", font=f_bold)
    draw.text((800, 500), "0..*", fill="#0F172A", font=f_bold)

    # 7. KanbanBoard ..> Task (Зависимость)
    draw.line([1300, 480, 800, 560], fill="#0284C7", width=2)
    draw.text((1050, 500), "«manages»", fill="#0284C7", font=f_rel)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG", dpi=(300, 300))
    print(f"Class diagram saved: {output_path}")


def draw_component_diagram(output_path):
    w, h = 1800, 1100
    img = Image.new("RGB", (w, h), "#F8FAFC")
    draw = ImageDraw.Draw(img)
    f_title, f_sub, f_box, f_text, f_bold, f_mono, f_rel = get_fonts()

    draw.text((w // 2, 35), "UML Диаграмма компонентов (Component Diagram)", fill="#0F172A", font=f_title, anchor="mm")
    draw.text((w // 2, 70), "Логическая организация подсистем и интерфейсов программного комплекса «TaskPulse»", fill="#475569", font=f_sub, anchor="mm")

    components = [
        {"id": "ui", "name": "«component»\nWeb Client (React / TS)", "x": 120, "y": 320, "w": 260, "h": 140, "color": "#0284C7"},
        {"id": "gw", "name": "«component»\nAPI Gateway & Auth", "x": 480, "y": 320, "w": 260, "h": 140, "color": "#E11D48"},
        {"id": "task_srv", "name": "«component»\nTask & Sprint Service", "x": 860, "y": 180, "w": 280, "h": 140, "color": "#2563EB"},
        {"id": "time_srv", "name": "«component»\nTime Tracking Service", "x": 860, "y": 460, "w": 280, "h": 140, "color": "#059669"},
        {"id": "git_hook", "name": "«component»\nGit Webhook Consumer", "x": 480, "y": 640, "w": 260, "h": 140, "color": "#475569"},
        {"id": "db_acc", "name": "«component»\nData Access Layer (ORM)", "x": 1260, "y": 320, "w": 270, "h": 140, "color": "#7C3AED"},
        {"id": "ext_git", "name": "«external»\nGitHub / GitLab API", "x": 120, "y": 640, "w": 240, "h": 110, "color": "#334155"}
    ]

    for c in components:
        x, y, cw, ch = c["x"], c["y"], c["w"], c["h"]
        draw.rectangle([x, y, x + cw, y + ch], fill="#FFFFFF", outline=c["color"], width=2)
        # Компонентная пиктограмма в углу
        draw.rectangle([x + cw - 32, y + 8, x + cw - 8, y + 26], fill="#F1F5F9", outline=c["color"], width=1)
        draw.rectangle([x + cw - 36, y + 11, x + cw - 28, y + 16], fill="#FFFFFF", outline=c["color"], width=1)
        draw.rectangle([x + cw - 36, y + 18, x + cw - 28, y + 23], fill="#FFFFFF", outline=c["color"], width=1)
        draw.text((x + cw // 2, y + ch // 2), c["name"], fill="#0F172A", font=f_box, anchor="mm", align="center")

    def draw_lolipop(x, y, name, direction="right"):
        r = 8
        draw.ellipse([x - r, y - r, x + r, y + r], fill="#FFFFFF", outline="#0284C7", width=2)
        draw.text((x, y - 16), name, fill="#0284C7", font=f_mono, anchor="mm")

    # Соединители
    # UI -> API Gateway (REST API)
    draw.line([380, 390, 440, 390], fill="#0284C7", width=2)
    draw_lolipop(440, 390, "IHttpRest")
    draw.line([448, 390, 480, 390], fill="#0284C7", width=2)

    # API Gateway -> Task Service
    draw.line([740, 360, 800, 250], fill="#2563EB", width=2)
    draw_lolipop(800, 250, "ITaskApi")
    draw.line([808, 250, 860, 250], fill="#2563EB", width=2)

    # API Gateway -> Time Service
    draw.line([740, 420, 800, 530], fill="#059669", width=2)
    draw_lolipop(800, 530, "ITimeApi")
    draw.line([808, 530, 860, 530], fill="#059669", width=2)

    # External Git -> Webhook Consumer
    draw.line([360, 695, 440, 695], fill="#475569", width=2)
    draw_lolipop(440, 695, "IWebhook")
    draw.line([448, 695, 480, 695], fill="#475569", width=2)

    # Webhook Consumer -> Task Service
    draw.line([610, 640, 860, 290], fill="#475569", width=2)
    draw.text((710, 480), "«calls ITaskApi»", fill="#475569", font=f_rel)

    # Task Service & Time Service -> Data Access Layer
    draw.line([1140, 250, 1200, 350], fill="#7C3AED", width=2)
    draw_lolipop(1200, 350, "IDataAccess")
    draw.line([1208, 350, 1260, 350], fill="#7C3AED", width=2)
    draw.line([1140, 530, 1200, 420], fill="#7C3AED", width=2)
    draw_lolipop(1200, 420, "IDataAccess")
    draw.line([1208, 420, 1260, 420], fill="#7C3AED", width=2)

    # База данных за пределами
    draw.rectangle([1590, 320, 1740, 440], fill="#F1F5F9", outline="#0F172A", width=2)
    draw.text((1665, 380), "PostgreSQL 16\nDatabase Engine", fill="#0F172A", font=f_bold, anchor="mm", align="center")
    draw.line([1530, 390, 1590, 390], fill="#0F172A", width=2)
    draw.text((1560, 370), "TCP 5432", fill="#475569", font=f_mono, anchor="mm")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG", dpi=(300, 300))
    print(f"Component diagram saved: {output_path}")


def draw_deployment_diagram(output_path):
    w, h = 1800, 1100
    img = Image.new("RGB", (w, h), "#F8FAFC")
    draw = ImageDraw.Draw(img)
    f_title, f_sub, f_box, f_text, f_bold, f_mono, f_rel = get_fonts()

    draw.text((w // 2, 35), "UML Диаграмма развёртывания (Deployment Diagram)", fill="#0F172A", font=f_title, anchor="mm")
    draw.text((w // 2, 70), "Физическая инфраструктура, контейнеризация Docker и сетевые протоколы «TaskPulse»", fill="#475569", font=f_sub, anchor="mm")

    def draw_3d_node(x, y, nw, nh, depth=20, fill="#FFFFFF", outline="#0284C7", title="«device»"):
        # Фронтальный прямоугольник
        draw.rectangle([x, y + depth, x + nw - depth, y + nh], fill=fill, outline=outline, width=2)
        # Верхняя грань
        draw.polygon([(x, y + depth), (x + depth, y), (x + nw, y), (x + nw - depth, y + depth)], fill="#E2E8F0", outline=outline)
        # Правая грань
        draw.polygon([(x + nw - depth, y + depth), (x + nw, y), (x + nw, y + nh - depth), (x + nw - depth, y + nh)], fill="#CBD5E1", outline=outline)
        draw.text((x + (nw - depth) // 2, y + depth + 18), title, fill="#0F172A", font=f_bold, anchor="mm")

    # Узел 1: Клиентская рабочая станция
    draw_3d_node(100, 260, 420, 480, title="«device: Workstation»\nClient PC / Browser")
    draw.rectangle([140, 360, 440, 520], fill="#EFF6FF", outline="#2563EB", width=2)
    draw.text((290, 390), "«execution environment»\nChromium / Firefox Browser", fill="#1E3A8A", font=f_bold, anchor="mm", align="center")
    draw.rectangle([160, 430, 420, 490], fill="#FFFFFF", outline="#2563EB")
    draw.text((290, 460), "«artifact»\nTaskPulse Web SPA (React)", fill="#0F172A", font=f_mono, anchor="mm", align="center")

    # Узел 2: Сервер приложений Docker Host
    draw_3d_node(640, 180, 540, 680, title="«device: App Server Host»\nLinux / Docker Engine Node")
    
    # Контейнер 1: Web App & API
    draw.rectangle([680, 280, 1100, 460], fill="#F0FDF4", outline="#16A34A", width=2)
    draw.text((890, 305), "«container: Docker»\nTaskPulse App Server (Port 3000)", fill="#166534", font=f_bold, anchor="mm", align="center")
    draw.rectangle([700, 340, 1080, 440], fill="#FFFFFF", outline="#16A34A")
    draw.text((890, 390), "«artifact»\nAPI Core & Webhook Engine\n(Node.js / Python Runtime)", fill="#0F172A", font=f_mono, anchor="mm", align="center")

    # Контейнер 2: Background Workers
    draw.rectangle([680, 500, 1100, 640], fill="#FFF7ED", outline="#EA580C", width=2)
    draw.text((890, 525), "«container: Docker»\nAsync Worker & Burndown Engine", fill="#9A3412", font=f_bold, anchor="mm", align="center")
    draw.rectangle([700, 560, 1080, 620], fill="#FFFFFF", outline="#EA580C")
    draw.text((890, 590), "«artifact»\nAnalytics Calculator Service", fill="#0F172A", font=f_mono, anchor="mm")

    # Узел 3: Сервер базы данных
    draw_3d_node(1300, 260, 420, 480, title="«device: Database Server»\nDedicated Storage Node")
    draw.rectangle([1340, 360, 1640, 540], fill="#FAF5FF", outline="#7C3AED", width=2)
    draw.text((1490, 390), "«container: Docker»\nPostgreSQL 16 Alpine", fill="#5B21B6", font=f_bold, anchor="mm", align="center")
    draw.rectangle([1360, 430, 1620, 510], fill="#FFFFFF", outline="#7C3AED")
    draw.text((1490, 470), "«artifact / database»\ntaskpulse_db (ACID Data)", fill="#0F172A", font=f_mono, anchor="mm", align="center")

    # Сетевые соединения
    # Клиент -> Сервер (HTTPS 443)
    draw.line([500, 440, 680, 390], fill="#2563EB", width=3)
    draw.text((590, 395), "HTTPS / WSS (443)\nTLS 1.3 encrypted", fill="#2563EB", font=f_mono, anchor="mm", align="center")

    # Сервер -> БД (TCP 5432)
    draw.line([1100, 390, 1340, 440], fill="#7C3AED", width=3)
    draw.text((1220, 395), "TCP / IP (5432)\nInternal Docker Network", fill="#7C3AED", font=f_mono, anchor="mm", align="center")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG", dpi=(300, 300))
    print(f"Deployment diagram saved: {output_path}")


def draw_activity_diagram(output_path):
    w, h = 1800, 1200
    img = Image.new("RGB", (w, h), "#F8FAFC")
    draw = ImageDraw.Draw(img)
    f_title, f_sub, f_box, f_text, f_bold, f_mono, f_rel = get_fonts()

    draw.text((w // 2, 35), "UML Диаграмма деятельности (Activity Diagram)", fill="#0F172A", font=f_title, anchor="mm")
    draw.text((w // 2, 70), "Бизнес-процесс: Смена статуса задачи на Kanban-доске, проверка WIP-лимитов и списание времени", fill="#475569", font=f_sub, anchor="mm")

    # Свимлейны (Разработчик и Система)
    draw.rectangle([140, 110, 880, 1150], fill="#FFFFFF", outline="#CBD5E1", width=2)
    draw.rectangle([140, 110, 880, 150], fill="#E2E8F0")
    draw.text((510, 130), "Свимлейн: Разработчик / Исполнитель", fill="#0F172A", font=f_bold, anchor="mm")

    draw.rectangle([880, 110, 1660, 1150], fill="#FFFFFF", outline="#CBD5E1", width=2)
    draw.rectangle([880, 110, 1660, 150], fill="#E2E8F0")
    draw.text((1270, 130), "Свимлейн: Сервер TaskPulse & Валидаторы", fill="#0F172A", font=f_bold, anchor="mm")

    def draw_action(x, y, text, aw=260, ah=50, bg="#F0F9FF", border="#0284C7"):
        r = 15
        draw.rounded_rectangle([x - aw // 2, y - ah // 2, x + aw // 2, y + ah // 2], radius=r, fill=bg, outline=border, width=2)
        draw.text((x, y), text, fill="#0F172A", font=f_text, anchor="mm", align="center")

    def draw_decision(x, y, text="", size=28):
        draw.polygon([(x, y - size), (x + size, y), (x, y + size), (x - size, y)], fill="#FEF3C7", outline="#D97706", width=2)
        if text:
            draw.text((x, y - size - 12), text, fill="#B45309", font=f_mono, anchor="mm")

    # Начальный узел
    draw.ellipse([510 - 15, 180 - 15, 510 + 15, 180 + 15], fill="#0F172A")
    draw.line([510, 195, 510, 230], fill="#0F172A", width=2)

    # 1. Захват карточки
    draw_action(510, 255, "1. Захватить карточку задачи\nв колонке «To Do»")
    draw.line([510, 280, 510, 325], fill="#0F172A", width=2)

    # 2. Перетаскивание
    draw_action(510, 350, "2. Перетащить карточку в\nколонку «In Progress»")
    draw.line([640, 350, 1270, 350], fill="#0F172A", width=2) # переход в свимлейн сервера

    # 3. Сервер: Проверка WIP
    draw_action(1270, 350, "3. Проверить WIP-лимит\nколонки «In Progress»")
    draw.line([1270, 375, 1270, 420], fill="#0F172A", width=2)

    # Ветвление 1: Лимит превышен?
    draw_decision(1270, 448, "WIP лимит превышен?")
    
    # Да -> Алерт
    draw.line([1270 - 28, 448, 510, 448], fill="#D97706", width=2)
    draw.text((900, 435), "[Превышен]", fill="#D97706", font=f_mono)
    draw_action(510, 510, "4a. Отобразить модальное окно\nс предупреждением о перегрузке", bg="#FFFBEB", border="#D97706")
    draw.line([510, 535, 510, 570], fill="#D97706", width=2)

    # Ветвление 2: Подтвердить перегрузку?
    draw_decision(510, 598, "Подтвердить?")
    draw.line([510 + 28, 598, 1270, 598], fill="#059669", width=2)
    draw.text((800, 585), "[Подтверждено тимлидом]", fill="#059669", font=f_mono)
    
    # Нет -> слияние
    draw.line([1270, 476, 1270, 650], fill="#059669", width=2)
    draw.text((1285, 490), "[Не превышен]", fill="#059669", font=f_mono)

    # 5. Сервер: Смена статуса
    draw_action(1270, 675, "5. Обновить статус тикета на IN_PROGRESS,\nзафиксировать время старта в БД")
    draw.line([1270, 700, 510, 740], fill="#0F172A", width=2)

    # 6. Разработчик: Выполнение работы
    draw_action(510, 765, "6. Выполнить написание\nпрограммного кода задачи")
    draw.line([510, 790, 510, 830], fill="#0F172A", width=2)

    # 7. Открыть форму логирования
    draw_action(510, 855, "7. Открыть форму списания времени\nи указать часы (напр. 2h 30m)")
    draw.line([640, 855, 1270, 855], fill="#0F172A", width=2)

    # 8. Сервер: Валидация времени
    draw_action(1270, 855, "8. Валидировать формат и\nдлительность списания")
    draw.line([1270, 880, 1270, 920], fill="#0F172A", width=2)

    # 9. Сервер: Сохранение Worklog
    draw_action(1270, 945, "9. Записать Worklog в БД, пересчитать\nspent_minutes и remaining_minutes")
    draw.line([1270, 970, 1270, 1020], fill="#0F172A", width=2)

    # 10. Обновление графиков
    draw_action(1270, 1045, "10. Актуализировать Burndown\nи табель Timesheet")
    draw.line([1270, 1070, 1270, 1100], fill="#0F172A", width=2)

    # Конечный узел
    draw.ellipse([1270 - 18, 1118 - 18, 1270 + 18, 1118 + 18], fill="#FFFFFF", outline="#0F172A", width=2)
    draw.ellipse([1270 - 12, 1118 - 12, 1270 + 12, 1118 + 12], fill="#0F172A")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG", dpi=(300, 300))
    print(f"Activity diagram saved: {output_path}")


def draw_state_machine_diagram(output_path):
    w, h = 1800, 900
    img = Image.new("RGB", (w, h), "#F8FAFC")
    draw = ImageDraw.Draw(img)
    f_title, f_sub, f_box, f_text, f_bold, f_mono, f_rel = get_fonts()

    draw.text((w // 2, 35), "UML Диаграмма состояний (State Machine Diagram)", fill="#0F172A", font=f_title, anchor="mm")
    draw.text((w // 2, 70), "Жизненный цикл сущности «Task» (Задача) на Kanban-доске программного комплекса «TaskPulse»", fill="#475569", font=f_sub, anchor="mm")

    states = [
        {"id": "backlog", "name": "BACKLOG\n(В бэклоге)", "x": 300, "y": 300, "w": 180, "h": 70, "color": "#64748B"},
        {"id": "todo", "name": "TO_DO\n(К выполнению)", "x": 620, "y": 300, "w": 180, "h": 70, "color": "#0284C7"},
        {"id": "in_prog", "name": "IN_PROGRESS\n(В работе)", "x": 950, "y": 300, "w": 200, "h": 70, "color": "#F59E0B"},
        {"id": "review", "name": "CODE_REVIEW\n(Код-ревью)", "x": 1280, "y": 300, "w": 200, "h": 70, "color": "#8B5CF6"},
        {"id": "done", "name": "DONE\n(Завершено)", "x": 1580, "y": 300, "w": 180, "h": 70, "color": "#10B981"}
    ]

    for s in states:
        x, y, sw, sh = s["x"], s["y"], s["w"], s["h"]
        draw.rounded_rectangle([x - sw // 2, y - sh // 2, x + sw // 2, y + sh // 2], radius=15, fill="#FFFFFF", outline=s["color"], width=3)
        draw.text((x, y), s["name"], fill="#0F172A", font=f_box, anchor="mm", align="center")

    # Начальный узел
    draw.ellipse([100 - 14, 300 - 14, 100 + 14, 300 + 14], fill="#0F172A")
    draw.line([114, 300, 210, 300], fill="#0F172A", width=2)
    draw.text((160, 280), "createTask()", fill="#0F172A", font=f_mono, anchor="mm")

    # 1. Backlog -> To Do
    draw.line([390, 300, 530, 300], fill="#0F172A", width=2)
    draw.polygon([(530, 300), (515, 294), (515, 306)], fill="#0F172A")
    draw.text((460, 280), "addToSprint()", fill="#0F172A", font=f_mono, anchor="mm")

    # 2. To Do -> In Progress
    draw.line([710, 300, 850, 300], fill="#0F172A", width=2)
    draw.polygon([(850, 300), (835, 294), (835, 306)], fill="#0F172A")
    draw.text((780, 280), "startWork() [wip_ok]", fill="#0F172A", font=f_mono, anchor="mm")

    # 3. In Progress -> Code Review
    draw.line([1050, 300, 1180, 300], fill="#0F172A", width=2)
    draw.polygon([(1180, 300), (1165, 294), (1165, 306)], fill="#0F172A")
    draw.text((1115, 280), "submitReview() / PR", fill="#0F172A", font=f_mono, anchor="mm")

    # 4. Code Review -> Done
    draw.line([1380, 300, 1490, 300], fill="#0F172A", width=2)
    draw.polygon([(1490, 300), (1475, 294), (1475, 306)], fill="#0F172A")
    draw.text((1435, 280), "approve() / merge", fill="#0F172A", font=f_mono, anchor="mm")

    # Конечный узел
    draw.line([1670, 300, 1720, 300], fill="#0F172A", width=2)
    draw.ellipse([1740 - 18, 300 - 18, 1740 + 18, 300 + 18], fill="#FFFFFF", outline="#0F172A", width=2)
    draw.ellipse([1740 - 12, 300 - 12, 1740 + 12, 300 + 12], fill="#0F172A")

    # Обратные переходы (Альтернативные потоки):
    # 5. Code Review -> In Progress (Правки по ревью)
    draw.arc([950, 335, 1280, 470], start=0, end=180, fill="#E11D48", width=2)
    draw.polygon([(950, 402), (965, 396), (965, 408)], fill="#E11D48")
    draw.text((1115, 440), "requestChanges() [defect_found]", fill="#E11D48", font=f_mono, anchor="mm")

    # 6. Done -> In Progress (Reopen при обнаружении регрессии)
    draw.arc([950, 335, 1580, 600], start=0, end=180, fill="#DC2626", width=2)
    draw.polygon([(950, 467), (965, 461), (965, 473)], fill="#DC2626")
    draw.text((1265, 560), "reopenTask() [bug_reported]", fill="#DC2626", font=f_mono, anchor="mm")

    # 7. In Progress -> To Do (Возврат при блокировке задачи)
    draw.arc([620, 335, 950, 430], start=0, end=180, fill="#64748B", width=2)
    draw.polygon([(620, 382), (635, 376), (635, 388)], fill="#64748B")
    draw.text((785, 410), "blockTask()", fill="#64748B", font=f_mono, anchor="mm")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG", dpi=(300, 300))
    print(f"State Machine diagram saved: {output_path}")


def draw_communication_diagram(output_path):
    w, h = 1800, 1000
    img = Image.new("RGB", (w, h), "#F8FAFC")
    draw = ImageDraw.Draw(img)
    f_title, f_sub, f_box, f_text, f_bold, f_mono, f_rel = get_fonts()

    draw.text((w // 2, 35), "UML Диаграмма кооперации (Communication Diagram)", fill="#0F172A", font=f_title, anchor="mm")
    draw.text((w // 2, 70), "Сценарий: Прием Git-вебхука, валидация сигнатуры, автопривязка коммита и сдвиг статуса задачи", fill="#475569", font=f_sub, anchor="mm")

    objects = [
        {"id": "git", "name": ":GitServer\n(GitHub/GitLab)", "x": 200, "y": 450, "w": 240, "h": 90, "color": "#334155"},
        {"id": "hook", "name": ":WebhookController\n(API Router)", "x": 650, "y": 250, "w": 260, "h": 90, "color": "#E11D48"},
        {"id": "task_svc", "name": ":TaskService\n(Domain Core)", "x": 1150, "y": 250, "w": 260, "h": 90, "color": "#2563EB"},
        {"id": "repo", "name": ":TaskRepository\n(Data Mapper)", "x": 1150, "y": 650, "w": 260, "h": 90, "color": "#7C3AED"},
        {"id": "db", "name": ":PostgreSQLDatabase\n(Persistent Store)", "x": 650, "y": 650, "w": 260, "h": 90, "color": "#0F172A"},
    ]

    for o in objects:
        x, y, ow, oh = o["x"], o["y"], o["w"], o["h"]
        draw.rectangle([x - ow // 2, y - oh // 2, x + ow // 2, y + oh // 2], fill="#FFFFFF", outline=o["color"], width=2)
        draw.rectangle([x - ow // 2, y - oh // 2, x + ow // 2, y - oh // 2 + 28], fill=o["color"])
        draw.text((x, y - oh // 2 + 14), o["name"].split("\n")[0], fill="#FFFFFF", font=f_bold, anchor="mm")
        draw.text((x, y + 14), o["name"].split("\n")[1], fill="#0F172A", font=f_mono, anchor="mm")

    # Связи между объектами
    # Git -> Hook
    draw.line([320, 420, 520, 290], fill="#0F172A", width=2)
    draw.text((380, 330), "1: POST /api/webhooks/git (payload, hmac) ->", fill="#0F172A", font=f_mono)

    # Hook -> TaskService
    draw.line([780, 250, 1020, 250], fill="#0F172A", width=2)
    draw.text((900, 220), "2: processCommit(sha, key, msg) ->", fill="#2563EB", font=f_mono, anchor="mm")
    draw.text((900, 275), "<- 6: return CommitLinkedResult", fill="#059669", font=f_mono, anchor="mm")

    # TaskService -> TaskRepository
    draw.line([1150, 295, 1150, 605], fill="#0F172A", width=2)
    draw.text((1165, 420), "3: findByIssueKey(key) ->\n4: saveGitEvent(event) ->\n5: updateStatus(REVIEW) ->", fill="#7C3AED", font=f_mono)

    # TaskRepository -> Database
    draw.line([1020, 650, 780, 650], fill="#0F172A", width=2)
    draw.text((900, 630), "<- 3.1: SQL SELECT task", fill="#0F172A", font=f_mono, anchor="mm")
    draw.text((900, 675), "4.1: SQL INSERT & UPDATE ->", fill="#0F172A", font=f_mono, anchor="mm")

    # Hook -> Git
    draw.text((340, 470), "<- 7: 200 OK (Event Processed)", fill="#059669", font=f_mono)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG", dpi=(300, 300))
    print(f"Communication diagram saved: {output_path}")


if __name__ == "__main__":
    base = r"C:\Users\paha2\.gemini\antigravity\scratch\taskpulse-tracker\docs\diagrams"
    draw_class_diagram(os.path.join(base, "class.png"))
    draw_component_diagram(os.path.join(base, "component.png"))
    draw_deployment_diagram(os.path.join(base, "deployment.png"))
    draw_activity_diagram(os.path.join(base, "activity.png"))
    draw_state_machine_diagram(os.path.join(base, "state-machine.png"))
    draw_communication_diagram(os.path.join(base, "communication.png"))
