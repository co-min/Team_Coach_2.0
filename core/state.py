# core/state.py : trial 상태

# 1. 동물 중복 선택 방지
# 2. 누적 점수 관리
# 3. trial 초기화


from dataclasses import dataclass, field


@dataclass
class TrialState:
    domain: str
    animals: list[str]

    # 현재 Trial에서 완료된 Turn 수 (0~4)
    turn: int = 0

    # 선택된 동물
    self_choices: list[str] = field(default_factory=list)
    agent_choices: list[str] = field(default_factory=list)

    # 현재 Trial의 누적 점수
    self_score: float = 0.0
    agent_score: float = 0.0

    # 동물 중복 선택 방지
    def available_animals(self):
        selected = set(self.self_choices + self.agent_choices)

        return [
            animal for animal in self.animals
            if animal not in selected
        ]

    # 동물 선택 및 점수 누적
    # 매 turn의 score를 합산하여 최종 trial score culculating
    def add_choice(self, actor, animal, score):

        if actor not in ("self", "agent"):
            raise ValueError("Invalid actor")

        if self.is_complete():
            raise ValueError("Trial already completed")

        if animal not in self.available_animals():
            raise ValueError("Animal already selected or unavailable")

        if not isinstance(score, (int, float)):
            raise ValueError("Score must be numeric")

        if actor == "self":
            if len(self.self_choices) >= 2:
                raise ValueError("Self team is full")

            self.self_choices.append(animal)
            self.self_score += score

        else:
            if len(self.agent_choices) >= 2:
                raise ValueError("Agent team is full")

            self.agent_choices.append(animal)
            self.agent_score += score

        self.turn += 1

    # Trial 완료 여부
    def is_complete(self):
        return (
            len(self.self_choices) == 2
            and len(self.agent_choices) == 2
        )

    # Trial 승자 확인
    def winner(self):
        if not self.is_complete():
            return None

        if self.self_score > self.agent_score:
            return "self"
        elif self.agent_score > self.self_score:
            return "agent"
        else:
            return "draw"
