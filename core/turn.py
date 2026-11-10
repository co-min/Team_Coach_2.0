# 한 번의 선택과 점수 계산
# core/turn.py

from dataclasses import dataclass
from function.calculate_score import calculate_turn_score


@dataclass(frozen=True)
class TurnResult:
    actor: str
    animal: str
    turn_score: float
    cumulative_score: float


def execute_turn(
    state,
    actor,
    animal,
    competence,
    synergy,
) -> TurnResult:
    """Calculate score and update TrialState."""

    # 1. Validate actor
    if actor not in ("self", "agent"):
        raise ValueError(f"Invalid actor: {actor}")

    # 2. Validate available animal
    if animal not in state.available_animals():
        raise ValueError(f"Unavailable animal: {animal}")

    # 3. Check team capacity before scoring
    choices = (
        state.self_choices
        if actor == "self"
        else state.agent_choices
    )

    if len(choices) >= 2:
        raise ValueError(f"{actor} team is already full")

    # 4. Calculate score
    turn_score = calculate_turn_score(
        leader=actor,
        animal=animal,
        domain=state.domain,
        competence=competence,
        synergy=synergy,
    )

    # 5. Update TrialState
    state.add_choice(actor, animal, turn_score)

    # 6. Get cumulative trial score
    cumulative_score = (
        state.self_score
        if actor == "self"
        else state.agent_score
    )

    # 7. Return immutable result
    return TurnResult(
        actor=actor,
        animal=animal,
        turn_score=turn_score,
        cumulative_score=cumulative_score,
    )


def run_turn(context, state, actor, stage, turn_number) -> TurnResult:
    """Run selection, scoring, feedback and logging."""

    # 1. Get available animals
    available = state.available_animals()

    # 2. Select animal
    if actor == "self":
        animal = context.display.get_choice(available)

    elif actor == "agent":
        animal = context.agent.choose(available)
        context.display.show_agent_choice(animal)

    else:
        raise ValueError(f"Invalid actor: {actor}")

    # 3. Execute game logic
    result = execute_turn(
        state=state,
        actor=actor,
        animal=animal,
        competence=context.competence,
        synergy=context.synergy,
    )

    # 4. Display cumulative scores
    context.display.show_turn_feedback(
        actor=result.actor,
        animal=result.animal,
        turn_score=result.turn_score,
        self_score=state.self_score,
        agent_score=state.agent_score,
    )

    # 5. Log result
    context.logger.log_turn(
        actor=result.actor,
        animal=result.animal,
        turn_score=result.turn_score,
        cumulative_score=result.cumulative_score,
        self_score=state.self_score,
        agent_score=state.agent_score,
    )

    return result
