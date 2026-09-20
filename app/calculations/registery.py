from app.calculations.pattern_x import PatternX
from app.calculations.pattern_y import PatternY
from app.calculations.pattern_z import PatternZ


PATTERNS = {
    PatternX.code: PatternX(),
    PatternY.code: PatternY(),
    PatternZ.code: PatternZ(),
}


def get_pattern(code):
    return PATTERNS.get(code)


def list_patterns():
    return list(PATTERNS.values())
