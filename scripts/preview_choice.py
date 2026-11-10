
# scripts/preview_choice.py

from display.window import create_window
from display.choice import ChoiceScreen
from core.state import TrialState

from psychopy import event


def main():

    win = create_window()

    try:
        state = TrialState(
            domain="cooking",
            animals=["bear", "cat", "chicken", "cow"],
        )

        choice_screen = ChoiceScreen(
            win=win,
            animals=state.animals,
        )

        actor_order = [
            "self",
            "agent",
            "self",
            "agent",
        ]

        for turn_number, actor in enumerate(actor_order, start=1):

            print(f"\nTurn {turn_number}: {actor}")

            animal = choice_screen.get_choice(
                available=state.available_animals(),
                actor=actor,
                domain=state.domain,
            )

            # Display test: add zero points
            state.add_choice(actor, animal, 0)

            print(f"Selected: {animal}")
            print(f"Available: {state.available_animals()}")

        print("\nTrial Complete:", state.is_complete())

        event.waitKeys(keyList=["space", "escape"])

    except KeyboardInterrupt:
        print("Preview interrupted")

    finally:
        win.close()


if __name__ == "__main__":
    main()
