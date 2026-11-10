# 전체 trial 시행

# new trial -> 초기화
# trial state 객체를 생성하기

# core/trial.py

from core.state import TrialState
from core.turn import run_turn

from core.segment import run_choice_segment


def validate_trial_design(trial_design):
    """Check whether trial design is valid."""

    required = ["domain", "animals", "actor_order"]

    for field in required:
        if field not in trial_design:
            raise ValueError(f"Missing field: {field}")

    animals = trial_design["animals"]
    actor_order = trial_design["actor_order"]

    if len(animals) != 4 or len(set(animals)) != 4:
        raise ValueError("Trial must contain 4 unique animals")

    if (
        len(actor_order) != 2
        or set(actor_order) != {"self", "agent"}
    ):
        raise ValueError(
            "actor_order must contain self and agent once"
        )

def run_trial(context, trial_design):
    """ Run one complete trial """

    # Validate
    validate_trial_design(trial_design)


    # New trial = New state(Initialize state)
    state = TrialState(
        domain=trial_design["domain"],
        animals=list(trial_design["animals"]),
    )

    # Mission shown
    context.display.show_mission(state.domain)

    # Choice 1
    choice1_results = run_choice_segment(
        context=context,
        state=state,
        actor_order=trial_design["actor_order"],
        stage=1,
        hint_visible=False,
    )

    # Hint Shown
    context.display.set_hints(
        hint_colors=trial_design["hint_colors"],
        visible=True,
    )


    # Choice 2
    choice2_results = run_choice_segment(
            context=context,
            state=state,
            actor_order=trial_design["actor_order"],
            stage=2,
            hint_visible=True,
        )

    # Confirm trial completion
    if not state.is_complete():
        raise RuntimeError("Trial ended before all turns completed")


    # Final scores
    context.display.show_trial_result(
        self_score=state.self_score,
        agent_score=state.agent_score,
    )

    return state