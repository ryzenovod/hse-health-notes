"""Deterministic SVG figures for Healthcare Economics: Rostislav Pavlov on Healthcare Management, AI, and Culture of Safety.
Visually reviewed and verified to prevent text collisions, clippings, or overflows.
"""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/assets/healthcare-economics'

INK = '#18213a'
MUTED = '#54627a'
GRID = '#e0e5ee'
BLUE = '#3859b5'
ORANGE = '#dd5a24'
TEAL = '#178477'
RED = '#b23b54'
PURPLE = '#6a3cbc'
BG_LIGHT = '#f8fafd'


class SVG:
    def __init__(self, title, desc, w=760, h=500):
        self.w, self.h = w, h
        self.items = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">',
            f'<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>',
            '<style>text{font-family:Inter,system-ui,-apple-system,sans-serif;fill:#18213a;font-size:15px} .small{font-size:13px;fill:#54627a} .heading{font-size:20px;font-weight:700} .bold{font-weight:600}</style>',
            f'<rect width="{w}" height="{h}" rx="12" fill="#fff"/>'
        ]
        self.text(32, 40, title, cls='heading')

    def text(self, x, y, value, color=INK, anchor='start', cls='', size=None):
        size_attr = f'font-size:{size}px;' if size else ''
        self.items.append(f'<text x="{x:.2f}" y="{y:.2f}" text-anchor="{anchor}" class="{cls}" style="{size_attr}fill:{color}">{escape(str(value))}</text>')

    def line(self, x1, y1, x2, y2, color=INK, width=2, dash=False):
        dash_attr = ' stroke-dasharray="6 6"' if dash else ''
        self.items.append(f'<path d="M{x1:.3f},{y1:.3f} L{x2:.3f},{y2:.3f}" fill="none" stroke="{color}" stroke-width="{width}"{dash_attr}/>')

    def rect(self, x, y, w, h, fill, rx=4, stroke=None, stroke_width=1):
        stroke_attr = f' stroke="{stroke}" stroke-width="{stroke_width}"' if stroke else ''
        self.items.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{rx}" fill="{fill}"{stroke_attr}/>')

    def save(self, name):
        OUT.mkdir(parents=True, exist_ok=True)
        path = OUT / name
        path.write_text('\n'.join(self.items + ['</svg>']) + '\n', encoding='utf-8')
        print(f"Saved: {path}")


