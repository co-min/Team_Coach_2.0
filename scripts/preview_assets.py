
# scripts/preview_assets.py

from pathlib import Path
from psychopy import visual, event, core


PROJECT_ROOT = Path(__file__).resolve().parents[1]

ANIMAL_DIR = PROJECT_ROOT / "assets" / "animals"

animal_files = [
    ANIMAL_DIR / "bear.png",
    ANIMAL_DIR / "cat.png",
    ANIMAL_DIR / "chicken.png",
    ANIMAL_DIR / "cow.png",
]

for path in animal_files:
    if not path.is_file():
        raise FileNotFoundError(path)

win = visual.Window(
    size=(1280, 720),
    fullscr=False,
    units="height",
    color="black",
)

try:
    positions = [
        (-0.55, 0),
        (-0.18, 0),
        (0.18, 0),
        (0.55, 0),
    ]

    animals = []

    for image_path, pos in zip(animal_files, positions):
        animal = visual.ImageStim(
            win,
            image=str(image_path),
            pos=pos,
            size=(0.25, 0.25),
        )

        animals.append(animal)

    instruction = visual.TextStim(
        win,
        text="Animal Preview - Press SPACE to exit",
        pos=(0, -0.3),
        height=0.035,
        color="white",
    )

    for animal in animals:
        animal.draw()

    instruction.draw()
    win.flip()

    event.waitKeys(keyList=["esc", "escape"])

finally:
    win.close()
    core.quit()
