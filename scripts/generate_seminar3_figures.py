"""Deterministic SVG figures for public-sector economics seminar 3."""

from __future__ import annotations

from fractions import Fraction
from html import escape
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]

Point = tuple[Fraction, Fraction]

INK = "#18213a"
MUTED = "#5b667a"
GRID = "#d9dfeb"
BLUE = "#3859b5"
ORANGE = "#dd5a24"
TEAL = "#178477"
RED = "#b23b54"
PAPER = "#ffffff"
PALE_BLUE = "#e9eefb"
PALE_ORANGE = "#fdeadd"
PALE_TEAL = "#e7f4ef"


def polygon_area(points: list[Point]) -> Fraction:
    """Return exact polygon area by the shoelace formula."""
    if len(points) < 3:
        return Fraction(0)
    total = Fraction(0)
    for (x1, y1), (x2, y2) in zip(points, points[1:] + points[:1]):
        total += x1 * y2 - x2 * y1
    return abs(total) / 2


def lorenz_area(points: list[Point]) -> Fraction:
    """Return exact area under a piecewise-linear Lorenz curve sorted by x."""
    ordered = sorted(points)
    total = Fraction(0)
    for (x1, y1), (x2, y2) in zip(ordered, ordered[1:]):
        total += (y1 + y2) * (x2 - x1) / 2
    return total


def gini_from_lorenz(points: list[Point]) -> Fraction:
    """Return G = 1 - 2 * lorenz_area(points)."""
    return Fraction(1) - 2 * lorenz_area(points)


def task7_before_after() -> dict[str, object]:
    """Return exact before/after Lorenz points, component areas, and Gini values."""
    before = [(Fraction(0), Fraction(0)), (Fraction(3, 5), Fraction(1, 5)), (Fraction(1), Fraction(1))]
    after = [(Fraction(0), Fraction(0)), (Fraction(3, 5), Fraction(9, 25)), (Fraction(1), Fraction(1))]
    before_area = lorenz_area(before)
    before_gini = gini_from_lorenz(before)
    after_area = lorenz_area(after)
    after_gini = gini_from_lorenz(after)
    return {
        "before_points": before,
        "after_points": after,
        "before_left_area": Fraction(3, 50),
        "before_right_area": Fraction(6, 25),
        "before_lorenz_area": before_area,
        "before_gini": before_gini,
        "after_left_area": Fraction(27, 250),
        "after_right_area": Fraction(68, 250),
        "after_lorenz_area": after_area,
        "after_gini": after_gini,
        "gini_change": before_gini - after_gini,
        "gini_relative_reduction": (before_gini - after_gini) / before_gini,
    }


def task8_tax_rows() -> list[dict[str, Fraction]]:
    """Return rows with rate, hours, gross_a, tax_revenue, net_a, income_b, total_income."""
    rows: list[dict[str, Fraction]] = []
    for rate, hours in [
        (0, Fraction(6)),
        (15, Fraction(7)),
        (30, Fraction(5)),
        (50, Fraction(5, 2)),
        (80, Fraction(1)),
        (100, Fraction(0)),
    ]:
        gross = hours * 100
        tax = gross * Fraction(rate, 100)
        net = gross - tax
        rows.append(
            {
                "rate": Fraction(rate),
                "hours": hours,
                "gross_a": gross,
                "tax_revenue": tax,
                "net_a": net,
                "income_b": tax,
                "total_income": net + tax,
            }
        )
    return rows


def table_maximin(
    rows: list[dict[str, Fraction]],
    a_key: str = "net_a",
    b_key: str = "income_b",
) -> dict[str, Fraction]:
    """Return the row maximizing min(a_key, b_key); ties keep source-table order."""
    return max(rows, key=lambda row: min(row[a_key], row[b_key]))


def render_all(out_dir: Path = Path("docs/assets/seminar-3")) -> list[Path]:
    """Write deterministic SVG files and return their paths."""
    resolved = out_dir if out_dir.is_absolute() else ROOT / out_dir
    resolved.mkdir(parents=True, exist_ok=True)
    paths = [
        _render_lorenz(resolved, "before"),
        _render_lorenz(resolved, "after"),
        _render_lorenz_comparison(resolved),
        _render_tax_revenue(resolved),
        _render_geometry_areas(resolved),
    ]
    return paths


