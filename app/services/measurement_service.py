CM_PER_INCH = 2.54


def to_cm(value, unit):
    if unit == "inch":
        return value * CM_PER_INCH
    return value


def from_cm(value, unit):
    if unit == "inch":
        return value / CM_PER_INCH
    return value


def normalize_measurements(data, unit):
    return {k: to_cm(float(v), unit) for k, v in data.items() if v not in (None, "")}


def denormalize_results(results, unit):
    for r in results:
        if r.unit == "cm":
            r.value = round(from_cm(r.value, unit), 2)
            r.unit = "سانتی‌متر" if unit == "cm" else "اینچ"
    return results
