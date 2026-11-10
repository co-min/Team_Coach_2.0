
# tests/test_trial.py

from unittest.mock import Mock, patch

from core.trial import run_trial


def test_trial_flow():

    context = Mock()
    context.phase_config = "competence_hint"

    context.competence = {
        "self": {"cooking": 5},
        "agent": {"cooking": 6},
        "A": {"cooking": 8},
        "B": {"cooking": 4},
        "C": {"cooking": 7},
        "D": {"cooking": 3},
    }

    context.synergy = {
        "self": {"A": 2, "B": 3, "C": 1, "D": 2},
        "agent": {"A": 1, "B": 2, "C": 2, "D": 3},
    }

    trial_design = {
        "domain": "cooking",
        "animals": ["A", "B", "C", "D"],
        "actor_order": ["self", "agent"],
    }

    # Mock display returns each animal choice
    context.display.get_choice.side_effect = ["A", "B"]
    context.agent.choose.side_effect = ["C", "D"]

    state = run_trial(context, trial_design)

    assert state.is_complete()
    assert state.self_choices == ["A", "B"]
    assert state.agent_choices == ["C", "D"]

    assert state.self_score == 53
    assert state.agent_score == 53

    context.display.show_mission.assert_called_once_with("cooking")
    context.display.show_hint.assert_called_once_with(
        "competence_hint"
    )

    context.display.show_trial_result.assert_called_once_with(
        self_score=53,
        agent_score=53,
    )
