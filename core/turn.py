# 한 번의 선택과 점수 계산
# core/turn.py


# core/turn.py

from dataclasses import dataclass

from core.state import TrialState
from function.calculate_score import calculate_turn_score


@dataclass(frozen=True)
class TurnResult:
    actor: str
    animal: str
    turn_score: float
    cumulative_score: float


def execute_turn(
    state: TrialState,
    actor: str,
    animal: str,
    competence: dict,
    synergy: dict,
) -> TurnResult:
    """Calculate score and update the trial state."""

    # Validate selection before scoring
    if actor not in ("self", "agent"):
        raise ValueError(f"Invalid actor: {actor}")

    if animal not in state.available_animals():
        raise ValueError(f"Unavailable animal: {animal}")

    # Calculate turn score
    turn_score = calculate_turn_score(
        leader=actor,
        animal=animal,
        domain=state.domain,
        competence=competence,
        synergy=synergy,
    )

    # Update choices and cumulative scores
    state.add_choice(actor, animal, turn_score)

    cumulative_score = (
        state.self_score
        if actor == "self"
        else state.agent_score
    )

    return TurnResult(
        actor=actor,
        animal=animal,
        turn_score=turn_score,
        cumulative_score=cumulative_score,
    )


def run_turn(
    context,
    state: TrialState,
    actor: str,
    stage: str,
    turn_number: int,
) -> TurnResult:
    """Run one turn: choice, score, feedback, logging."""

    available = state.available_animals()

    # Select animal
    if actor == "self":
        animal = context.display.get_choice(
            state=state,
            stage=stage,
        )

    elif actor == "agent":
        animal = context.agent.choose(available)
        context.display.show_agent_choice(animal)

    else:
        raise ValueError(f"Invalid actor: {actor}")

    # Calculate score and update state
    result = execute_turn(
        state=state,
        actor=actor,
        animal=animal,
        competence=context.competence,
        synergy=context.synergy,
    )

    # Show feedback
    context.display.show_turn_feedback(
        actor=result.actor,
        animal=result.animal,
        turn_score=result.turn_score,
        self_score=state.self_score,
        agent_score=state.agent_score,
    )

    # Log completed turn
    context.logger.log_turn(
        turn_number=turn_number,
        stage=stage,
        actor=result.actor,
        animal=result.animal,
        turn_score=result.turn_score,
        cumulative_score=result.cumulative_score,
        self_score=state.self_score,
        agent_score=state.agent_score,
    )

    return result
