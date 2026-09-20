from app.calculations.pattern_x import PatternX
from app.calculations.pattern_y import PatternY
from app.calculations.pattern_z import PatternZ


def test_pattern_x_calculate():
    p = PatternX()
    results = p.calculate({"chest": 100, "waist": 80, "height": 170})
    assert len(results) > 0
    assert results[0].value > 0


def test_pattern_x_validate_empty():
    p = PatternX()
    errors = p.validate({"chest": "", "waist": "", "height": ""})
    assert len(errors) == 3


def test_pattern_x_validate_negative():
    p = PatternX()
    errors = p.validate({"chest": -10, "waist": 80, "height": 170})
    assert len(errors) > 0


def test_pattern_y_calculate():
    p = PatternY()
    results = p.calculate({"waist": 80, "hip": 100, "length": 60})
    assert len(results) == 3


def test_pattern_z_calculate():
    p = PatternZ()
    results = p.calculate({"arm_length": 60, "arm_round": 30, "wrist": 18})
    assert len(results) == 3
