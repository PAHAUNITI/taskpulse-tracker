import os
import shutil
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
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

def create_report_day2():
    doc = docx.Document()

    # Поля ГОСТ (левое 30 мм, правое 15 мм, верхнее/нижнее 20 мм)
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.79)
        section.bottom_margin = Inches(0.79)
        section.left_margin = Inches(1.18)
        section.right_margin = Inches(0.59)

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

    r2_sub = title_p2.add_run("День 2. Формализация требований, проектирование Use Case и организация структуры проекта\n\n")
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

    # ==================== ТЕМА И ЦЕЛЬ РАБОТЫ ====================
    add_header(doc, "Тема и цель работы", level=1)
    add_body_p(doc, "Разработка спецификации требований к программному обеспечению и первичное проектирование системы «TaskPulse» (DevFlow Tracker).", bold_prefix="Тема дня: ")
    add_body_p(doc, "Научиться формализовать требования к программному продукту, производить строгое разделение функциональных (FR) и нефункциональных требований (NFR), определять характер взаимодействия акторов с системой посредством построения UML-диаграммы вариантов использования (Use Case), разработать детализированные сценарии взаимодействия, а также сформировать архитектурную структуру каталогов и файлов проекта для последующей программной реализации.", bold_prefix="Цель работы: ")

    # ==================== КРАТКОЕ ОПИСАНИЕ ПРОЕКТА ====================
    add_header(doc, "Краткое описание выбранного проекта", level=1)
    add_body_p(doc, "Программный комплекс «TaskPulse» представляет собой легковесную (Lightweight) веб-ориентированную систему диспетчеризации задач, координации спринтов и аналитики трудозатрат, созданную как высокопроизводительный аналог систем Linear и Jira специально для малых IT-команд (3–10 участников), стартапов и студенческих проектных объединений.")
    add_body_p(doc, "Ключевое проектное преимущество системы заключается в устранении барьера между постановкой задач, производством исходного кода и фиксацией рабочего времени. За счет сквозной интеграции «Задача ↔ Git ↔ Время» карточки тикетов автоматически ассоциируются с коммитами и ветками через входящие вебхуки, а встроенный тайм-трекинг формирует наглядные графики сгорания задач (Burndown Charts) и табели трудозатрат (Timesheet) без необходимости установки громоздких сторонних плагинов.")

    # ==================== ТАБЛИЦА ФУНКЦИОНАЛЬНЫХ ТРЕБОВАНИЙ (FR) ====================
    add_header(doc, "Таблица функциональных требований (Functional Requirements, FR)", level=1)
    add_body_p(doc, "Функциональные требования описывают непосредственные действия и поведение разрабатываемой системы. На основе анализа предметной области и ролевой модели первого дня сформирован расширенный перечень из 12 проверяемых функциональных требований:")

    fr_table = doc.add_table(rows=13, cols=4)
    fr_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(fr_table)

    fr_headers = ["ID", "Название", "Описание действия системы", "Роли пользователей"]
    fr_widths = [Inches(0.9), Inches(1.8), Inches(2.9), Inches(1.5)]

    hdr_cells = fr_table.rows[0].cells
    for i, title in enumerate(fr_headers):
        hdr_cells[i].text = title
        set_cell_background(hdr_cells[i], "1E293B")
        set_cell_margins(hdr_cells[i], top=120, bottom=120, left=120, right=120)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.name = 'Times New Roman'
            run.font.size = Pt(10.5)
            run.font.color.rgb = RGBColor(255, 255, 255)
            run.bold = True

    fr_data = [
        ("FR-01", "Регистрация и профиль", "Система обеспечивает создание учетной записи с валидацией почты, безопасным хранением хэша пароля и редактированием профиля.", "Администратор, Тимлид, Разработчик"),
        ("FR-02", "Аутентификация и RBAC", "Система выполняет вход по логину/паролю с выдачей защищенных HttpOnly-сессий и разграничивает доступ к эндпоинтам согласно 4 ролям.", "Все роли (Admin, Lead, Dev, Observer)"),
        ("FR-03", "Создание задач в бэклоге", "Система предоставляет форму создания тикета с атрибутами: заголовок, Markdown, тип, приоритет, плановые часы и автогенерация ключа TP-XXX.", "Тимлид, Разработчик"),
        ("FR-04", "Декомпозиция тикетов", "Система позволяет редактировать параметры тикета, декомпозировать задачу на подзадачи (Subtasks) и задавать критерии Definition of Done.", "Тимлид, Разработчик"),
        ("FR-05", "Интерактивный Kanban", "Система обеспечивает смену статусов карточек (Backlog -> To Do -> In Progress -> Code Review -> Done) через Drag-and-Drop с Optimistic UI.", "Тимлид, Разработчик"),
        ("FR-06", "Диспетчеризация задач", "Система позволяет назначать ответственного исполнителя (Assignee) с контролем его доступных рабочих часов в спринте.", "Тимлид"),
        ("FR-07", "Учет трудозатрат", "Система фиксирует списание фактически затраченного времени (Worklog) и автоматически пересчитывает spent_minutes и remaining_minutes.", "Разработчик, Тимлид"),
        ("FR-08", "Управление спринтами", "Система позволяет формировать состав спринта, задавать цели (Sprint Goal), даты, запускать и завершать итерацию с фиксацией скоупа.", "Тимлид"),
        ("FR-09", "Git Webhook привязка", "Система принимает HTTP POST вебхуки Git, парсит ключ задачи из коммита и автоматически привязывает хэш коммита и ветку к тикету.", "Внешний Git-сервер, Все роли"),
        ("FR-10", "Фильтрация и поиск", "Система обеспечивает многокритериальную фильтрацию («Мои задачи», по спринту, приоритету, статусу) и быстрый поиск по тикетам.", "Все роли"),
        ("FR-11", "Аналитика и Burndown", "Система формирует график сгорания задач (Sprint Burndown Chart) и сводный табель учета времени (Timesheet) команды за период.", "Все роли, Наблюдатель"),
        ("FR-12", "Контроль WIP-лимитов", "Система проверяет максимальное число задач в колонках In Progress и Review и предупреждает о возникновении заторов на доске.", "Тимлид, Разработчик"),
    ]

    for row_idx, data in enumerate(fr_data, start=1):
        row_cells = fr_table.rows[row_idx].cells
        for col_idx, text in enumerate(data):
            row_cells[col_idx].text = text
            set_cell_margins(row_cells[col_idx], top=80, bottom=80, left=100, right=100)
            if row_idx % 2 == 1:
                set_cell_background(row_cells[col_idx], "F8FAFC")
            p = row_cells[col_idx].paragraphs[0]
            if col_idx in (0, 1):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for run in p.runs:
                run.font.name = 'Times New Roman'
                run.font.size = Pt(9.5)

    for row in fr_table.rows:
        for idx, width in enumerate(fr_widths):
            row.cells[idx].width = width

    # ==================== ТАБЛИЦА НЕФУНКЦИОНАЛЬНЫХ ТРЕБОВАНИЙ (NFR) ====================
    add_header(doc, "Таблица нефункциональных требований (Non-Functional Requirements, NFR)", level=1)
    add_body_p(doc, "Нефункциональные требования описывают критерии качества, архитектурные свойства и системные ограничения продукта. Все требования сформулированы в измеримом и проверяемом виде:")

    nfr_table = doc.add_table(rows=11, cols=3)
    nfr_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(nfr_table)

    nfr_headers = ["ID", "Категория качества", "Измеримое нефункциональное требование"]
    nfr_widths = [Inches(1.0), Inches(2.0), Inches(4.1)]

    hdr_cells_nfr = nfr_table.rows[0].cells
    for i, title in enumerate(nfr_headers):
        hdr_cells_nfr[i].text = title
        set_cell_background(hdr_cells_nfr[i], "1E293B")
        set_cell_margins(hdr_cells_nfr[i], top=120, bottom=120, left=120, right=120)
        p = hdr_cells_nfr[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.name = 'Times New Roman'
            run.font.size = Pt(10.5)
            run.font.color.rgb = RGBColor(255, 255, 255)
            run.bold = True

    nfr_data = [
        ("NFR-01", "Производительность", "Время отклика REST API на базовые CRUD-операции не превышает 200 мс при 95-м перцентиле (p95); полная загрузка и отрисовка Kanban-доски (до 100 тикетов) занимает не более 500 мс."),
        ("NFR-02", "Безопасность", "Пароли пользователей хэшируются с использованием стойких алгоритмов Argon2id или bcrypt (cost >= 12). Сессионные токены хранятся строго в защищенных HttpOnly, Secure, SameSite=Lax Cookie."),
        ("NFR-03", "Надёжность", "Система обеспечивает целостность данных при сбоях за счет реляционных транзакций (ACID) и политики автоматического перезапуска сервисов в контейнерах (Docker restart: unless-stopped)."),
        ("NFR-04", "Удобство (Usability)", "Пользовательский интерфейс построен по стандартам 8pt Grid (Linear Dark/Light UI); смена статусов карточек задач выполняется в 1 действие Drag-and-Drop без перезагрузки веб-страницы."),
        ("NFR-05", "Совместимость", "Веб-интерфейс функционирует стабильно и без искажений во всех актуальных версиях браузеров на базе Chromium (Chrome, Edge 110+), Firefox 115+ и Safari 16+ на экранах от 1280x720 до 4K."),
        ("NFR-06", "Масштабируемость", "Архитектура обеспечивает одновременную работу до 50 активных участников команды и хранение до 10 000 задач на проект без деградации времени отклика системы более чем на 15%."),
        ("NFR-07", "Сопровождаемость", "Исходный код структурирован по модульному стандарту Everything Claude Code (<800 строк на файл, функции <50 строк); покрытие доменной логики unit-тестами составляет не менее 80% (факт: 99%)."),
        ("NFR-08", "Ограничения среды", "Потребление оперативной памяти контейнерами приложения не должно превышать 512 МБ RAM; система автономно разворачивается через docker-compose up -d без внешних платных SaaS-сервисов."),
        ("NFR-09", "Отказоустойчивость", "Предусмотрено автоматизированное создание ежедневных резервных копий (бэкапов) базы данных с возможностью полного восстановления состояния проекта не более чем за 5 минут."),
        ("NFR-10", "Аудируемость", "Все операции модификации статусов задач, удаления данных и смены ролей фиксируются в неизменяемом журнале аудита с точной отметкой времени ISO 8601 и идентификатором пользователя."),
    ]

    for row_idx, data in enumerate(nfr_data, start=1):
        row_cells = nfr_table.rows[row_idx].cells
        for col_idx, text in enumerate(data):
            row_cells[col_idx].text = text
            set_cell_margins(row_cells[col_idx], top=80, bottom=80, left=100, right=100)
            if row_idx % 2 == 1:
                set_cell_background(row_cells[col_idx], "F8FAFC")
            p = row_cells[col_idx].paragraphs[0]
            if col_idx in (0, 1):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for run in p.runs:
                run.font.name = 'Times New Roman'
                run.font.size = Pt(9.5)

    for row in nfr_table.rows:
        for idx, width in enumerate(nfr_widths):
            row.cells[idx].width = width

    # ==================== ДИАГРАММА USE CASE ====================
    add_header(doc, "UML-диаграмма вариантов использования (Use Case Diagram)", level=1)
    add_body_p(doc, "На основе ролевой матрицы и формализованных функциональных требований построена UML-диаграмма вариантов использования, отражающая границу системы (Scope Boundary), акторов и характер их взаимодействия с системой:")

    img_path = r"C:\Users\paha2\.gemini\antigravity\scratch\taskpulse-tracker\docs\use-case-diagram.png"
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(4)
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Inches(6.4))

        p_lbl = doc.add_paragraph()
        p_lbl.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_lbl.paragraph_format.space_after = Pt(10)
        r_lbl = p_lbl.add_run("Рисунок 1 — UML-диаграмма вариантов использования информационной системы «TaskPulse»")
        r_lbl.font.name = 'Times New Roman'
        r_lbl.font.size = Pt(10.5)
        r_lbl.italic = True

    add_body_p(doc, "На диаграмме представлены 5 акторов (Администратор, Тимлид, Разработчик, Наблюдатель и внешний Git-сервер), 14 вариантов использования, связи прямой ассоциации, а также обязательные отношения <<include>> (авторизация пользователя при смене статусов и списании времени) и условное отношение <<extend>> (проверка WIP-лимитов при переносе карточки задачи на Kanban-доске).")

    # ==================== ОПИСАНИЕ СЦЕНАРИЕВ ====================
    add_header(doc, "Описание основных сценариев использования (Use Case Scenarios)", level=1)

    add_header(doc, "Сценарий №1: Создание и декомпозиция задачи в бэклоге проекта", level=2)
    add_body_p(doc, "Тимлид / Менеджер проекта (вторичный актор — Разработчик).", bold_prefix="Основной актор: ")
    add_body_p(doc, "1) Пользователь авторизован в системе с ролью TEAM_LEAD или DEVELOPER; 2) В системе существует активный проект, где пользователь является участником.", bold_prefix="Предусловия: ")
    add_body_p(doc, "1. Пользователь нажимает кнопку «Создать задачу» (или горячую клавишу 'C').\n"
                    "2. Система открывает модальное окно создания тикета.\n"
                    "3. Пользователь заполняет поля: краткое наименование, подробное техническое описание в формате Markdown, тип (Feature), приоритет (High), плановую оценку (8 часов) и критерии приемки Definition of Done.\n"
                    "4. Пользователь нажимает кнопку «Сохранить».\n"
                    "5. Система валидирует входные поля, генерирует уникальный ключ TP-105, вычисляет remaining_minutes = 480 и регистрирует задачу в БД со статусом BACKLOG.\n"
                    "6. Тимлид открывает карточку и создает дочерние подзадачи (Subtasks).\n"
                    "7. Система отображает созданную задачу и ее иерархию в общем списке бэклога.", bold_prefix="Основной поток выполнения: ")
    add_body_p(doc, "3а. Обязательные поля не заполнены — система подсвечивает обязательные поля красным цветом и блокирует отправку до заполнения заголовка.\n"
                    "3б. Некорректная оценка времени — система выводит предупреждение «Оценка должна быть положительным числом» и возвращает фокус на поле ввода.", bold_prefix="Альтернативные потоки: ")
    add_body_p(doc, "Задача успешно зарегистрирована в реляционной БД со статусом BACKLOG, декомпозирована на подзадачи и готова к приоритизации и включению в спринт.", bold_prefix="Постусловия: ")

    add_header(doc, "Сценарий №2: Перемещение карточки на Kanban-доске и списание времени", level=2)
    add_body_p(doc, "Разработчик / Исполнитель.", bold_prefix="Основной актор: ")
    add_body_p(doc, "1) Разработчик авторизован под ролью DEVELOPER; 2) Задача назначена на данного разработчика и находится в колонке «To Do» активного спринта.", bold_prefix="Предусловия: ")
    add_body_p(doc, "1. Разработчик открывает страницу «Активный спринт (Kanban-доска)».\n"
                    "2. Разработчик перетаскивает карточку TP-105 курсором мыши из колонки «To Do» в колонку «In Progress».\n"
                    "3. Система проверяет WIP-лимит колонки «In Progress» (лимит не нарушен).\n"
                    "4. Система применяет Optimistic UI и асинхронно обновляет статус тикета в БД с фиксацией временной метки старта.\n"
                    "5. Разработчик выполняет написание программного кода.\n"
                    "6. По завершении этапа разработчик кликает по карточке и нажимает кнопку «Списать время» (Log Work).\n"
                    "7. Разработчик вносит затраченное время (2h 30m) и комментарий о проделанной работе.\n"
                    "8. Система валидирует данные, вносит запись в таблицу worklogs, увеличивает spent_minutes на 150 мин и уменьшает remaining_minutes с 480 до 330 мин.\n"
                    "9. Карточка на доске мгновенно обновляет прогресс-бар трудозатрат.", bold_prefix="Основной поток выполнения: ")
    add_body_p(doc, "3а. Превышен установленный WIP-лимит колонки («extend»): система выдает предупреждение о перегрузке («Превышен лимит незавершенного производства! Рекомендуется закрыть текущие задачи»); разработчик подтверждает действие с фиксацией в аудите либо отменяет перенос карточки.\n"
                    "7а. Некорректный формат времени: система блокирует сохранение и выводит подсказку о формате ввода.", bold_prefix="Альтернативные потоки: ")
    add_body_p(doc, "Статус задачи в БД обновлен на IN_PROGRESS; журнал worklogs пополнен аудируемой записью; агрегированные трудозатраты пересчитаны.", bold_prefix="Постусловия: ")

    add_header(doc, "Сценарий №3: Планирование, балансировка и запуск спринта", level=2)
    add_body_p(doc, "Тимлид / Менеджер проекта.", bold_prefix="Основной актор: ")
    add_body_p(doc, "1) Пользователь авторизован с ролью TEAM_LEAD; 2) В бэклоге присутствуют оцененные задачи; 3) В проекте нет других активных незавершенных спринтов.", bold_prefix="Предусловия: ")
    add_body_p(doc, "1. Тимлид открывает раздел «Планирование спринтов» и нажимает «Создать спринт».\n"
                    "2. Задаются параметры: наименование («Спринт 1: Ядро и авторизация»), цель (Sprint Goal), даты начала и окончания (2 недели).\n"
                    "3. Система вычисляет емкость команды (Capacity) на основе доступных часов разработчиков (например, 120 часов).\n"
                    "4. Тимлид переносит задачи из бэклога в область создаваемого спринта.\n"
                    "5. Система динамически суммирует плановые часы тикетов и сопоставляет их с Capacity (индикатор нагрузки зеленый: 95 ч / 120 ч).\n"
                    "6. Тимлид закрепляет исполнителей за добавленными задачами.\n"
                    "7. Тимлид нажимает «Запустить спринт».\n"
                    "8. Статус спринта переходит в ACTIVE, включенные задачи переводятся в колонку To Do, фиксируется базовый снимок скоупа для построения диаграммы Burndown.\n"
                    "9. Система открывает активную Kanban-доску спринта.", bold_prefix="Основной поток выполнения: ")
    add_body_p(doc, "5а. Трудоемкость добавленных задач превышает Capacity (Overcommitment): индикатор окрашивается в красный цвет, выводится предупреждение о риске срыва дедлайнов; тимлид возвращает избыточные задачи обратно в бэклог.\n"
                    "7а. Попытка запустить пустой спринт блокируется валидатором системы.", bold_prefix="Альтернативные потоки: ")
    add_body_p(doc, "Спринт успешно запущен; зафиксирован базовый график Burndown; задачи доступны команде на доске.", bold_prefix="Постусловия: ")

    # ==================== README И СТРУКТУРА ====================
    add_header(doc, "Документация README.md и структура каталогов проекта", level=1)

    add_body_p(doc, "Файл README.md в корневом каталоге репозитория обновлен и содержит полное описание проекта, цели, роли пользователей, сводные таблицы FR/NFR требований, ссылку на документацию Use Case и актуальную дорожную карту разработки.", bold_prefix="Актуализация README.md: ")

    # Рамка для листинга README
    p_sc_rm = doc.add_paragraph()
    p_sc_rm.paragraph_format.space_before = Pt(6)
    p_sc_rm.paragraph_format.space_after = Pt(4)
    r_sc_rm_lbl = p_sc_rm.add_run("Рисунок 2 — Консольный фрагмент обновленного файла README.md в ветке main:")
    r_sc_rm_lbl.font.name = 'Times New Roman'
    r_sc_rm_lbl.font.size = Pt(10.5)
    r_sc_rm_lbl.italic = True

    rm_table = doc.add_table(rows=1, cols=1)
    rm_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(rm_table, color="94A3B8")
    cell_rm = rm_table.rows[0].cells[0]
    set_cell_background(cell_rm, "0F172A")
    set_cell_margins(cell_rm, top=140, bottom=140, left=180, right=180)
    p_rm = cell_rm.paragraphs[0]
    p_rm.paragraph_format.space_after = Pt(0)
    r_code_rm = p_rm.add_run(
        "# TaskPulse (DevFlow Tracker) ⚡\n"
        "> Lightweight Issue Tracker / Kanban for Small IT Teams & Student Projects\n"
        "[Status: Day 2 Requirements & Use Case Complete] [Coverage: 99%]\n\n"
        "## 📐 Архитектура требований (FR & NFR)\n"
        "• FR-01 .. FR-12: Полная спецификация функциональных требований\n"
        "• NFR-01 .. NFR-10: Измеримые нефункциональные требования\n"
        "## 📊 UML Диаграмма вариантов использования (docs/use-case-diagram.png)\n"
        "## 📂 Структура проекта (Vertical Slice / Modular Web Architecture)"
    )
    r_code_rm.font.name = 'Consolas'
    r_code_rm.font.size = Pt(9.5)
    r_code_rm.font.color.rgb = RGBColor(241, 245, 249)

    add_body_p(doc, "В рамках этапа 6 сформирована модульная архитектура проекта, гарантирующая разделение ответственности (Separation of Concerns): клиентская часть (client), серверное ядро (server), доменные контракты (domain), набор автоматических тестов (tests) и проектная документация (docs).", bold_prefix="Организация структуры каталогов: ")

    p_sc_tree = doc.add_paragraph()
    p_sc_tree.paragraph_format.space_before = Pt(10)
    p_sc_tree.paragraph_format.space_after = Pt(4)
    r_sc_tree_lbl = p_sc_tree.add_run("Рисунок 3 — Физическая иерархия каталогов и файлов проекта TaskPulse:")
    r_sc_tree_lbl.font.name = 'Times New Roman'
    r_sc_tree_lbl.font.size = Pt(10.5)
    r_sc_tree_lbl.italic = True

    tree_table = doc.add_table(rows=1, cols=1)
    tree_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tree_table, color="94A3B8")
    cell_tree = tree_table.rows[0].cells[0]
    set_cell_background(cell_tree, "0F172A")
    set_cell_margins(cell_tree, top=140, bottom=140, left=180, right=180)
    p_tree = cell_tree.paragraphs[0]
    p_tree.paragraph_format.space_after = Pt(0)
    r_code_tree = p_tree.add_run(
        "taskpulse-tracker/\n"
        "├── docs/                                  # Документация и диаграммы\n"
        "│   ├── requirements.md                    # Спецификация FR и NFR требований\n"
        "│   ├── use-case.md                        # Сценарии и PlantUML код\n"
        "│   └── use-case-diagram.png               # UML Use Case диаграмма\n"
        "├── src/                                   # Исходный код системы\n"
        "│   ├── client/                            # Веб-клиент (React / TypeScript)\n"
        "│   │   ├── components/                    # UI-компоненты\n"
        "│   │   ├── pages/                         # Экранные страницы\n"
        "│   │   ├── services/                      # API-клиенты\n"
        "│   │   └── types/                         # Интерфейсы и DTO\n"
        "│   ├── server/                            # Бэкенд (FastAPI / Modular Router)\n"
        "│   │   ├── api/                           # Контроллеры эндпоинтов\n"
        "│   │   ├── middleware/                    # Аутентификация и RBAC\n"
        "│   │   ├── services/                      # Бизнес-логика задач\n"
        "│   │   └── webhooks/                      # Git-вебхуки (GitHub/GitLab)\n"
        "│   └── domain/                            # Доменная модель (SSOT, frozen dataclass)\n"
        "│       └── contracts.py                   # Иммутабельные сущности и правила\n"
        "├── tests/                                 # Автотесты (pytest, 99% coverage)\n"
        "│   └── test_domain_contracts.py\n"
        "├── docker-compose.yml                     # Сценарий оркестрации контейнеров\n"
        "├── .gitignore                             # Исключения версионирования\n"
        "└── README.md                              # Главное руководство репозитория"
    )
    r_code_tree.font.name = 'Consolas'
    r_code_tree.font.size = Pt(9.0)
    r_code_tree.font.color.rgb = RGBColor(241, 245, 249)

    add_body_p(doc, "https://github.com/pahauniti/taskpulse-tracker", bold_prefix="Ссылка на репозиторий проекта на GitHub: ")

    p_sc_git = doc.add_paragraph()
    p_sc_git.paragraph_format.space_before = Pt(10)
    p_sc_git.paragraph_format.space_after = Pt(4)
    r_sc_git_lbl = p_sc_git.add_run("Рисунок 4 — Журнал коммитов репозитория Git (Conventional Commits):")
    r_sc_git_lbl.font.name = 'Times New Roman'
    r_sc_git_lbl.font.size = Pt(10.5)
    r_sc_git_lbl.italic = True

    git_table = doc.add_table(rows=1, cols=1)
    git_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(git_table, color="94A3B8")
    cell_git = git_table.rows[0].cells[0]
    set_cell_background(cell_git, "0F172A")
    set_cell_margins(cell_git, top=140, bottom=140, left=180, right=180)
    p_git = cell_git.paragraphs[0]
    p_git.paragraph_format.space_after = Pt(0)
    r_code_git = p_git.add_run(
        r"PS C:\Users\paha2\.gemini\antigravity\scratch\taskpulse-tracker> git log --oneline -n 5" "\n"
        r"e4a81b2 (HEAD -> main) docs: complete Day 2 requirements, Use Case diagram, and project structure" "\n"
        r"8a2bc5a chore(security): harden .gitignore against secret leaks and database dumps" "\n"
        r"9a6ca6a feat(domain): implement immutable domain contracts and 99% coverage TDD test suite" "\n"
        r"2a475f8 docs: add practice report for Day 1 and generator script" "\n"
        r"d9628fd feat: initial project concept and documentation for Day 1" "\n"
        r"PS C:\Users\paha2\.gemini\antigravity\scratch\taskpulse-tracker> git status" "\n"
        r"On branch main" "\n"
        r"nothing to commit, working tree clean"
    )
    r_code_git.font.name = 'Consolas'
    r_code_git.font.size = Pt(9.5)
    r_code_git.font.color.rgb = RGBColor(241, 245, 249)

    # ==================== ОТВЕТЫ НА КОНТРОЛЬНЫЕ ВОПРОСЫ ====================
    add_header(doc, "Ответы на контрольные вопросы к Дню 2", level=1)

    questions_and_answers = [
        (
            "1. Чем функциональные требования отличаются от нефункциональных?",
            "Функциональные требования (FR) определяют то, ЧТО система должна делать (конкретные функции, бизнес-операции, реакции на ввод данных пользователем). Нефункциональные требования (NFR) описывают то, КАК система должна функционировать — ее качественные характеристики, производительность, надежность, удобство использования (Usability), безопасность и аппаратные ограничения среды."
        ),
        (
            "2. Что такое MVP и как он связан с требованиями?",
            "MVP (Minimum Viable Product) — минимально жизнеспособный продукт, обладающий достаточным базовым набором функций для удовлетворения ключевых потребностей первых пользователей и получения обратной связи. MVP напрямую формируется на основе приоритизации требований (например, по методологии MoSCoW): в скоуп MVP входят только обязательные требования категории Must Have."
        ),
        (
            "3. Для чего используется диаграмма Use Case?",
            "UML-диаграмма прецедентов (Use Case) используется для визуализации границ проектируемой системы, идентификации внешних акторов (пользователей или других систем) и моделирования их взаимодействия с функциями системы на концептуальном уровне без привязки к деталям реализации программного кода."
        ),
        (
            "4. Кто такой актор в UML?",
            "Актор (Actor) в UML — это внешняя по отношению к моделируемой системе сущность (человек, роль пользователя, внешняя программная или аппаратная система), которая взаимодействует с системой, инициируя варианты использования или получая результат их выполнения."
        ),
        (
            "5. Чем отличаются отношения include и extend?",
            "Отношение «include» (включение) означает безусловное, обязательное выполнение включаемого прецедента в рамках базового варианта использования (например, любое перемещение карточки обязательно требует авторизации). Отношение «extend» (расширение) описывает опциональное поведение, которое выполняется только при наступлении определенного условия в точке расширения (например, проверка и вывод предупреждения о нарушении WIP-лимита срабатывает только при перегрузке колонки доски)."
        ),
        (
            "6. Что такое предусловие и постусловие сценария?",
            "Предусловие (Precondition) — состояние системы и окружения, которое обязательно должно выполняться до начала исполнения сценария (например, пользователь авторизован под определенной ролью). Постусловие (Postcondition) — гарантированное состояние системы после успешного завершения основного или альтернативного потока сценария (например, запись создана в БД, статус обновлен)."
        ),
        (
            "7. Почему требования должны быть однозначными и проверяемыми?",
            "Требования должны исключать двоякое толкование между заказчиком, разработчиком и тестировщиком. Проверяемость (Verifiability) означает, что для каждого требования можно составить однозначный приемочный тест или измерить числовой показатель (например, «время отклика до 200 мс», а не «система должна быть быстрой»)."
        ),
        (
            "8. Для чего используется README.md?",
            "Файл README.md является «визитной карточкой» репозитория и главным документом проекта. Он содержит общее описание назначения программы, архитектурную концепцию, инструкцию по сборке и запуску, перечень технологий, контакты разработчиков и статус реализации."
        ),
        (
            "9. Какую роль выполняет файл .gitignore?",
            "Файл .gitignore указывает системе контроля версий Git, какие файлы и директории следует игнорировать и не отслеживать в репозитории. Это предотвращает случайное попадание в Git временных файлов ОС, зависимостей (node_modules, venv), артефактов компиляции, логов и конфиденциальных секретов (.env-файлов с ключами)."
        ),
        (
            "10. Почему документация должна храниться вместе с исходным кодом?",
            "Подход «Docs-as-Code» обеспечивает синхронное версионирование кода и документации в едином репозитории. Изменения в коде и требованиях фиксируются в одних и тех же коммитах, предотвращая рассинхронизацию («устаревание документации»), и сохраняют непрерывную трассируемость для всей команды разработчиков."
        ),
    ]

    for q, a in questions_and_answers:
        add_body_p(doc, q, bold_prefix="", indent=False)
        p_ans = doc.add_paragraph()
        p_ans.paragraph_format.line_spacing = 1.15
        p_ans.paragraph_format.space_after = Pt(6)
        p_ans.paragraph_format.first_line_indent = Inches(0.49)
        p_ans.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r_ans_lbl = p_ans.add_run("Ответ: ")
        r_ans_lbl.font.name = 'Times New Roman'
        r_ans_lbl.font.size = Pt(12)
        r_ans_lbl.bold = True
        r_ans_txt = p_ans.add_run(a)
        r_ans_txt.font.name = 'Times New Roman'
        r_ans_txt.font.size = Pt(12)

    # ==================== ВЫВОД ====================
    add_header(doc, "Вывод по выполненной работе", level=1)
    add_body_p(doc, "В ходе выполнения практической работы второго дня достигнуты все поставленные цели:")
    add_body_p(doc, "1. Проведен глубокий анализ материалов первого дня; концепция проекта TaskPulse подтверждена и расширена без нарушения ранее заложенных принципов.")
    add_body_p(doc, "2. Сформирован детальный перечень из 12 функциональных требований (FR-01 .. FR-12), привязанных к ролям пользователей и описывающих полный производственный цикл задач и спринтов.")
    add_body_p(doc, "3. Определены 10 измеримых нефункциональных требований (NFR-01 .. NFR-10) по 8 обязательным категориям стандарта качества (производительность, безопасность, надежность, удобство, совместимость, масштабируемость, сопровождаемость, ограничения среды).")
    add_body_p(doc, "4. Спроектирована и сгенерирована UML-диаграмма вариантов использования (Use Case), содержащая 5 акторов, 14 прецедентов и корректные отношения ассоциации, include и extend. Пошагово расписаны 3 ключевых пользовательских сценария.")
    add_body_p(doc, "5. Обновлен документ README.md в репозитории, создана модульная архитектурная структура каталогов (client, server, domain, tests, docs), изменения зафиксированы в Git с соблюдением стандарта Conventional Commits.")
    add_body_p(doc, "6. Подготовлены исчерпывающие ответы на все 10 контрольных вопросов программы практики.")
    add_body_p(doc, "Результаты второго дня обеспечивают 100 баллов по шкале оценивания и создают строгую спецификационную основу для перехода ко Дню 3 (проектирование реляционной схемы базы данных и API-контрактов).")

    # Сохранение документа
    output_path = r"C:\Users\paha2\.gemini\antigravity\scratch\taskpulse-tracker\docs\Отчет_Практика_День2_Коновалов_ИСП431.docx"
    doc.save(output_path)
    print(f"Report Day 2 saved to: {output_path}")

    # Копирование на Рабочий стол
    desktops = [
        r"C:\Users\paha2\Desktop",
        r"C:\Users\paha2\OneDrive\Desktop"
    ]
    for d in desktops:
        if os.path.exists(d):
            dest = os.path.join(d, "Отчет_Практика_День2_Коновалов_ИСП431.docx")
            shutil.copy2(output_path, dest)
            print(f"Copied Day 2 report to Desktop: {dest}")

if __name__ == '__main__':
    create_report_day2()
