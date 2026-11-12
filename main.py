
# main.py
# Team Coach 2.0 - Single Trial Test

import random

from core.context import ExperimentContext
from core.trial import run_trial
from config.animals import ANIMAL_SETS

from display.window import create_window
from display.game import GameDisplay


# --------------------------------------------------
# 1. Temporary Random Agent
# --------------------------------------------------

class RandomAgent:

    def __init__(self, seed=42):
        self.rng = random.Random(seed)

    def choose(self, available):
        """Randomly select an available animal."""

        if not available:
            raise ValueError("No available animals")

        return self.rng.choice(available)


# --------------------------------------------------
# 2. Temporary Logger
# --------------------------------------------------

class TestLogger:

    def __init__(self):
        self.records = []

    def log_turn(self, **kwargs):
        """Store and print turn data."""

        self.records.append(kwargs)
        print("TURN LOG:", kwargs)


# --------------------------------------------------
# 3. Main
# --------------------------------------------------

def main():

    # 1. Test animals
    animals = ["A", "B", "C", "D"]

    # 2. True attributes (test values)
    competence = {
        "self": {"cooking": 5},
        "agent": {"cooking": 5},
        "A": {"cooking": 8},
        "B": {"cooking": 4},
        "C": {"cooking": 6},
        "D": {"cooking": 3},
    }

    synergy = {
        "self": {
            "A": 3, "B": 2,
            "C": 1, "D": 2,
        },
        "agent": {
            "A": 2, "B": 1,
            "C": 3, "D": 2,
        },
    }

    # 3. Trial design
    trial_design = {
        "domain": "cooking",
        "animals": animals,
        "actor_order": ["self", "agent"],
        "hint_colors": {
            "A": "#2BB830",
            "B": "#FF1515",
            "C": "#F3E221",
            "D": "#FF1515",
        },
    }

    # 4. Initialize PsychoPy Window
    win = create_window()

    try:
        # 5. Initialize display, agent, logger
        display = GameDisplay(win, animals)
        agent = RandomAgent(seed=42)
        logger = TestLogger()

        # 6. Create ExperimentContext
        context = ExperimentContext(
            display=display,
            agent=agent,
            logger=logger,
            competence=competence,
            synergy=synergy,
        )

        # 7. Run Single Trial
        state = run_trial(
            context=context,
            trial_design=trial_design,
        )

        # 8. Validate results
        assert state.is_complete()
        assert state.turn == 4
        assert len(logger.records) == 4

        # 9. Print trial summary
        print("\n--- TRIAL RESULT ---")
        print("Self choices:", state.self_choices)
        print("Agent choices:", state.agent_choices)
        print("Self score:", state.self_score)
        print("Agent score:", state.agent_score)
        print("Winner:", state.winner())
        print("Completed turns:", state.turn)

        print("\nSingle Trial Test PASSED")

    finally:
        # 10. Close PsychoPy Window
        win.close()


if __name__ == "__main__":
    main()
