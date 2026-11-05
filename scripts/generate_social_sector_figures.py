"""Deterministic, accessible SVG figures for Social Sector Economics and Management.
"""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/assets/social-sector'

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
    def __init__(self, title, desc, w=760, h=480):
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


def generate_spending_figure():
    s = SVG(
        "Расходы на отрасли социальной сферы (% ВВП)",
        "Сравнение масштабов расходов на здравоохранение, образование и соцзащиту в мире и отдельных странах.",
        w=760, h=490
    )
    s.text(32, 70, "Доли совокупных (гос. + частных) расходов по данным World Bank и ОЭСР", cls='small')

    # Categories
    data = [
        ("Соцрасходы (Франция, Германия)", 26.5, RED, "25–29% ВВП"),
        ("Соцрасходы (Великобритания, Россия, Израиль)", 14.0, ORANGE, "13–15% ВВП"),
        ("Здравоохранение: страны с высоким доходом", 11.5, BLUE, "~11–12% ВВП"),
        ("Здравоохранение: среднемировой уровень", 10.0, TEAL, "~10% ВВП"),
        ("Здравоохранение: низкий и средний доход", 4.5, PURPLE, "3,5–5% ВВП"),
        ("Образование: государственные расходы в мире", 4.0, '#3f51b5', "3,5–4,5% ВВП"),
    ]

    base_y = 100
    row_height = 58
    max_pct = 30.0
    bar_max_w = 420.0
    start_x = 32

    # Draw grid lines
    for pct in [5, 10, 15, 20, 25, 30]:
        gx = start_x + (pct / max_pct) * bar_max_w
        s.line(gx, base_y - 10, gx, base_y + len(data) * row_height - 15, color=GRID, width=1, dash=True)
        s.text(gx, base_y - 16, f"{pct}%", color=MUTED, anchor='middle', size=12)

    for i, (label, val, col, text_val) in enumerate(data):
        y = base_y + i * row_height
        s.text(start_x, y + 16, label, color=INK, cls='bold', size=14)
        bar_w = (val / max_pct) * bar_max_w
        s.rect(start_x, y + 24, bar_w, 20, fill=col, rx=4)
        s.text(start_x + bar_w + 14, y + 39, text_val, color=INK, size=14, cls='bold')

    s.text(32, 465, "Совокупно отрасли социальной сферы в развитых странах аккумулируют не менее 30–35% ВВП", cls='small')
    s.save("social-sector-gdp-spending.svg")


def generate_acute_care_mix_figure():
    s = SVG(
        "Формы собственности больниц неотложной помощи (Acute Care, ОЭСР)",
        "Структура коечного фонда больниц общего профиля: государственные, некоммерческие и коммерческие.",
        w=760, h=480
    )
    s.text(32, 68, "Доли коек по типам владения (OECD Health Systems Characteristics Survey)", cls='small')

    # Data: country, public, not_for_profit, for_profit
    countries = [
        ("Канада", 100.0, 0.0, 0.0),
        ("Великобритания", 96.0, 4.0, 0.0),
        ("Франция", 66.0, 9.0, 25.0),
        ("Германия", 49.0, 36.0, 15.0),
        ("Япония", 26.3, 73.7, 0.0),
        ("Нидерланды", 0.0, 100.0, 0.0),
    ]

    base_y = 100
    row_h = 50
    start_x = 170
    bar_total_w = 430

    for i, (country, pub, nfp, fp) in enumerate(countries):
        y = base_y + i * row_h
        s.text(32, y + 18, country, color=INK, cls='bold', size=15)

        curr_x = start_x
        # Public
        if pub > 0:
            w = (pub / 100.0) * bar_total_w
            s.rect(curr_x, y + 2, w, 24, fill=BLUE, rx=3 if nfp == 0 and fp == 0 else 0)
            if pub >= 12:
                s.text(curr_x + w / 2, y + 19, f"{pub:.0f}%", color='#fff', anchor='middle', size=12, cls='bold')
            curr_x += w

        # Not for profit
        if nfp > 0:
            w = (nfp / 100.0) * bar_total_w
            s.rect(curr_x, y + 2, w, 24, fill=TEAL, rx=3 if pub == 0 and fp == 0 else 0)
            if nfp >= 12:
                s.text(curr_x + w / 2, y + 19, f"{nfp:.0f}%", color='#fff', anchor='middle', size=12, cls='bold')
            curr_x += w

        # For profit
        if fp > 0:
            w = (fp / 100.0) * bar_total_w
            s.rect(curr_x, y + 2, w, 24, fill=ORANGE, rx=3 if pub == 0 and nfp == 0 else 0)
            if fp >= 10:
                s.text(curr_x + w / 2, y + 19, f"{fp:.0f}%", color='#fff', anchor='middle', size=12, cls='bold')
            curr_x += w

    # Legend
    leg_y = 425
    s.rect(start_x, leg_y - 12, 16, 16, fill=BLUE, rx=3)
    s.text(start_x + 24, leg_y, "Государственные (Public)", size=13)

    s.rect(start_x + 200, leg_y - 12, 16, 16, fill=TEAL, rx=3)
    s.text(start_x + 224, leg_y, "Частные некоммерческие (NFP)", size=13)

    s.rect(start_x + 440, leg_y - 12, 16, 16, fill=ORANGE, rx=3)
    s.text(start_x + 464, leg_y, "Частные коммерческие", size=13)

    s.text(32, 465, "Мировой баланс: ~82% госпитализаций в мире приходится на государственный сектор", cls='small')
    s.save("hospital-acute-care-mix.svg")


