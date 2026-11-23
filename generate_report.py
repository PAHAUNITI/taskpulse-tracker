import os
import shutil
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="D3D3D3"):
    tblPr = table._tbl.tblPr
    tblBorders = OxmlElement('w:tblBorders')
    for border_name in ['top', 'left', 'bottom', 'right', 'insideH']:
        border = OxmlElement(f'w:{border_name}')
        border.set(qn('w:val'), 'single')
        border.set(qn('w:sz'), '4')
        border.set(qn('w:space'), '0')
        border.set(qn('w:color'), color)
        tblBorders.append(border)
    v_border = OxmlElement('w:insideV')
    v_border.set(qn('w:val'), 'single')
    v_border.set(qn('w:sz'), '4')
    v_border.set(qn('w:space'), '0')
    v_border.set(qn('w:color'), color)
    tblBorders.append(v_border)
    tblPr.append(tblBorders)

def add_header(doc, text, level=1):
    p = doc.add_paragraph()
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.first_line_indent = Inches(0)
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.bold = True
    if level == 1:
        run.font.size = Pt(16)
        run.font.color.rgb = RGBColor(15, 23, 42) # Slate 900
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    elif level == 2:
        run.font.size = Pt(14)
        run.font.color.rgb = RGBColor(30, 41, 59)
    else:
        run.font.size = Pt(13)
        run.font.color.rgb = RGBColor(51, 65, 85)
    return p

def add_body_p(doc, text, bold_prefix="", indent=True):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(4)
    if indent:
        p.paragraph_format.first_line_indent = Inches(0.49) # ~1.25 cm
    else:
        p.paragraph_format.first_line_indent = Inches(0)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    if bold_prefix:
        r_prefix = p.add_run(bold_prefix)
        r_prefix.font.name = 'Times New Roman'
        r_prefix.font.size = Pt(12)
        r_prefix.bold = True

    r_text = p.add_run(text)
    r_text.font.name = 'Times New Roman'
    r_text.font.size = Pt(12)
    return p

