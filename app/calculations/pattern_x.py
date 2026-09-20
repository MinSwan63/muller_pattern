from app.calculations.base import BasePattern, CalculationResult, MeasurementField


class PatternX(BasePattern):
    code = "pattern_x"
    name = "الگوی X"
    description = "الگوی پایه بالاتنه"

    measurements = [
        MeasurementField(key="chest", label="دور سینه", min_value=40, max_value=200),
        MeasurementField(key="waist", label="دور کمر", min_value=40, max_value=200),
        MeasurementField(key="height", label="قد", min_value=100, max_value=250),
    ]

    def calculate(self, data):
        chest = float(data["chest"])
        waist = float(data["waist"])
        height = float(data["height"])

        # ================================================
        # PLACEHOLDER CALCULATION
        # Replace with official Müller formula later.
        # ================================================
        return [
            CalculationResult(
                name="عرض پشت",
                value=round(chest * 0.25 + 1.5, 2),
                unit="cm",
                description="محاسبه آزمایشی — بعداً با فرمول مولر جایگزین می‌شود.",
            ),
            CalculationResult(
                name="عرض جلو",
                value=round(chest * 0.20 + 2.0, 2),
                unit="cm",
                description="محاسبه آزمایشی — بعداً با فرمول مولر جایگزین می‌شود.",
            ),
            CalculationResult(
                name="عمق حلقه آستین",
                value=round(height * 0.12, 2),
                unit="cm",
                description="محاسبه آزمایشی — بعداً با فرمول مولر جایگزین می‌شود.",
            ),
            CalculationResult(
                name="فاصله کمر تا باسن",
                value=round(waist * 0.10 + 5, 2),
                unit="cm",
                description="محاسبه آزمایشی — بعداً با فرمول مولر جایگزین می‌شود.",
            ),
        ]
