
# tests/test_score.py

from function.calculate_score import calculate_turn_score


def test_turn_score():

    competence = {
        "self": {"cooking": 5},
        "agent": {"cooking": 6},
        "A": {"cooking": 8},
        "B": {"cooking": 4},
    }

    synergy = {
        "self": {"A": 2, "B": 3},
        "agent": {"A": 1, "B": 2},
    }

    # Self selects A
    score = calculate_turn_score(
        leader="self",
        animal="A",
        domain="cooking",
        competence=competence,
        synergy=synergy,
    )

    # 2 * (5 + 8) = 26
    assert score == 26

    # Agent selects B
    score = calculate_turn_score(
        leader="agent",
        animal="B",
        domain="cooking",
        competence=competence,
        synergy=synergy,
    )

    # 2 * (6 + 4) = 20
    assert score == 20
