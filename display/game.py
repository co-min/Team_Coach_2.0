# display controller
# display/game.py
# mission, screeen flow control

from psychopy import visual, core

from display.choice import ChoiceScreen
from display.feedback import FeedbackScreen


class GameDisplay:

    def __init__(self, win, animals):
        # 화면 객체 초기화
        self.win = win

        self.choice_screen = ChoiceScreen(win, animals)
        self.feedback_screen = FeedbackScreen(win)

        self.domain = None
        self.hint_visible = False
        self.hint_colors = {}

    # mission 화면
    def show_mission(self, domain, duration=1.0):
        self.domain = domain

        title = visual.TextStim(
            self.win,
            text=f"MISSION: {domain.upper()}",
            pos=(0, 0),
            height=0.06,
            color="white",
        )

        title.draw()
        self.win.flip()
        core.wait(duration)

    # hint 1)visible 여부와 2)colors 설정 
    def set_hints(self, hint_colors, visible):
        """Update visual hint state without showing a new screen."""
        self.hint_colors = dict(hint_colors)
        self.hint_visible = visible

    def get_choice(self, state, stage):
        return self.choice_screen.get_choice(
            state=state,
            stage=stage,
            hint_visible=self.hint_visible,
            hint_colors=self.hint_colors,
        )

    def show_agent_choice(self, animal):
        # Temporary placeholder for Agent animation.
        pass

    def show_turn_feedback(
        self, actor, animal, turn_score, self_score, agent_score
    ):
        self.feedback_screen.show_turn_feedback(
            actor=actor,
            animal=animal,
            turn_score=turn_score,
            self_score=self_score,
            agent_score=agent_score,
        )

    def show_trial_result(self, self_score, agent_score):
        self.feedback_screen.show_trial_result(
            self_score=self_score,
            agent_score=agent_score,
        )
