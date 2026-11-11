# display/choice.py
# 동물 선택 화면, 입력 처리
# ------
# 1. 네 마리 동물 이미지를 표시
# 2. 좌우 방향키로 동물을 탐색
# 3. Space를 누르면 선택이 확정
# 4. 이미 선택된 동물은 어둡게 표시하고 선택할 수 없도록
# 5. self와 agent 선택 상태 구분: 선택된 동물의 소속(Self/Agent)을 표시
# 6. 선택 직후 점수 및 누적 trial 점수 표시


# display/choice.py

from pathlib import Path

from PIL import Image
from psychopy import visual, event

from config.settings import ANIMAL_IMAGE_HEIGHT
from config.keymapping import MOVE_LEFT, MOVE_RIGHT, CONFIRM, QUIT

# 이미지 경로
PROJECT_ROOT = Path(__file__).resolve().parents[1]
ANIMAL_DIR = PROJECT_ROOT / "assets" / "animals"


class ChoiceScreen:

    # __init__: 화면에 사용할 동물 이미지 미리 생성
    def __init__(self, win, animals):
        self.win = win
        self.animals = list(animals)

        if len(self.animals) != 4 or len(set(self.animals)) != 4:
            raise ValueError("Exactly four unique animals are required")

        # Four positions arranged horizontally
        self.positions = [
            (-0.54, -0.05),
            (-0.18, -0.05),
            (0.18, -0.05),
            (0.54, -0.05),
        ]

        self.images = {}

        # norm 단위는 가로/세로 스케일이 달라서 화면 비율로 보정해야 원본 비율 유지
        win_aspect = win.size[0] / win.size[1]

        for animal, pos in zip(self.animals, self.positions):
            image_path = ANIMAL_DIR / f"{animal.lower()}.png"

            if not image_path.is_file():
                raise FileNotFoundError(image_path)

            with Image.open(image_path) as img:
                img_aspect = img.width / img.height

            self.images[animal] = visual.ImageStim(
                win,
                image=str(image_path),
                pos=pos,
                size=(ANIMAL_IMAGE_HEIGHT * img_aspect / win_aspect, ANIMAL_IMAGE_HEIGHT),
                units="norm",
            )

        # cursor
        self.cursor = visual.ShapeStim(
            win, 
            vertices=[
                (-0.035, -0.025),
                (0.035, -0.025),
                (0.000, 0.035),
            ],
            fillColor="#FF9000",
            lineColor="#FF9000",
            units="norm",
        )

        # animal name, is_selected
        self.animals_names = {}
        self.owner_labels = {}
        self.hint_markers = {}

        for animal, pos in zip(self.animals, self.positions):
            # 동물 이름
            # self.animals_names[animal] = visual.TextStim(
            #     win,
            #     text=animal.upper(),
            #     pos=(pos[0], pos[1] - 0.15),
            #     height=0.03,
            #     color="white",
            #     units="norm",
            # )

            # 선택이 확정된 동물의 소속
            self.owner_labels[animal] = visual.TextStim(
                win,
                text="",
                pos=(pos[0], pos[1] - 0.26),
                height=0.028,
                color="white",
                units="norm",
            )

            # 동물별 색상 힌트
            self.hint_markers[animal] = visual.Rect(
                win,
                pos=(pos[0], pos[1] + 0.23),
                width=0.13,
                height=0.025,
                fillColor="white",
                lineColor="white",
                units="norm",
            )

        # 상단 점수
        self.self_score_text = visual.TextStim(
            win,
            text="SELF  0",
            pos=(-0.55, 0.76),
            height=0.055,
            color="white",
            units="norm",
        )

        self.agent_score_text = visual.TextStim(
            win,
            text="AGENT  0",
            pos=(0.55, 0.76),
            height=0.055,
            color="white",
            units="norm",
        )

        # Mission

        self.title = visual.TextStim(
            win,
            text="",
            pos=(0, 0.46),
            height=0.05,
            color="white",
            units="norm",
        )

        # 지시 설명
        self.instruction = visual.TextStim(
            win,
            text="",
            pos=(0, 0.35),
            height=0.035,
            color="white",
            units="norm",
        )

        # 키보드 안내
        # self.key_instruction = visual.TextStim(
        #     win,
        #     text="LEFT / RIGHT: Move     SPACE: Confirm     ESC: Quit",
        #     pos=(0, -0.68),
        #     height=0.025,
        #     color="#AAAAAA",
        #     units="norm",
        # )


    # draw(): 현재 선택 가능한 동물과 선택된 동물 상태 화면에 반영
    # --------------------------------------------------
    # draw(): 현재 상태를 화면에 표시
    # --------------------------------------------------

    def draw(
        self,
        available,
        selected=None,
        owners=None,
        actor="self",
        domain="cooking",
        pick_number=1,
        hint_visible=False,
        hint_colors=None,
        self_score=0,
        agent_score=0,
    ):
        """동물, 삼각형 커서, 힌트, 점수를 그린다."""

        available = set(available)
        owners = owners if owners is not None else {}
        hint_colors = hint_colors if hint_colors is not None else {}

        # --------------------------------------------------
        # 1. 점수 표시
        # --------------------------------------------------

        self.self_score_text.text = f"SELF  {self_score}"
        self.agent_score_text.text = f"AGENT  {agent_score}"

        self.self_score_text.draw()
        self.agent_score_text.draw()

        # --------------------------------------------------
        # 2. Mission 및 선택 단계 표시
        # --------------------------------------------------

        self.title.text = domain.upper()

        pick_label = "FIRST" if pick_number == 1 else "SECOND"

        self.instruction.text = (
            f"{actor.upper()}'S TURN  |  "
            f"CHOOSE YOUR {pick_label} TEAMMATE"
        )

        self.title.draw()
        self.instruction.draw()

        # --------------------------------------------------
        # 3. 네 마리 동물 표시
        # --------------------------------------------------

        for animal, pos in zip(self.animals, self.positions):

            owner = owners.get(animal)
            is_available = animal in available
            is_highlighted = (
                animal == selected and is_available
            )

            # 선택된 동물 또는 선택 불가능한 동물은 어둡게
            image = self.images[animal]
            image.opacity = 1.0 if is_available else 0.25
            image.draw()

            # 동물 이름 표시
            # self.animal_names[animal].draw()

            # --------------------------------------------------
            # 4. 색상 힌트
            # --------------------------------------------------

            if hint_visible and is_available:
                color = hint_colors.get(animal)

                if color is not None:
                    marker = self.hint_markers[animal]
                    marker.fillColor = color
                    marker.lineColor = color
                    marker.draw()

            # --------------------------------------------------
            # 5. 선택 확정 상태
            # --------------------------------------------------

            if owner is not None:

                label = self.owner_labels[animal]
                label.text = f"{owner.upper()} PICK"
                label.draw()

            elif not is_available:

                # 소속 정보가 없는 선택 불가능 동물
                label = self.owner_labels[animal]
                label.text = "TAKEN"
                label.draw()

            # --------------------------------------------------
            # 6. 현재 커서 위치에 삼각형 표시
            # --------------------------------------------------

            elif is_highlighted:

                self.cursor.pos = (
                    pos[0],
                    pos[1] - 0.26,
                )
                self.cursor.draw()

        # 하단 키보드 안내
        # self.key_instruction.draw()

        # 그린 자극을 실제 모니터에 표시
        self.win.flip()


    # get_choice(): 참가자 선택 처리
    
    def get_choice(
        self,
        state,
        stage,
        hint_visible=False,
        hint_colors=None,
    ):
        """Display choices and return the selected animal."""

        available = state.available_animals()

        if not available:
            raise ValueError("No available animals")

        # Previous selections and their owners
        owners = {
            animal: "self"
            for animal in state.self_choices
        }
        owners.update({
            animal: "agent"
            for animal in state.agent_choices
        })

        # 선택 가능한 동물에 cursor 위치 
        index = self.animals.index(available[0])

        # 이전 입력이 다음 선택에 남지 않도록 초기화
        event.clearEvents(eventType="keyboard")

        while True:
            selected = self.animals[index]

            # 현재 상태 화면 표시
            self.draw(
                available=available,
                selected=selected,
                owners=owners,
                actor="self",
                domain=state.domain,
                pick_number=stage,
                hint_visible=hint_visible,
                hint_colors=hint_colors,
                self_score=state.self_score,
                agent_score=state.agent_score,
            )

            keys = event.waitKeys(
                keyList=[
                    MOVE_LEFT,
                    MOVE_RIGHT,
                    CONFIRM,
                    QUIT,
                ]
            )

            key = keys[0]

            if key == QUIT:
                raise KeyboardInterrupt("Experiment interrupted")

            elif key == MOVE_LEFT:
                index = self._move(index, available, -1)

            elif key == MOVE_RIGHT:
                index = self._move(index, available, 1)

            elif key == CONFIRM:
                return self.animals[index]


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
