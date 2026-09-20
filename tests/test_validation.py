from app.services.measurement_service import to_cm, from_cm
from app.services.validation_service import validate_number


def test_to_cm():
    assert to_cm(1, "inch") == 2.54
    assert to_cm(100, "cm") == 100


def test_from_cm():
    assert abs(from_cm(2.54, "inch") - 1) < 0.001
    assert from_cm(100, "cm") == 100


def test_validate_number_valid():
    val, err = validate_number("50", "دور سینه", 40, 200)
    assert val == 50
    assert err is None


def test_validate_number_invalid():
    val, err = validate_number("abc", "دور سینه")
    assert val is None
    assert err is not None


def test_validate_number_negative():
    val, err = validate_number("-5", "دور سینه")
    assert val is None
    assert err is not None