def generate_rf_institutions_figure():
    s = SVG(
        "Структура учреждений госсектора в России (Минфин РФ)",
        "Распределение государственных и муниципальных учреждений по типам: БУ, КУ, АУ.",
        w=760, h=400
    )
    s.text(32, 68, "Всего в РФ: 178,8 тыс. учреждений (по закону № 83-ФЗ)", cls='small')

    cards = [
        ("Бюджетные (БУ)", "118,2 тыс.", "66,1%", "Субсидии на госзадание, закупки по 44-ФЗ и 223-ФЗ, счета в казначействе", BLUE),
        ("Казенные (КУ)", "49,1 тыс.", "27,5%", "Строгая постатейная смета, доходы в бюджет, субсидиарная ответственность", ORANGE),
        ("Автономные (АУ)", "11,5 тыс.", "6,4%", "Субсидии, счета в банках, закупки по 223-ФЗ, Наблюдательный совет", TEAL)
    ]

    card_w = 216
    card_h = 240
    gap = 24
    start_x = 32
    start_y = 95

    for i, (name, count, pct, desc, col) in enumerate(cards):
        x = start_x + i * (card_w + gap)
        s.rect(x, start_y, card_w, card_h, fill=BG_LIGHT, rx=8, stroke=col, stroke_width=2)
        s.rect(x, start_y, card_w, 42, fill=col, rx=8)
        # Fix rounded top corners only visually
        s.rect(x, start_y + 30, card_w, 12, fill=col, rx=0)

        s.text(x + card_w / 2, start_y + 26, name, color='#fff', anchor='middle', cls='bold', size=15)
        s.text(x + card_w / 2, start_y + 80, count, color=INK, anchor='middle', cls='heading', size=24)
        s.text(x + card_w / 2, start_y + 110, f"доля: {pct}", color=col, anchor='middle', cls='bold', size=16)

        # Multi-line description
        words = desc.split(", ")
        curr_desc_y = start_y + 145
        for word_chunk in words:
            s.text(x + 12, curr_desc_y, f"• {word_chunk}", color=MUTED, size=12)
            curr_desc_y += 20

    s.text(32, 375, "Реформа 83-ФЗ перевела большую часть учреждений (БУ и АУ) на модель субсидий взамен смет.", cls='small')
    s.save("public-institutions-rf-structure.svg")


def generate_trust_governance_figure():
    s = SVG(
        "Модель управления английским больничным трастом (NHS Trust)",
        "Схема разделения полномочий и общественного контроля в автономной медицинской организации.",
        w=760, h=430
    )
    s.text(32, 68, "Замена прямого бюрократического контроля институтом общественного представительства", cls='small')

    # Top: Minister
    s.rect(230, 95, 300, 52, fill=BLUE, rx=6)
    s.text(380, 118, "Госсекретарь (Министр) здравоохранения", color='#fff', anchor='middle', cls='bold', size=13)
    s.text(380, 136, "Назначает председателя совета директоров", color='#e0e5ee', anchor='middle', size=11)

    # Line down
    s.line(380, 147, 380, 180, color=BLUE, width=2)

    # Middle: Chair & Non-execs
    s.rect(130, 180, 500, 85, fill='#eef1fa', rx=8, stroke=BLUE, stroke_width=2)
    s.text(380, 204, "Совет директоров: Общественное представительство", color=BLUE, anchor='middle', cls='bold', size=14)
    s.text(380, 226, "• Председатель совета (статусное лицо, не сотрудник траста)", color=INK, anchor='middle', size=12)
    s.text(380, 246, "• До 5 внешних неисполнительных директоров (профессора, эксперты, аудиторы)", color=INK, anchor='middle', size=12)

    # Line down
    s.line(380, 265, 380, 300, color=TEAL, width=2)
    s.text(395, 287, "нанимает и контролирует", color=MUTED, size=11)

    # Bottom: Executive Directors
    s.rect(160, 300, 440, 75, fill='#e6f4f1', rx=8, stroke=TEAL, stroke_width=2)
    s.text(380, 325, "Исполнительные директора (Менеджеры траста)", color=TEAL, anchor='middle', cls='bold', size=14)
    s.text(380, 345, "Генеральный директор, главный врач, финансовый директор", color=INK, anchor='middle', size=12)
    s.text(380, 363, "Оперативное управление глобальным бюджетом, штатом и активами", color=MUTED, anchor='middle', size=11)

    s.text(32, 410, "При неэффективной работе совет директоров может досрочно расторгнуть контракт с топ-менеджментом.", cls='small')
    s.save("english-trust-governance.svg")


if __name__ == '__main__':
    generate_spending_figure()
    generate_acute_care_mix_figure()
    generate_rf_institutions_figure()
    generate_trust_governance_figure()
