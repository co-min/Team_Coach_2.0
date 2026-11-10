# choice 1 / hint / choice 2


# core/segment.py

from core.turn import run_turn


# stage는 choice 1 or 2인지 구분하는 변수: Logger에 choice_stage를 기록하거나 TTL Trigger를 구분할 때 활용
def run_choice_segment(context, state, actor_order, stage):
    """Run two turns for one choice stage."""

    results = []

    # for actor in actor_order:
    #     result = run_turn(context, state, actor)
    #     results.append(result)


    for index, actor in enumerate(actor_order):

        turn_number = (stage - 1) * 2 + index + 1

        result = run_turn(
            context=context,
            state=state,
            actor=actor,
            stage=stage,
            turn_number=turn_number,
        )

        results.append(result)

    return results
