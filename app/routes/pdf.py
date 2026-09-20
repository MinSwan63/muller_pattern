from io import BytesIO
from flask import Blueprint, send_file
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pathlib import Path

try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    HAS_RTL = True
except ImportError:
    HAS_RTL = False

from app.models import Calculation
from app.calculations import get_pattern

pdf_bp = Blueprint("pdf", __name__)

FONT_PATH = Path(__file__).resolve().parent.parent / "static" / "fonts" / "Vazirmatn-Regular.ttf"


def _fa(text):
    if not text:
        return ""
    if HAS_RTL:
        return get_display(arabic_reshaper.reshape(str(text)))
    return str(text)


@pdf_bp.route("/calculation/<int:calc_id>")
def export_calculation(calc_id):
    calc = Calculation.query.get_or_404(calc_id)
    pattern = get_pattern(calc.pattern)

    try:
        if FONT_PATH.exists():
            pdfmetrics.registerFont(TTFont("Vazir", str(FONT_PATH)))
            font_name = "Vazir"
        else:
            font_name = "Helvetica"
    except Exception:
        font_name = "Helvetica"

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 30 * mm

    def line(text, size=11, gap=8):
        nonlocal y
        c.setFont(font_name, size)
        c.drawRightString(width - 20 * mm, y, _fa(text))
        y -= gap * mm

    line("گزارش محاسبه الگو", 16, 12)
    line(f"الگو: {pattern.name if pattern else calc.pattern}", 12, 10)
    client_name = calc.client.name if calc.client else "—"
    line(f"مشتری: {client_name}", 11)
    line(f"تاریخ: {calc.created_at.strftime('%Y-%m-%d %H:%M')}", 11)
    line(f"واحد: {'سانتی‌متر' if calc.unit == 'cm' else 'اینچ'}", 11, 12)

    line("اندازه‌های ورودی:", 13, 10)
    for k, v in calc.measurements.items():
        label = k
        if pattern:
            for m in pattern.measurements:
                if m.key == k:
                    label = m.label
                    break
        line(f"{label}: {v}", 11)

    y -= 5 * mm
    line("نتایج محاسبه:", 13, 10)
    for name, data in calc.results.items():
        val = data.get("value") if isinstance(data, dict) else data
        unit = data.get("unit", "") if isinstance(data, dict) else ""
        line(f"{name}: {val} {unit}", 11)

    c.showPage()
    c.save()
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"calculation_{calc.id}.pdf",
        mimetype="application/pdf",
    )
