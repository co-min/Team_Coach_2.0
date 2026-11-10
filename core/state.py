# trial 상태

# 동물 중복 선택 방지
# 누적 점수 관리
# trial 초기화


from dataclasses import dataclass, field


@dataclass
class TrialState:
    domain: str
    animals: list[str]

    self_choices: list[str] = field(default_factory=list)
    agent_choices: list[str] = field(default_factory=list)

    self_score: float = 0.0
    agent_score: float = 0.0

    # 동물 중복 선택 방지
    def available_animals(self):
        selected = set(
            self.self_choices + self.agent_choices
        )

        return [
            animal for animal in self.animals
            if animal not in selected
        ]

    def add_choice(self, actor, animal, score):

        if actor not in ("self", "agent"):
            raise ValueError("Invalid actor")

        if animal not in self.available_animals():
            raise ValueError("Animal already selected or unavailable")

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

    def is_complete(self):
        return (
            len(self.self_choices) == 2
            and len(self.agent_choices) == 2
        )
