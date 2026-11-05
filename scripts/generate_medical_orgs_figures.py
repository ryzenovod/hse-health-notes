"""Deterministic SVG figures for Medical Organizations: Finance, Staffing and Norms.
"""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/assets/medical-organizations'

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


def generate_fot_structure_figure():
    s = SVG(
        "Норматив структуры фонда оплаты труда медорганизации",
        "Соотношение медицинского и административно-управленческого персонала в ФОТ по рекомендациям РТК.",
        w=760, h=400
    )
    s.text(32, 68, "Единые рекомендации Российской трехсторонней комиссии по социально-трудовым отношениям", cls='small')

    bar_x = 32
    bar_y = 110
    total_w = 696
    h = 48

    med_w = total_w * 0.60
    aup_w = total_w * 0.40

    # Bar
    s.rect(bar_x, bar_y, med_w, h, fill=BLUE, rx=6)
    s.rect(bar_x + med_w, bar_y, aup_w, h, fill=ORANGE, rx=6)
    # Fix joint
    s.rect(bar_x + med_w - 4, bar_y, 8, h, fill=ORANGE, rx=0)

    s.text(bar_x + med_w / 2, bar_y + 30, "Медицинский персонал: не менее 60% ФОТ", color='#fff', anchor='middle', cls='bold', size=14)
    s.text(bar_x + med_w + aup_w / 2, bar_y + 30, "АУП и прочие: не более 40%", color='#fff', anchor='middle', cls='bold', size=13)

    # Details Cards
    # Left Card: Medical
    cx1 = 32
    cy1 = 185
    cw1 = med_w
    s.rect(cx1, cy1, cw1, 165, fill='#f0f4ff', rx=8, stroke=BLUE, stroke_width=2)
    s.text(cx1 + 16, cy1 + 28, "Непосредственно лечебный состав", color=BLUE, cls='bold', size=15)
    s.text(cx1 + 16, cy1 + 56, "• Врачи всех специальностей", size=13)
    s.text(cx1 + 16, cy1 + 80, "• Средний медперсонал (СМП: медсестры, фельдшеры, акушеры)", size=13)
    s.text(cx1 + 16, cy1 + 104, "• Младший медперсонал (ММП: санитары, младшие медсестры)", size=13)
    s.text(cx1 + 16, cy1 + 128, "• Немедицинские специалисты (психологи, биологи, эксперты лабораторий)", color=MUTED, size=12)
    s.text(cx1 + 16, cy1 + 150, "Целевой ориентир майских указов: врачи 200%, СМП/ММП 100% средней по региону", color=BLUE, size=11, cls='bold')

    # Right Card: Non-medical
    cx2 = bar_x + med_w + 12
    cy2 = 185
    cw2 = aup_w - 12
    s.rect(cx2, cy2, cw2, 165, fill='#fff5eb', rx=8, stroke=ORANGE, stroke_width=2)
    s.text(cx2 + 16, cy2 + 28, "АУП и вспомогательные службы", color=ORANGE, cls='bold', size=15)
    s.text(cx2 + 16, cy2 + 56, "• Главный врач и его заместители", size=13)
    s.text(cx2 + 16, cy2 + 80, "• Бухгалтерия, экономический отдел, юристы", size=13)
    s.text(cx2 + 16, cy2 + 104, "• Отдел кадров, IT-служба, инженеры", size=13)
    s.text(cx2 + 16, cy2 + 128, "• Хозяйственные и эксплуатационные службы", size=13)
    s.text(cx2 + 16, cy2 + 150, "Превышение 40% лимита — маркер неэффективности", color=ORANGE, size=11, cls='bold')

    s.text(32, 380, "Заведующие отделениями относятся к АУП, но обычно совмещают ставку врача.", cls='small')
    s.save("medical-fot-structure.svg")


