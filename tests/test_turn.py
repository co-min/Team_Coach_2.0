
# tests/test_turn.py

import pytest
from dataclasses import FrozenInstanceError

from core.state import TrialState
from core.turn import execute_turn, TurnResult


@pytest.fixture
def attributes():
    """Example competence and synergy values."""

    competence = {
        "self": {"cooking": 5},
        "agent": {"cooking": 6},
        "A": {"cooking": 8},
        "B": {"cooking": 4},
        "C": {"cooking": 7},
        "D": {"cooking": 3},
    }

    synergy = {
        "self": {"A": 2, "B": 3, "C": 1, "D": 2},
        "agent": {"A": 1, "B": 2, "C": 2, "D": 3},
    }

    return competence, synergy


@pytest.fixture
def state():
    """Create a fresh TrialState."""

    return TrialState(
        domain="cooking",
        animals=["A", "B", "C", "D"],
    )


def test_four_turns(state, attributes):

    competence, synergy = attributes

    turns = [
        ("self", "A"),
        ("agent", "C"),
        ("self", "B"),
        ("agent", "D"),
    ]

    results = []

    for actor, animal in turns:
        result = execute_turn(
            state=state,
            actor=actor,
            animal=animal,
            competence=competence,
            synergy=synergy,
        )
        results.append(result)

    # Self: A=26, B=27 → 53
    assert state.self_score == 53

    # Agent: C=26, D=27 → 53
    assert state.agent_score == 53

    # Individual turn scores
    assert [r.turn_score for r in results] == [
        26, 26, 27, 27
    ]

    # Cumulative score for each actor
    assert [r.cumulative_score for r in results] == [
        26, 26, 53, 53
    ]

    assert state.is_complete()
    assert state.available_animals() == []


def test_duplicate_animal(state, attributes):

    competence, synergy = attributes

    execute_turn(
        state, "self", "A", competence, synergy
    )

    with pytest.raises(ValueError):
        execute_turn(
            state, "agent", "A", competence, synergy
        )

    # Invalid choice must not change Agent score
    assert state.agent_score == 0


def test_trial_reset(state, attributes):

    competence, synergy = attributes

    execute_turn(
        state, "self", "A", competence, synergy
    )

    # A new TrialState resets trial-specific data
    next_state = TrialState(
        domain="cooking",
        animals=["A", "B", "C", "D"],
    )

    assert next_state.self_score == 0
    assert next_state.agent_score == 0
    assert next_state.available_animals() == [
        "A", "B", "C", "D"
    ]


def test_turn_result_is_immutable():

    result = TurnResult(
        actor="self",
        animal="A",
        turn_score=26,
        cumulative_score=26,
    )

    with pytest.raises(FrozenInstanceError):
        result.turn_score = 100
