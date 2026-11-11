# display/window.py
# psychopy window 생성 및 종료

from psychopy import visual

from config.settings import (
    SCREEN_SIZE,
    FULLSCREEN,
    BACKGROUND_COLOR,
)


def create_window():
    """Create the main PsychoPy window."""

    win = visual.Window(
        size=SCREEN_SIZE,
        fullscr=FULLSCREEN,
        units="height",
        color=BACKGROUND_COLOR,
        colorSpace="rgb",
        allowGUI=not FULLSCREEN,
    )

    return win