def generate_iceberg_figure():
    s = SVG(
        "Модель айсберга: восприятие качества медицины пациентом",
        "Сравнение видимой верхушки (сервис и эмпатия) и подводной толщи (клиническая безопасность и стерильность).",
        w=760, h=510
    )
    s.text(32, 66, "Пациент оценивает отношение и чистоту, но его жизнь спасает подводная часть системы", cls='small')

    # Top Section: 15% Visible
    top_y = 90
    s.rect(32, top_y, 696, 104, fill='#f0f7ff', rx=8, stroke='#b3d7ff', stroke_width=1)
    s.rect(46, top_y + 12, 130, 26, fill='#0288d1', rx=6)
    s.text(111, top_y + 29, "ВЕРХУШКА (15%)", color='#fff', anchor='middle', cls='bold', size=11)
    s.text(188, top_y + 29, "Видимый сервис: то, на основе чего пациент формирует выбор", color='#0277bd', cls='bold', size=12)

    # 2 Sub-cards in the top part to prevent any text overlap
    c1_w = 328
    c_h = 48
    s.rect(46, top_y + 44, c1_w, c_h, fill='#fff', rx=6, stroke='#cbe3fb', stroke_width=1)
    s.text(58, top_y + 63, "• Эмпатия врача, уважительный диалог без сарказма", color=INK, size=10.5)
    s.text(58, top_y + 81, "• Понятное объяснение плана лечения и прогноза", color=MUTED, size=10)

    s.rect(386, top_y + 44, c1_w, c_h, fill='#fff', rx=6, stroke='#cbe3fb', stroke_width=1)
    s.text(398, top_y + 63, "• Чистота палат, горячее питание, понятная навигация", color=INK, size=10.5)
    s.text(398, top_y + 81, "• Быстрая запись через приложение, без очередей", color=MUTED, size=10)

    # Waterline divider zone with dedicated clearance
    wl_y = 208
    s.line(32, wl_y, 728, wl_y, color='#0288d1', width=2, dash=True)
    s.rect(235, wl_y - 11, 290, 22, fill='#e1f0fe', rx=11, stroke='#0288d1', stroke_width=1)
    s.text(380, wl_y + 4, "ВАТЕРЛИНИЯ ВОСПРИЯТИЯ ПАЦИЕНТА", color='#01579b', anchor='middle', cls='bold', size=10)

    # Bottom Section: 85% Hidden
    bot_y = 226
    s.rect(32, bot_y, 696, 202, fill='#eef4fb', rx=8, stroke='#90b8e4', stroke_width=1)
    s.rect(46, bot_y + 12, 175, 26, fill='#1a365d', rx=6)
    s.text(133, bot_y + 29, "ПОДВОДНАЯ ЧАСТЬ (85%)", color='#fff', anchor='middle', cls='bold', size=11)
    s.text(233, bot_y + 29, "Фундамент безопасности: пациент не может оценить профессионально", color='#1a365d', cls='bold', size=12)

    hidden_cards = [
        ("Стерильность и санэпидрежим", "Контроль ИСМП, ламинарный поток в операционных"),
        ("Чек-листы ВОЗ и тайм-ауты", "Тайм-аут перед разрезом, сверка стороны и салфеток"),
        ("Калибровка оборудования", "Поверка томографов, наркозных аппаратов и дозаторов"),
        ("Фармаконадзор и совместимость", "Двойной контроль введения высокорисковых лекарств"),
        ("M&M-конференции по ошибкам", "Системный разбор осложнений без поиска козла отпущения"),
        ("Симуляционные учения бригад", "Внезапные тренировки экстренной сердечной реанимации")
    ]

    card_w = 328
    card_h = 44
    for idx, (head, desc) in enumerate(hidden_cards):
        col = idx % 2
        row = idx // 2
        bx = 46 + col * 340
        by = bot_y + 46 + row * 49
        s.rect(bx, by, card_w, card_h, fill='#fff', rx=6, stroke='#b9d3ef', stroke_width=1)
        s.text(bx + 10, by + 18, head, color='#0d47a1', cls='bold', size=11)
        s.text(bx + 10, by + 35, desc, color=MUTED, size=9.8)

    # Bottom Takeaway box
    s.rect(32, 442, 696, 50, fill='#fff9e6', rx=8, stroke='#fbc02d', stroke_width=1)
    s.text(380, 462, "Парадокс восприятия: невкусный кофе отпугнет пациента быстрее, чем слабая вентиляция.", color='#e65100', anchor='middle', cls='bold', size=11)
    s.text(380, 480, "Но без скрытого фундамента безопасность рушится, приводя к сепсису и летальности.", color='#b78103', anchor='middle', size=10.5)

    s.save("iceberg-quality-perception.svg")


