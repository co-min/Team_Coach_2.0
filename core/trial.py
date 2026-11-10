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

    # 반드시 서로 다른 4마리 동물   
    if len(animals) != 4 or len(set(animals)) != 4:
        raise ValueError("Trial must contain 4 unique animals")

    # self, agent가 각 한번씩 등장
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

    # 3. Reset hints for the new trial
    context.display.set_hints(
        hint_colors=trial_design["hint_colors"],
        visible=False,
    )

    # 4. Present mission
    context.display.show_mission(state.domain)

    # 5. First choice segment
    run_choice_segment(
        context=context,
        state=state,
        actor_order=trial_design["actor_order"],
        stage=1,
        hint_visible=False,
        cumulative_scores=context.cumulative_scores,
    )

    # 6. Reveal hints
    context.display.set_hints(
        hint_colors=trial_design["hint_colors"],
        visible=True,
    )

    # 7. Second choice segment
    run_choice_segment(
        context=context,
        state=state,
        actor_order=trial_design["actor_order"],
        stage=2,
        hint_visible=True,
        cumulative_scores=context.cumulative_scores,
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

    # 11. Show trial result
    context.display.show_trial_result(
        self_score=self_trial_score,
        agent_score=agent_trial_score,
    )

    return state
