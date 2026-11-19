"""Deterministic SVG figures for Research Seminar: Sheiman on KSG, Staffing and Case Study.
"""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/assets/research-seminar'

INK = '#18213a'
MUTED = '#54627a'
GRID = '#e0e5ee'
BLUE = '#3859b5'
ORANGE = '#dd5a24'
TEAL = '#178477'
RED = '#b23b54'
PURPLE = '#6a3cbc'
BG_LIGHT = '#f5f6ff'

class SVG:
    def __init__(self, title, desc, w=760, h=450):
        self.w, self.h = w, h
        self.items = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">',
            f'<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>',
            '<style>text{font-family:Inter,system-ui,-apple-system,sans-serif;fill:#18213a;font-size:16px} .small{font-size:14px;fill:#54627a} .heading{font-size:21px;font-weight:700} .bold{font-weight:600}</style>',
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


def generate_ksg_evolution_figure():
    s = SVG(
        "Эволюция оплаты стационарной помощи: от перечней к КСГ",
        "Исторический кейс В. И. Бураковского в Институте Бакулева: конфликт стимулов и переход к укрупненным тарифам.",
        w=760, h=420
    )
    s.text(32, 68, "Как клинический интерес медиков к тарифам трансформировался в модель укрупнённых групп", cls='small')

    steps = [
        ("1. Поуслуговой расчет", "Детальные протоколы (напр. тетрада Фалло). Хирурги расписывают каждый шов.", ORANGE),
        ("2. Ловушка стимулов", "Поняв влияние на зарплату, врачи бесконечно удлиняют списки услуг ради тарифа.", RED),
        ("3. Инсайт Бураковского", "«Хирурги тебя дурят — давайте укрупнять!» Системный взгляд на клиническую однородность.", BLUE),
        ("4. 7 групп Института", "Сведение сотен манипуляций в 7 базовых клинико-экономических групп с твердым тарифом.", TEAL),
        ("5. Прообраз системы КСГ", "Основа современного финансирования стационаров по клинико-статистическим группам.", PURPLE)
    ]

    base_y = 95
    row_h = 55
    start_x = 32
    step_w = 696

    for i, (title, desc, col) in enumerate(steps):
        y = base_y + i * row_h
        s.rect(start_x, y, 175, 42, fill=col, rx=6)
        s.text(start_x + 12, y + 26, title, color='#fff', cls='bold', size=13)

        s.rect(start_x + 185, y, step_w - 185, 42, fill=BG_LIGHT, rx=6, stroke=col, stroke_width=1)
        s.text(start_x + 200, y + 26, desc, color=INK, size=13)

        if i < len(steps) - 1:
            s.line(start_x + 88, y + 42, start_x + 88, y + row_h, color=col, width=2)

    s.text(32, 395, "Урок: попытка учесть каждую мелочь в тарифе ведёт к инфляции расходов; работает только укрупнение.", cls='small')
    s.save("ksg-evolution-bakulev.svg")


