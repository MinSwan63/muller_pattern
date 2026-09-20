from dataclasses import dataclass


@dataclass
class MeasurementField:
    key: str
    label: str
    min_value: float = 1.0
    max_value: float = 500.0
    required: bool = True
    unit: str = "cm"


@dataclass
class CalculationResult:
    name: str
    value: float
    unit: str
    description: str = ""


class BasePattern:
    code = "base"
    name = "الگوی پایه"
    description = "توضیحات"
    measurements = []

    def validate(self, data):
        errors = []
        for field in self.measurements:
            value = data.get(field.key)
            if value is None or value == "":
                if field.required:
                    errors.append(f"{field.label}: لطفاً این قسمت را وارد کنید.")
                continue
            try:
                num = float(value)
            except (TypeError, ValueError):
                errors.append(f"{field.label}: مقدار واردشده معتبر نیست.")
                continue
            if num < field.min_value:
                errors.append(f"{field.label}: مقدار باید حداقل {field.min_value} باشد.")
            elif num > field.max_value:
                errors.append(f"{field.label}: مقدار باید حداکثر {field.max_value} باشد.")
        return errors

    def calculate(self, data):
        raise NotImplementedError("این الگو محاسبه را پیاده‌سازی نکرده است.")

    def to_dict(self):
        return {
            "code": self.code,
            "name": self.name,
            "description": self.description,
            "measurements": [
                {"key": m.key, "label": m.label, "required": m.required}
                for m in self.measurements
            ],
        }