def generate_digitalization_figure():
    s = SVG(
        "Ловушка цифровизации: Процесс → Цифровой контур → ИИ",
        "Почему автоматизация хаоса приводит к катастрофе: сравнение Babylon Health и ЕМИАС Москвы.",
        w=760, h=490
    )
    s.text(32, 66, "Формула Ростислава Павлова: сначала стандартизация процессов, затем цифра, затем ИИ", cls='small')

    c_w = 696

    # Top: Bad Case (Babylon Health)
    top_y = 90
    s.rect(32, top_y, c_w, 142, fill='#fff5f5', rx=8, stroke=RED, stroke_width=1.5)
    s.rect(46, top_y + 10, 220, 26, fill=RED, rx=6)
    s.text(156, top_y + 27, "Крах: Babylon Health (UK/USA)", color='#fff', anchor='middle', cls='bold', size=11)
    s.text(280, top_y + 27, "Оценка $4.2 млрд → Банкротство с долгами -$1 млрд", color=RED, cls='bold', size=11.5)

    babylon_cards = [
        ("1. Хаос в процессах", "Протоколы не согласованы,", "стандарты приема размыты"),
        ("2. Хайповый ИИ", "Чат-бот обучен на сырых", "и противоречивых данных"),
        ("3. Ошибки триажа", "Пропуск стенокардии,", "совет пить чай при боли"),
        ("4. Ликвидация", "Разрыв контрактов NHS,", "обвал акций и банкротство")
    ]

    card_w = 152
    card_h = 74
    gap = 24
    for idx, (t1, t2, t3) in enumerate(babylon_cards):
        bx = 46 + idx * (card_w + gap)
        by = top_y + 48
        s.rect(bx, by, card_w, card_h, fill='#fff', rx=6, stroke='#ffcdd2', stroke_width=1)
        s.text(bx + 8, by + 20, t1, color=RED, cls='bold', size=10.5)
        s.text(bx + 8, by + 40, t2, color=MUTED, size=9.5)
        s.text(bx + 8, by + 56, t3, color=MUTED, size=9.5)

        if idx < 3:
            arrow_x = bx + card_w + gap / 2
            s.text(arrow_x, by + 42, "→", color=RED, anchor='middle', cls='bold', size=15)

    # Bottom: Good Case (ЕМИАС Москвы)
    bot_y = 248
    s.rect(32, bot_y, c_w, 154, fill='#f0fdf4', rx=8, stroke=TEAL, stroke_width=1.5)
    s.rect(46, bot_y + 10, 200, 26, fill=TEAL, rx=6)
    s.text(146, bot_y + 27, "Эталон: ЕМИАС (Москва)", color='#fff', anchor='middle', cls='bold', size=11)
    s.text(260, bot_y + 27, "Крупнейшая в мире единая система лучевой диагностики и ИИ", color=TEAL, cls='bold', size=11.5)

    emias_cards = [
        ("Шаг 1. Процессы", [
            "• Унификация расписаний и норм",
            "• Стандартизация маршрутов",
            "• Единые справочники нозологий"
        ]),
        ("Шаг 2. Цифровой контур", [
            "• Сквозная медкарта (ЭМК)",
            "• Подключение аппаратов КТ/МРТ",
            "• Облачный архив снимков (ЕРИС)"
        ]),
        ("Шаг 3. ИИ-ассистент", [
            "• Автоматический второй просмотр",
            "• Подсветка ранних признаков рака",
            "• Помощник, но не замена врача"
        ])
    ]

    em_w = 210
    em_h = 86
    em_gap = 23
    for idx, (title, points) in enumerate(emias_cards):
        bx = 46 + idx * (em_w + em_gap)
        by = bot_y + 46
        s.rect(bx, by, em_w, em_h, fill='#fff', rx=6, stroke='#c8e6c9', stroke_width=1)
        s.text(bx + 10, by + 20, title, color=TEAL, cls='bold', size=11)
        for p_idx, pt in enumerate(points):
            s.text(bx + 10, by + 40 + p_idx * 17, pt, color=MUTED, size=9.5)

        if idx < 2:
            arrow_x = bx + em_w + em_gap / 2
            s.text(arrow_x, by + 48, "→", color=TEAL, anchor='middle', cls='bold', size=16)

    # Footer takeaway
    s.rect(32, 420, c_w, 46, fill='#edf2fc', rx=6, stroke='#c5d5f5', stroke_width=1)
    s.text(380, 440, "Золотое правило цифровизации: Оцифрованный хаос = Автоматизированный хаос с тройным бюджетом.", color=BLUE, anchor='middle', cls='bold', size=11)
    s.text(380, 456, "Цифровой контур и ИИ внедряются ТОЛЬКО после стабилизации и аудита базовых клинических процессов.", color=MUTED, anchor='middle', size=10)

    s.save("digitalization-babylon-vs-emias.svg")