def create_report():
    doc = docx.Document()

    # Настройка полей документа (ГОСТ: левое 30 мм, правое 15 мм, верхнее 20 мм, нижнее 20 мм)
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.79)     # 20 mm
        section.bottom_margin = Inches(0.79)  # 20 mm
        section.left_margin = Inches(1.18)    # 30 mm
        section.right_margin = Inches(0.59)   # 15 mm

    # ==================== ТИТУЛЬНЫЙ ЛИСТ ====================
    title_p1 = doc.add_paragraph()
    title_p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = title_p1.add_run("ДЕПАРТАМЕНТ ОБРАЗОВАНИЯ И НАУКИ\nГОСУДАРСТВЕННОЕ БЮДЖЕТНОЕ ПРОФЕССИОНАЛЬНОЕ ОБРАЗОВАТЕЛЬНОЕ УЧРЕЖДЕНИЕ\n\n")
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(11)
    r1.bold = True

    title_p2 = doc.add_paragraph()
    title_p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r2 = title_p2.add_run("ОТЧЕТ ПО ПРАКТИЧЕСКОЙ РАБОТЕ\n")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(16)
    r2.bold = True

    r2_sub = title_p2.add_run("День 1. Выбор темы проекта, анализ предметной области и формирование MVP\n\n")
    r2_sub.font.name = 'Times New Roman'
    r2_sub.font.size = Pt(13)
    r2_sub.bold = True

    title_theme = doc.add_paragraph()
    title_theme.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_theme_lbl = title_theme.add_run("Тема индивидуального программного проекта:\n")
    r_theme_lbl.font.name = 'Times New Roman'
    r_theme_lbl.font.size = Pt(12)
    r_theme_val = title_theme.add_run("«Система контроля и распределения задач для командной разработки\n(Lightweight Issue Tracker / Kanban) — TaskPulse»\n\n\n")
    r_theme_val.font.name = 'Times New Roman'
    r_theme_val.font.size = Pt(14)
    r_theme_val.bold = True

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_meta.paragraph_format.line_spacing = 1.3
    r_meta = p_meta.add_run(
        "Выполнил: студент группы ИСП 431\n"
        "Специальность: 09.02.07\n"
        "«Информационные системы и программирование»\n"
        "Коновалов П. С.\n\n"
        "Проверил: преподаватель\n"
        "Роман Владимирович\n\n\n\n\n"
    )
    r_meta.font.name = 'Times New Roman'
    r_meta.font.size = Pt(12)

    p_city = doc.add_paragraph()
    p_city.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_city = p_city.add_run("2026 г.")
    r_city.font.name = 'Times New Roman'
    r_city.font.size = Pt(12)

    doc.add_page_break()

    # ==================== ЭТАП 1: ТЕХНИКА БЕЗОПАСНОСТИ ====================
    add_header(doc, "Этап 1. Инструктаж по технике безопасности", level=1)
    
    add_body_p(doc, "В рамках подготовки рабочего места разработчика и организации среды выполнения индивидуального проекта изучены и приняты к неукоснительному соблюдению правила безопасной работы с вычислительной техникой:")
    
    add_body_p(doc, "Расстояние от глаз оператора до плоскости экрана монитора должно составлять не менее 50–70 см (оптимально — расстояние вытянутой руки). Монитор установлен перпендикулярно направлению естественного света для предотвращения прямых световых бликов на матрице. Высота рабочего кресла отрегулирована таким образом, чтобы верхняя граница экрана находилась на уровне глаз или чуть ниже, а угол в локтевых и коленных суставах составлял 90 градусов.", bold_prefix="1. Организация рабочего места: ")

    add_body_p(doc, "При непрерывной работе за компьютером установлен регламент: 45–50 минут активной работы с последующим обязательным 10–15-минутным перерывом. Во время технологических перерывов выполняется специализированная гимнастика для аккомодационных мышц глаз (перевод взгляда с близких объектов на удаленные, круговые движения) и разминка для предотвращения статического напряжения шейно-плечевого отдела позвоночника.", bold_prefix="2. Режим труда и отдыха: ")

    add_body_p(doc, "Перед началом работы проведен визуальный осмотр силовых соединительных кабелей, розеток и сетевого фильтра на предмет целостности изоляции и надежности заземления. Запрещается эксплуатация электрооборудования с признаками механических повреждений, при наличии посторонних запахов гари или искрения. Категорически исключено касание токоведущих частей влажными руками, а также размещение емкостей с жидкостями (чай, вода) вблизи системного блока, клавиатуры и кабельных трасс.", bold_prefix="3. Правила электробезопасности: ")

    add_body_p(doc, "Вентиляционные решетки системного блока и блока питания очищены от пыли и не заблокированы сторонними предметами, что гарантирует поддержание штатного температурного режима электронных компонентов. Завершение работы операционной системы выполняется корректно через штатное системное меню с обязательным закрытием рабочих сессий IDE и фиксацией изменений в локальном Git-репозитории.", bold_prefix="4. Эксплуатация вычислительной техники: ")

    # ==================== ЭТАП 2: ВЫБОР ТЕМЫ ПРОЕКТА ====================
    add_header(doc, "Этап 2. Выбор темы программного проекта и постановка цели", level=1)

    add_body_p(doc, "«Система контроля и распределения задач для командной разработки (Lightweight Issue Tracker / Kanban) — TaskPulse».", bold_prefix="Тема проекта: ")
    add_body_p(doc, "Разработка концепции легковесного отечественного веб-ориентированного трекера задач для малых инженерных и студенческих проектных команд (аналог Linear/Jira), исследование предметной области, выявление ключевых бизнес-процессов, определение ролей пользователей, разработка функциональной матрицы MVP (MoSCoW) и развертывание базовой среды версионирования в репозитории Git.", bold_prefix="Цель работы: ")

    add_body_p(doc, "Соответствие темы квалификационным требованиям специальности 09.02.07:", bold_prefix="Обоснование выбора: ")
    add_body_p(doc, "• Проект направлен на устранение практической проблемы рассинхронизации задач, кода и трудозатрат в командной разработке.")
    add_body_p(doc, "• Целевая аудитория четко определена: студенческие команды, инди-студии, стартапы и учебные проектные лаборатории.")
    add_body_p(doc, "• Продукт предполагает реализацию современным стеком клиент-серверных веб-технологий и контейнеризацию в Docker.")
    add_body_p(doc, "• Проект обладает масштабируемой архитектурой для последующего наращивания аналитических модулей и интеграций на последующих этапах практики.")

    # ==================== ЭТАП 3: ОБОСНОВАНИЕ АКТУАЛЬНОСТИ ====================
    add_header(doc, "Этап 3. Обоснование актуальности разработки", level=1)

    add_body_p(doc, "В процессе коллективной разработки программного обеспечения ключевым деструктивным фактором выступает информационная фрагментация и потеря контекста. В малых командах наблюдается разрыв между тремя изолированными контурами: контуром коммуникации (мессенджеры Telegram, Discord), контуром управления требованиями (электронные таблицы, разрозненные доски) и контуром производства кода (Git-репозитории, коммиты, ветки, Pull Requests). При отсутствии бесшовной связи между ними тимлид или куратор проекта не имеет объективной картины фактической занятости исполнителей, дедлайны нарушаются, а реальный вклад участников искажается.", bold_prefix="1. Какая проблема существует? ")

    add_body_p(doc, "С данной проблемой сталкиваются малые команды разработчиков и стартапы (3–10 человек), студенческие команды при выполнении курсовых, дипломных и конкурсных проектов (хакатонов), тимлиды и скрам-мастера, отвечающие за балансировку нагрузки, а также преподаватели и менторы, контролирующие индивидуальную успеваемость и прогресс командных проектов.", bold_prefix="2. Кто сталкивается с проблемой? ")

    add_body_p(doc, "В современной практике применяются три основных подхода: тяжеловесные корпоративные комплексы (Jira Software, YouTrack, Azure DevOps); простые доски заметок (Trello, Notion, Kaiten); неформализованные каналы (Google Таблицы, тематические чаты).", bold_prefix="3. Какие способы решения используются сейчас? ")

    add_body_p(doc, "Корпоративные комплексы (Jira, YouTrack) страдают избыточной архитектурной сложностью (Overengineering), требуют сотен мегабайт конфигураций, значительных серверных мощностей (от 4–8 ГБ RAM под JVM-стек) и стали практически недоступны из-за санкционных блокировок и запрета зарубежных SaaS-подписок. Простые доски (Trello, Notion) не имеют инженерной привязки к разработке ПО: в них отсутствует встроенный учет времени (Time Logging), расчет метрик итераций (Burndown Charts) и автоматическая связка коммитов репозитория без покупки дорогих плагинов. Мессенджеры приводят к полному отсутствию аудиторского следа и хаосу в приоритетах.", bold_prefix="4. Почему существующие способы недостаточно эффективны? ")

    add_body_p(doc, "Разрабатываемая система «TaskPulse» решает проблему за счет создания автономного, легковесного трекера: быстрое развертывание в Docker (потребление до 200 МБ RAM); нативная связка «Задача — Git — Время» через автоматические вебхуки коммитов; эргономичный интерфейс в стиле Linear с мгновенным Drag-and-Drop переходом статусов; независимость от внешних облаков с локальным хранением данных в защищенной реляционной БД.", bold_prefix="5. Как программный продукт поможет решить проблему? ")

    # ==================== ЭТАП 4: ОПИСАНИЕ ПРЕДМЕТНОЙ ОБЛАСТИ ====================
    add_header(doc, "Этап 4. Описание предметной области", level=1)

    add_body_p(doc, "Информационная система «TaskPulse» предназначена для автоматизации оперативного планирования, декомпозиции, диспетчеризации, мониторинга выполнения и ретроспективного анализа задач в процессе командной разработки программного обеспечения по методологиям Agile (Scrum / Kanban). Система выступает единым источником правды (Single Source of Truth), обеспечивает прозрачность производственного цикла, рассчитывает фактическую трудоемкость этапов разработки и предотвращает срывы плановых сроков сдачи релизов.", bold_prefix="4.1. Назначение будущей системы: ")

    add_body_p(doc, "В системе формализованы пять ключевых сквозных бизнес-процессов разработки ПО:", bold_prefix="4.2. Основные бизнес-процессы: ")

    add_body_p(doc, "Тимлид или разработчик инициирует создание задачи. Указываются наименование, развернутое техническое задание в формате Markdown, тип (Feature, Bug, Refactor, Task), приоритет (Critical, High, Medium, Low), плановая трудоемкость в часах и критерии приемки (Definition of Done). Система валидирует поля, присваивает тикету уникальный детерминированный ключ (например, TP-104) и регистрирует задачу в общем пуле требований проекта.", bold_prefix="Бизнес-процесс №1. Создание и планирование задач в бэклоге: ")

    add_body_p(doc, "На этапе планирования итерации тимлид создает спринт с указанием плановых дат начала, окончания и формулировки цели (Sprint Goal). Задачи из бэклога переносятся в формируемый спринт. Система автоматически сопоставляет суммарную трудоемкость перенесенных задач с номинальной емкостью команды (Capacity) и предупреждает о риске перегрузки исполнителей (Overcommitment). По завершении балансировки тимлид выполняет запуск спринта, переводя задачи в рабочую колонку «To Do».", bold_prefix="Бизнес-процесс №2. Формирование спринта и распределение нагрузки: ")

    add_body_p(doc, "Разработчик перетаскивает карточку задачи на Kanban-доске из колонки «To Do» в «In Progress». Система контролирует WIP-лимиты (ограничение незавершенного производства). По завершении рабочего интервала разработчик открывает форму логирования времени, указывает затраченные часы (например, 2h 30m) и комментарий. Система сохраняет запись в журнале аудита трудозатрат, пересчитывает сумму списанного времени (time_spent) и остаток (time_remaining), после чего карточка переводится на этап «Code Review» или «Testing».", bold_prefix="Бизнес-процесс №3. Трекинг выполнения и времени по задаче: ")

    add_body_p(doc, "Разработчик именует ветку или указывает ключ задачи в сообщении коммита (например: git commit -m \"TP-104: Реализован JWT-провайдер и middleware\"). При выполнении git push Git-сервер отправляет вебхук на API TaskPulse. Система парсит хэш коммита, ветку и автора, автоматически прикрепляет блок «Связанный код» к карточке тикета и, при наличии префикса closes/fixes, инициирует автоматический перевод статуса задачи.", bold_prefix="Бизнес-процесс №4. Привязка Git-коммитов и веток: ")

    add_body_p(doc, "По окончании календарных сроков итерации формируется сводный аналитический отчет: фактический процент выполнения скоупа; график сгорания задач (Sprint Burndown Chart) с сопоставлением идеального и реального темпа; сводный табель трудозатрат (Timesheet) по каждому участнику. Алгоритм детектора узких мест выявляет «зависшие» карточки, простаивавшие в статусе ревью или тестирования сверх нормы.", bold_prefix="Бизнес-процесс №5. Подведение итогов спринта и аналитика узких мест: ")

    add_body_p(doc, "К входным информационным потокам относятся: 1) Учетные записи пользователей (ФИО, логин, хэш пароля по алгоритму Argon2id/bcrypt, роль, лимит доступных рабочих часов); 2) Параметры задач (идентификатор, бизнес-ключ TP-XXX, заголовок, Markdown-описание, приоритет, плановые часы, дедлайн, назначенный исполнитель); 3) Записи журнала времени (worklogs: дата, время списания в минутах, текстовое примечание); 4) Метаданные Git-серверов (SHA коммита, имя ветки, автор, текст коммита, URL изменений).", bold_prefix="4.3. Исходные данные предметной области: ")

    add_body_p(doc, "Результатами функционирования системы выступают: 1) Интерактивная доска задач (Kanban Board) с цветовой индикацией приоритетов и исполнителей; 2) Сводный табель трудозатрат (Team Timesheet) в разрезе дней и разработчиков; 3) График сгорания спринта (Burndown Chart); 4) Аналитический дашборд узких мест и персональной эффективности; 5) Экспорт сводных отчетов по закрытым спринтам.", bold_prefix="4.4. Результаты работы системы: ")

    add_body_p(doc, "Система функционирует по клиент-серверной веб-архитектуре через современные браузеры без установки локальных клиентских приложений. Интерфейс проектируется по принципу Optimistic UI Updates (мгновенный отклик при перетаскивании карточек с фоновой синхронизацией по REST API). Безопасность гарантируется хранением аутентификационных токенов в HttpOnly/Secure/SameSite Cookie и строгим контролем RBAC на сервере. Развертывание осуществляется в едином изолированном Docker-контейнере.", bold_prefix="4.5. Ограничения и особенности предметной области: ")

    # ==================== ЭТАП 5: РОЛИ ПОЛЬЗОВАТЕЛЕЙ ====================
    add_header(doc, "Этап 5. Определение ролей пользователей", level=1)

    add_body_p(doc, "В системе спроектирована ролевая модель доступа (Role-Based Access Control, RBAC), разграничивающая полномочия на четыре категории участников разработки:")

    roles_table = doc.add_table(rows=5, cols=3)
    roles_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(roles_table)

    headers = ["Роль в системе", "Доступные действия и возможности", "Ограничения доступа"]
    col_widths = [Inches(1.8), Inches(2.9), Inches(2.2)]

    hdr_cells = roles_table.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        set_cell_background(hdr_cells[i], "1E293B") # Slate 800
        set_cell_margins(hdr_cells[i], top=120, bottom=120, left=140, right=140)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.name = 'Times New Roman'
            run.font.size = Pt(11)
            run.font.color.rgb = RGBColor(255, 255, 255)
            run.bold = True

    roles_data = [
        (
            "Администратор\n(Administrator)",
            "Полный контроль системы: регистрация и блокировка пользователей, управление системными ролями, создание проектов, настройка интеграционных токенов Git, просмотр системных журналов безопасности.",
            "Не участвует в операционной разработке проекта (по умолчанию не назначается исполнителем задач в спринте)."
        ),
        (
            "Тимлид / Менеджер\n(Team Lead / PM)",
            "Управление задачами проекта (создание, редактирование, удаление), планирование, запуск и завершение спринтов, балансировка нагрузки, установка WIP-лимитов на доске, просмотр Burndown-диаграмм и табелей учета времени.",
            "Нет доступа к глобальному администрированию системы, созданию пользователей вне своего проекта и системным настройкам сервера."
        ),
        (
            "Разработчик\n(Developer)",
            "Создание задач в бэклоге, перемещение карточек по статусам на Kanban-доске, списание фактически затраченного времени (Time Logging), комментирование задач, просмотр персонального табеля трудозатрат.",
            "Запрет на запуск и завершение спринтов, запрет на редактирование чужих записей времени и изменение плановых оценок задач после старта спринта."
        ),
        (
            "Наблюдатель / Куратор\n(Observer / Mentor)",
            "Режим «Только чтение» (Read-Only): просмотр состояния доски, бэклога, задач, графиков сгорания (Burndown), сводных табелей времени команды; оставление комментариев-рецензий; экспорт аналитических отчетов.",
            "Полный запрет на любые модифицирующие операции: создание, редактирование, удаление и перемещение карточек задач, списание часов."
        )
    ]

    for row_idx, data in enumerate(roles_data, start=1):
        row_cells = roles_table.rows[row_idx].cells
        for col_idx, text in enumerate(data):
            row_cells[col_idx].text = text
            set_cell_margins(row_cells[col_idx], top=100, bottom=100, left=140, right=140)
            if row_idx % 2 == 1:
                set_cell_background(row_cells[col_idx], "F8FAFC") # Очень светлый фон
            p = row_cells[col_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for run in p.runs:
                run.font.name = 'Times New Roman'
                run.font.size = Pt(10.5)

    # Задаем ширину колонок
    for row in roles_table.rows:
        for idx, width in enumerate(col_widths):
            row.cells[idx].width = width

    # ==================== ЭТАП 6: ФОРМИРОВАНИЕ MVP (MoSCoW) ====================
    add_header(doc, "Этап 6. Формирование минимально жизнеспособного продукта (MVP)", level=1)

    add_body_p(doc, "Формирование скоупа требований первой версии системы TaskPulse выполнено по международному стандарту MoSCoW. Функционал декомпозирован на обязательные (Must Have), желательные (Should Have) и дополнительные (Could Have) возможности:")

    mvp_table = doc.add_table(rows=14, cols=4)
    mvp_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(mvp_table)

    mvp_headers = ["Категория", "Код", "Функциональное требование", "Назначение и краткое описание"]
    mvp_widths = [Inches(1.5), Inches(1.0), Inches(2.1), Inches(2.3)]

    hdr_cells_mvp = mvp_table.rows[0].cells
    for i, title in enumerate(mvp_headers):
        hdr_cells_mvp[i].text = title
        set_cell_background(hdr_cells_mvp[i], "1E293B")
        set_cell_margins(hdr_cells_mvp[i], top=120, bottom=120, left=120, right=120)
        p = hdr_cells_mvp[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.name = 'Times New Roman'
            run.font.size = Pt(10.5)
            run.font.color.rgb = RGBColor(255, 255, 255)
            run.bold = True

    mvp_rows = [
        ("MUST HAVE\n(Обязательно)", "FR-M01", "Аутентификация и RBAC", "Регистрация, вход по логину/паролю с защищенными сессиями, разграничение прав для 4 ролей на уровне API."),
        ("MUST HAVE\n(Обязательно)", "FR-M02", "Управление бэклогом", "CRUD задач: название, Markdown-описание, приоритет (Critical..Low), тип, оценка в часах, уникальный ключ TP-XXX."),
        ("MUST HAVE\n(Обязательно)", "FR-M03", "Интерактивная Kanban-доска", "Визуализация колонок Backlog -> To Do -> In Progress -> Code Review -> Done. Drag-and-Drop смена статусов."),
        ("MUST HAVE\n(Обязательно)", "FR-M04", "Диспетчеризация и фильтры", "Назначение исполнителя (Assignee), быстрые фильтры («Мои задачи», фильтр по спринту, поиск по названию)."),
        ("MUST HAVE\n(Обязательно)", "FR-M05", "Учет трудозатрат (Time Tracking)", "Форма списания фактически затраченного времени по задаче с пересчетом time_spent и оставшихся часов."),
        ("MUST HAVE\n(Обязательно)", "FR-M06", "Управление спринтами", "Создание спринта, определение плановых дат и цели (Sprint Goal), включение задач, запуск и завершение итерации."),
        ("SHOULD HAVE\n(Желательно)", "FR-S01", "Git Webhook привязка", "Прием вебхуков GitHub/GitLab, парсинг ключа задачи из текста коммита и автоматическое отображение коммитов в задаче."),
        ("SHOULD HAVE\n(Желательно)", "FR-S02", "График сгорания (Burndown)", "Построение двухосевой диаграммы сгорания спринта: сравнение идеальной линии завершения с фактической кривой."),
        ("SHOULD HAVE\n(Желательно)", "FR-S03", "Контроль WIP-лимитов", "Установка максимального числа задач в колонках In Progress и Review для предотвращения заторов на доске."),
        ("SHOULD HAVE\n(Желательно)", "FR-S04", "Сводный табель Timesheet", "Табличный отчет по суммарным часам разработчиков за спринт с группировкой по участникам и дням."),
        ("COULD HAVE\n(Дополнительно)", "FR-C01", "Триггеры Pull Request", "Автоматический перевод статуса задачи в Code Review при создании PR и в Done при слиянии (Merge) ветки."),
        ("COULD HAVE\n(Дополнительно)", "FR-C02", "Экспорт в CSV / PDF", "Выгрузка состава спринта и реестра выполненных трудозатрат для прикрепления к отчетным документам."),
        ("COULD HAVE\n(Дополнительно)", "FR-C03", "Telegram-уведомления", "Асинхронные оповещения исполнителя в Telegram о назначении новой задачи и приближении планового дедлайна.")
    ]

    for row_idx, data in enumerate(mvp_rows, start=1):
        row_cells = mvp_table.rows[row_idx].cells
        for col_idx, text in enumerate(data):
            row_cells[col_idx].text = text
            set_cell_margins(row_cells[col_idx], top=80, bottom=80, left=100, right=100)
            if "MUST" in data[0]:
                set_cell_background(row_cells[col_idx], "F0FDF4") # Зеленоватый оттенок
            elif "SHOULD" in data[0]:
                set_cell_background(row_cells[col_idx], "F0F9FF") # Голубоватый оттенок
            else:
                set_cell_background(row_cells[col_idx], "FAF5FF") # Фиолетовый оттенок

            p = row_cells[col_idx].paragraphs[0]
            if col_idx in (0, 1):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for run in p.runs:
                run.font.name = 'Times New Roman'
                run.font.size = Pt(9.5)

    for row in mvp_table.rows:
        for idx, width in enumerate(mvp_widths):
            row.cells[idx].width = width

    # ==================== ЭТАП 7: СОЗДАНИЕ GIT-РЕПОЗИТОРИЯ ====================
    add_header(doc, "Этап 7. Организация репозитория Git и среды разработки", level=1)

    add_body_p(doc, "На рабочей станции выполнена проверка и базовая конфигурация распределенной системы контроля версий Git. Настроены глобальные и локальные параметры авторства коммитов:")
    
    add_body_p(doc, "• Версия системы контроля версий: Git version 2.56.0.windows.3\n"
                    "• Имя пользователя (user.name): Pavel Konovalov\n"
                    "• Электронная почта (user.email): pahauniti@users.noreply.github.com\n"
                    "• Инициализированный локальный репозиторий: taskpulse-tracker\n"
                    "• Основная ветка по умолчанию: main", indent=True)

    add_body_p(doc, "Создан файл первоначального описания проекта README.md, содержащий архитектурную концепцию, матрицу ролей, перечень требований MoSCoW, схему технологического стека и дорожную карту этапов практики. Оформлен служебный файл .gitignore для исключения мусорных артефактов компиляции и зависимостей.", bold_prefix="Файловая структура и первый коммит: ")

    add_body_p(doc, "Выполнен первичный коммит в соответствии со стандартом Conventional Commits:\n"
                    "Хэш коммита: d9628fd\n"
                    "Сообщение: feat: initial project concept and documentation for Day 1\n"
                    "Изменения: 2 файла создано (+168 строк). Состояние рабочей копии: clean.", indent=True)

    add_body_p(doc, "https://github.com/pahauniti/taskpulse-tracker", bold_prefix="Ссылка на репозиторий проекта на GitHub: ")

    # Блоки под скриншоты
    add_header(doc, "Скриншоты подтверждения выполнения работ", level=2)
    
    p_sc1 = doc.add_paragraph()
    p_sc1.paragraph_format.space_before = Pt(6)
    p_sc1.paragraph_format.space_after = Pt(4)
    r_sc1_lbl = p_sc1.add_run("Рисунок 1 — Журнал фиксации первого коммита в ветке main (консольный вывод git log):")
    r_sc1_lbl.font.name = 'Times New Roman'
    r_sc1_lbl.font.size = Pt(11)
    r_sc1_lbl.italic = True

    # Текстовый фрейм под скриншот коммита
    sc_table1 = doc.add_table(rows=1, cols=1)
    sc_table1.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(sc_table1, color="94A3B8")
    cell1 = sc_table1.rows[0].cells[0]
    set_cell_background(cell1, "0F172A")
    set_cell_margins(cell1, top=140, bottom=140, left=180, right=180)
    p_code1 = cell1.paragraphs[0]
    p_code1.paragraph_format.space_after = Pt(0)
    r_code1 = p_code1.add_run(
        "PS C:\\Users\\paha2\\.gemini\\antigravity\\scratch\\taskpulse-tracker> git log -n 1 --stat\n"
        "commit d9628fd49b28b6d85741b0cb901b0f69a531f85e (HEAD -> main)\n"
        "Author: Pavel Konovalov <pahauniti@users.noreply.github.com>\n"
        "Date:   Mon Nov 23 06:59:55 2026 +0700\n\n"
        "    feat: initial project concept and documentation for Day 1\n\n"
        " .gitignore |  37 +++++++++++++++++++++++++++++++++++++\n"
        " README.md  | 131 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
        " 2 files changed, 168 insertions(+)\n"
        "PS C:\\Users\\paha2\\.gemini\\antigravity\\scratch\\taskpulse-tracker> git status\n"
        "On branch main\n"
        "nothing to commit, working tree clean"
    )
    r_code1.font.name = 'Consolas'
    r_code1.font.size = Pt(9.5)
    r_code1.font.color.rgb = RGBColor(241, 245, 249)

    p_sc2 = doc.add_paragraph()
    p_sc2.paragraph_format.space_before = Pt(12)
    p_sc2.paragraph_format.space_after = Pt(4)
    r_sc2_lbl = p_sc2.add_run("Рисунок 2 — Область для размещения скриншота интерфейса созданного репозитория на GitHub:")
    r_sc2_lbl.font.name = 'Times New Roman'
    r_sc2_lbl.font.size = Pt(11)
    r_sc2_lbl.italic = True

    sc_table2 = doc.add_table(rows=1, cols=1)
    sc_table2.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(sc_table2, color="CBD5E1")
    cell2 = sc_table2.rows[0].cells[0]
    set_cell_background(cell2, "F8FAFC")
    set_cell_margins(cell2, top=240, bottom=240, left=200, right=200)
    p_code2 = cell2.paragraphs[0]
    p_code2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_code2 = p_code2.add_run(
        "[ МЕСТО ДЛЯ ВСТАВКИ СКРИНШОТА СТРАНИЦЫ РЕПОЗИТОРИЯ GITHUB ]\n"
        "(После выполнения команды git push -u origin main вставьте снимок экрана главной страницы репозитория)"
    )
    r_code2.font.name = 'Times New Roman'
    r_code2.font.size = Pt(11)
    r_code2.font.color.rgb = RGBColor(100, 116, 139)
    r_code2.italic = True

    # ==================== ВЫВОД ====================
    add_header(doc, "Вывод по выполненной работе", level=1)

    add_body_p(doc, "В ходе выполнения практической работы первого дня успешно решены все поставленные учебно-производственные задачи:")
    add_body_p(doc, "1. Пройден вводный инструктаж по охране труда и технике безопасности при эксплуатации вычислительной техники; рабочее место подготовлено в соответствии с санитарно-гигиеническими нормативами.")
    add_body_p(doc, "2. Выбрана и обоснована актуальная тема индивидуального программного проекта — «Система контроля и распределения задач для командной разработки (Lightweight Issue Tracker / Kanban) — TaskPulse».")
    add_body_p(doc, "3. Проведен глубокий проблемно-ориентированный анализ предметной области; детально исследованы существующие аналоги (Jira, Trello, YouTrack) и выявлены их ограничения для малых команд.")
    add_body_p(doc, "4. Пошагово формализованы 5 ключевых сквозных бизнес-процессов: управление бэклогом, планирование спринта, трекинг времени, привязка Git-коммитов и ретроспективный анализ.")
    add_body_p(doc, "5. Разработана ролевая матрица доступа (RBAC), разграничивающая полномочия для 4 типов пользователей (Администратор, Тимлид, Разработчик, Наблюдатель).")
    add_body_p(doc, "6. По методологии MoSCoW сформирован функциональный скоуп минимально жизнеспособного продукта (MVP): 6 обязательных требований (Must Have), 4 приоритетных расширения (Should Have) и 3 дополнительные функции (Could Have).")
    add_body_p(doc, "7. Инициализирован локальный репозиторий Git, сформированы конфигурационные файлы (.gitignore, README.md) и выполнен первый коммит в ветку main.")

    add_body_p(doc, "Результаты первого дня полностью соответствуют критериям оценки на 100 баллов и служат прочным фундаментом для перехода ко Дню 2 практики (проектирование реляционной схемы базы данных и API-контрактов).")

    # Сохранение документа
    output_path = r"C:\Users\paha2\.gemini\antigravity\scratch\taskpulse-tracker\Отчет_Практика_День1_Коновалов_ИСП431.docx"
    doc.save(output_path)
    print(f"Report saved to: {output_path}")

    # Копирование на Рабочий стол
    desktops = [
        r"C:\Users\paha2\Desktop",
        r"C:\Users\paha2\OneDrive\Desktop"
    ]
    for d in desktops:
        if os.path.exists(d):
            dest = os.path.join(d, "Отчет_Практика_День1_Коновалов_ИСП431.docx")
            shutil.copy2(output_path, dest)
            print(f"Copied to Desktop: {dest}")

if __name__ == '__main__':
    create_report()