def generate_gatekeeping_figure():
    s = SVG(
        "Роль врача общей практики: барьерная функция (Gatekeeping)",
        "Сравнение эффективности фильтрации первичных обращений в зарубежных системах и в России.",
        w=760, h=450
    )
    s.text(32, 68, "Полномочия ВОП, маршрутизация пациентов и предотвратимые госпитализации", cls='small')

    # Left: Europe/Canada
    c1_x = 32
    col_w = 336
    card_y = 95
    card_h = 300

    s.rect(c1_x, card_y, col_w, card_h, fill='#f0f7f5', rx=8, stroke=TEAL, stroke_width=2)
    s.rect(c1_x, card_y, col_w, 40, fill=TEAL, rx=8)
    s.rect(c1_x, card_y + 28, col_w, 12, fill=TEAL, rx=0)
    s.text(c1_x + col_w / 2, card_y + 26, "Европа и Канада (Сильная ПМСП)", color='#fff', anchor='middle', cls='bold', size=14)

    s.text(c1_x + col_w / 2, card_y + 75, "70–95% (ср. 80%)", color=TEAL, anchor='middle', cls='heading', size=24)
    s.text(c1_x + col_w / 2, card_y + 98, "обращений решает сам ВОП", color=MUTED, anchor='middle', size=12)

    s.text(c1_x + 16, card_y + 130, "• Доля ВОП в кадрах: 30–45%", size=13)
    s.text(c1_x + 16, card_y + 155, "• Компетенция: ЛОР, офтальмология, неврология", size=12)
    s.text(c1_x + 16, card_y + 180, "• Трудный доступ к узким спецам = фильтр", size=12)
    s.text(c1_x + 16, card_y + 205, "• Кейс Йорка: самоизлечение за время очереди", size=12)
    s.line(c1_x + 16, card_y + 225, c1_x + col_w - 16, card_y + 225, color='#c5e6df')
    s.text(c1_x + 16, card_y + 250, "Результат:", color=TEAL, cls='bold', size=13)
    s.text(c1_x + 16, card_y + 272, "Минимум avoidable admissions и ниже расходы", color=INK, size=12)

    # Right: Russia
    c2_x = 392
    s.rect(c2_x, card_y, col_w, card_h, fill='#fff4f2', rx=8, stroke=ORANGE, stroke_width=2)
    s.rect(c2_x, card_y, col_w, 40, fill=ORANGE, rx=8)
    s.rect(c2_x, card_y + 28, col_w, 12, fill=ORANGE, rx=0)
    s.text(c2_x + col_w / 2, card_y + 26, "Россия (Слабая фильтрация)", color='#fff', anchor='middle', cls='bold', size=14)

    s.text(c2_x + col_w / 2, card_y + 75, "~33% (падение с 50%)", color=ORANGE, anchor='middle', cls='heading', size=24)
    s.text(c2_x + col_w / 2, card_y + 98, "обращений замыкается на терапевте", color=MUTED, anchor='middle', size=12)

    s.text(c2_x + 16, card_y + 130, "• Доля участковых врачей: всего ~16%", size=13)
    s.text(c2_x + 16, card_y + 155, "• Раздвоение врачей: стационарные vs «не оперирующие»", size=12)
    s.text(c2_x + 16, card_y + 180, "• Любая жалоба перенаправляется к специалисту", size=12)
    s.text(c2_x + 16, card_y + 205, "• Искусственное удвоение дефицита кадров", size=12)
    s.line(c2_x + 16, card_y + 225, c2_x + col_w - 16, card_y + 225, color='#ffd5ce')
    s.text(c2_x + 16, card_y + 250, "Результат:", color=ORANGE, cls='bold', size=13)
    s.text(c2_x + 16, card_y + 272, "Перегрузка узких специалистов и стационаров", color=INK, size=12)

    s.text(32, 425, "Avoidable mortality & admissions — ключевые эконометрические маркеры эффективности ПМСП.", cls='small')
    s.save("phc-gatekeeping-avoidable.svg")


