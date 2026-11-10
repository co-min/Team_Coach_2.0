# test/test_state.py

import pytest

from core.state import TrialState



def test_trial_state():

    state = TrialState(
        domain="cooking",
        animals=["A", "B", "C", "D"],
    )

    # Turn 1: Self selects A
    state.add_choice("self", "A", 24)

    assert state.self_score == 24
    assert "A" not in state.available_animals()

    # Turn 2: Agent selects C
    state.add_choice("agent", "C", 18)

    assert state.agent_score == 18

    # Duplicate selection is prohibited
    with pytest.raises(ValueError):
        state.add_choice("agent", "A", 10)

    # Turn 3: Self selects B
    state.add_choice("self", "B", 32)

    assert state.self_score == 56

    # Turn 4: Agent selects D
    state.add_choice("agent", "D", 27)

    assert state.agent_score == 45
    assert state.is_complete()
    assert state.available_animals() == []

    # New trial resets scores and selections
    next_state = TrialState(
        domain="tennis",
        animals=["A", "B", "C", "D"],
    )

    assert next_state.self_score == 0
    assert next_state.agent_score == 0
    assert len(next_state.available_animals()) == 4
