
# scripts/preview_turn.py

from core.state import TrialState
from core.turn import execute_turn


def main():

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

    state = TrialState(
        domain="cooking",
        animals=["A", "B", "C", "D"],
    )

    turns = [
        ("self", "A"),
        ("agent", "C"),
        ("self", "B"),
        ("agent", "D"),
    ]

    for turn_number, (actor, animal) in enumerate(
        turns, start=1
    ):

        result = execute_turn(
            state, actor, animal, competence, synergy
        )

        print(f"\nTurn {turn_number}")
        print(f"Actor: {result.actor}")
        print(f"Selected: {result.animal}")
        print(f"Turn Score: +{result.turn_score}")
        print(f"Cumulative: {result.cumulative_score}")
        print(
            f"Self: {state.self_score} | "
            f"Agent: {state.agent_score}"
        )
        print(f"Available: {state.available_animals()}")

    print(f"\nTrial Complete: {state.is_complete()}")


if __name__ == "__main__":
    main()