def _fraction_attr(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}" if value.denominator != 1 else str(value.numerator)


def _percent(value: Fraction) -> str:
    return str(int(value * 100))


def _points_attr(points: Iterable[Point]) -> str:
    return " ".join(f"{_fraction_attr(x)},{_fraction_attr(y)}" for x, y in points)


def _fmt_fraction(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{float(value):.2f}".replace(".", ",")


def _grouped_integer(value: int) -> str:
    return f"{value:,}".replace(",", " ")


class SVG:
    def __init__(self, title: str, desc: str, width: int = 760, height: int = 680):
        self.width = width
        self.height = height
        self.items = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
            f'<title id="title">{escape(title)}</title>',
            f'<desc id="desc">{escape(desc)}</desc>',
            "<style>"
            "text{font-family:system-ui,-apple-system,Segoe UI,sans-serif;fill:#18213a;font-size:22px}"
            ".heading{font-size:26px;font-weight:650}"
            ".axis{font-size:22px;font-weight:600}"
            ".tick{font-size:20px;fill:#5b667a}"
            ".small{font-size:20px;fill:#5b667a}"
            ".note{font-size:23px;font-weight:650}"
            ".label{font-size:22px;font-weight:650}"
            "</style>",
            f'<rect width="{width}" height="{height}" rx="10" fill="{PAPER}"/>',
        ]
        self.text(34, 42, title, cls="heading")

    def text(
        self,
        x: float,
        y: float,
        value: str,
        *,
        color: str = INK,
        anchor: str = "start",
        cls: str = "",
        rotate: float | None = None,
    ) -> None:
        transform = f' transform="rotate({rotate:.1f} {x:.2f} {y:.2f})"' if rotate is not None else ""
        class_attr = f' class="{cls}"' if cls else ""
        self.items.append(
            f'<text x="{x:.2f}" y="{y:.2f}" text-anchor="{anchor}"{class_attr}{transform} '
            f'style="fill:{color}">{escape(value)}</text>'
        )

    def line(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        *,
        color: str = INK,
        width: float = 2,
        dash: bool = False,
    ) -> None:
        dash_attr = ' stroke-dasharray="7 7"' if dash else ""
        self.items.append(
            f'<path d="M{x1:.3f},{y1:.3f} L{x2:.3f},{y2:.3f}" fill="none" '
            f'stroke="{color}" stroke-width="{width}" stroke-linecap="round"{dash_attr}/>'
        )

    def polyline(self, points: list[tuple[float, float]], *, color: str, width: float = 3.5) -> None:
        coords = " ".join(f"{x:.3f},{y:.3f}" for x, y in points)
        self.items.append(
            f'<polyline points="{coords}" fill="none" stroke="{color}" stroke-width="{width}" '
            'stroke-linecap="round" stroke-linejoin="round"/>'
        )

    def polygon(
        self,
        points: list[tuple[float, float]],
        *,
        fill: str,
        stroke: str = "none",
        opacity: float = 1,
        data: str = "",
    ) -> None:
        coords = " ".join(f"{x:.3f},{y:.3f}" for x, y in points)
        data_attr = f" {data}" if data else ""
        self.items.append(
            f'<polygon points="{coords}" fill="{fill}" fill-opacity="{opacity}" '
            f'stroke="{stroke}" stroke-width="2"{data_attr}/>'
        )

    def dot(self, x: float, y: float, *, color: str = INK, radius: float = 5.5, data: str = "") -> None:
        data_attr = f" {data}" if data else ""
        self.items.append(f'<circle cx="{x:.3f}" cy="{y:.3f}" r="{radius}" fill="{color}"{data_attr}/>')

    def rect(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        *,
        fill: str,
        stroke: str = "none",
        rx: float = 0,
        data: str = "",
    ) -> None:
        data_attr = f" {data}" if data else ""
        self.items.append(
            f'<rect x="{x:.3f}" y="{y:.3f}" width="{width:.3f}" height="{height:.3f}" '
            f'rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="2"{data_attr}/>'
        )

    def save(self, path: Path) -> Path:
        path.write_text("\n".join(self.items + ["</svg>"]) + "\n", encoding="utf-8")
        return path


