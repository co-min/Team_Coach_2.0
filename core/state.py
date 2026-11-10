# core/state.py : trial 상태

# 1. 동물 중복 선택 방지
# 2. 누적 점수 관리
# 3. trial 초기화



from dataclasses import dataclass, field
import math


@dataclass
class TrialState:
    domain: str
    animals: list[str]

    # 완료된 Turn 수
    turn: int = 0

    # 선택된 동물
    self_choices: list[str] = field(default_factory=list)
    agent_choices: list[str] = field(default_factory=list)

    # 현재 Trial 누적 점수
    self_score: float = 0.0
    agent_score: float = 0.0

    def available_animals(self) -> list[str]:
        """아직 선택되지 않은 동물 반환"""
        selected = set(self.self_choices + self.agent_choices)

        return [
            animal for animal in self.animals
            if animal not in selected
        ]

    # 매 turn의 score 합산하여 최종 trial score calculating
    def add_choice(
        self,
        actor: str,
        animal: str,
        score: float
    ) -> None:
        """동물 선택 및 점수 누적"""

        if actor not in ("self", "agent"):
            raise ValueError("Invalid actor")

        if self.is_complete():
            raise ValueError("Trial already completed")

        if animal not in self.available_animals():
            raise ValueError("Animal unavailable")

        if not isinstance(score, (int, float)) or not math.isfinite(score):
            raise ValueError("Score must be a finite number")

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

    def is_complete(self) -> bool:
        """두 팀이 모두 완성되었는지 확인"""
        return (
            len(self.self_choices) == 2
            and len(self.agent_choices) == 2
        )

    def winner(self) -> str | None:
        """Trial 종료 후 승자 반환"""

        if not self.is_complete():
            return None

        if self.self_score > self.agent_score:
            return "self"

        if self.agent_score > self.self_score:
            return "agent"

        return "draw"
