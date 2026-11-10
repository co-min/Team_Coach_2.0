
# function/agent.py

import random


class Agent:
    def __init__(self, seed=None):
        self.rng = random.Random(seed)

    def choose(self, available):
        """Randomly choose one available animal."""

        if not available:
            raise ValueError("No available animals")

        return self.rng.choice(available)


# random.Random(seed) : Agent 전용 난수 생성기(Random Number Generator)를 생성
# self.rng.choice(available) : 선택 가능한 동물 중 하나를 동일한 확률로 선택
# seed : 동일한 난수 시퀀스를 재현할 때 사용