class SquarePlot:
    def __init__(
        self,
        svg: SVG,
        *,
        x: float = 120,
        y: float = 82,
        size: float = 480,
        xlabel: str,
        ylabel: str,
    ):
        self.svg = svg
        self.x = x
        self.y = y
        self.size = size
        for tick in range(0, 101, 20):
            tx = self.to_xy(Fraction(tick, 100), Fraction(0))[0]
            ty = self.to_xy(Fraction(0), Fraction(tick, 100))[1]
            svg.line(tx, y, tx, y + size, color=GRID, width=1)
            svg.line(x, ty, x + size, ty, color=GRID, width=1)
            svg.text(tx, y + size + 27, str(tick), anchor="middle", cls="tick")
            svg.text(x - 17, ty + 6, str(tick), anchor="end", cls="tick")
        svg.line(x, y + size, x + size + 8, y + size, color=INK, width=2.3)
        svg.line(x, y + size, x, y - 8, color=INK, width=2.3)
        svg.text(x + size / 2, y + size + 62, xlabel, anchor="middle", cls="axis")
        svg.text(x - 72, y + size / 2, ylabel, anchor="middle", cls="axis", rotate=-90)

    def to_xy(self, px: Fraction, py: Fraction) -> tuple[float, float]:
        return (
            self.x + float(px) * self.size,
            self.y + (1 - float(py)) * self.size,
        )

    def guide(self, px: Fraction, py: Fraction) -> None:
        x, y = self.to_xy(px, py)
        x0, y0 = self.to_xy(Fraction(0), Fraction(0))
        self.svg.line(x0, y, x, y, color=MUTED, width=1.4, dash=True)
        self.svg.line(x, y0, x, y, color=MUTED, width=1.4, dash=True)


def _render_lorenz(out_dir: Path, variant: str) -> Path:
    data = task7_before_after()
    is_after = variant == "after"
    points = data["after_points" if is_after else "before_points"]
    triangle = data["after_left_area" if is_after else "before_left_area"]
    trapezoid = data["after_right_area" if is_after else "before_right_area"]
    area = data["after_lorenz_area" if is_after else "before_lorenz_area"]
    gini = data["after_gini" if is_after else "before_gini"]
    area_percent = int(area * 10000)
    middle_y = points[1][1]
    title = "Лоренц после налога" if is_after else "Лоренц до налога"
    desc = (
        f"Точки кривой: {_points_attr(points)}. "
        f"Площадь под кривой {_fraction_attr(area)}, коэффициент Джини {_fraction_attr(gini)}."
    )
    svg = SVG(title, desc, height=730)
    plot = SquarePlot(svg, xlabel="Доля населения, %", ylabel="Доля дохода, %")
    origin = plot.to_xy(Fraction(0), Fraction(0))
    mid = plot.to_xy(Fraction(3, 5), middle_y)
    top = plot.to_xy(Fraction(1), Fraction(1))
    right_base = plot.to_xy(Fraction(1), Fraction(0))
    mid_base = plot.to_xy(Fraction(3, 5), Fraction(0))
    svg.polygon(
        [origin, mid, mid_base],
        fill=PALE_BLUE,
        stroke=BLUE,
        opacity=0.9,
        data=f'data-area="{_fraction_attr(triangle)}" data-area-percent="{int(triangle * 10000)}"',
    )
    svg.polygon(
        [mid_base, mid, top, right_base],
        fill=PALE_ORANGE,
        stroke=ORANGE,
        opacity=0.9,
        data=f'data-area="{_fraction_attr(trapezoid)}" data-area-percent="{int(trapezoid * 10000)}"',
    )
    svg.polyline([plot.to_xy(Fraction(0), Fraction(0)), top], color=MUTED, width=2.2)
    svg.polyline([plot.to_xy(x, y) for x, y in points], color=BLUE, width=4)
    for x, y in points:
        svg.dot(*plot.to_xy(x, y), color=BLUE, data=f'data-point="{_fraction_attr(x)},{_fraction_attr(y)}"')
    plot.guide(Fraction(3, 5), middle_y)
    label_y = mid[1] - 72
    svg.line(mid[0] + 7, mid[1], 608, label_y, color=MUTED, width=1.4)
    svg.text(620, label_y + 7, f"(60; {_percent(middle_y)})", color=BLUE, cls="label")
    triangle_center_y = 562 - float(middle_y) * 480 / 3
    svg.text(312, triangle_center_y + 7, f"S₁ = {_grouped_integer(int(triangle * 10000))}", color=BLUE, anchor="middle", cls="note")
    svg.text(520, 430 if is_after else 450, f"S₂ = {_grouped_integer(int(trapezoid * 10000))}", color=ORANGE, anchor="middle", cls="note")
    svg.text(120, 675, f"B = {_grouped_integer(area_percent)};  G = {_fmt_fraction(gini)}", cls="note")
    svg.text(120, 706, "Под диагональю: 5 000; B = S₁ + S₂", cls="small")
    return svg.save(out_dir / ("lorenz-after-tax.svg" if is_after else "lorenz-before.svg"))


