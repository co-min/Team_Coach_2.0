# 전체 trial 시행

# new trial -> 초기화
# trial state 객체를 생성하기



# core/trial.py

from core.state import TrialState
from core.segment import run_choice_segment


def validate_trial_design(trial_design):
    """Validate trial configuration."""

    required = [
        "domain",
        "animals",
        "actor_order",
        "hint_colors",
    ]

    for field in required:
        if field not in trial_design:
            raise ValueError(f"Missing field: {field}")

    animals = trial_design["animals"]
    actor_order = trial_design["actor_order"]

    # Exactly four unique animals
    if len(animals) != 4 or len(set(animals)) != 4:
        raise ValueError("Trial must contain 4 unique animals")

    # Self and Agent must each appear once
    if (
        len(actor_order) != 2
        or set(actor_order) != {"self", "agent"}
    ):
        raise ValueError(
            "actor_order must contain self and agent once"
        )


def run_trial(context, trial_design):
    """Run one complete trial."""

    # 1. Validate trial design
    validate_trial_design(trial_design)

    # 2. Initialize TrialState
    state = TrialState(
        domain=trial_design["domain"],
        animals=list(trial_design["animals"]),
    )

    # 3. Reset hints
    context.display.set_hints(
        hint_colors=trial_design["hint_colors"],
        visible=False,
    )

    # 4. Present mission
    context.display.show_mission(state.domain)

    # 5. Choice Stage 1 (Turn 1, Turn 2)
    run_choice_segment(
        context=context,
        state=state,
        actor_order=trial_design["actor_order"],
        stage=1,
    )

    # 6. Reveal hints
    context.display.set_hints(
        hint_colors=trial_design["hint_colors"],
        visible=True,
    )

    # 7. Choice Stage 2 (Turn 3, Turn 4)
    run_choice_segment(
        context=context,
        state=state,
        actor_order=trial_design["actor_order"],
        stage=2,
    )

    # 8. Validate trial completion
    if not state.is_complete():
        raise RuntimeError("Trial incomplete")

    # 9. Get final trial scores
    self_trial_score = state.self_score
    agent_trial_score = state.agent_score

    # 10. Update block cumulative scores
    context.cumulative_scores["self"] += self_trial_score
    context.cumulative_scores["agent"] += agent_trial_score

    # 11. Determine winner
    winner = state.winner()

    # 12. Display trial result
    context.display.show_trial_result(
        self_score=self_trial_score,
        agent_score=agent_trial_score,
        winner=winner,
    )

    return state
