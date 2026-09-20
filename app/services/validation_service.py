def validate_required(value, label):
    if value is None or str(value).strip() == "":
        return f"{label}: لطفاً این قسمت را وارد کنید."
    return None


def validate_number(value, label, min_val=0, max_val=10000):
    if value is None or str(value).strip() == "":
        return None, f"{label}: لطفاً این قسمت را وارد کنید."
    try:
        num = float(value)
    except (TypeError, ValueError):
        return None, f"{label}: مقدار واردشده معتبر نیست."
    if num <= 0:
        return None, f"{label}: مقدار باید بزرگ‌تر از صفر باشد."
    if num < min_val or num > max_val:
        return None, f"{label}: مقدار باید بین {min_val} و {max_val} باشد."
    return num, None
