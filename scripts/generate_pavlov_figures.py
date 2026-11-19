"""Deterministic SVG figures for Healthcare Economics: Rostislav Pavlov on Healthcare Management, AI, and Culture of Safety.
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
    def __init__(self, title, desc, w=760, h=450):
        self.w, self.h = w, h
        self.items = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">',
            f'<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>',
            '<style>text{font-family:Inter,system-ui,-apple-system,sans-serif;fill:#18213a;font-size:16px} .small{font-size:13px;fill:#54627a} .heading{font-size:20px;font-weight:700} .bold{font-weight:600}</style>',
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

    def polygon(self, points, fill, stroke=None, stroke_width=1):
        stroke_attr = f' stroke="{stroke}" stroke-width="{stroke_width}"' if stroke else ''
        self.items.append(f'<polygon points="{points}" fill="{fill}"{stroke_attr}/>')

    def save(self, name):
        OUT.mkdir(parents=True, exist_ok=True)
        path = OUT / name
        path.write_text('\n'.join(self.items + ['</svg>']) + '\n', encoding='utf-8')
        print(f"Saved: {path}")


def generate_iceberg_figure():
    s = SVG(
        "Модель айсберга: восприятие качества медицины пациентом",
        "Сравнение видимой верхушки (сервис и эмпатия) и подводной толщи (клиническая безопасность и стерильность).",
        w=760, h=460
    )
    s.text(32, 68, "Пациент оценивает отношение и чистоту, но его жизнь спасает подводная часть системы", cls='small')

    # Waterline boundary
    wl_y = 175
    s.rect(32, 95, 696, wl_y - 95, fill='#f0f7ff', rx=8)
    s.rect(32, wl_y, 696, 220, fill='#e6f0fa', rx=8)

    # Waterline wave/line
    s.line(32, wl_y, 728, wl_y, color='#0288d1', width=3, dash=True)
    s.text(716, wl_y - 8, "Ватерлиния восприятия пациента", color='#0288d1', anchor='end', cls='bold', size=11)

    # Top Part: 15% Visible
    s.rect(48, 108, 140, 28, fill='#0288d1', rx=6)
    s.text(118, 127, "ВЕРХУШКА (15%)", color='#fff', anchor='middle', cls='bold', size=11)
    s.text(202, 127, "Видимый сервис (то, на основе чего пациент делает осознанный выбор)", color='#0277bd', cls='bold', size=13)

    visible_points = [
        "• Эмпатия врача, уважительный тон, отсутствие снисходительности",
        "• Чистота палат, свежий ремонт, опрятный вид медперсонала",
        "• Вкусное горячее питание и прозрачная навигация в коридорах",
        "• Скорость записи, отсутствие очередей, мобильное приложение"
    ]
    for idx, pt in enumerate(visible_points):
        col = idx % 2
        row = idx // 2
        s.text(52 + col * 340, 148 + row * 18, pt, color=INK, size=11)

    # Bottom Part: 85% Hidden
    s.rect(48, 190, 140, 28, fill='#1a365d', rx=6)
    s.text(118, 209, "ПОДВОДНАЯ ЧАСТЬ (85%)", color='#fff', anchor='middle', cls='bold', size=10)
    s.text(202, 209, "Фундамент безопасности (пациент не может оценить профессионально)", color='#1a365d', cls='bold', size=13)

    hidden_points = [
        ("Стерильность и санэпидрежим", "Контроль ИСМП, вентиляция с ламинарным потоком в операционных"),
        ("Чек-листы ВОЗ и тайм-ауты", "Идентификация пациента, стороны операции, подсчет салфеток и игл"),
        ("Калибровка оборудования", "Поверка томографов, наркозно-дыхательных аппаратов и дозаторов"),
        ("Фармаконадзор и совместимость", "Двойной контроль введения высокорисковых лекарств и антибиотиков"),
        ("Учет осложнений (M&M Conferences)", "Регулярный разбор клинических инцидентов без поиска козла отпущения"),
        ("Командная слаженность бригад", "Регулярные симуляционные учения при экстренных реанимациях")
    ]

    for idx, (head, desc) in enumerate(hidden_points):
        bx = 48 + (idx % 2) * 340
        by = 226 + (idx // 2) * 52
        s.rect(bx, by, 326, 46, fill='#fff', rx=6, stroke='#b0bec5', stroke_width=1)
        s.text(bx + 10, by + 18, head, color='#0d47a1', cls='bold', size=11)
        s.text(bx + 10, by + 36, desc, color=MUTED, size=10)

    # Bottom takeaway
    s.rect(32, 405, 696, 42, fill='#fff9e6', rx=6, stroke='#fbc02d', stroke_width=1)
    s.text(48, 431, "Управленческий парадокс: плохой кофе отпугнет пациента быстрее, чем отсутствие протокола стерильности.", color='#e65100', cls='bold', size=12)
    s.save("iceberg-quality-perception.svg")


def generate_digitalization_figure():
    s = SVG(
        "Ловушка цифровизации: Процесс → Цифровой контур → ИИ",
        "Почему автоматизация хаоса приводит к катастрофе: сравнение Babylon Health и ЕМИАС Москвы.",
        w=760, h=450
    )
    s.text(32, 68, "Формула Ростислава Павлова: сначала стандартизация процессов, затем цифра, затем ИИ", cls='small')

    # Top: Bad Case (Babylon Health)
    c_y = 95
    c_w = 696
    s.rect(32, c_y, c_w, 130, fill='#fff5f5', rx=8, stroke=RED, stroke_width=1.5)
    s.rect(32, c_y, 220, 32, fill=RED, rx=8)
    s.rect(32, c_y + 20, 220, 12, fill=RED, rx=0)
    s.text(142, c_y + 22, "Крах: Babylon Health (UK/USA)", color='#fff', anchor='middle', cls='bold', size=12)

    s.text(265, c_y + 22, "Оценка $4.2 млрд → Банкротство с долгами -$1 млрд", color=RED, cls='bold', size=12)

    babylon_steps = [
        ("1. Хаос в процессах", "Попытка перепрыгнуть базовые клинические протоколы"),
        ("2. Хайповый чат-бот", "ИИ-триаж на неподготовленных данных симптомов"),
        ("3. Клинический провал", "Пропуск стенокардии у курильщиков, риск для жизней"),
        ("4. Финал", "Отзыв контрактов NHS, ликвидация бизнеса")
    ]
    for idx, (title, sub) in enumerate(babylon_steps):
        bx = 46 + idx * 168
        by = c_y + 42
        s.rect(bx, by, 160, 72, fill='#fff', rx=6, stroke='#ffcdd2', stroke_width=1)
        s.text(bx + 8, by + 22, title, color=RED, cls='bold', size=11)
        s.text(bx + 8, by + 40, sub[:24], color=MUTED, size=9)
        s.text(bx + 8, by + 54, sub[24:], color=MUTED, size=9)
        if idx < 3:
            s.text(bx + 163, by + 40, "→", color=RED, cls='bold', size=14)

    # Bottom: Good Case (ЕМИАС Москвы)
    g_y = 245
    s.rect(32, g_y, c_w, 145, fill='#f0fdf4', rx=8, stroke=TEAL, stroke_width=1.5)
    s.rect(32, g_y, 220, 32, fill=TEAL, rx=8)
    s.rect(32, g_y + 20, 220, 12, fill=TEAL, rx=0)
    s.text(142, g_y + 22, "Эталон: ЕМИАС (Москва)", color='#fff', anchor='middle', cls='bold', size=12)

    s.text(265, g_y + 22, "Крупнейшая в мире единая система лучевой диагностики и ИИ", color=TEAL, cls='bold', size=12)

    emias_steps = [
        ("Шаг 1. Процессы", "Унификация расписаний, нозологий, протоколов приема и регламентов времени"),
        ("Шаг 2. Цифровой контур", "Сквозная электронная медкарта (ЭМК), подключение всех аппаратов КТ/МРТ"),
        ("Шаг 3. ИИ-ассистент", "Автоматический второй просмотр КТ/маммографии, подсказки врачу-рентгенологу")
    ]
    for idx, (title, sub) in enumerate(emias_steps):
        bx = 46 + idx * 226
        by = g_y + 42
        s.rect(bx, by, 218, 86, fill='#fff', rx=6, stroke='#c8e6c9', stroke_width=1)
        s.text(bx + 10, by + 24, title, color=TEAL, cls='bold', size=12)
        # wrap text
        words = sub.split()
        line1 = " ".join(words[:4])
        line2 = " ".join(words[4:8])
        line3 = " ".join(words[8:])
        s.text(bx + 10, by + 44, line1, color=MUTED, size=10)
        s.text(bx + 10, by + 58, line2, color=MUTED, size=10)
        s.text(bx + 10, by + 72, line3, color=MUTED, size=10)
        if idx < 2:
            s.text(bx + 221, by + 46, "→", color=TEAL, cls='bold', size=14)

    # Footer takeaway
    s.rect(32, 405, c_w, 36, fill='#edf2fc', rx=6)
    s.text(48, 428, "Золотое правило цифровизации: Оцифрованный хаос = Автоматизированный хаос с тройным бюджетом.", color=BLUE, cls='bold', size=11)
    s.save("digitalization-babylon-vs-emias.svg")


def generate_how_the_mighty_fall_figure():
    s = SVG(
        "5 стадий гибели великих компаний (по Джиму Коллинзу)",
        "Закономерности деградации лидеров рынка и клиник при потере контакта с реальностью.",
        w=760, h=440
    )
    s.text(32, 68, "От Kodak и Nokia до неэффективных медицинских гигантов: траектория упадка", cls='small')

    stages = [
        ("1. Высокомерие от успехов", "Hubris Born of Success", "«Мы непререкаемые лидеры, конкуренты бессильны, пациенты никуда не денутся». Потеря самокритики.", '#1e88e5'),
        ("2. Безудержная экспансия", "Undisciplined Pursuit of More", "Неконтролируемый рост коек и филиалов в ущерб клиническому качеству и компетентности врачей.", '#3949ab'),
        ("3. Отрицание рисков", "Denial of Risk and Peril", "Игнорирование тревожных сигналов (рост осложнений, жалобы). Наказание за плохие новости.", '#fb8c00'),
        ("4. Поиски «чудо-таблетки»", "Grasping for Salvation", "Судорожная смена главврачей, слепая покупка дорогого ИИ или хайпового оборудования без процессов.", '#e53935'),
        ("5. Капитуляция и крах", "Capitulation to Irrelevance", "Потеря доверия врачей и пациентов, финансовая яма, банкротство или передача под внешнее управление.", '#8e0000')
    ]

    base_y = 95
    row_h = 58
    start_x = 32
    step_w = 696

    for idx, (title, en_title, desc, col) in enumerate(stages):
        y = base_y + idx * row_h
        s.rect(start_x, y, 195, 46, fill=col, rx=6)
        s.text(start_x + 12, y + 20, title, color='#fff', cls='bold', size=11)
        s.text(start_x + 12, y + 36, en_title, color='#ffecb3' if idx >= 2 else '#bbdefb', size=9)

        s.rect(start_x + 205, y, step_w - 205, 46, fill=BG_LIGHT, rx=6, stroke=col, stroke_width=1)
        s.text(start_x + 218, y + 27, desc, color=INK, size=11)

        if idx < len(stages) - 1:
            s.line(start_x + 97, y + 46, start_x + 97, y + row_h, color=col, width=2)

    s.text(32, 405, "Главный симптом стадии 3: подчиненные боятся сообщать руководителю о реальных инцидентах и врачебных ошибках.", cls='small')
    s.save("how-the-mighty-fall-stages.svg")


def generate_leadership_triad_figure():
    s = SVG(
        "Куда уходит время системного лидера медицинской организации",
        "Разделение зон ответственности: почему главврач не должен проверять полы и карты пациентов.",
        w=760, h=440
    )
    s.text(32, 68, "Архитектура управления: внешний контур, стратегическая культура и автономные процессы", cls='small')

    col_w = 218
    col_h = 245
    col_y = 95

    cols = [
        ("1. Защита и ресурсы (GR)", "Внешний контур и безопасность", '#1565c0', [
            "• «Крыша» и щит для коллектива",
            "• Защита врачей от силового давления",
            "• Переговоры с Минздравом и ТФОМС",
            "• Привлечение субсидий и инвестиций",
            "• Защита фонда заработной платы"
        ]),
        ("2. Стратегия и культура", "Внутренний климат и инновации", '#2e7d32', [
            "• Культура No-Blame (без поиска виновных)",
            "• Внедрение стандартов ISO 9001 / JCI",
            "• Психологическая безопасность в команде",
            "• Выращивание лидеров и работа с Gen Z",
            "• Внедрение ИИ и цифровых помощников"
        ]),
        ("3. Продукт и исходы (VBHC)", "Ценность для пациента", '#c2185b', [
            "• Клинические исходы (PROMs / PREMs)",
            "• Снижение летальности и осложнений",
            "• Развитие симуляционного центра",
            "• Пациентский сервис и репутация",
            "• Доверие и долгосрочная лояльность"
        ])
    ]

    for idx, (title, sub, col, items) in enumerate(cols):
        cx = 32 + idx * (col_w + 21)
        s.rect(cx, col_y, col_w, col_h, fill='#fcfdfe', rx=8, stroke=col, stroke_width=1.5)
        s.rect(cx, col_y, col_w, 42, fill=col, rx=8)
        s.rect(cx, col_y + 30, col_w, 12, fill=col, rx=0)
        s.text(cx + col_w / 2, col_y + 20, title, color='#fff', anchor='middle', cls='bold', size=11)
        s.text(cx + col_w / 2, col_y + 34, sub, color='#e0e0e0', anchor='middle', size=9)

        for i_item, it in enumerate(items):
            s.text(cx + 12, col_y + 68 + i_item * 34, it, color=INK, size=10)

    # Base Foundation: Autonomous Operations
    s.rect(32, 355, 696, 65, fill='#263238', rx=8)
    s.text(380, 380, "ФУНДАМЕНТ: АВТОНОМНЫЕ ОПЕРАЦИОННЫЕ ПРОЦЕССЫ", color='#80cbc4', anchor='middle', cls='bold', size=12)
    s.text(380, 402, "Если главврач лично указывает санитаркам, как мыть полы, или вручную проверяет каждую историю болезни —", color='#eceff1', anchor='middle', size=10)
    s.text(380, 414, "организация обречена на стагнацию. Рутина должна работать по четким чек-листам без ручного вмешательства.", color='#b0bec5', anchor='middle', size=10)

    s.save("leadership-system-triad.svg")


if __name__ == '__main__':
    generate_iceberg_figure()
    generate_digitalization_figure()
    generate_how_the_mighty_fall_figure()
    generate_leadership_triad_figure()