def generate_how_the_mighty_fall_figure():
    s = SVG(
        "5 стадий гибели великих компаний (по Джиму Коллинзу)",
        "Закономерности деградации лидеров рынка и клиник при потере контакта с реальностью.",
        w=760, h=490
    )
    s.text(32, 66, "От Kodak и Nokia до неэффективных медицинских гигантов: траектория упадка", cls='small')

    stages = [
        ("1. Высокомерие от успехов", "Hubris Born of Success",
         "«Мы лучшие, пациенты никуда не денутся». Потеря самокритики.",
         "Игнорирование конкурентов и технологических сдвигов среды.", '#1e88e5'),
        ("2. Безудержная экспансия", "Undisciplined Pursuit of More",
         "Агрессивный рост коек и филиалов без квалифицированных кадров.",
         "Размывание стандартов клинического качества ради валового дохода.", '#3949ab'),
        ("3. Отрицание рисков", "Denial of Risk and Peril",
         "Игнорирование роста осложнений. Наказание за плохие новости.",
         "Атмосфера страха: врачи начинают скрывать дефекты и ошибки.", '#fb8c00'),
        ("4. Поиски «чудо-таблетки»", "Grasping for Salvation",
         "Судорожная смена главврачей, покупка дорогого ИИ ради «чуда».",
         "Хаотичные метания без выстраивания базовых процессов клиники.", '#e53935'),
        ("5. Капитуляция и крах", "Capitulation to Irrelevance",
         "Потеря доверия персонала и пациентов, бегство ключевых врачей.",
         "Финансовая яма, банкротство или ликвидация организации.", '#8e0000')
    ]

    base_y = 90
    row_h = 58
    start_x = 32
    step_w = 696

    for idx, (title, en_title, l1, l2, col) in enumerate(stages):
        y = base_y + idx * row_h
        # Left tag box
        s.rect(start_x, y, 195, 48, fill=col, rx=6)
        s.text(start_x + 12, y + 21, title, color='#fff', cls='bold', size=11)
        s.text(start_x + 12, y + 38, en_title, color='#ffecb3' if idx >= 2 else '#bbdefb', size=9.5)

        # Right description box (multiline text cleanly wrapped)
        s.rect(start_x + 205, y, step_w - 205, 48, fill=BG_LIGHT, rx=6, stroke=col, stroke_width=1)
        s.text(start_x + 218, y + 20, l1, color=INK, size=10.5)
        s.text(start_x + 218, y + 37, l2, color=MUTED, size=10)

        if idx < len(stages) - 1:
            s.line(start_x + 97, y + 48, start_x + 97, y + row_h, color=col, width=2)

    # Bottom insight
    s.rect(start_x, 395, step_w, 65, fill='#fff9e6', rx=8, stroke='#e6b800', stroke_width=1)
    s.text(start_x + 16, 417, "Главный симптом необратимого упадка (стадия 3):", color='#997a00', cls='bold', size=11)
    s.text(start_x + 16, 434, "Подчиненные боятся сообщать руководителю о реальных инцидентах и врачебных ошибках.", color=INK, size=10.5)
    s.text(start_x + 16, 449, "Культура страха и сокрытия неизбежно толкает организацию к стадиям 4 и 5.", color=MUTED, size=10)

    s.save("how-the-mighty-fall-stages.svg")


