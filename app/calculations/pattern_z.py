from app.calculations.base import BasePattern, CalculationResult, MeasurementField


class PatternZ(BasePattern):
    code = "pattern_z"
    name = "الگوی Z"
    description = "الگوی پایه آستین"

    measurements = [
        MeasurementField(key="arm_length", label="قد آستین", min_value=20, max_value=100),
        MeasurementField(key="arm_round", label="دور بازو", min_value=20, max_value=80),
        MeasurementField(key="wrist", label="دور مچ", min_value=10, max_value=40),
    ]

    def calculate(self, data):
        arm_length = float(data["arm_length"])
        arm_round = float(data["arm_round"])
        wrist = float(data["wrist"])

        # ================================================
        # PLACEHOLDER CALCULATION
        # Replace with official Müller formula later.
        # ================================================
        return [
            CalculationResult(
                name="بلندی آستین",
                value=round(arm_length, 2),
                unit="cm",
                description="محاسبه آزمایشی — بعداً با فرمول مولر جایگزین می‌شود.",
            ),
            CalculationResult(
                name="عرض سر آستین",
                value=round(arm_round / 3 + 2, 2),
                unit="cm",
                description="محاسبه آزمایشی — بعداً با فرمول مولر جایگزین می‌شود.",
            ),
            CalculationResult(
                name="عرض مچ",
                value=round(wrist + 2, 2),
                unit="cm",
                description="محاسبه آزمایشی — بعداً با فرمول مولر جایگزین می‌شود.",
            ),
        ]
