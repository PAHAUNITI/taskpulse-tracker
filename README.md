# TaskPulse (DevFlow Tracker) ⚡

> **Легковесная система контроля и распределения задач для командной разработки (Lightweight Issue Tracker / Kanban)**  
> Проект разрабатывается в рамках производственной / учебной практики по специальности **09.02.07 «Информационные системы и программирование»** (группа ИСП 431).  
> **Автор:** Коновалов П.С.  
> **Руководитель практики:** Роман Владимирович  

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Status: Day 3 Complete](https://img.shields.io/badge/Status-Day%203%20UML%2C%20IDEF0%2C%20DFD%20Complete-success.svg)](#)
[![Diagrams: 10/10 Complete](https://img.shields.io/badge/Architecture-10%20Diagrams%20Suite-blueviolet.svg)](#)
[![Stack: Node.js / React / Docker](https://img.shields.io/badge/Architecture-Modular%20Web-orange.svg)](#)
[![Tests: 99% Coverage](https://img.shields.io/badge/Coverage-99%25-brightgreen.svg)](#)

---

## 📌 О проекте

**TaskPulse** — это специализированная веб-система оперативного управления задачами и спринтами, спроектированная как высокопроизводительный и эргономичный аналог *Linear* и *Jira* для небольших IT-команд (3–10 разработчиков), студенческих проектных объединений и инди-студий.

### Проблема, которую решает продукт:
В коллективной разработке ПО ключевым узким местом выступает **информационная фрагментация**: задачи ведутся в громоздких или разрозненных трекерах (Jira, Trello), обсуждение идет в мессенджерах (Telegram, Discord), а фиксация кода — в Git-серверах (GitHub, GitLab). Возникает рассинхрон между требованиями, кодом и трудозатратами. Существующие корпоративные ALM-системы перегружены (Overengineering), требуют 4–8 ГБ памяти под JVM и заблокированы санкциями.

### Цели разработки:
* Создание легковесного автономного веб-трекера задач с потреблением RAM до 200–512 МБ в Docker.
* Обеспечение сквозной трассируемости: **«Задача ↔ Git-коммит ↔ Списанное время»**.
* Внедрение наглядного контроля нагрузки: интерактивный Kanban с WIP-лимитами, Burndown-диаграммы и табели Timesheet.

---

## 👥 Роли пользователей (RBAC)

1. 👑 **Администратор системы (System Administrator):** Управление аккаунтами пользователей, проектами, системными токенами Git и аудитом безопасности.
2. 🎯 **Тимлид / Менеджер проекта (Team Lead / PM):** Планирование и запуск спринтов, приоритеты бэклога, распределение исполнителей, аналитика Burndown и Timesheet, контроль WIP-лимитов.
3. 💻 **Разработчик / Исполнитель (Developer):** Создание тикетов, смена статусов на Kanban-доске, списание затраченных часов (Worklog), связка веток и коммитов.
4. 👁️ **Наблюдатель / Куратор (Observer / Mentor):** Режим «только чтение», аудит успеваемости, просмотр графиков сгорания задач, выгрузка сводных отчетов.

---

## 📐 Архитектура требований (FR & NFR)

Полная проектная спецификация доступна в каталоге `docs/requirements/`:
* 📄 **[docs/requirements/functional.md](docs/requirements/functional.md):** 12 функциональных требований (FR-01 .. FR-12).
* 📄 **[docs/requirements/non-functional.md](docs/requirements/non-functional.md):** 10 измеримых нефункциональных требований (NFR-01 .. NFR-10).

---

## 📊 Комплект архитектурных диаграмм (День 3: 10 диаграмм)

Все диаграммы разработаны в высоком разрешении и согласованы с единым источником правды (SSOT):

| № | Диаграмма | Стандарт / Нотация | Назначение | Исходный файл |
| :-: | :--- | :--- | :--- | :--- |
| **1** | **Class Diagram** | UML 2.5 Static | 7 классов (`User`, `Project`, `Task`, `Sprint`, `Worklog`, `GitCommit`, `KanbanBoard`), кратности, композиция, агрегация | [docs/diagrams/class.png](docs/diagrams/class.png) |
| **2** | **Component Diagram** | UML 2.5 Logical | 6 модулей (`Web Client`, `API Gateway`, `Task Service`, `Time Service`, `Webhook`, `ORM`), интерфейсы Lollipop | [docs/diagrams/component.png](docs/diagrams/component.png) |
| **3** | **Deployment Diagram** | UML 2.5 Physical | Топология узлов (Client Workstation, App Server Docker Node, Database Node), протоколы HTTPS, TCP 5432 | [docs/diagrams/deployment.png](docs/diagrams/deployment.png) |
| **4** | **Activity Diagram** | UML 2.5 Dynamic | Смена статуса карточки, проверка WIP-лимитов (2 ветвления) и списание времени со свимлейнами | [docs/diagrams/activity.png](docs/diagrams/activity.png) |
| **5** | **State Machine Diagram** | UML 2.5 Behavioral | Жизненный цикл сущности `Task` (5 состояний, 7 переходов, условия, возврат Reopen и правки по ревью) | [docs/diagrams/state-machine.png](docs/diagrams/state-machine.png) |
| **6** | **Communication Diagram** | UML 2.5 Interaction | Сценарий приема Git-вебхука: 5 объектов, 7 пронумерованных сообщений обмена | [docs/diagrams/communication.png](docs/diagrams/communication.png) |
| **7** | **IDEF0 A-0** | IDEF0 Functional | Контекстная диаграмма верхнего уровня (Входы, Управление, Механизмы, Выходы) | [docs/diagrams/idef0-a-0.png](docs/diagrams/idef0-a-0.png) |
| **8** | **IDEF0 A0** | IDEF0 Functional | Декомпозиция на 4 подсистемы: Бэклог (А1), Спринты (А2), Трекинг (А3), Аналитика (А4) | [docs/diagrams/idef0-a0.png](docs/diagrams/idef0-a0.png) |
| **9** | **DFD Level 0** | Data Flow Diagram | Глобальное движение данных: 3 внешние сущности, 5 процессов, 3 хранилища (D1, D2, D3) | [docs/diagrams/dfd-level-0.png](docs/diagrams/dfd-level-0.png) |
| **10** | **DFD Level 1** | Data Flow Diagram | Декомпозиция процесса 3.0 на 4 подпроцесса (3.1..3.4) движения трудозатрат и статусов | [docs/diagrams/dfd-level-1.png](docs/diagrams/dfd-level-1.png) |

---

## 🛠 Технологический стек

* **Frontend:** React 18, TypeScript, Tailwind CSS, Lucide Icons, Drag-and-Drop Context (Optimistic UI).
* **Backend:** Node.js (Fastify/Express) / Python (FastAPI), REST API, Webhook Engine.
* **База данных:** PostgreSQL 16 (реляционная модель с каскадным удалением) / SQLite (для портативного запуска).
* **Архитектурный стандарт:** Everything Claude Code (ECC) — строгая иммутабельность, контракты данных, модульность (<800 строк/файл), TDD-покрытие тестами $\ge 80\%$ (факт: **99%**).
* **Инфраструктура:** Docker, Docker Compose.

---

## 📂 Структура проекта

```text
taskpulse-tracker/
├── docs/                                  # Проектная документация и отчеты
│   ├── requirements/                      # Спецификация требований
│   │   ├── functional.md                  # Таблица функциональных требований FR
│   │   └── non-functional.md              # Таблица нефункциональных требований NFR
│   ├── diagrams/                          # Полный комплект из 10 инженерных диаграмм
│   │   ├── class.png                      # 1. Диаграмма классов UML
│   │   ├── component.png                  # 2. Диаграмма компонентов UML
│   │   ├── deployment.png                 # 3. Диаграмма развертывания UML
│   │   ├── activity.png                   # 4. Диаграмма деятельности UML
│   │   ├── state-machine.png              # 5. Диаграмма состояний UML
│   │   ├── communication.png              # 6. Диаграмма кооперации UML
│   │   ├── idef0-a-0.png                  # 7. Контекстная диаграмма IDEF0 A-0
│   │   ├── idef0-a0.png                   # 8. Диаграмма декомпозиции IDEF0 A0
│   │   ├── dfd-level-0.png                # 9. Диаграмма потоков данных DFD Уровень 0
│   │   └── dfd-level-1.png                # 10. Диаграмма потоков данных DFD Уровень 1
│   └── reports/                           # Официальные отчеты по дням практики (.docx)
│       ├── day-1-report.docx              # Отчет за День 1
│       ├── day-2-report.docx              # Отчет за День 2
│       └── day-3-report.docx              # Официальный отчет за День 3
├── src/                                   # Исходный код программного комплекса
│   ├── client/                            # Веб-клиент (Frontend)
│   │   ├── components/                    # UI-компоненты (Kanban, модалки, тайм-трекер)
│   │   ├── pages/                         # Страницы (Доска, Бэклог, Аналитика)
│   │   ├── services/                      # API-клиенты и сетевые сервисы
│   │   └── types/                         # TypeScript-интерфейсы и типы данных
│   ├── server/                            # Серверная часть (Backend API)
│   │   ├── api/                           # Маршруты и контроллеры REST API
│   │   ├── middleware/                    # Аутентификация, RBAC и валидаторы
│   │   ├── services/                      # Бизнес-логика задач и спринтов
│   │   └── webhooks/                      # Обработчик вебхуков Git (GitHub/GitLab)
│   └── domain/                            # Доменная модель и контракты данных (SSOT)
│       ├── __init__.py
│       └── contracts.py                   # Иммутабельные сущности (frozen dataclass)
├── tests/                                 # Набор автоматических тестов
│   ├── __init__.py
│   └── test_domain_contracts.py           # Unit-тесты доменной логики (99% coverage)
├── .gitignore                             # Правила исключений Git (усилено DevSecOps)
├── docker-compose.yml                     # Сценарий оркестрации контейнеров
└── README.md                              # Главный файл документации репозитория
```

---

## 📅 Дорожная карта практики

- [x] **День 1:** Выбор темы, анализ предметной области, роли участников, спецификация MVP (MoSCoW), инициализация Git-репозитория.
- [x] **День 2:** Формализация функциональных (FR-01..FR-12) и нефункциональных требований (NFR-01..NFR-10), построение UML Use Case диаграммы, описание сценариев, организация структуры проекта.
- [x] **День 3:** Комплексное проектирование программной системы: разработка комплекта из 10 диаграмм (Class, Component, Deployment, Activity, State Machine, Communication, IDEF0 A-0, IDEF0 A0, DFD 0, DFD 1) и официального отчета.
- [ ] **День 4:** Разработка серверных модулей, реляционной схемы базы данных и пользовательского интерфейса (Kanban, таймер).
- [ ] **День 5:** Интеграция Git-вебхуков, модульное тестирование, итоговая сборка и защита проекта.

---

## 📄 Лицензия
Проект распространяется под свободной лицензией MIT.