def generate_leadership_triad_figure():
    s = SVG(
        "Куда уходит время системного лидера медицинской организации",
        "Разделение зон ответственности: почему главврач не должен проверять полы и карты пациентов.",
        w=760, h=480
    )
    s.text(32, 66, "Архитектура управления: внешний контур, стратегическая культура и автономные процессы", cls='small')

    col_w = 222
    col_h = 245
    col_y = 90
    gap = 15

    cols = [
        ("1. Защита и ресурсы (GR)", "Внешний контур и безопасность", '#1565c0', [
            "• «Крыша» и защита коллектива",
            "• Щит от силового давления",
            "• Диалог с ТФОМС и Минздравом",
            "• Привлечение инвестиций и субсидий",
            "• Защита фонда оплаты труда"
        ]),
        ("2. Стратегия и культура", "Внутренний климат и инновации", '#2e7d32', [
            "• Культура No-Blame (без вины)",
            "• Стандарты ISO 9001 и JCI",
            "• Психологическая безопасность",
            "• Наставничество, кадры Gen Z",
            "• Внедрение ИИ-ассистентов"
        ]),
        ("3. Продукт и исходы (VBHC)", "Ценность для пациента", '#c2185b', [
            "• Исходы лечения (PROMs / PREMs)",
            "• Снижение летальности и сепсиса",
            "• Симуляционный тренинг бригад",
            "• Пациентский опыт и сервис",
            "• Доверие и лояльность пациентов"
        ])
    ]

    for idx, (title, sub, col, items) in enumerate(cols):
        cx = 32 + idx * (col_w + gap)
        s.rect(cx, col_y, col_w, col_h, fill='#fcfdfe', rx=8, stroke=col, stroke_width=1.5)
        s.rect(cx, col_y, col_w, 42, fill=col, rx=8)
        s.rect(cx, col_y + 30, col_w, 12, fill=col, rx=0)
        s.text(cx + col_w / 2, col_y + 20, title, color='#fff', anchor='middle', cls='bold', size=11)
        s.text(cx + col_w / 2, col_y + 34, sub, color='#e0e0e0', anchor='middle', size=9.5)

        for i_item, it in enumerate(items):
            s.text(cx + 10, col_y + 70 + i_item * 34, it, color=INK, size=9.8)

    # Base Foundation: Autonomous Operations
    s.rect(32, 355, 696, 85, fill='#263238', rx=8)
    s.text(380, 380, "ФУНДАМЕНТ: АВТОНОМНЫЕ ОПЕРАЦИОННЫЕ ПРОЦЕССЫ", color='#80cbc4', anchor='middle', cls='bold', size=11.5)
    s.text(380, 404, "Если главврач лично указывает санитаркам, как мыть полы, или вручную правит карты — система мертва.", color='#eceff1', anchor='middle', size=10.5)
    s.text(380, 422, "Рутина обязана работать по отточенным СОПам и чек-листам без постоянного ручного вмешательства лидера.", color='#b0bec5', anchor='middle', size=10)

    s.save("leadership-system-triad.svg")


