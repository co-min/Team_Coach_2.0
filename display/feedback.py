# turn score feedback, trial score feedback
# display/feedback.py

from psychopy import visual, core


class FeedbackScreen:

    def __init__(self, win):
        self.win = win

    def show_turn_feedback(
        self,
        actor,
        animal,
        turn_score,
        self_score,
        agent_score,
        duration=2.5,
    ):
        """Display score gained after one turn."""

        title = visual.TextStim(
            self.win,
            text=f"{actor.upper()} selected {animal.upper()}",
            pos=(0, 0.20),
            height=0.045,
            color="white",
        )

        gained = visual.TextStim(
            self.win,
            text=f"+{turn_score:g} points",
            pos=(0, 0.05),
            height=0.075,
            color="#77DD77",
        )

        totals = visual.TextStim(
            self.win,
            text=(
                f"SELF: {self_score:g}       "
                f"AGENT: {agent_score:g}"
            ),
            pos=(0, -0.13),
            height=0.045,
            color="white",
        )

        title.draw()
        gained.draw()
        totals.draw()

        self.win.flip()
        core.wait(duration)

    def show_trial_result(
        self,
        self_score,
        agent_score,
        duration=None,
    ):
        """Display final scores at trial end."""

        if self_score > agent_score:
            result = "SELF WINS"
        elif agent_score > self_score:
            result = "AGENT WINS"
        else:
            result = "DRAW"

        title = visual.TextStim(
            self.win,
            text="TRIAL RESULT",
            pos=(0, 0.23),
            height=0.055,
            color="white",
        )

        scores = visual.TextStim(
            self.win,
            text=(
                f"SELF: {self_score:g}\n"
                f"AGENT: {agent_score:g}"
            ),
            pos=(0, 0),
            height=0.065,
            color="white",
        )

        winner = visual.TextStim(
            self.win,
            text=result,
            pos=(0, -0.23),
            height=0.055,
            color="#77DD77",
        )

        title.draw()
        scores.draw()
        winner.draw()

        self.win.flip()
        core.wait(duration)
