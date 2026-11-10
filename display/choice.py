
# ------
# 네 마리 동물 이미지를 표시
# 좌우 방향키로 동물을 탐색
# Space를 누르면 선택이 확정
# 이미 선택된 동물은 어둡게 표시하고 선택할 수 없도록
# self와 agent 선택 상태 구분: 선택된 동물의 소속(Self/Agent)을 표시
# 선택 직후 점수 및 누적 trial 점수 표시


# display/choice.py

from pathlib import Path

from psychopy import visual, event

from config.settings import ANIMAL_IMAGE_SIZE
from config.keymapping import MOVE_LEFT, MOVE_RIGHT, CONFIRM, QUIT


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ANIMAL_DIR = PROJECT_ROOT / "assets" / "animals"


class ChoiceScreen:

    # __init__: 화면에 사용할 동물 이미지 미리 생성
    def __init__(self, win, animals):
        self.win = win
        self.animals = list(animals)

        # Four positions arranged horizontally
        self.positions = [
            (-0.54, -0.05),
            (-0.18, -0.05),
            (0.18, -0.05),
            (0.54, -0.05),
        ]

        self.images = {}

        for animal, pos in zip(self.animals, self.positions):
            image_path = ANIMAL_DIR / f"{animal.lower()}.png"

            if not image_path.is_file():
                raise FileNotFoundError(image_path)

            self.images[animal] = visual.ImageStim(
                win,
                image=str(image_path),
                pos=pos,
                size=ANIMAL_IMAGE_SIZE,
            )

    # draw(): 현재 선택 가능한 동물과 선택된 동물 상태 화면에 반영
    def draw(
            self, 
            available, 
            selected, 
            actor="self", 
            domain="cooking",
            hint_visible=False,
            hint_colors=None,
            ):
        """Draw all animals and their selection states."""

        title = visual.TextStim(
            self.win,
            text=f"{domain.upper()}  |  {actor.upper()}'S TURN",
            pos=(0, 0.32),
            height=0.045,
            color="white",
        )
        title.draw()

        # Draw attribute hint when enabled
        if hint_visible and hint_colors:
            color = hint_colors.get(animal)

            if color:
                hint_marker = visual.Rect(
                    self.win,
                    pos=(pos[0], pos[1] + 0.17),
                    width=0.12,
                    height=0.035,
                    fillColor=color,
                    lineColor=color,
                )
                hint_marker.draw()

        for animal, pos in zip(self.animals, self.positions):
            is_available = animal in available
            is_selected = animal == selected and is_available

            border = visual.Rect(
                self.win,
                pos=pos,
                width=0.30,
                height=0.36,
                lineColor="#FFD166" if is_selected else "#536174",
                lineWidth=4 if is_selected else 1,
                fillColor="#33435B" if is_selected else "#242F40",
            )
            border.draw()

            image = self.images[animal]
            image.opacity = 1.0 if is_available else 0.25
            image.draw()

            name = visual.TextStim(
                self.win,
                text=animal,
                pos=(pos[0], pos[1] - 0.15),
                height=0.03,
                color="white",
            )
            name.draw()

            if not is_available:
                unavailable = visual.TextStim(
                    self.win,
                    text="TAKEN",
                    pos=(pos[0], pos[1]),
                    height=0.027,
                    color="white",
                )
                unavailable.draw()

        instruction = visual.TextStim(
            self.win,
            text="LEFT / RIGHT: Move     SPACE: Confirm     ESC: Quit",
            pos=(0, -0.36),
            height=0.026,
            color="white",
        )
        instruction.draw()

        self.win.flip()

    # 키보드 입력을 받아 참가자가 최종 선택한 동물 ID 반환
    def get_choice(self, available, actor="self", domain="cooking", hint_visible=False, hint_colors=None):
        """Return the animal confirmed by the participant."""

        available = list(available)

        if not available:
            raise ValueError("No available animals")

        # Start on the first available animal
        index = self.animals.index(available[0])

        while True:
            selected = self.animals[index]

            self.draw(
                available=available,
                selected=selected,
                actor=actor,
                domain=domain,
                hint_visible=hint_visible,
                hint_colors=hint_colors,
            )

            # 지정한 키 입력 발생할 때까지 기다리는 함수
            keys = event.waitKeys(
                keyList=[MOVE_LEFT, MOVE_RIGHT, CONFIRM, QUIT]
            )

            key = keys[0]

            if key == QUIT:
                raise KeyboardInterrupt("Experiment interrupted")

            if key == MOVE_LEFT:
                index = self._move(index, available, -1)

            elif key == MOVE_RIGHT:
                index = self._move(index, available, 1)

            elif key == CONFIRM:
                return self.animals[index]

    # 이미 데려간 동물 건너뛰어 다음 선택 가능한 동물로 이동
    def _move(self, index, available, direction):
        """Move to the next available animal."""

        for _ in range(len(self.animals)):
            index = (index + direction) % len(self.animals)

            if self.animals[index] in available:
                return index

        return index