def generate_semmelweis_triad_figure():
    s = SVG(
        "Драма доктора Земмельвейса: три опоры внедрения инноваций",
        "Почему даже безупречная доказанность гибнет без культуры диалога и поддержки институтов.",
        w=760, h=470
    )
    s.text(32, 66, "Формула Павлова: мало быть правым по цифрам — инновация требует эмпатии и институтов", cls='small')

    # Connecting triangle lines in the background
    s.line(380, 140, 200, 270, color=GRID, width=3, dash=True)
    s.line(380, 140, 560, 270, color=GRID, width=3, dash=True)
    s.line(200, 290, 560, 290, color=GRID, width=3, dash=True)

    # Center Hub badge
    s.rect(325, 205, 110, 26, fill='#fff', rx=13, stroke=MUTED, stroke_width=1)
    s.text(380, 222, "БАЛАНС 3 ОПОР", color=INK, anchor='middle', cls='bold', size=10)

    # 1. Top Card: Facts & Data (Green / Success)
    s.rect(200, 90, 360, 90, fill='#f0fdf4', rx=8, stroke=TEAL, stroke_width=1.5)
    s.rect(212, 102, 185, 24, fill=TEAL, rx=6)
    s.text(304, 118, "1. ФАКТЫ И ДАННЫЕ (Hard Data)", color='#fff', anchor='middle', cls='bold', size=10)
    s.rect(435, 102, 112, 24, fill='#dcfce7', rx=6, stroke=TEAL, stroke_width=1)
    s.text(491, 118, "УСПЕХ: ДОКАЗАНО", color=TEAL, anchor='middle', cls='bold', size=9.5)
    s.text(214, 145, "• Смертность рожениц снижена с 18% до менее 1%", color=INK, size=10.5)
    s.text(214, 163, "• Обработка рук хлорной водой: строгая статистика клиники", color=MUTED, size=10)

    # 2. Bottom Left Card: Soft Skills & Communication (Red / Failure)
    s.rect(32, 246, 335, 102, fill='#fff5f5', rx=8, stroke=RED, stroke_width=1.5)
    s.rect(44, 258, 175, 24, fill=RED, rx=6)
    s.text(131, 274, "2. КОММУНИКАЦИЯ (Soft Skills)", color='#fff', anchor='middle', cls='bold', size=10)
    s.rect(238, 258, 116, 24, fill='#fee2e2', rx=6, stroke=RED, stroke_width=1)
    s.text(296, 274, "ПРОВАЛ: АГРЕССИЯ", color=RED, anchor='middle', cls='bold', size=9.5)
    s.text(46, 300, "• Публично называл профессоров «убийцами матерей»", color=INK, size=10)
    s.text(46, 318, "• Высокомерный тон, отказ от академического диалога", color=MUTED, size=9.8)
    s.text(46, 336, "• Полная изоляция от коллег и отсутствие союзников", color=MUTED, size=9.8)

    # 3. Bottom Right Card: Institutions & Governance (Red / Failure)
    s.rect(393, 246, 335, 102, fill='#fff5f5', rx=8, stroke=RED, stroke_width=1.5)
    s.rect(405, 258, 175, 24, fill=RED, rx=6)
    s.text(492, 274, "3. ИНСТИТУТЫ (Governance)", color='#fff', anchor='middle', cls='bold', size=10)
    s.rect(599, 258, 116, 24, fill='#fee2e2', rx=6, stroke=RED, stroke_width=1)
    s.text(657, 274, "ОТТОРЖЕНИЕ СРЕДОЙ", color=RED, anchor='middle', cls='bold', size=9)
    s.text(407, 300, "• Теория микробов еще не открыта (до работ Пастера)", color=INK, size=10)
    s.text(407, 318, "• Отсутствие поддержки руководства больницы и норм", color=MUTED, size=9.8)
    s.text(407, 336, "• Финал: травля, увольнение и гибель в психбольнице", color=MUTED, size=9.8)

    # Bottom Takeaway box
    s.rect(32, 368, 696, 68, fill='#fff9e6', rx=8, stroke='#e6b800', stroke_width=1)
    s.text(380, 392, "Управленческий закон инноваций: Результат = Данные × Эмпатия × Институты", color='#997a00', anchor='middle', cls='bold', size=11.5)
    s.text(380, 410, "Если хотя бы один множитель равен нулю — инновация отторгается корпоративной средой.", color=INK, anchor='middle', size=10.5)
    s.text(380, 426, "Одной лишь правоты по цифрам недостаточно: лидер обязан инвестировать в диалог и институционализацию.", color=MUTED, anchor='middle', size=10)

    s.save("semmelweis-innovation-triad.svg")