def _render_lorenz_comparison(out_dir: Path) -> Path:
    data = task7_before_after()
    before = data["before_points"]
    after = data["after_points"]
    svg = SVG(
        "Лоренц: до и после налога",
        "Сравнение кривых Лоренца до налога и после перераспределения: средняя точка поднимается с 20 до 36 процентов дохода.",
        height=710,
    )
    plot = SquarePlot(svg, y=78, size=470, xlabel="Доля населения, %", ylabel="Доля дохода, %")
    svg.polygon(
        [plot.to_xy(Fraction(0), Fraction(0)), plot.to_xy(Fraction(3, 5), Fraction(9, 25)), plot.to_xy(Fraction(3, 5), Fraction(1, 5))],
        fill=PALE_TEAL,
        stroke=TEAL,
        opacity=0.95,
        data='data-transfer-lift="60,20->60,36"',
    )
    svg.polyline([plot.to_xy(Fraction(0), Fraction(0)), plot.to_xy(Fraction(1), Fraction(1))], color=MUTED, width=2.2)
    svg.polyline([plot.to_xy(x, y) for x, y in before], color=ORANGE, width=4)
    svg.polyline([plot.to_xy(x, y) for x, y in after], color=BLUE, width=4)
    for x, y in before:
        svg.dot(*plot.to_xy(x, y), color=ORANGE, radius=5, data=f'data-before-point="{_fraction_attr(x)},{_fraction_attr(y)}"')
    for x, y in after:
        svg.dot(*plot.to_xy(x, y), color=BLUE, radius=5.5, data=f'data-after-point="{_fraction_attr(x)},{_fraction_attr(y)}"')
    plot.guide(Fraction(3, 5), Fraction(1, 5))
    plot.guide(Fraction(3, 5), Fraction(9, 25))
    x20, y20 = plot.to_xy(Fraction(3, 5), Fraction(1, 5))
    x36, y36 = plot.to_xy(Fraction(3, 5), Fraction(9, 25))
    svg.text(x20 + 12, y20 + 8, "до: (60; 20)", color=ORANGE, cls="label")
    svg.text(x36 + 12, y36 - 12, "после: (60; 36)", color=BLUE, cls="label")
    svg.line(x36 - 28, y36, x20 - 28, y20, color=TEAL, width=3)
    svg.text(120, 651, "Джини: 0,40 → 0,24", color=TEAL, cls="note")
    svg.text(120, 684, "Нижние 60% получают 36% дохода вместо 20%", cls="small")
    return svg.save(out_dir / "lorenz-before-after.svg")