def generate_staffing_imbalance_figure():
    s = SVG(
        "Структурный дефицит кадров: модель «Too Many / Too Few»",
        "Матрица кадровых диспропорций в российском здравоохранении и пределы 3-летней отработки.",
        w=760, h=450
    )
    s.text(32, 68, "Дефицит кадров в РФ носит не абсолютный, а структурный и географический характер", cls='small')

    items = [
        ("География", "Москва, региональные центры, Татарстан", "Малые города, ЦРБ, периферия областей"),
        ("Специальности", "«Доходные» платные профили (УЗИ, гинекология, стоматология)", "Участковые терапевты, педиатры, врачи общей практики"),
        ("Уровни помощи", "Стационары (в т. ч. неоперирующие хирурги)", "Поликлиники, амбулатории, первичное звено (ПМСП)"),
        ("Возраст", "Высокая доля врачей предпенсионного возраста", "Низкое закрепление молодых выпускников на местах")
    ]

    base_y = 100
    row_h = 56
    start_x = 32
    col_w = 696

    # Headers
    s.text(start_x + 10, base_y - 8, "Ось дисбаланса", color=MUTED, cls='bold', size=13)
    s.text(start_x + 170, base_y - 8, "Где «ГУСТО» (профицит / концентрация)", color=BLUE, cls='bold', size=13)
    s.text(start_x + 440, base_y - 8, "Где «ПУСТО» (острый дефицит)", color=RED, cls='bold', size=13)

    for i, (axis, plenty, lack) in enumerate(items):
        y = base_y + i * row_h
        s.rect(start_x, y, 150, 46, fill='#edf2fc', rx=6)
        s.text(start_x + 12, y + 28, axis, color=INK, cls='bold', size=13)

        s.rect(start_x + 160, y, 260, 46, fill='#eef3fa', rx=6, stroke=BLUE, stroke_width=1)
        s.text(start_x + 172, y + 28, plenty, color=BLUE, size=11)

        s.rect(start_x + 430, y, 266, 46, fill='#fff0f0', rx=6, stroke=RED, stroke_width=1)
        s.text(start_x + 442, y + 28, lack, color=RED, size=11)

    # Bottom insight on 3-year mandate
    s.rect(start_x, 340, col_w, 65, fill='#fff9e6', rx=8, stroke='#e6b800', stroke_width=1)
    s.text(start_x + 16, 362, "Ограничение обязательной 3-летней отработки выпускников:", color='#997a00', cls='bold', size=13)
    s.text(start_x + 16, 385, "Удерживает 25% оттока ровно 3 года. Без ликвидации профессиональной изоляции и роста зарплат", color=INK, size=12)
    s.text(start_x + 16, 401, "на 4-й год врачи уходят, а новые выпуски лишь компенсируют отток без накопления кадров.", color=INK, size=12)

    s.save("staffing-too-many-too-few.svg")


def generate_case_study_roadmap_figure():
    s = SVG(
        "Дорожная карта подготовки Case Study (НИС, 1 курс)",
        "Сроки, контрольные точки и ключевые требования к письменной работе по организации здравоохранения.",
        w=760, h=420
    )
    s.text(32, 68, "Кейс-стади — не реферат, а доказательный разбор интриги и управленческого противоречия", cls='small')

    milestones = [
        ("До 1 декабря", "Выбор темы и группы", "Группы 1–5 чел. Формулировка темы в виде проблемного вопроса с интригой.", BLUE),
        ("Декабрь", "Проверка данных", "Анализ доступности статистики (формы №30, 47), интервью с ~30 коллегами.", TEAL),
        ("Декабрь – Январь", "Итерации текста", "Серия правок с научруком. Тестирование на ясность («правило домохозяйки»).", PURPLE),
        ("20–23 января", "Сдача финала", "Текст до 15 стр. Ссылки на эмпирику в тексте, баланс управления и экономики.", ORANGE),
        ("Конец января", "Доклады лучших", "10 минут, 4–5 слайдов на семинаре. Оценка 8 (отлично), 9–10 (публикация).", RED)
    ]

    base_y = 95
    row_h = 58
    start_x = 32
    step_w = 696

    for i, (date, step, desc, col) in enumerate(milestones):
        y = base_y + i * row_h
        s.rect(start_x, y, 130, 44, fill=col, rx=6)
        s.text(start_x + 65, y + 27, date, color='#fff', anchor='middle', cls='bold', size=12)

        s.rect(start_x + 140, y, 160, 44, fill='#edf2fc', rx=6)
        s.text(start_x + 152, y + 27, step, color=INK, cls='bold', size=13)

        s.rect(start_x + 310, y, step_w - 310, 44, fill=BG_LIGHT, rx=6, stroke=col, stroke_width=1)
        s.text(start_x + 322, y + 27, desc, color=MUTED, size=12)

        if i < len(milestones) - 1:
            s.line(start_x + 65, y + 44, start_x + 65, y + row_h, color=col, width=2)

    s.text(32, 400, "Запрещены бытовые суждения («мне кажется») — только доказательные выводы и строгие ссылки.", cls='small')
    s.save("case-study-roadmap.svg")


if __name__ == '__main__':
    generate_ksg_evolution_figure()
    generate_gatekeeping_figure()
    generate_staffing_imbalance_figure()
    generate_case_study_roadmap_figure()