def generate_time_norm_compromise_figure():
    s = SVG(
        "Нормирование времени приема терапевта: экономический компромисс",
        "Сравнение фактических хронометражных замеров ЦНИИОИЗ и утвержденного норматива Минздрава.",
        w=760, h=430
    )
    s.text(32, 68, "Приказ Минздрава России № 290н и данные фотохронометражных исследований", cls='small')

    # Two columns comparison
    col_w = 330
    c1_x = 32
    c2_x = 398
    card_y = 100
    card_h = 270

    # Left: Fact
    s.rect(c1_x, card_y, col_w, card_h, fill='#fff2f2', rx=8, stroke=RED, stroke_width=2)
    s.rect(c1_x, card_y, col_w, 40, fill=RED, rx=8)
    s.rect(c1_x, card_y + 28, col_w, 12, fill=RED, rx=0)
    s.text(c1_x + col_w / 2, card_y + 26, "Реальный хронометраж (ЦНИИОИЗ)", color='#fff', anchor='middle', cls='bold', size=14)

    s.text(c1_x + col_w / 2, card_y + 80, "25–28 минут", color=RED, anchor='middle', cls='heading', size=26)
    s.text(c1_x + col_w / 2, card_y + 105, "фактическое время качественного приема", color=MUTED, anchor='middle', size=12)

    s.text(c1_x + 16, card_y + 140, "• Осмотр, сбор анамнеза, опрос: 12–15 мин", size=12)
    s.text(c1_x + 16, card_y + 162, "• Заполнение ЕМИАС / документация: 8–10 мин", size=12)
    s.text(c1_x + 16, card_y + 184, "• Разъяснение схемы лечения: 4–5 мин", size=12)
    s.line(c1_x + 16, card_y + 200, c1_x + col_w - 16, card_y + 200, color='#f5c6cb')
    s.text(c1_x + 16, card_y + 220, "Экономическое последствие:", color=RED, cls='bold', size=12)
    s.text(c1_x + 16, card_y + 240, "Потребовалось бы почти в 2 раза больше врачей", color=RED, size=11)
    s.text(c1_x + 16, card_y + 256, "и удвоение фонда оплаты труда", color=RED, size=11)

    # Right: Standard
    s.rect(c2_x, card_y, col_w, card_h, fill='#eef8f6', rx=8, stroke=TEAL, stroke_width=2)
    s.rect(c2_x, card_y, col_w, 40, fill=TEAL, rx=8)
    s.rect(c2_x, card_y + 28, col_w, 12, fill=TEAL, rx=0)
    s.text(c2_x + col_w / 2, card_y + 26, "Типовая норма (Приказ № 290н)", color='#fff', anchor='middle', cls='bold', size=14)

    s.text(c2_x + col_w / 2, card_y + 80, "15 минут", color=TEAL, anchor='middle', cls='heading', size=26)
    s.text(c2_x + col_w / 2, card_y + 105, "управленческая типовая норма Минздрава", color=MUTED, anchor='middle', size=12)

    s.text(c2_x + 16, card_y + 140, "• Расчетная норма для планирования штатов", size=12)
    s.text(c2_x + 16, card_y + 162, "• Обеспечивает функцию врачебной должности", size=12)
    s.text(c2_x + 16, card_y + 184, "• Ориентир для слотов записи в ЕМИАС", size=12)
    s.line(c2_x + 16, card_y + 200, c2_x + col_w - 16, card_y + 200, color='#bfe5df')
    s.text(c2_x + 16, card_y + 220, "Практика и автономия МО:", color=TEAL, cls='bold', size=12)
    s.text(c2_x + 16, card_y + 240, "Клиники могут утверждать локальные нормы", color=INK, size=11)
    s.text(c2_x + 16, card_y + 256, "и вводить буферные интервалы для сложных пациентов", color=INK, size=11)

    s.text(32, 405, "Типовая норма служит инструментом макропланирования кадровой потребности отрасли.", cls='small')
    s.save("time-norm-compromise.svg")


def generate_staffing_pipeline_figure():
    s = SVG(
        "Цепочка кадрового планирования медицинской организации",
        "От демографического анализа прикрепленного населения к штатному расписанию и бюджету ФОТ.",
        w=760, h=410
    )
    s.text(32, 68, "Алгоритм перехода от потребностей жителей к штатным единицам и расходам ПФХД", cls='small')

    steps = [
        ("1. Население", "Численность, пол, возраст (0–4 и 55+), профиль заболеваемости", BLUE),
        ("2. Инфраструктура", "Мощность объектов («домиков»), койки, визиты в смену, ФАПы", TEAL),
        ("3. Параметры помощи", "3 формы (экстренная/неотложная/плановая), 4 вида, 4 условия", PURPLE),
        ("4. Нормативы Порядков", "Более 90 порядков медпомощи (напр. 1 уролог на 20 тыс. взр.)", ORANGE),
        ("5. Штаты и ФОТ", "Штатное расписание, ставки, совместительство, ФОТ в ПФХД", RED)
    ]

    base_y = 95
    row_h = 55
    start_x = 32
    step_w = 696

    for i, (title, desc, col) in enumerate(steps):
        y = base_y + i * row_h
        s.rect(start_x, y, 160, 42, fill=col, rx=6)
        s.text(start_x + 12, y + 26, title, color='#fff', cls='bold', size=13)

        s.rect(start_x + 172, y, step_w - 172, 42, fill=BG_LIGHT, rx=6, stroke=col, stroke_width=1)
        s.text(start_x + 188, y + 26, desc, color=INK, size=13)

        if i < len(steps) - 1:
            s.line(start_x + 80, y + 42, start_x + 80, y + row_h, color=col, width=2)

    s.text(32, 385, "Дробные доли ставок (0,25 или 0,5) на уровне отдельной клиники требуют найма целого физлица.", cls='small')
    s.save("staffing-planning-pipeline.svg")


if __name__ == '__main__':
    generate_fot_structure_figure()
    generate_time_norm_compromise_figure()
    generate_staffing_pipeline_figure()
