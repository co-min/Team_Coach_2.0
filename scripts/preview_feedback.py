
# scripts/preview_feedback.py

from core.state import TrialState
from core.turn import execute_turn

from display.window import create_window
from display.choice import ChoiceScreen
from display.feedback import FeedbackScreen

from function.hints import get_hint_color


def main():

    # 1. Experimental attributes
    competence = {
        "self": {"cooking": 5},
        "agent": {"cooking": 6},
        "bear": {"cooking": 8},
        "cat": {"cooking": 4},
        "chicken": {"cooking": 7},
        "cow": {"cooking": 3},
    }

    synergy = {
        "self": {
            "bear": 2, "cat": 3,
            "chicken": 1, "cow": 2,
        },
        "agent": {
            "bear": 1, "cat": 2,
            "chicken": 2, "cow": 3,
        },
    }

    # 2. Temporary competence hint categories
    hint_levels = {
        "bear": "high",
        "cat": "low",
        "chicken": "medium",
        "cow": "high",
    }

    hint_colors = {
        animal: get_hint_color(level)
        for animal, level in hint_levels.items()
    }

    # 3. Initialize trial state
    state = TrialState(
        domain="cooking",
        animals=["bear", "cat", "chicken", "cow"],
    )

    # 4. Create display
    win = create_window()

    try:
        choice_screen = ChoiceScreen(win, state.animals)
        feedback_screen = FeedbackScreen(win)

        actor_order = ["self", "agent"]

        # 5. Choice 1 and Choice 2
        for stage in (1, 2):

            hint_visible = (stage == 2)

            for actor in actor_order:

                # Temporary preview:
                # both actors are selected by keyboard
                animal = choice_screen.get_choice(
                    available=state.available_animals(),
                    actor=actor,
                    domain=state.domain,
                    hint_visible=hint_visible,
                    hint_colors=hint_colors,
                )

                # Calculate and accumulate score
                result = execute_turn(
                    state=state,
                    actor=actor,
                    animal=animal,
                    competence=competence,
                    synergy=synergy,
                )

                # Display turn feedback
                feedback_screen.show_turn_feedback(
                    actor=result.actor,
                    animal=result.animal,
                    turn_score=result.turn_score,
                    self_score=state.self_score,
                    agent_score=state.agent_score,
                )

                print(
                    f"Stage {stage} | "
                    f"{actor} → {animal} | "
                    f"+{result.turn_score:g}"
                )

        # 6. Final trial result
        assert state.is_complete()

        feedback_screen.show_trial_result(
            self_score=state.self_score,
            agent_score=state.agent_score,
        )

    except KeyboardInterrupt:
        print("Preview interrupted")

    finally:
        win.close()


if __name__ == "__main__":
    main()