def _render_tax_revenue(out_dir: Path) -> Path:
    rows = task8_tax_rows()
    svg = SVG(
        "Налоговая выручка: шесть наблюдений",
        "Дискретные точки задачи: ставки 0, 15, 30, 50, 80, 100 процентов; выручка 0, 105, 150, 125, 80, 0.",
        height=680,
    )
    x0, y0, width, height = 105, 118, 565, 365
    max_y = Fraction(160)
    for rate in range(0, 101, 20):
        x = x0 + width * rate / 100
        svg.line(x, y0, x, y0 + height, color=GRID, width=1)
        svg.text(x, y0 + height + 27, str(rate), anchor="middle", cls="tick")
    for value in range(0, 161, 40):
        y = y0 + height * (1 - value / float(max_y))
        svg.line(x0, y, x0 + width, y, color=GRID, width=1)
        svg.text(x0 - 16, y + 6, str(value), anchor="end", cls="tick")
    svg.line(x0, y0 + height, x0 + width + 8, y0 + height, color=INK, width=2.3)
    svg.line(x0, y0 + height, x0, y0 - 8, color=INK, width=2.3)
    svg.text(x0 + width / 2, y0 + height + 62, "Ставка налога, %", anchor="middle", cls="axis")
    svg.text(x0 - 72, y0 + height / 2, "T, ден. ед.", anchor="middle", cls="axis", rotate=-90)

    def xy(rate: Fraction, tax: Fraction) -> tuple[float, float]:
        return x0 + width * float(rate) / 100, y0 + height * (1 - float(tax / max_y))

    points = [(row["rate"], row["tax_revenue"]) for row in rows]
    svg.polyline([xy(rate, tax) for rate, tax in points], color=BLUE, width=3.5)
    for row in rows:
        x, y = xy(row["rate"], row["tax_revenue"])
        color = RED if row["rate"] == 30 else BLUE
        svg.dot(x, y, color=color, radius=6, data=f'data-tax-point="{int(row["rate"])},{int(row["tax_revenue"])}"')
        dy = -13 if row["rate"] not in (0, 100) else -18
        anchor = "middle"
        svg.text(x, y + dy, f'{int(row["rate"])}%; {int(row["tax_revenue"])}', color=color, anchor=anchor, cls="label")
    svg.text(105, 86, "Максимум в таблице: 30%, T = 150.", color=ORANGE, cls="small")
    svg.text(105, 625, "Поступления: T = ставка × заработок A", cls="small")
    return svg.save(out_dir / "tax-revenue-discrete.svg")


def _render_geometry_areas(out_dir: Path) -> Path:
    svg = SVG(
        "Площади в задаче Лоренца",
        "Отдельная схема: треугольник 60 на 20 имеет площадь 600; трапеция с вертикальными основаниями 20 и 100 и расстоянием 40 имеет площадь 2400.",
        height=760,
    )
    svg.text(85, 88, "Треугольник: основание 60, высота 20", cls="axis")
    tri = [(105, 240), (345, 240), (345, 160)]
    svg.polygon(tri, fill=PALE_BLUE, stroke=BLUE, opacity=0.95, data='data-shape="triangle" data-base="60" data-height="20" data-area="600"')
    svg.line(105, 240, 345, 240, color=BLUE, width=3)
    svg.line(345, 240, 345, 160, color=BLUE, width=3)
    svg.text(225, 276, "60", color=BLUE, anchor="middle", cls="label")
    svg.text(368, 205, "20", color=BLUE, cls="label")
    svg.text(105, 320, "S = 60 × 20 / 2 = 600", color=BLUE, cls="note")

    svg.text(85, 405, "Трапеция: основания 20 и 100, расстояние 40", cls="axis")
    trap = [(215, 680), (215, 630), (315, 430), (315, 680)]
    svg.polygon(
        trap,
        fill=PALE_ORANGE,
        stroke=ORANGE,
        opacity=0.95,
        data='data-shape="trapezoid" data-bases="20,100" data-distance="40" data-area="2400"',
    )
    svg.line(215, 680, 215, 630, color=ORANGE, width=3)
    svg.line(315, 680, 315, 430, color=ORANGE, width=3)
    # Dimension line measures the perpendicular gap between the parallel sides.
    svg.line(215, 700, 315, 700, color=MUTED, width=2.5, dash=True)
    svg.text(193, 660, "20", color=ORANGE, anchor="end", cls="label")
    svg.text(337, 560, "100", color=ORANGE, cls="label")
    svg.text(265, 730, "40", color=MUTED, anchor="middle", cls="label")
    svg.text(410, 535, "S = (20 + 100)", color=ORANGE, cls="note")
    svg.text(410, 572, "÷ 2 × 40 = 2 400", color=ORANGE, cls="note")
    return svg.save(out_dir / "geometry-areas.svg")


if __name__ == "__main__":
    written = render_all()
    print("Generated", len(written), "seminar 3 SVG figures.")
