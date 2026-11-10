# choice 1 / hint / choice 2

# core/segment.py

from core.state import TrialState
from core.turn import run_turn, TurnResult

# stage는 choice 1 or 2인지 구분하는 변수: Logger에 choice_stage를 기록하거나 TTL Trigger를 구분할 때 활용
def run_choice_segment(
    context,
    state: TrialState,
    actor_order: list[str],
    stage: int,
) -> list[TurnResult]:
    """Run two turns for one choice stage."""

    if stage not in (1, 2):
        raise ValueError(f"Invalid stage: {stage}")

    if (
        len(actor_order) != 2
        or set(actor_order) != {"self", "agent"}
    ):
        raise ValueError("Invalid actor order")

    results = []

    for index, actor in enumerate(actor_order):

        # Convert stage and index to turn number (1~4)
        turn_number = (stage - 1) * 2 + index + 1

        # Ensure previous turns are completed
        if state.turn != turn_number - 1:
            raise RuntimeError(
                f"Expected {turn_number - 1} completed turns, "
                f"but found {state.turn}"
            )

        result = run_turn(
            context=context,
            state=state,
            actor=actor,
            stage=stage,
            turn_number=turn_number,
        )

        results.append(result)

    return results
