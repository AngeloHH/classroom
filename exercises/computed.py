import difflib


def score_percentage(exercise: dict, answer: dict, points: float) -> float:
    if exercise is None or answer is None: return 0.00
    args = None, exercise['value'], answer['value']
    sequence = difflib.SequenceMatcher(*args)
    return round((points * (sequence.ratio() * 100)) / 100, 2)