def generate_ted_lasso_figure():
    s = SVG(
        "Модель эмпатичного лидерства: уроки сериала «Тед Лассо»",
        "Как вера в команду, неформальное доверие и внимание к деталям создают победную культуру.",
        w=760, h=470
    )
    s.text(32, 66, "Инструменты мягкой силы лидера: от утреннего печенья до психологической безопасности", cls='small')

    # Top Center Banner: BELIEVE Poster
    s.rect(260, 90, 240, 52, fill='#fbc02d', rx=8, stroke='#f57f17', stroke_width=2)
    s.text(380, 122, "BELIEVE", color='#0d47a1', anchor='middle', cls='heading', size=24)
    s.text(380, 136, "Вера в потенциал команды и право на ошибку", color='#1565c0', anchor='middle', size=9.5)

    # Connecting tree lines
    s.line(380, 142, 142, 172, color='#fbc02d', width=2)
    s.line(380, 142, 380, 172, color='#fbc02d', width=2)
    s.line(380, 142, 618, 172, color='#fbc02d', width=2)

    # 3 Column Cards
    col_w = 220
    col_h = 168

    # 1. Coach Beard
    s.rect(32, 172, col_w, col_h, fill='#f8fbff', rx=8, stroke='#1976d2', stroke_width=1.5)
    s.rect(32, 172, col_w, 40, fill='#1976d2', rx=8)
    s.rect(32, 198, col_w, 14, fill='#1976d2', rx=0)
    s.text(142, 190, "Тренер Бирд (Coach Beard)", color='#fff', anchor='middle', cls='bold', size=11)
    s.text(142, 204, "Системный балансир", color='#bbdefb', anchor='middle', size=9.5)

    beard_pts = [
        "• Тихий стратег за спиной лидера",
        "• Знание правил и регламентов",
        "• Холодный расчет без паники",
        "• Балансирует эмоции команды"
    ]
    for i, pt in enumerate(beard_pts):
        s.text(42, 230 + i * 26, pt, color=INK, size=10)

    # 2. Biscuits with the Boss
    s.rect(270, 172, col_w, col_h, fill='#f6fbf7', rx=8, stroke='#2e7d32', stroke_width=1.5)
    s.rect(270, 172, col_w, 40, fill='#2e7d32', rx=8)
    s.rect(270, 198, col_w, 14, fill='#2e7d32', rx=0)
    s.text(380, 190, "Печенье с боссом (Biscuits)", color='#fff', anchor='middle', cls='bold', size=11)
    s.text(380, 204, "Культура неформального доверия", color='#c8e6c9', anchor='middle', size=9.5)

    bisc_pts = [
        "• 15 минут в день без повесток",
        "• Разрушение барьера власти",
        "• Искренний интерес к человеку",
        "• Гашение конфликтов на старте"
    ]
    for i, pt in enumerate(bisc_pts):
        s.text(280, 230 + i * 26, pt, color=INK, size=10)

    # 3. Nate the Great
    s.rect(508, 172, col_w, col_h, fill='#fdf6f9', rx=8, stroke='#c2185b', stroke_width=1.5)
    s.rect(508, 172, col_w, 40, fill='#c2185b', rx=8)
    s.rect(508, 198, col_w, 14, fill='#c2185b', rx=0)
    s.text(618, 190, "Трагедия Нейта (Nate)", color='#fff', anchor='middle', cls='bold', size=11)
    s.text(618, 204, "Цена невнимания к талантам", color='#f8bbd0', anchor='middle', size=9.5)

    nate_pts = [
        "• Недооценка скромного ума",
        "• Дефицит признания ранит эго",
        "• Затаенная обида рождает яд",
        "• Забота о невидимых героях"
    ]
    for i, pt in enumerate(nate_pts):
        s.text(518, 230 + i * 26, pt, color=INK, size=10)

    # Bottom Takeaway box
    s.rect(32, 360, 696, 68, fill='#f0f7ff', rx=8, stroke=BLUE, stroke_width=1)
    s.text(380, 384, "Принцип Уолта Уитмена: «Be curious, not judgmental» (Будь любознательным, а не осуждающим)", color=BLUE, anchor='middle', cls='bold', size=11.5)
    s.text(380, 402, "При ошибке сотрудника лидер выясняет системную причину сбоя, вместо крика и поиска виновных.", color=INK, anchor='middle', size=10.5)
    s.text(380, 418, "Побеждает культура психологической безопасности, а не страх репрессий.", color=MUTED, anchor='middle', size=10)

    s.save("ted-lasso-leadership-model.svg")


if __name__ == '__main__':
    generate_iceberg_figure()
    generate_digitalization_figure()
    generate_how_the_mighty_fall_figure()
    generate_leadership_triad_figure()
    generate_semmelweis_triad_figure()
    generate_ted_lasso_figure()
