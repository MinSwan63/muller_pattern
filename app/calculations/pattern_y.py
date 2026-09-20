from app.calculations.base import BasePattern, CalculationResult, MeasurementField


class PatternY(BasePattern):
    code = "pattern_y"
    name = "الگوی Y"
    description = "الگوی پایه دامن"

    measurements = [
        MeasurementField(key="waist", label="دور کمر", min_value=40, max_value=200),
        MeasurementField(key="hip", label="دور باسن", min_value=40, max_value=200),
        MeasurementField(key="length", label="قد دامن", min_value=20, max_value=150),
    ]

    def calculate(self, data):
        waist = float(data["waist"])
        hip = float(data["hip"])
        length = float(data["length"])

        # ================================================
        # PLACEHOLDER CALCULATION
        # Replace with official Müller formula later.
        # ================================================
        return [
            CalculationResult(
                name="عرض کمر",
                value=round(waist / 4 + 1, 2),
                unit="cm",
                description="محاسبه آزمایشی — بعداً با فرمول مولر جایگزین می‌شود.",
            ),
            CalculationResult(
                name="عرض باسن",
                value=round(hip / 4 + 1.5, 2),
                unit="cm",
                description="محاسبه آزمایشی — بعداً با فرمول مولر جایگزین می‌شود.",
            ),
            CalculationResult(
                name="بلندی قد دامن",
                value=round(length, 2),
                unit="cm",
                description="محاسبه آزمایشی — بعداً با فرمول مولر جایگزین می‌شود.",
            ),
        ]
